#----------------------------------------------------------------------

    # Libraries
from data.lib.storage import XMLNode
#----------------------------------------------------------------------

    # Class
class BaseSprite:
    def __init__(self, data: XMLNode) -> None:
        pass

    def export(self) -> XMLNode:
        return XMLNode('sprite')

    def copy(self) -> 'BaseSprite':
        return BaseSprite(self.export())

    @staticmethod
    def create() -> 'BaseSprite':
        return BaseSprite(XMLNode('sprite'))
#----------------------------------------------------------------------
