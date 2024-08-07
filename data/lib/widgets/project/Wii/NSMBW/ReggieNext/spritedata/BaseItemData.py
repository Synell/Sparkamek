#----------------------------------------------------------------------

    # Libraries
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QLabel, QPushButton
from PySide6.QtCore import Qt, Signal
from data.lib.QtUtils import QDragListItem, QGridWidget, QBaseApplication, QSaveData, QNamedTextEdit, QNamedToggleButton, QssSelector, QLangData
from ..sprites.BaseItem import BaseItem
from .NybbleData import NybbleData
from .ReqNybbleData import ReqNybbleData
#----------------------------------------------------------------------

    # Class
class BaseItemData(QDragListItem):
    type: str = 'BaseItem'
    child_cls: BaseItem = BaseItem
    nybble_type: NybbleData.Type = NybbleData.Type.All

    _normal_color = '#FFFFFF'
    _checked_color = '#FFFFFF'

    deleted = Signal(QDragListItem)
    selected = Signal(QDragListItem, QGridWidget or None)
    data_changed = Signal()

    _lang: QLangData = QLangData.NoTranslation()

    _delete_icon = None

    def init(app: QBaseApplication) -> None:
        BaseItemData._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.projectWidget.Wii.NSMBW.ReggieNextWidget.SpriteWidget.BaseItemData')
        BaseItemData._delete_icon = app.get_icon('pushbutton/deleteBig.png', True, QSaveData.IconMode.Local)

        BaseItemData._normal_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'BaseItemData': True}),
            QssSelector(widget = 'QLabel')
        )
        BaseItemData._checked_color = app.qss.search(
            QssSelector(widget = 'QWidget', attributes = {'color': app.window.property('color')}),
            QssSelector(widget = 'QWidget', attributes = {'BaseItemData': True, 'color': 'main'}),
            QssSelector(widget = 'QLabel', attributes = {'checked': True})
        )['color']

        NybbleData.init(app)
        ReqNybbleData.init(app)

    def __init__(self, data: BaseItem, path: str) -> None:
        super().__init__()

        self.setProperty('color', 'main')
        self.setProperty('side', 'all')
        self.setProperty('checkable', True)
        self.setProperty('checked', False)
        self.setProperty('bottom-border-only', True)
        self.setProperty('border-radius', 8)

        self._data = data

        self.layout_.setContentsMargins(10, 10, 10, 10)
        self.layout_.setSpacing(8)


        top_frame = QGridWidget()
        top_frame.layout_.setContentsMargins(0, 0, 0, 0)
        top_frame.layout_.setSpacing(8)
        self.layout_.addWidget(top_frame, 0, 0)

        topleft_frame = QGridWidget()
        topleft_frame.layout_.setContentsMargins(0, 0, 0, 0)
        topleft_frame.layout_.setSpacing(8)
        top_frame.layout_.addWidget(topleft_frame, 0, 0)

        self._type_label = QLabel()
        self._type_label.setProperty('brightsubtitle', True)
        topleft_frame.layout_.addWidget(self._type_label, 0, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self._update_title_text()

        self._content_frame = QGridWidget()
        self._content_frame.layout_.setContentsMargins(0, 0, 0, 0)
        self._content_frame.layout_.setSpacing(8)
        topleft_frame.layout_.addWidget(self._content_frame, 1, 0)


        topright_frame = QGridWidget()
        topright_frame.layout_.setContentsMargins(0, 0, 0, 0)
        topright_frame.layout_.setSpacing(8)
        top_frame.layout_.addWidget(topright_frame, 0, 1, Qt.AlignmentFlag.AlignRight)
        topright_frame.layout_.setColumnStretch(2, 1)

        delete_button = QPushButton()
        delete_button.clicked.connect(self._delete)
        delete_button.setIcon(self._delete_icon)
        delete_button.setProperty('color', 'main')
        delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        topright_frame.layout_.addWidget(delete_button, 0, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)


        bottom_frame = QGridWidget()
        bottom_frame.layout_.setContentsMargins(0, 0, 0, 0)
        bottom_frame.layout_.setSpacing(8)
        self.layout_.addWidget(bottom_frame, 1, 0)

        self._nybbles_label = QLabel()
        self._nybbles_label.setProperty('title', True)
        bottom_frame.layout_.addWidget(self._nybbles_label, 0, 0, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)

        self._settings_label = QLabel()
        self._settings_label.setProperty('title', True)
        bottom_frame.layout_.addWidget(self._settings_label, 0, 1, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)

        self._update_nybbles_settings_text()


        self._property_frame = QGridWidget()
        self._property_frame.layout_.setContentsMargins(0, 0, 0, 0)
        self._property_frame.layout_.setSpacing(20)


        nybble_frame = QGridWidget()
        nybble_frame.layout_.setContentsMargins(0, 0, 0, 0)
        nybble_frame.layout_.setSpacing(8)
        self._property_frame.layout_.addWidget(nybble_frame, self._property_frame.layout_.rowCount(), 0)

        label = QLabel(self._lang.get('QLabel.nybbleTitle'))
        label.setProperty('h', 2)
        label.setProperty('small', True)
        nybble_frame.layout_.addWidget(label, 0, 0)

        self._property_frame._nybble_frame = NybbleData(self._data, self.nybble_type)
        self._property_frame._nybble_frame.data_changed.connect(self._nybble_changed)
        nybble_frame.layout_.addWidget(self._property_frame._nybble_frame, 1, 0)


        self._required_nybbleval_frame = ReqNybbleData(self._data.requirednybblevals, self._data.parent)
        self._required_nybbleval_frame.data_changed.connect(self._reqnybble_changed)
        self._property_frame.layout_.addWidget(self._required_nybbleval_frame, self._property_frame.layout_.rowCount(), 0)


        label = QLabel(self._lang.get('QLabel.propertyTitle'))
        label.setProperty('h', 2)
        label.setProperty('small', True)
        self._property_frame.layout_.addWidget(label, self._property_frame.layout_.rowCount(), 0)

        self._property_last_frame = QGridWidget()
        self._property_last_frame.layout_.setContentsMargins(0, 0, 0, 0)
        self._property_last_frame.layout_.setSpacing(8)
        self._property_frame.layout_.addWidget(self._property_last_frame, self._property_frame.layout_.rowCount(), 0)


        comment_frame = QGridWidget()
        comment_frame.layout_.setContentsMargins(0, 0, 0, 0)
        comment_frame.layout_.setSpacing(8)
        self._property_frame.layout_.addWidget(comment_frame, self._property_frame.layout_.rowCount(), 0)

        self._property_frame._comment_textedit = QNamedTextEdit(None, '', self._lang.get('QNamedTextEdit.comment'))
        self._property_frame._comment_textedit.setText(self._data.comment)
        self._property_frame._comment_textedit.text_edit.textChanged.connect(self._comment_changed)
        comment_frame.layout_.addWidget(self._property_frame._comment_textedit, 0, 0)

        self._property_frame._comment2_textedit = QNamedTextEdit(None, '', self._lang.get('QNamedTextEdit.comment2'))
        self._property_frame._comment2_textedit.setText(self._data.comment2)
        self._property_frame._comment2_textedit.text_edit.textChanged.connect(self._comment2_changed)
        comment_frame.layout_.addWidget(self._property_frame._comment2_textedit, 0, 1)


        advanced_frame = QGridWidget()
        advanced_frame.layout_.setContentsMargins(0, 0, 0, 0)
        advanced_frame.layout_.setSpacing(8)
        self._property_frame.layout_.addWidget(advanced_frame, self._property_frame.layout_.rowCount(), 0)


        self._property_frame.advanced_togglebutton = QNamedToggleButton(None, self._lang.get('QNamedToggleButton.advanced'))
        self._property_frame.advanced_togglebutton.setChecked(self._data.advanced)
        self._property_frame.advanced_togglebutton.toggle_button.stateChanged.connect(self._advanced_changed)
        advanced_frame.layout_.addWidget(self._property_frame.advanced_togglebutton, 0, 0, Qt.AlignmentFlag.AlignLeft)

        self._property_frame.advancedcomment_textedit = QNamedTextEdit(None, '', self._lang.get('QNamedTextEdit.advancedcomment'))
        if not data.advanced: self._property_frame.advancedcomment_textedit.hide()
        self._property_frame.advancedcomment_textedit.setText(self._data.advancedcomment)
        self._property_frame.advancedcomment_textedit.text_edit.textChanged.connect(self._advancedcomment_changed)
        advanced_frame.layout_.addWidget(self._property_frame.advancedcomment_textedit, 0, 1)


    @property
    def data(self) -> BaseItem:
        return self._data


    def _update_title_text(self) -> None:
        s = [
            self._lang.get('QLabel.requiredNybbleValue')
                .replace('%s', str(reqnybble.block), 1)
                .replace('%s', reqnybble.nybbles.export(), 1)
                .replace('%s', reqnybble.values.export(), 1)
            for reqnybble in self._data.requirednybblevals
        ]

        if s:
            t = self._lang.get('QLabel.requiredNybbles').replace('%s', ' | '.join(s))
            self._type_label.setText(f'{self.type} • {t}')

        else: self._type_label.setText(self.type)

    def _update_nybbles_settings_text(self) -> None:
        l = self._data.nybbles.export().split('-')
        if len(l) == 1: l = l[0]
        else: l = (
                self._lang.get('QLabel.nybbleRange')
                    .replace('%s', l[0], 1)
                    .replace('%s', l[1], 1)
                )

        self._nybbles_label.setText(
            self._lang.get('QLabel.nybbles')
                .replace('%s', str(self._data.block), 1)
                .replace('%s', l, 1)
            )
        self._settings_label.setText(
            self._lang.get('QLabel.settings')
                .replace('%s', str(self._data.block), 1)
                .replace('%s', self._data.nybbles.convert2hex_formatted(self._data.block), 1)
            )

    def _delete(self) -> None:
        self.deleted.emit(self)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.set_checked(not self.property('checked'))
        self.selected.emit(self, self._property_frame if self.property('checked') else None)
        return super().mousePressEvent(event)

    def is_checked(self) -> bool:
        return self.property('checked')

    def set_checked(self, checked: bool) -> None:
        self.setProperty('checked', checked)
        self._type_label.setStyleSheet(f'color: {self._checked_color if checked else self._normal_color}')
        self.style().unpolish(self)
        self.style().polish(self)


    def _comment_changed(self) -> None:
        self._data.comment = self._property_frame._comment_textedit.text()
        self.data_changed.emit()

    def _comment2_changed(self) -> None:
        self._data.comment2 = self._property_frame._comment2_textedit.text()
        self.data_changed.emit()

    def _advanced_changed(self, advanced: bool) -> None:
        self._data.advanced = advanced
        self._property_frame.advancedcomment_textedit.setVisible(advanced)
        self.data_changed.emit()

    def _advancedcomment_changed(self) -> None:
        self._data.advancedcomment = self._property_frame.advancedcomment_textedit.text()
        self.data_changed.emit()


    def _nybble_changed(self) -> None:
        self._update_nybbles_settings_text()
        self.data_changed.emit()

    def _reqnybble_changed(self) -> None:
        self._update_title_text()
        self.data_changed.emit()


    def update_extended(self, extended: bool) -> None:
        self._property_frame._nybble_frame.convert_to_extended(extended)
        self._required_nybbleval_frame.convert_to_extended(extended)
        self._update_nybbles_settings_text()
        self._update_title_text()
        self.data_changed.emit()
#----------------------------------------------------------------------
