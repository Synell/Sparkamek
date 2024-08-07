#----------------------------------------------------------------------

    # Libraries
from enum import Enum
from ..QtGui.QUtilsColor import QUtilsColor
#----------------------------------------------------------------------

    # Class
class QLogsColor(Enum):
    Error = QUtilsColor.from_hex('#df2020')
    Warning = QUtilsColor.from_hex('#df9f20')
    Success = QUtilsColor.from_hex('#20df20')
    Info = QUtilsColor.from_hex('#207fdf')
#----------------------------------------------------------------------
