#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QSize
from data.lib.QtUtils import QBaseApplication, QSaveData, QNamedLineEdit, QIconWidget
from .BaseItemData import BaseItemData
from ..sprites.CheckBox import CheckBox
#----------------------------------------------------------------------

    # Class
class CheckBoxData(BaseItemData):
    type: str = 'Check Box'
    child_cls = CheckBox

    _sublang = {}

    _checkbox_icon = None
    _icon_size = QSize(24, 24)

    def init(app: QBaseApplication) -> None:
        CheckBoxData._sublang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.projectWidget.Wii.NSMBW.ReggieNextWidget.SpriteWidget.CheckBoxData')
        CheckBoxData._checkbox_icon = app.get_icon('baseitemdata/checkbox.png', True, QSaveData.IconMode.Local)

        CheckBoxData.type = app.get_lang_data(f'QMainWindow.QSlidingStackedWidget.mainMenu.projects.projectWidget.Wii.NSMBW.ReggieNextWidget.type.{CheckBox.name}')

    def __init__(self, data: CheckBox, path: str) -> None:
        super().__init__(data, path)

        self._title_label = QLabel(self._data.title)
        self._title_label.setProperty('brighttitle', True)
        self._content_frame.layout_.addWidget(self._title_label, 0, 0)

        iw = QIconWidget(None, self._checkbox_icon, self._icon_size, False)
        self._content_frame.layout_.addWidget(iw, 0, 1)

        self._content_frame.layout_.setColumnStretch(2, 1)

        self._property_last_frame.title_lineedit = QNamedLineEdit(None, '', self._sublang.get('QNamedLineEdit.title'))
        self._property_last_frame.title_lineedit.setText(self._data.title)
        self._property_last_frame.title_lineedit.line_edit.textChanged.connect(self._title_changed)
        self._property_last_frame.layout_.addWidget(self._property_last_frame.title_lineedit, 0, 0)


    def _title_changed(self) -> None:
        self._data.title = self._property_last_frame.title_lineedit.text()
        self._title_label.setText(self._data.title)
        self.data_changed.emit()
#----------------------------------------------------------------------
