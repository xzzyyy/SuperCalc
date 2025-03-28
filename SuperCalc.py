from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QPushButton
from PyQt6.QtGui import QPainter, QColor, QPen, QGuiApplication, QBrush
from PyQt6.QtCore import Qt, QRect


# create recognition class
class CRecognition:
    def __init__(self):
        pass

    def recognize(self, screenshot):
        # choose recognition framework
        # let's use EasyOCR
        return [0]


class ScreenshotWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.start_point = None
        self.end_point = None

        screen = QGuiApplication.primaryScreen()
        self.screen_geom = screen.geometry()
        self.setGeometry(self.screen_geom)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawObjects(qp)
        qp.end()

    def drawObjects(self, qp):
        brush = QBrush(QColor(255, 255, 255, 25))
        qp.setBrush(brush)
        qp.drawRect(self.screen_geom)

        if self.start_point and self.end_point and self.start_point != self.end_point:
            qp.fillRect(QRect(self.start_point, self.end_point).normalized(), QColor(0, 0, 255, 50))
            pen = QPen(QColor(255, 0, 0), 2)
            qp.setPen(pen)
            qp.drawRect(QRect(self.start_point, self.end_point).normalized())

    def mousePressEvent(self, event):
        self.start_point = event.pos()
        self.end_point = event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        self.end_point = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.end_point = event.pos()
        self.update()
        self.takeScreenshot()
        # close the window after screenshot is made
        self.close()

    def takeScreenshot(self):
        rect = QRect(self.start_point, self.end_point).normalized()
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(0, rect.x(), rect.y(), rect.width(), rect.height())
        screenshot.save("screenshot.png", "png")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        cw = QWidget()
        self.setCentralWidget(cw)
        self.setWindowTitle("SuperCalc")
        self.setMinimumSize(640, 480)

        v_lay = QVBoxLayout()
        cw.setLayout(v_lay)

        self.bt_select = QPushButton("Select region")
        self.bt_select.clicked.connect(self.select_clicked)
        v_lay.addWidget(self.bt_select)

        self.screenshot_win = ScreenshotWindow()

    def select_clicked(self):
        self.screenshot_win.show()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
