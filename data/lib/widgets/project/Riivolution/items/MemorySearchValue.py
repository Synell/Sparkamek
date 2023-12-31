#----------------------------------------------------------------------

    # Libraries
from interface import implements
from data.lib.storage import XMLNode
from .IBaseItem import IBaseItem
#----------------------------------------------------------------------

    # Class
class MemorySearchValue(implements(IBaseItem)):
    name: str = 'memory'
    key: str = 'memorysearchvalue'

    def __init__(self, data: XMLNode = None) -> None:
        if not data: data = self.create().export()

        self.original: int = int(str(data.get_attribute('original', 0)), 16) # Required
        self.value: int = int(str(data.get_attribute('value', 0)), 16) # Required
        self.align: int = data.get_attribute('align', 1) # Optional
        self.comment: str = data.get_attribute('comment', '') # Optional

    def export(self) -> XMLNode:
        return XMLNode(
            self.name,
            (
                {'original': f'{self.original:X}'} |
                {('value'): f'{self.value:X}'} |
                ({'align': self.align} if self.align != 1 else {}) |
                {'search': True} |
                ({'comment': self.comment} if self.comment else {})
            )
        )

    def copy(self) -> 'MemorySearchValue':
        return MemorySearchValue(self.export())

    @staticmethod
    def create() -> 'MemorySearchValue':
        return MemorySearchValue(XMLNode(MemorySearchValue.name))
#----------------------------------------------------------------------
