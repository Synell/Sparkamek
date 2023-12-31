#----------------------------------------------------------------------

    # Libraries
from interface import implements
from data.lib.storage import XMLNode
from .IBaseItem import IBaseItem
from .Region import Region
#----------------------------------------------------------------------

    # Class
class ID(implements(IBaseItem)):
    name: str = 'id'

    def __init__(self, data: XMLNode = None) -> None:
        if not data: data = self.create().export()

        self.game: str = data.get_attribute('game', '') # Optional
        self.developer: str = data.get_attribute('developer', '') # Optional
        self.disc: int = data.get_attribute('disc', -1) # Optional
        self.version: int = data.get_attribute('version', -1) # Optional
        self.region_children: list[Region] = [Region(child) for child in data.get_children(Region.name)]

    def export(self) -> XMLNode:
        return XMLNode(
            self.name,
            (
                ({'game': self.game} if self.game else {}) |
                ({'developer': self.developer} if self.developer else {}) |
                ({'disc': self.disc} if self.disc != -1 else {}) |
                ({'version': self.version} if self.version != -1 else {})
            ),
            ([r.export() for r in self.region_children] if self.region_children else [])
        )

    def copy(self) -> 'ID':
        return ID(self.export())

    @staticmethod
    def create() -> 'ID':
        return ID(XMLNode(ID.name))
#----------------------------------------------------------------------
