from ....atom import R3atom, R3private
from ....globals import pg
from ....utils import div2_v2i, div_v2i, mul_v2, sub_v2, add_v2
import r3frame2 as r3

class R3gridPartition(R3atom):
    def __init__(
            self, world,
            pos: list[int],
            node_size: list[int],
            cell_size: list[int],
            grid_size: list[int],
            depth: int = 0,
        ) -> None:
        super().__init__()
        self.depth: int = depth
        self.world: r3.resource.R3world = world

        self.node_size: list[int] = [*map(int, node_size)]
        self.node_width: int = self.node_size[0]
        self.node_height: int = self.node_size[1]
        self.node_area: int = self.node_width * self.node_height

        self.cell_size: list[int] = [*map(int, cell_size)]
        self.cell_width: int = self.cell_size[0]
        self.cell_height: int = self.cell_size[1]
        self.cell_area: int = self.cell_width * self.cell_height
        
        # cells[cx, cy] = dict[tuple[int], list[R3entity]]
        # cells[cx, cy][nx, ny] = [entities...]
        self.loaded_cells: list[tuple[int]] = []
        self.cells: dict[tuple[int, int], dict[tuple[int, int], list[r3.resource.R3entity]]] = {}
        
        self.size: list[int] = [*map(int, grid_size)]
        self.width: int = self.size[0]
        self.height: int = self.size[1]
        self.area: int = self.width * self.height
        
        self.cell_size_raw: list[int] = mul_v2(self.cell_size, self.node_size)
        self.size_raw: list[int] = mul_v2(self.cell_size_raw, self.size)
        
        self.pos: list[int] =  [*map(int, pos)]
        self.x: int = self.pos[0]
        self.y: int = self.pos[1]
        self.center: list[int] = add_v2(self.pos, div_v2i(self.size, 2))

        self._freeze()

    def cell_transform(self, pos: list[int|float]) -> tuple[int, int]:
        cell_pos = div2_v2i(sub_v2(pos, self.pos), mul_v2(self.cell_size, self.node_size))
        return tuple(cell_pos)
    
    def node_transform(self, pos: list[int | float]) -> tuple[tuple[int, int], tuple[int, int]]:
        global_nx, global_ny = div2_v2i(sub_v2(pos, self.pos), self.node_size)

        ncx = global_nx // self.cell_width
        ncy = global_ny // self.cell_height
        lnx = global_nx % self.cell_width
        lny = global_ny % self.cell_height

        # fixes python's negative modulo :|
        if lnx < 0:
            lnx += self.cell_width
            ncx -= 1
        if lny < 0:
            lny += self.cell_height
            ncy -= 1

        return (ncx, ncy), (lnx, lny)


    def insert(self, entity: "r3.resource.R3entity") -> None:
        cell_pos, node_pos = self.node_transform(entity.pos)

        if cell_pos not in self.cells:
            self.cells[cell_pos] = {}
            self.loaded_cells.append(cell_pos)

        cell = self.cells[cell_pos]

        if node_pos not in cell: cell[node_pos] = []

        node = cell[node_pos]
        if entity not in node:
            node.append(entity)

    def remove(self, entity: "r3.resource.R3entity") -> None:
        if entity.pos[0] >= self.size_raw[0] or entity.pos[1] >= self.size_raw[1]: return

        cell_pos = self.cell_transform(entity.pos)
        node_pos = self.node_transform(entity.pos)

        cell = self.cells.get(cell_pos, None)
        if cell is None: return

        node = cell.get(node_pos, None)
        if node is None: return

        if entity in node:
            node.remove(entity)
            if not node:  # node empty
                del cell[node_pos]
            if not cell:  # cell empty
                del self.cells[cell_pos]
                if cell_pos in self.loaded_cells:
                    self.loaded_cells.remove(cell_pos)


    @R3private
    def _insert(self, entity: "r3.resource.R3entity", cell_pos: list[int], node_pos: list[int]) -> None:
        if cell_pos not in self.cells:
            self.cells[cell_pos] = {}
            self.loaded_cells.append(cell_pos)

        cell = self.cells[cell_pos]

        if node_pos not in cell: cell[node_pos] = []

        node = cell[node_pos]
        if entity not in node:
            node.append(entity)

    @R3private
    def _remove(self, entity: "r3.resource.R3entity", cell_pos: list[int], node_pos: list[int]) -> None:
        if cell_pos[0] >= self.cell_size[0] or cell_pos[1] >= self.cell_size[1]\
        or node_pos[0] >= self.node_size[0] or node_pos[1] >= self.node_size[1]: return

        cell = self.cells.get(cell_pos, None)
        if cell is None: return

        node = cell.get(node_pos, None)
        if node is None: return

        if entity in node:
            node.remove(entity)
            if not node:  # node empty
                del cell[node_pos]
            if not cell:  # cell empty
                del self.cells[cell_pos]
                if cell_pos in self.loaded_cells:
                    self.loaded_cells.remove(cell_pos)


    def query_node(self, pos: list[int | float]):
        if pos[0] >= self.size_raw[0] or pos[1] >= self.size_raw[1]:
            return

        cell_pos, node_pos = self.node_transform(pos)

        cell = self.cells.get(cell_pos)
        if not cell:
            return

        node = cell.get(node_pos)
        if not node:
            return

        yield from node
            
    def query_neighbor_nodes(self, pos: list[int | float]):
        if pos[0] >= self.size_raw[0] or pos[1] >= self.size_raw[1]:
            return

        global_nx, global_ny = div2_v2i(sub_v2(pos, self.pos), self.node_size)

        for dy in range(-1, 2):
            for dx in range(-1, 2):
                npx = global_nx + dx
                npy = global_ny + dy

                cell_pos, node_pos = self.node_transform(
                    add_v2(self.pos, mul_v2([npx, npy], self.node_size))
                )

                cell = self.cells.get(cell_pos)
                if not cell:
                    continue

                node = cell.get(node_pos)
                if not node:
                    continue

                yield from node

    def query_node_region(self, pos: list[int | float], size: list[int | float]):
        if pos[0] >= self.size_raw[0] or pos[1] >= self.size_raw[1]:
            return

        pos_end = add_v2(pos, size)

        # Top-left and bottom-right in global node space
        n0x, n0y = div2_v2i(sub_v2(pos, self.pos), self.node_size)
        n1x, n1y = div2_v2i(sub_v2(pos_end, self.pos), self.node_size)

        for ny in range(n0y, n1y + 1):
            for nx in range(n0x, n1x + 1):
                # Convert global node coord -> world space -> (cell, node)
                world_pos = add_v2(self.pos, mul_v2([nx, ny], self.node_size))
                cell_pos, node_pos = self.node_transform(world_pos)

                cell = self.cells.get(cell_pos)
                if not cell:
                    continue

                node = cell.get(node_pos)
                if not node:
                    continue

                yield from node


    def query_cell(self, pos: list[int|float]):
        if pos[0] >= self.size_raw[0] or pos[1] >= self.size_raw[1]: return tuple()

        cell = self.cells.get(self.cell_transform(pos), None)
        if cell is None: return tuple()
        
        for node in cell:
            for entity in cell[node]:
                yield entity

    def query_neighbor_cells(self, pos: list[int|float]):
        if pos[0] >= self.size_raw[0] or pos[1] >= self.size_raw[1]: return
        
        cx, cy = self.cell_transform(pos)
        for dy in range(-1, 2, 1):
            for dx in range(-1, 2, 1):
                qpos = (dx + cx, dy + cy)
                cell = self.cells.get(qpos, None)
                if cell is None: continue

                for node in cell:
                    for entity in cell[node]:
                        yield entity
    
    def query_cell_region(self, pos: list[int | float], size: list[int | float]):
        if pos[0] >= self.size_raw[0] or pos[1] >= self.size_raw[1]: return

        cx0, cy0 = self.cell_transform(pos)
        cx1, cy1 = self.cell_transform(add_v2(pos, size))
        for cy in range(cy0, cy1 + 1):
            for cx in range(cx0, cx1 + 1):
                cell_pos = (cx, cy)
                cell = self.cells.get(cell_pos, None)
                if cell is None: continue

                for node in cell:
                    for entity in cell[node]:
                        yield entity

