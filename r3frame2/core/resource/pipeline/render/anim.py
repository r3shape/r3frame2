from ....atom import R3atom
from ....status import R3status
from ....globals import pg
# from ..utils import 
import r3frame2 as r3

class R3anim(R3atom):
    def __init__(
            self,
            path: str,
            size: list[int] = [32, 32],
            frame_duration: float = 4.0,
            frame_offset: list[int] = [0, 0],
    ) -> None:
        super().__init__()
        self.path: str = path
        self.size: list[int] = size[:]
        self.surfaces: list[r3.resource.R3surf] = None

        self.frame_index: int = 0
        self.frame_count: int = 0
        self.frame_scale: float = 0.0
        self.frame_duration: float = frame_duration
        self.frames: list[r3.resource.R3surf] = list()
        self.frame_offset: list[int] = [*map(int, frame_offset)]

        self.set_flag(R3status.anim.LOOP)

        self._freeze()
    
    @property
    def frame(self) -> "r3.resource.R3surf":
        return self.frames[int(self.frame_index / self.frame_duration)]

    @property
    def width(self) -> float:
        return self.size[0]
    @property
    def height(self) -> float:
        return self.size[1]
    @property
    def area(self) -> float:
        return self.size[0] * self.size[1]
