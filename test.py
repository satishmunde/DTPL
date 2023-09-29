import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window flags to include Qt.WindowMaximized
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximized)

        # Set up your main window content here
        self.setWindowTitle("Maximized Window Example")
        self.setGeometry(100, 100, 800, 600)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec_())
