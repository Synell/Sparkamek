#----------------------------------------------------------------------

    # Libraries
from data.lib.storage import XML, XMLNode
from .ID import ID
from .Options import Options
from .Patch import Patch
from .Network import Network
#----------------------------------------------------------------------

    # Class
class WiiDisc: # Doc at https://riivolution.github.io/wiki/Patch_Format/ & https://riivolution.github.io/wiki/RiiFS/
    def __init__(self, data: XML = None) -> None:
        if not data: data = self.create().export()

        node: XMLNode = data.root
        if not node: raise ValueError('Invalid XML data')

        self.version: int = int(node.get_attribute('version', 1)) # Required
        self.shiftfiles: bool = bool(node.get_attribute('shiftfiles', False)) # Optional
        self.root: str = node.get_attribute('root', '') # Optional
        self.log: bool = bool(node.get_attribute('log', False)) # Optional

        self.id = ID(node.get_first_child('id'))
        self.options = Options(node.get_first_child('options'))
        self.patch_children = [Patch(p) for p in node.get_children('patch')]

        network = node.get_first_child('network')
        self.network = Network(network) if network else None # Optional

    def export(self) -> XML:
        return XML(
            XMLNode(
                'wiidisc',
                (
                    {'version': self.version} |
                    ({'shiftfiles': self.shiftfiles} if self.shiftfiles else {}) |
                    {'root': self.root} if self.root else {} |
                    ({'log': self.log} if self.log else {})
                ),
                [
                    self.id.export(),
                    self.options.export(),
                    *[p.export() for p in self.patch_children]
                ] + ([self.network.export()] if self.network else [])
            )
        )

    def copy(self) -> 'WiiDisc':
        return WiiDisc(self.export())

    @staticmethod
    def create() -> 'WiiDisc':
        return WiiDisc(XML(XMLNode('wiidisc', attributes = {'version': 1, 'shiftfiles': True, 'root': '/NewerSMBW', 'log': True})))
#----------------------------------------------------------------------
