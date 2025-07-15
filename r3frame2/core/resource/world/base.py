from ...atom import R3atom
from ...globals import pg
from ...utils import div_v2i
import r3frame2 as r3

class R3world(R3atom):
    def __init__(
            self,
            cell_size: list[int] = [32, 32],
            world_origin: list[int] = [0, 0]
        ) -> None:
        super().__init__()
        self.ecs: r3.resource.R3ecs = r3.resource.R3ecs()
        self.partition: r3.resource.R3gridPartition = r3.resource.R3gridPartition(cell_size, world_origin)

        self.origin: list[int] = self.partition.grid_origin
        
        self.cell_area: int = self.partition.cell_area
        self.cell_width: int = self.partition.cell_width
        self.cell_height: int = self.partition.cell_height
        self.cell_size: list[int] = self.partition.cell_size

        self._freeze()
        
    def _write_to_disk(self) -> None: pass
    def _read_from_disk(self) -> None: pass

    def insert(self, entity: "r3.resource.R3entity", pos: list[int|float] = None) -> None:
        self.partition.insert(entity)
    def remove(self, entity: "r3.resource.R3entity", pos: list[int|float] = None) -> None:
        self.partition.remove(entity)
