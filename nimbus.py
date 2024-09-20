from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QStatusBar, QToolBar, QLineEdit, QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView
import sys


class MainWindow(QMainWindow):
    HOME = "https://www.google.com"

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(MainWindow.HOME))
        self.browser.urlChanged.connect(self.update_url_bar)
        self.browser.loadFinished.connect(
            lambda: self.setWindowTitle(self.browser.page().title() + " - NIMBUS Browser")
        )
        self.setCentralWidget(self.browser)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        nav = QToolBar("Navigation")
        self.addToolBar(nav)

        back_btn = QAction("Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(self.browser.back)
        nav.addAction(back_btn)

        next_btn = QAction("Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(self.browser.forward)
        nav.addAction(next_btn)

        reload_btn = QAction("Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(self.browser.reload)
        nav.addAction(reload_btn)

        home_btn = QAction("Home", self)
        home_btn.setStatusTip("Go Home")
        home_btn.triggered.connect(self.go_home)
        nav.addAction(home_btn)

        nav.addSeparator()

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.change_url)
        nav.addWidget(self.url_bar)

        stop_btn = QAction("Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(self.browser.stop)
        stop_btn.triggered.connect(lambda: stop_btn.setDisabled(True))
        self.browser.loadStarted.connect(lambda: stop_btn.setDisabled(False))
        self.browser.loadFinished.connect(lambda: stop_btn.setDisabled(True))
        nav.addAction(stop_btn)

        self.show()

    def go_home(self):
        self.browser.setUrl(QUrl(MainWindow.HOME))

    def change_url(self):
        q = QUrl(self.url_bar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.browser.setUrl(q)

    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)


app = QApplication(sys.argv)
app.setApplicationName("NIMBUS Browser")
window = MainWindow()
raise SystemExit(app.exec())
