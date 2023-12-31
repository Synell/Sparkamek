#----------------------------------------------------------------------

    # Libraries
from data.lib.storage import XMLNode
from .BaseItem import BaseItem
#----------------------------------------------------------------------

    # Class
class External(BaseItem):
    name: str = 'external'

    def __init__(self, data: XMLNode) -> None:
        super().__init__(data)

        self.title = data.get_attribute('title', '')
        self.type = data.get_attribute('type', '')

    def export(self) -> XMLNode:
        sup = super().export()

        return XMLNode(
            self.name,
            (
                ({'title': self.title} if self.title else {}) |
                ({'type': self.type} if self.type else {})
            ) | sup.attributes,
            sup.children,
            sup.value
        )

    def copy(self) -> 'External':
        return External(self.export())

    @staticmethod
    def create() -> 'External':
        return External(XMLNode('external', attributes = {'nybble': 1, 'title': 'New External', 'type': 'actors'}))
#----------------------------------------------------------------------
