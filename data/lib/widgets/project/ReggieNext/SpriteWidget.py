#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QPushButton, QLabel
from PySide6.QtCore import Qt, Signal
from data.lib.qtUtils import QBaseApplication, QGridWidget, QSaveData, QDragList, QNamedTextEdit, QNamedLineEdit, QNamedSpinBox, QNamedToggleButton
from data.lib.widgets.ProjectKeys import ProjectKeys
from .sprites.Sprite import Sprite, DualBox, CheckBox, Value, List, External
from .sprites.Dependency import Required, Suggested
from .spritedata import *
from data.lib.storage.xml import XMLNode
#----------------------------------------------------------------------

    # Class
class SpriteWidget(QGridWidget):
    type: ProjectKeys = ProjectKeys.ReggieNext

    _add_entry_icon = None

    _lang = {}

    current_sprite_changed = Signal(Sprite or None)
    sprite_edited = Signal()
    property_entry_selected = Signal(QGridWidget or None)

    def init(app: QBaseApplication) -> None:
        SpriteWidget._lang = app.get_lang_data('QMainWindow.QSlidingStackedWidget.mainMenu.projects.ReggieNextWidget.SpriteWidget')
        SpriteWidget._add_entry_icon = app.get_icon('pushbutton/add.png', True, QSaveData.IconMode.Local)

        DependencyDataItem.init(app)

        BaseItemData.init(app)
        DualBoxData.init(app)
        ValueData.init(app)
        CheckBoxData.init(app)
        ListData.init(app)
        ExternalData.init(app)

    def __init__(self, path: str) -> None:
        super().__init__()

        self._path = path

        self._disable_send = True

        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(30)


        self._top_info_widget = QGridWidget()
        self._top_info_widget.grid_layout.setContentsMargins(0, 0, 0, 0)
        self._top_info_widget.grid_layout.setSpacing(8)
        self.grid_layout.addWidget(self._top_info_widget, 0, 0)

        label = QLabel(self._lang.get_data('QLabel.generalInfo'))
        label.setProperty('h', 2)
        label.setProperty('small', True)
        self._top_info_widget.grid_layout.addWidget(label, 0, 0, 1, 2)

        self._id_spinbox = QNamedSpinBox(None, self._lang.get_data('QNamedSpinBox.spriteID'))
        self._id_spinbox.spin_box.valueChanged.connect(self._send_data)
        self._id_spinbox.setRange(0, 2147483647) # profileID is u32 (2^32 - 1) but QSpinBox are s32 (2^31 - 1) -> Tbf nobody will have 2^31 sprites lmao
        self._id_spinbox.setValue(0)
        self._id_spinbox.setProperty('wide', True)
        self._top_info_widget.grid_layout.addWidget(self._id_spinbox, 1, 0)

        self._name_lineedit = QNamedLineEdit(None, '', self._lang.get_data('QNamedLineEdit.name'))
        self._name_lineedit.line_edit.textChanged.connect(self._send_data)
        self._top_info_widget.grid_layout.addWidget(self._name_lineedit, 1, 1)

        self._used_settings_label = QLabel()
        self._used_settings_label.setProperty('title', True)
        self._top_info_widget.grid_layout.addWidget(self._used_settings_label, 2, 0, 1, 2, Qt.AlignmentFlag.AlignRight)


        toggle_and_comment_frame = QGridWidget()
        toggle_and_comment_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        toggle_and_comment_frame.grid_layout.setSpacing(8)
        self._top_info_widget.grid_layout.addWidget(toggle_and_comment_frame, 3, 0, 1, 2)


        toggle_topframe = QGridWidget()
        toggle_topframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        toggle_topframe.grid_layout.setSpacing(8)
        toggle_and_comment_frame.grid_layout.addWidget(toggle_topframe, 0, 0)

        self._asmhacks_toggle = QNamedToggleButton(None, self._lang.get_data('QNamedToggleButton.asmhacks'), False, True)
        self._asmhacks_toggle.toggle_button.toggled.connect(self._asmhacks_changed)
        toggle_topframe.grid_layout.addWidget(self._asmhacks_toggle, 0, 0)

        self._sizehacks_toggle = QNamedToggleButton(None, self._lang.get_data('QNamedToggleButton.sizehacks'), False, True)
        self._sizehacks_toggle.toggle_button.toggled.connect(self._sizehacks_changed)
        toggle_topframe.grid_layout.addWidget(self._sizehacks_toggle, 0, 1)

        self._noyoshi_toggle = QNamedToggleButton(None, self._lang.get_data('QNamedToggleButton.noyoshi'), False, True)
        self._noyoshi_toggle.toggle_button.toggled.connect(self._noyoshi_changed)
        toggle_topframe.grid_layout.addWidget(self._noyoshi_toggle, 0, 2)


        comment_middleframe = QGridWidget()
        comment_middleframe.grid_layout.setContentsMargins(0, 0, 0, 0)
        comment_middleframe.grid_layout.setSpacing(8)
        toggle_and_comment_frame.grid_layout.addWidget(comment_middleframe, 1, 0)

        self._notes_textedit = QNamedTextEdit(None, '', self._lang.get_data('QNamedTextEdit.notes'))
        self._notes_textedit.text_edit.textChanged.connect(self._notes_changed)
        comment_middleframe.grid_layout.addWidget(self._notes_textedit, 0, 0)

        self._yoshinotes_textedit = QNamedTextEdit(None, '', self._lang.get_data('QNamedTextEdit.yoshinotes'))
        self._yoshinotes_textedit.text_edit.textChanged.connect(self._yoshinotes_changed)
        comment_middleframe.grid_layout.addWidget(self._yoshinotes_textedit, 0, 1)


        self._advancednotes_textedit = QNamedTextEdit(None, '', self._lang.get_data('QNamedTextEdit.advancednotes'))
        self._advancednotes_textedit.text_edit.textChanged.connect(self._advancednotes_changed)
        comment_middleframe.grid_layout.addWidget(self._advancednotes_textedit, 0, 2)


        self._dependencies_widget = QGridWidget()
        self._dependencies_widget.grid_layout.setContentsMargins(0, 0, 0, 0)
        self._dependencies_widget.grid_layout.setSpacing(8)
        self.grid_layout.addWidget(self._dependencies_widget, 1, 0)

        label = QLabel(self._lang.get_data('QLabel.dependencies'))
        label.setProperty('h', 2)
        label.setProperty('small', True)
        self._dependencies_widget.grid_layout.addWidget(label, 0, 0)


        dependencies_bottom_frame = QGridWidget()
        dependencies_bottom_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        dependencies_bottom_frame.grid_layout.setSpacing(30)
        self._dependencies_widget.grid_layout.addWidget(dependencies_bottom_frame, 1, 0)


        required_frame = QGridWidget()
        required_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        required_frame.grid_layout.setSpacing(8)
        dependencies_bottom_frame.grid_layout.addWidget(required_frame, 1, 0, Qt.AlignmentFlag.AlignTop)

        label = QLabel(self._lang.get_data('QLabel.required'))
        label.setProperty('brighttitle', True)
        required_frame.grid_layout.addWidget(label, 0, 0)

        self._required_draglist = QDragList(None, Qt.Orientation.Vertical)
        self._required_draglist.moved.connect(self._required_entry_moved)
        required_frame.grid_layout.addWidget(self._required_draglist, 1, 0)

        self._add_required_entry_button = QPushButton(self._lang.get_data('QPushButton.addEntry'))
        self._add_required_entry_button.setIcon(self._add_entry_icon)
        self._add_required_entry_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._add_required_entry_button.setProperty('color', 'main')
        self._add_required_entry_button.clicked.connect(self._add_required_entry)
        required_frame.grid_layout.addWidget(self._add_required_entry_button, 2, 0)


        suggested_frame = QGridWidget()
        suggested_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        suggested_frame.grid_layout.setSpacing(8)
        dependencies_bottom_frame.grid_layout.addWidget(suggested_frame, 1, 1, Qt.AlignmentFlag.AlignTop)

        label = QLabel(self._lang.get_data('QLabel.suggested'))
        label.setProperty('brighttitle', True)
        suggested_frame.grid_layout.addWidget(label, 0, 0)

        self._suggested_draglist = QDragList(None, Qt.Orientation.Vertical)
        self._suggested_draglist.moved.connect(self._suggested_entry_moved)
        suggested_frame.grid_layout.addWidget(self._suggested_draglist, 1, 0)

        self._add_suggested_entry_button = QPushButton(self._lang.get_data('QPushButton.addEntry'))
        self._add_suggested_entry_button.setIcon(self._add_entry_icon)
        self._add_suggested_entry_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._add_suggested_entry_button.setProperty('color', 'main')
        self._add_suggested_entry_button.clicked.connect(self._add_suggested_entry)
        suggested_frame.grid_layout.addWidget(self._add_suggested_entry_button, 2, 0)


        self._settings_widget = QGridWidget()
        self._settings_widget.grid_layout.setContentsMargins(0, 0, 0, 0)
        self._settings_widget.grid_layout.setSpacing(8)
        self.grid_layout.addWidget(self._settings_widget, 2, 0)

        label = QLabel(self._lang.get_data('QLabel.settings'))
        label.setProperty('h', 2)
        label.setProperty('small', True)
        self._settings_widget.grid_layout.addWidget(label, 0, 0)

        self._settings_draglist = QDragList(None, Qt.Orientation.Vertical)
        self._settings_draglist.moved.connect(self._settings_entry_moved)
        self._settings_widget.grid_layout.addWidget(self._settings_draglist, 1, 0)

        self._add_settings_entry_button = QPushButton(self._lang.get_data('QPushButton.addEntry'))
        self._add_settings_entry_button.setIcon(self._add_entry_icon)
        self._add_settings_entry_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._add_settings_entry_button.setProperty('color', 'main')
        self._add_settings_entry_button.clicked.connect(self._add_settings_entry)
        self._settings_widget.grid_layout.addWidget(self._add_settings_entry_button, 2, 0, Qt.AlignmentFlag.AlignBottom)

        self.sprite = None


    @property
    def sprite(self) -> Sprite or None:
        self._sprite.sprite_name = self._name_lineedit.text()
        self._sprite.id = self._id_spinbox.value()

        return self._sprite

    @sprite.setter
    def sprite(self, sprite: Sprite or None) -> None:
        self._sprite = sprite
        self.current_sprite_changed.emit(sprite)

        self._disable_send = True

        self._settings_draglist.clear()
        self._required_draglist.clear()
        self._suggested_draglist.clear()

        self.setEnabled(sprite is not None)
        self.property_entry_selected.emit(None)

        self._update_used_settings()

        if sprite is None:
            self._name_lineedit.setText('')
            self._id_spinbox.setValue(0)

            self._asmhacks_toggle.setChecked(False)
            self._sizehacks_toggle.setChecked(False)
            self._noyoshi_toggle.setChecked(False)

            self._notes_textedit.setText('')
            self._yoshinotes_textedit.setText('')
            self._advancednotes_textedit.setText('')

        else:
            self._name_lineedit.setText(sprite.sprite_name)
            self._id_spinbox.setValue(sprite.id)

            self._asmhacks_toggle.setChecked(sprite.asmhacks)
            self._sizehacks_toggle.setChecked(sprite.sizehacks)
            self._noyoshi_toggle.setChecked(sprite.noyoshi)

            self._notes_textedit.setText(sprite.notes)
            self._yoshinotes_textedit.setText(sprite.yoshinotes)
            self._advancednotes_textedit.setText(sprite.advancednotes)

            self._required_draglist.clear()
            for required in self._sprite.dependency.required:
                item = DependencyDataItem(required)
                item.deleted.connect(self._delete_required_entry)
                self._required_draglist.add_item(item)

            self._suggested_draglist.clear()
            for suggested in self._sprite.dependency.suggested:
                item = DependencyDataItem(suggested)
                item.deleted.connect(self._delete_suggested_entry)
                self._suggested_draglist.add_item(item)

            for child in sprite.children:
                match child.name:
                    case DualBox.name:
                        item = DualBoxData(child)

                    case Value.name:
                        item = ValueData(child)

                    case CheckBox.name:
                        item = CheckBoxData(child)

                    case List.name:
                        item = ListData(child)

                    case External.name:
                        item = ExternalData(child, self._path)

                    case _:
                        item = BaseItemData(child)

                self._settings_draglist.add_item(item)
                item.selected.connect(self._entry_selected)
                item.deleted.connect(self._delete_settings_entry)
                item.data_changed.connect(self._send_data)

        self._disable_send = False


    def _update_used_settings(self) -> None:
        used_settings = 0
        if self._sprite is not None:
            for child in self._sprite.children:
                used_settings |= child.nybbles.convert2int()

        s = f'{used_settings:016X}'
        self._used_settings_label.setText(self._lang.get_data('QLabel.usedSettings').replace('%s', f'{s[:4]} {s[4:8]} {s[8:12]} {s[12:16]}'))


    def _settings_entry_moved(self, from_: int, to_: int) -> None:
        if self._sprite is None: return
        self._sprite.children.insert(to_, self._sprite.children.pop(from_))
        self._send_data()

    def _required_entry_moved(self, from_: int, to_: int) -> None:
        if self._sprite is None: return
        self._sprite.dependency.required.insert(to_, self._sprite.dependency.required.pop(from_))
        self._send_data()

    def _suggested_entry_moved(self, from_: int, to_: int) -> None:
        if self._sprite is None: return
        self._sprite.dependency.suggested.insert(to_, self._sprite.dependency.suggested.pop(from_))
        self._send_data()

    def _send_data(self, *args) -> None:
        if self._disable_send: return
        self._update_used_settings()
        self.sprite_edited.emit()


    def _add_settings_entry(self) -> None:
        if self._sprite is None: return
        self._send_data()
        # todo: add entry

    def _add_required_entry(self) -> None:
        if self._sprite is None: return

        req = Required.create()
        item = DependencyDataItem(req)
        item.deleted.connect(self._delete_required_entry)
        self._required_draglist.add_item(item)
        self._sprite.dependency.required.append(req)

        self._send_data()

    def _add_suggested_entry(self) -> None:
        if self._sprite is None: return

        sug = Suggested.create()
        item = DependencyDataItem(sug)
        item.deleted.connect(self._delete_suggested_entry)
        self._suggested_draglist.add_item(item)
        self._sprite.dependency.suggested.append(sug)

        self._send_data()

    def _delete_settings_entry(self, item: BaseItemData) -> None:
        if self._sprite is None: return

        self._sprite.children.remove(item.data)
        item.deleteLater()

        self.property_entry_selected.emit(None)
        for item in self._settings_draglist.items:
            item.set_checked(False)

        self._send_data()

    def _delete_required_entry(self, item: BaseItemData) -> None:
        if self._sprite is None: return

        self._sprite.dependency.required.remove(item.data)
        item.deleteLater()
        self._send_data()

    def _delete_suggested_entry(self, item: BaseItemData) -> None:
        if self._sprite is None: return

        self._sprite.dependency.suggested.remove(item.data)
        item.deleteLater()
        self._send_data()

    def _entry_selected(self, sender: BaseItemData, widget: QGridWidget | None) -> None:
        checked = sender.is_checked()

        for item in self._settings_draglist.items:
            item.set_checked(False)

        sender.set_checked(checked)
        self.property_entry_selected.emit(widget)

    def _asmhacks_changed(self, state: bool) -> None:
        if self._sprite is None: return
        self._sprite.asmhacks = state
        self._send_data()

    def _sizehacks_changed(self, state: bool) -> None:
        if self._sprite is None: return
        self._sprite.sizehacks = state
        self._send_data()

    def _noyoshi_changed(self, state: bool) -> None:
        if self._sprite is None: return
        self._sprite.noyoshi = state
        self._send_data()

    def _notes_changed(self) -> None:
        if self._sprite is None: return
        self._sprite.notes = self._notes_textedit.text()
        self._send_data()

    def _yoshinotes_changed(self) -> None:
        if self._sprite is None: return
        self._sprite.yoshinotes = self._yoshinotes_textedit.text()
        self._send_data()

    def _advancednotes_changed(self) -> None:
        if self._sprite is None: return
        self._sprite.advancednotes = self._advancednotes_textedit.text()
        self._send_data()
#----------------------------------------------------------------------
