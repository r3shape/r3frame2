from ..log import R3logger
from ..atom import R3atom
from ..globals import pg
# from ..utils import 
import r3frame2 as r3

class R3database(R3atom):
    def __init__(self) -> None:
        self.surf: dict[str, r3.resource.R3surf] =          {}
        self.anim: dict[str, r3.resource.R3anim] =          {}
        self.atlas: dict[str, r3.resource.R3atlas] =        {}
        self.entity: dict[str, r3.resource.R3entity] =      {}
        self.element: dict[str, r3.resource.R3element] =    {}

    def _valid_key(self, cache: str, key: str) -> bool:
        if not getattr(self, cache, 0):
            R3logger.error(f"[R3database] invalid cache attr: (cache){cache}")
            return 0
        elif not getattr(self, cache).get(key, 0):
            R3logger.error(f"[R3database] invalid cache key: (cache){cache} (key){key}")
            return 0
        else: return 1
