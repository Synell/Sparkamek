#----------------------------------------------------------------------

    # Libraries
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtSvg import *
from PySide6.QtSvgWidgets import *
from math import *
import os, json, sys
from datetime import datetime, timedelta
from data.lib import *
#----------------------------------------------------------------------

    # Class
class Application(QBaseApplication):
    BUILD = '07e79429'
    VERSION = 'Experimental'

    SERVER_NAME = 'Sparkamek'

    TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
    MESSAGE_DURATION = 5000

    ALERT_RAISE_DURATION = 350
    ALERT_PAUSE_DURATION = 2300
    ALERT_FADE_DURATION = 350

    UPDATE_LINK = 'https://github.com/Synell/Sparkamek'

    def __init__(self, platform: QPlatform) -> None:
        super().__init__(platform = platform, single_instance = True)

        self.update_request = None
        self.must_update = False
        self.must_restart = False

        self.setOrganizationName('Synel')
        # self.setApplicationDisplayName('Sparkamek')
        self.setApplicationName('Sparkamek')
        self.setApplicationVersion(self.VERSION)

        self.another_instance_opened.connect(self.on_another_instance)

        self.save_data = SaveData(save_path = os.path.abspath('./data/save.dat').replace('\\', '/'))

        Project.init(self)
        OpenProjectDialog.init(self)

        self.save_data.set_stylesheet(self)
        self.window.setProperty('color', 'blue')

        self.setWindowIcon(QIcon('./data/icons/Sparkamek.svg'))

        self.projects: list[Project] = []

        self.load_colors()
        self.create_widgets()
        self.update_title()

        self.create_about_menu()
        self.create_tray_icon()

        if self.save_data.check_for_updates == 4: self.check_updates()
        elif self.save_data.check_for_updates > 0 and self.save_data.check_for_updates < 4:
            deltatime = datetime.now() - self.save_data.last_check_for_updates

            match self.save_data.check_for_updates:
                case 1:
                    if deltatime > timedelta(days = 1): self.check_updates()
                case 2:
                    if deltatime > timedelta(weeks = 1): self.check_updates()
                case 3:
                    if deltatime > timedelta(weeks = 4): self.check_updates()

        self.window.setMinimumSize(int(self.primaryScreen().size().width() * (8 / 15)), int(self.primaryScreen().size().height() * (14 / 27))) # 128x71 -> 1022x568



    def on_another_instance(self) -> None:
        self.window.showMinimized()
        self.window.setWindowState(self.window.windowState() and (not Qt.WindowState.WindowMinimized or Qt.WindowState.WindowActive))



    def update_title(self) -> None:
        self.window.setWindowTitle(self.save_data.language_data['QMainWindow']['title'] + f' | Version: {self.VERSION} | Build: {self.BUILD}')

    def load_colors(self) -> None:
        qss = super().load_colors()

        SaveData.COLOR_LINK = self.COLOR_LINK



    def settings_menu(self) -> None:
        if self.save_data.settings_menu(self):
            self.load_colors()



    def not_implemented(self, text = '') -> None:
        if text:
            w = QDropDownWidget(text = lang['details'], widget = QLabel(text))
        else: w = None

        lang = self.save_data.language_data['QMessageBox']['critical']['notImplemented']

        QMessageBoxWithWidget(
            app = self,
            title = lang['title'],
            text = lang['text'],
            icon = QMessageBoxWithWidget.Icon.Critical,
            widget = w
        ).exec()

    def create_widgets(self) -> None:
        self.root = QGridFrame()
        self.root.grid_layout.setSpacing(0)
        self.root.grid_layout.setContentsMargins(0, 0, 0, 0)

        self.window.setCentralWidget(self.root)

        self.create_top_bar()
        self.create_main_menu()


    def create_top_bar(self) -> None:
        lang = self.save_data.language_data['QMainWindow']['topBar']

        top_menu = QGridFrame()
        top_menu.grid_layout.setSpacing(10)
        top_menu.grid_layout.setContentsMargins(16, 16, 16, 16)
        top_menu.setProperty('light', True)
        top_menu.setProperty('border-bottom', True)


        left_frame = QGridFrame()
        left_frame.grid_layout.setSpacing(10)
        left_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        top_menu.grid_layout.addWidget(left_frame, 0, 0, Qt.AlignmentFlag.AlignLeft)

        open_project_button = QPushButton(lang['QPushButton']['openProject'])
        open_project_button.setProperty('icon-padding', True)
        open_project_button.setProperty('color', 'main')
        open_project_button.setCursor(Qt.CursorShape.PointingHandCursor)
        open_project_button.setIcon(self.save_data.get_icon('pushbutton/open.png', mode = QSaveData.IconMode.Local))
        open_project_button.clicked.connect(self.open_project_clicked)
        left_frame.grid_layout.addWidget(open_project_button, 0, 0)

        # edit_project_button = QPushButton(lang['QPushButton']['editProject'])
        # edit_project_button.setProperty('icon-padding', True)
        # edit_project_button.setProperty('color', 'main')
        # edit_project_button.setCursor(Qt.CursorShape.PointingHandCursor)
        # edit_project_button.setIcon(self.save_data.get_icon('pushbutton/edit.png', mode = QSaveData.IconMode.Local))
        # edit_project_button.clicked.connect(self.not_implemented)
        # edit_project_button.setDisabled(True)
        # left_frame.grid_layout.addWidget(edit_project_button, 0, 1)


        right_frame = QGridFrame()
        right_frame.grid_layout.setSpacing(10)
        right_frame.grid_layout.setContentsMargins(0, 0, 0, 0)
        top_menu.grid_layout.addWidget(right_frame, 0, 0, Qt.AlignmentFlag.AlignRight)

        self.update_button = QPushButton(lang['QPushButton']['update'])
        self.update_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_button.clicked.connect(self.update_click)
        self.update_button.setProperty('color', 'main')
        self.update_button.setProperty('transparent', True)
        right_frame.grid_layout.addWidget(self.update_button, 0, 1)
        self.update_button.setVisible(False)

        settings_button = QPushButton(lang['QPushButton']['settings'])
        settings_button.setProperty('icon-padding', True)
        settings_button.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_button.setIcon(self.save_data.get_icon('pushbutton/settings.png', mode = QSaveData.IconMode.Local))
        settings_button.clicked.connect(self.settings_menu)
        right_frame.grid_layout.addWidget(settings_button, 0, 2)


        self.root.grid_layout.addWidget(top_menu, 0, 0, Qt.AlignmentFlag.AlignTop)


    def create_main_menu(self) -> None:
        lang = self.save_data.language_data['QMainWindow']['QSlidingStackedWidget']

        def create_empty_menu() -> QGridFrame:
            sublang = lang['emptyMenu']
            w = QGridFrame()
            w.grid_layout.setSpacing(10)
            w.grid_layout.setContentsMargins(16, 16, 16, 16)

            frame = QGridFrame()
            frame.grid_layout.setSpacing(10)
            frame.grid_layout.setContentsMargins(0, 0, 0, 0)

            icon = QIconWidget(
                icon = self.save_data.get_icon('mainmenu/empty.png', mode = QSaveData.IconMode.Local),
                icon_size = QSize(72, 72),
                check_file = False
            )
            frame.grid_layout.addWidget(icon, 0, 0, Qt.AlignmentFlag.AlignCenter)

            label = QLabel(sublang['QLabel']['title'])
            label.setProperty('h', 2)
            frame.grid_layout.addWidget(label, 1, 0, Qt.AlignmentFlag.AlignCenter)

            label = QLabel(sublang['QLabel']['text'])
            label.setProperty('h', 4)
            frame.grid_layout.addWidget(label, 2, 0, Qt.AlignmentFlag.AlignCenter)

            frame.grid_layout.setRowStretch(3, 1)
            w.grid_layout.addWidget(frame, 0, 0, Qt.AlignmentFlag.AlignCenter)

            return w


        def create_projects_menu() -> QSidePanelWidget:
            sidepanelwidget = QSidePanelWidget(width = 220, direction = QSlidingStackedWidget.Direction.Automatic)
            sidepanelwidget.setProperty('color', 'main')

            return sidepanelwidget


        self.main_menu = QSlidingStackedWidget()

        em = create_empty_menu()
        self.main_menu.addWidget(em)

        self.sidepanelwidget: QSidePanelWidget = create_projects_menu()
        self.main_menu.addWidget(self.sidepanelwidget)

        self.root.grid_layout.addWidget(self.main_menu, 1, 0)

        if not self.save_data.projects: return

        for project in self.save_data.projects:
            self.projects.append(Project(project = project['data']))
            self.sidepanelwidget.add_widget(self.projects[-1], project['name'], project['icon'])

        self.main_menu.setCurrentIndex(1)



    def open_project_clicked(self) -> None:
        result = OpenProjectDialog(self.window).exec()
        print(result)



    def check_updates(self) -> None:
        self.update_request = RequestWorker([self.UPDATE_LINK])
        self.update_request.signals.received.connect(self.check_updates_release)
        self.update_request.signals.failed.connect(self.check_updates_failed)
        self.update_request.start()

    def check_updates_release(self, rel: dict, app: str) -> None:
        self.update_request.exit()
        self.must_update_link = RequestWorker.get_release(rel, None).link
        if rel['tag_name'] > self.BUILD: self.set_update(True)
        else: self.save_data.last_check_for_updates = datetime.now()

    def check_updates_failed(self, error: str) -> None:
        self.update_request.exit()
        print('Failed to check for updates:', error)

    def set_update(self, update: bool) -> None:
        self.update_button.setVisible(update)

    def update_click(self) -> None:
        self.save_data.save()
        self.must_update = self.must_update_link
        self.exit()



    def create_about_menu(self) -> None:
        self.about_menu = QMenu(self.window)
        self.about_menu.setCursor(Qt.CursorShape.PointingHandCursor)

        act = self.about_menu.addAction(self.save_data.get_icon('menubar/qt.png', mode = QSaveData.IconMode.Global), self.save_data.language_data['QMenu']['about']['PySide'])
        act.triggered.connect(self.aboutQt)

        act = self.about_menu.addAction(QIcon('./data/icons/Sparkamek.svg'), self.save_data.language_data['QMenu']['about']['Sparkamek'])
        act.triggered.connect(self.about_clicked)

        self.about_menu.addSeparator()

        act = self.about_menu.addAction(self.save_data.get_icon('menubar/bug.png', mode = QSaveData.IconMode.Local), self.save_data.language_data['QMenu']['reportBug'])
        act.triggered.connect(lambda: QDesktopServices.openUrl(QUrl('https://github.com/Synell/Sparkamek/issues')))

        self.about_menu.addSeparator()

        def create_donate_menu():
            donate_menu = QMenu(self.save_data.language_data['QMenu']['donate']['title'], self.window)
            donate_menu.setIcon(self.save_data.get_icon('menubar/donate.png'))

            buymeacoffee_action = QAction(self.save_data.get_icon('menubar/buyMeACoffee.png'), 'Buy Me a Coffee', self.window)
            buymeacoffee_action.triggered.connect(lambda: QDesktopServices.openUrl(QUrl('https://www.buymeacoffee.com/Synell')))

            patreon_action = QAction(self.save_data.get_icon('menubar/patreon.png'), 'Patreon', self.window)
            patreon_action.triggered.connect(lambda: QDesktopServices.openUrl(QUrl('https://www.patreon.com/synel')))

            donate_menu.addAction(buymeacoffee_action)
            donate_menu.addAction(patreon_action)

            return donate_menu

        self.about_menu.addMenu(create_donate_menu())

    def about_menu_clicked(self) -> None:
        self.about_menu.popup(QCursor.pos())

    def about_clicked(self) -> None:
        lang = self.save_data.language_data['QAbout']['Sparkamek']
        supports = '\n'.join(f'&nbsp;&nbsp;&nbsp;• <a href=\"{link}\" style=\"color: {self.COLOR_LINK.hex}; text-decoration: none;\">{name}</a>' for name, link in [
            ('GitHub', 'https://github.com')
        ])
        QAboutBox(
            app = self,
            title = lang['title'],
            logo = './data/icons/Sparkamek.svg',
            texts = [
                lang['texts'][0],
                lang['texts'][1].replace('%s', f'<a href=\"https://github.com/Synell\" style=\"color: {self.COLOR_LINK.hex}; text-decoration: none;\">Synel</a>'),
                lang['texts'][2].replace('%s', supports),
                lang['texts'][3].replace('%s', f'<a href=\"https://github.com/Synell/Sparkamek\" style=\"color: {self.COLOR_LINK.hex}; text-decoration: none;\">Sparkamek Github</a>')
            ]
        ).exec()


    def create_tray_icon(self) -> None:
        self.window.closeEvent = self.close_event

        self.sys_tray = QSystemTrayIcon(self)
        self.sys_tray.setToolTip('Sparkamek')
        self.sys_tray.setIcon(QIcon('./data/icons/Sparkamek.svg'))
        self.sys_tray.setVisible(True)
        self.sys_tray.activated.connect(self.on_sys_tray_activated)

        self.sys_tray_menu = QMenu(self.window)
        self.sys_tray_menu.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sys_tray_menu.setProperty('QSystemTrayIcon', True)
        act = self.sys_tray_menu.addAction(self.save_data.get_icon('popup/exit.png'), self.save_data.language_data['QSystemTrayIcon']['QMenu']['exit'])
        act.triggered.connect(self.exit)


    def on_sys_tray_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        match reason:
            case QSystemTrayIcon.ActivationReason.Trigger:
                self.window.show()
                self.window.raise_()
                self.window.setWindowState(Qt.WindowState.WindowActive)
            case QSystemTrayIcon.ActivationReason.Context:
                self.sys_tray_menu.popup(QCursor.pos())


    def close_event(self, event: QCloseEvent) -> None:
        event.ignore()
        self.window.hide()

        if self.save_data.minimize_to_tray:
            if self.save_data.goes_to_tray_notif: self.sys_tray.showMessage(
                self.save_data.language_data['QSystemTrayIcon']['showMessage']['goesToTray']['title'],
                self.save_data.language_data['QSystemTrayIcon']['showMessage']['goesToTray']['message'],
                QSystemTrayIcon.MessageIcon.Information,
                self.MESSAGE_DURATION
            )
            self.show_alert(
                self.save_data.language_data['QSystemTrayIcon']['showMessage']['goesToTray']['message'],
                raise_duration = self.ALERT_RAISE_DURATION,
                pause_duration = self.ALERT_PAUSE_DURATION,
                fade_duration = self.ALERT_FADE_DURATION,
                color = 'main'
            )
        else:
            self.exit()

    def exit(self) -> None:
        if self.update_request:
            self.update_request.exit()

            if self.update_request.isRunning():
                self.update_request.terminate()

        super().exit()
#----------------------------------------------------------------------

    # Main
if __name__ == '__main__':
    app = Application(QPlatform.Windows)
    app.window.showNormal()
    sys.exit(app.exec())
#----------------------------------------------------------------------
