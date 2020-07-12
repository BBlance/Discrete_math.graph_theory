import sys
import time
import PySide2
from PySide2 import QtWidgets
from PySide2.QtCore import QObject, Signal, Qt, QThread
from PySide2.QtGui import QPixmap, QMovie, QFont
from PySide2.QtWidgets import QSplashScreen, QProgressBar, QApplication, QMainWindow


class SplashScreen(QSplashScreen):
    def __init__(self):
        super(SplashScreen, self).__init__()
        self.movie = QMovie(r'20190320111722218.gif')
        self.movie.frameChanged.connect(lambda: self.setPixmap(self.movie.currentPixmap()))
        self.movie.start()

    def mousePressed(self, event):
        pass


class LoadData(QObject):
    finished = Signal()
    message_signal = Signal(str)

    def __init__(self):
        super(LoadData, self).__init__()

    def run(self):
        for i in range(100):
            time.sleep(1)
            self.message_signal.emit(f'程序加载中。。。{i * 10}%')
        self.finished.emit()


class Form(QMainWindow):
    def __init__(self, splash):
        super(Form, self).__init__()
        self.resize(800, 600)

        self.splash = splash

        self.load_thread = QThread()
        self.load_worker = LoadData()
        self.load_worker.moveToThread(self.load_thread)
        self.load_thread.started.connect(self.load_worker.run)
        self.load_worker.message_signal.connect(self.set_message)
        self.load_worker.finished.connect(self.load_worker_finished)
        self.load_thread.start()

        while self.load_thread.isRunning():
            QtWidgets.QApplication.processEvents()  # 不断刷新，保证动画流畅


        self.load_thread.deleteLater()

    def load_worker_finished(self):
        self.load_thread.quit()
        self.load_thread.wait()

    def set_message(self, message):
        self.splash.showMessage(message, Qt.AlignLeft | Qt.AlignBottom, Qt.white)


##  ============窗体测试程序 ================================
if __name__ == "__main__":  # 用于当前窗体测试
    app = QApplication(sys.argv)

    splash = SplashScreen()
    # splash.setPixmap(QPixmap(r'D:\图标\28c932975ab836b2d1939979db0fd8b8.jpg'))  # 设置背景图片
    splash.setFont(QFont('微软雅黑', 10))  # 设置字体
    splash.show()

    app.processEvents()  # 处理主进程，不卡顿
    form = Form(splash)
    form.show()
    splash.finish(form)  # 主界面加载完成后隐藏
    splash.movie.stop()  # 停止动画
    splash.deleteLater()
    app.exec_()
