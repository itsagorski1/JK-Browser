"""
 * COPYRIGHT (c) 2026 JKSW CO. LICENSED UNDER THE GNU GENERAL PUBLIC LICENSE VERSION 3.0
 @version 0.1
 @author JKSW Co.
 @author Jonah Gorski
 @author Kirin Goda
 @author JONAH GORSKI/ITSAGORSKI1
 @author KIRIN GODA/BLOCK120
 @license GNU-GPL-3.0
"""
# Import necessary libraries
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
import sys
import tlds
import qdarktheme

# Create a main window class
class MainWindow(QMainWindow):
    confFile = open("browser.conf", 'rt')
    confText = confFile.read()
    # Constructor of this class
    def __init__(self):
        super(MainWindow, self).__init__()
        # To provide a widget for viewing and editing web documents:
        self.browser = QWebEngineView()
        # To set default browser homepage as google homepage:
        if "searchEngine = 'google'" in self.confText or "searchEngine = " not in self.confText:
            self.browser.setUrl(QUrl("http://www.google.com"))
        elif "searchEngine = 'yahoo'" in self.confText:
            self.browser.setUrl(QUrl("http://yahoo.com"))
        # To set browser as central widget of main window:
        self.setCentralWidget(self.browser)
        # To open browser in a maximized window:
        self.showMaximized()

        # To create a navigation bar:
        navbar = QToolBar()
        navbar.adjustSize()
        # To add the navigation bar to the browser:
        self.addToolBar(navbar)

        # To add back button within navigation bar:
        back_btn = QAction('⮜', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        # To add forward button within navigation bar:
        forward_btn = QAction('⮞', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        # To add reload button within navigation bar:
        reload_btn = QAction('⟳', self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        # To add URL bar within navigation bar:
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.open_url)
        navbar.addWidget(self.url_bar)
        self.browser.urlChanged.connect(self.update_url)

    def checkIfURL(self, url):
        if " " in url or "." not in url:
            if "searchEngine = 'google'" in self.confText or "searchEngine = " not in self.confText:
                return f'https://google.com/search?q={url}'
            elif "searchEngine = 'yahoo'" in self.confText:
                return f'https://search.yahoo.com/search?p={url}'
        elif " " not in url and "." in url:
            return url


    # To navigate to desired URL specified within URL bar:
    def open_url(self):
        url = self.url_bar.text()
        urlValid = self.checkIfURL(url)
        url = urlValid
        if "http://" not in str(url) and "https://" not in str(url):
            self.browser.setUrl(QUrl("http://" + str(url)))
        else:
            self.browser.setUrl(QUrl(url))

    # To update the URL bar contents when navigated from one page to another:
    def update_url(self, q):
        self.url_bar.setText(q.toString())


# To call constructor of the C++ class QApplication:
# Here, sys.argv is used to initialize the QT application
app = QApplication(sys.argv)
qdarktheme.setup_theme()
# To specify name of the browser:
QApplication.setApplicationName("JK Browser")
# To create an object of MainWindow class defined above:
window = MainWindow()
# To run the main event loop and wait until exit() is called:
app.exec()
