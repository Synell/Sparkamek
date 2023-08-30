#----------------------------------------------------------------------

    # Libraries
from interface import implements
from data.lib.storage import XMLNode
from .IBaseItem import IBaseItem
from .Macro import Macro
from .Section import Section
#----------------------------------------------------------------------

    # Class
class Options(implements(IBaseItem)):
    name: str = 'options'

    def __init__(self, data: XMLNode = None) -> None:
        if not data: data = self.create().export()

        self.macro_children: list[Macro] = data.get_children(Macro.name)
        self.section_children: list[Section] = data.get_children(Section.name)

    def export(self) -> XMLNode:
        return XMLNode(
            self.name,
            children = (
                [m.export() for m in self.macro_children] +
                [s.export() for s in self.section_children]
            )
        )

    def copy(self) -> 'Options':
        return Options(self.export())

    @staticmethod
    def create() -> 'Options':
        return Options(XMLNode(Options.name))
#----------------------------------------------------------------------
