#----------------------------------------------------------------------

    # Libraries
from PySide6.QtWidgets import QLabel, QFrame
from PySide6.QtCore import Qt
from data.lib.QtUtils import QGridFrame, QFileButton, QFiles, QBaseApplication, QLangData
from data.lib.widgets.project import ProjectKeys
from ...BaseWidget import BaseWidget
#----------------------------------------------------------------------

    # Class
class LoaderWidget(BaseWidget):
    _lang: QLangData = QLangData.NoTranslation()

    _open_file_icon: str = ''


    @staticmethod
    def init(app: QBaseApplication) -> None:
        LoaderWidget._lang = app.get_lang_data('OpenProjectDialog.game.Wii.NSMBW.loader')
        LoaderWidget._open_file_icon = f'{app.save_data.get_icon_dir()}filebutton/file.png'


    def __init__(self, data: dict) -> None:
        super().__init__()

        loader_data: dict = data['data'].get(ProjectKeys.Wii.NSMBW.Loader, None) if data else None

        lang = self._lang

        self.layout_.setSpacing(30)
        self.layout_.setContentsMargins(0, 0, 16, 0)

        topframe = QGridFrame()
        topframe.layout_.setSpacing(8)
        topframe.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.addWidget(topframe, self.layout_.count(), 0)

        label = QLabel(lang.get('QLabel.title'))
        label.setProperty('h', 1)
        label.setProperty('margin-left', True)
        topframe.layout_.addWidget(label, 0, 0)

        frame = QFrame()
        frame.setProperty('separator', True)
        frame.setFixedHeight(4)
        topframe.layout_.addWidget(frame, 1, 0)

        root_frame = QGridFrame()
        root_frame.layout_.setSpacing(16)
        root_frame.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.addWidget(root_frame, self.layout_.count(), 0)
        self.layout_.setAlignment(root_frame, Qt.AlignmentFlag.AlignTop)


        label = self._text_group(lang.get('QLabel.loaderFile.title'), lang.get('QLabel.loaderFile.description'))
        root_frame.layout_.addWidget(label, root_frame.layout_.count(), 0)

        kw = ('edit' if loader_data else 'open') + 'LoaderFile'
        l = {
            "title": lang.get(f'QFileButton.{kw}.title'),
            "dialog": lang.get(f'QFileButton.{kw}.dialog')
        }

        self.loader_file_button = QFileButton(
            None,
            l,
            loader_data['path'] if loader_data else None,
            self._open_file_icon,
            QFiles.Dialog.OpenFileName,
            'All supported files (*.s *.S);;ASM (*.s *.S)'
        )
        self.loader_file_button.setFixedWidth(350)
        root_frame.layout_.addWidget(self.loader_file_button, root_frame.layout_.count(), 0)
        root_frame.layout_.setAlignment(self.loader_file_button, Qt.AlignmentFlag.AlignLeft)


        frame = QFrame()
        frame.setProperty('border-top', True)
        frame.setFixedHeight(1)
        root_frame.layout_.addWidget(frame, root_frame.layout_.count(), 0)


        label = self._text_group(lang.get('QLabel.outputFile.title'), lang.get('QLabel.outputFile.description'))
        root_frame.layout_.addWidget(label, root_frame.layout_.count(), 0)

        kw = ('edit' if loader_data else 'open') + 'OutputFile'
        l = {
            "title": lang.get(f'QFileButton.{kw}.title'),
            "dialog": lang.get(f'QFileButton.{kw}.dialog')
        }

        self.loader_output_file_button = QFileButton(
            None,
            l,
            loader_data.get('outputFile', None) if loader_data else None,
            self._open_file_icon,
            QFiles.Dialog.OpenFileName,
            'All supported files (*.bin);;Binary (*.bin)'
        )
        self.loader_output_file_button.setFixedWidth(350)
        root_frame.layout_.addWidget(self.loader_output_file_button, root_frame.layout_.count(), 0)
        root_frame.layout_.setAlignment(self.loader_output_file_button, Qt.AlignmentFlag.AlignLeft)


    def export(self) -> dict | None:
        if self.loader_file_button.path() in self._forbidden_paths: return None

        return {
            'path': self.loader_file_button.path(),
            'outputFile': self.loader_output_file_button.path() if self.loader_output_file_button.path() not in self._forbidden_paths else None,
        }
#----------------------------------------------------------------------
