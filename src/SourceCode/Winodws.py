import sys
import os

from PyQt5.QtWidgets import QLayout, QMainWindow, QWidget, QApplication, QHBoxLayout, QToolBar, QVBoxLayout, QAction, \
    qApp, QPushButton, QMenu, QListView, QComboBox, QLabel, QColorDialog, QDockWidget, QWizard, QWizardPage, \
    QMessageBox, QFileDialog, QActionGroup
from PyQt5.QtGui import QIcon, QColor, QPixmap, QCloseEvent
from PyQt5.QtCore import Qt, QSize
from PyQt5.Qt import QCloseEvent
from PainterBoard import Demo
from OperatorFile import OperatorData


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__InitData(QApplication.desktop())
        self.__InitView()

    def __InitData(self, desktop=QApplication.desktop()):
        self.painterBoard = Demo()
        self.operatorData = OperatorData()
        self.painterBoard.ChangePenColor(QColor('black'))
        self.painterBoard.ChangePenThickness(3, 5)

        self.__colorList = QColor.colorNames()
        self.screenRect = desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()

    def __InitView(self):
        self.resize(self.width / 1.5, self.height / 1.8)
        self.painterBoard.resize(self.width / 2, self.height / 2)
        self.setWindowTitle('离散数学可视化')  # 给窗口命名

        self.setCentralWidget(self.painterBoard)

        # 菜单栏
        self.menuBar = self.menuBar()

        self.fileMenu = self.menuBar.addMenu('&菜单')
        self.editMenu = self.menuBar.addMenu('&编辑')
        self.toolsMenu = self.menuBar.addMenu('&工具')
        self.settingMenu = self.menuBar.addMenu('&设置 ')
        self.modeMenu = self.menuBar.addMenu('&模式')
        self.windowMenu = self.menuBar.addMenu('&窗口')
        self.helpMenu = self.menuBar.addMenu('&帮助')

        #  属性栏
        self.propertyDock = QWidget()

        self.setWindowTitle('离散数学可视化认知系统')
        self.setWindowIcon(QIcon('/images/GraphTheory.png'))

        self.statusBar = self.statusBar()

        self.__initStatusBar()

        self.__initFileMenu()
        self.__initEditMenu()
        self.__initModeMenu()
        self.__initSettingMenu()
        self.__initToolsMenu()
        self.__initWindowsMenu()
        self.__initHelpMenu()

        self.__initToolBar()
        self.__initPropertyDock()

    #  初始化文件菜单列表
    def __initFileMenu(self):
        #  菜单功能
        self.createFileAction = QAction(QIcon('images/CreateFile.png'), '新建', self)
        self.openFileAction = QAction(QIcon('/images/OpenFile.png'), '&打开', self)

        self.openRecentFileAction = QMenu('&最近打开的', self)

        self.closeFileAction = QAction('&关闭', self)
        self.closeAllFileAction = QAction('&关闭所有', self)
        self.saveFileAction = QAction(QIcon('/images/SaveFile.png'), '&保存', self)
        self.saveAllFileAction = QAction('&保存全部', self)
        self.saveAsFileAction = QAction('&另存为', self)
        self.importDataAction = QAction('&导入数据', self)
        self.outputDataAction = QAction('&导出数据', self)
        self.exitAppAction = QAction('&退出', self)

        #  设置快捷键
        self.createFileAction.setShortcut('Ctrl+N')
        self.openFileAction.setShortcut('Ctrl+O')
        self.saveFileAction.setShortcut('Ctrl+S')
        self.importDataAction.setShortcut('I')
        self.outputDataAction.setShortcut('E')
        self.exitAppAction.setShortcut('X')

        # 设置状态栏状态提示
        self.createFileAction.setStatusTip('新建文件')
        self.openFileAction.setStatusTip('打开文件')
        self.openRecentFileAction.setStatusTip('最近打开的文件')
        self.closeFileAction.setStatusTip('关闭文件')
        self.closeAllFileAction.setStatusTip('关闭全部文件')
        self.saveAllFileAction.setStatusTip('保存全部文件')
        self.saveAsFileAction.setStatusTip('另存为')
        self.saveFileAction.setStatusTip('保存文件')
        self.importDataAction.setStatusTip('导入图数据')
        self.outputDataAction.setStatusTip('导出图数据')
        self.exitAppAction.setStatusTip('退出程序')

        # 设置提示
        self.createFileAction.setToolTip('新建文件')
        self.openFileAction.setToolTip('打开文件')
        self.closeFileAction.setToolTip('关闭当前文件')
        self.closeAllFileAction.setToolTip('关闭所有文件')
        self.saveAllFileAction.setToolTip('保存全部文件')
        self.saveAsFileAction.setToolTip('另存为其他文件')
        self.importDataAction.setToolTip('导入数据')
        self.outputDataAction.setToolTip('导出数据')
        self.saveFileAction.setToolTip('保存文件')
        self.exitAppAction.setToolTip('退出程序')

        #  动作绑定
        self.exitAppAction.triggered.connect(self.close)
        self.openFileAction.triggered.connect(self.open_file)
        self.saveFileAction.triggered.connect(self.save_file)

        #  添加菜单动作
        self.fileMenu.addAction(self.createFileAction)
        self.fileMenu.addAction(self.openFileAction)
        self.fileMenu.addMenu(self.openRecentFileAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.closeFileAction)
        self.fileMenu.addAction(self.closeAllFileAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.saveAllFileAction)
        self.fileMenu.addAction(self.saveAsFileAction)
        self.fileMenu.addAction(self.saveFileAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.importDataAction)
        self.fileMenu.addAction(self.outputDataAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAppAction)

    # 初始化编辑菜单列表
    def __initEditMenu(self):
        #  创建功能动作
        self.uodoAction = QAction('撤销', self)
        self.redoAction = QAction('重做', self)
        self.cutAction = QAction('剪切', self)
        self.copyAction = QAction('复制', self)
        self.pasteAction = QAction('粘贴', self)
        self.deleteAction = QAction('删除', self)

        self.findMenu = QMenu('查找', self)

        self.findAction = QAction('查找', self)
        self.replaceAction = QAction('替换', self)


        #  设置快捷键
        self.uodoAction.setShortcut('Ctrl+Z')
        self.redoAction.setShortcut('Ctrl+Shift+Z')
        self.cutAction.setShortcut('Ctrl+X')
        self.copyAction.setShortcut('Ctrl+C')
        self.pasteAction.setShortcut('Ctrl+V')
        self.deleteAction.setShortcut('Delete')
        self.findAction.setShortcut('Ctrl+F')
        self.replaceAction.setShortcut('Ctrl+R')

        #  设置状态栏提示
        self.uodoAction.setStatusTip('撤销')
        self.redoAction.setStatusTip('重做')
        self.cutAction.setStatusTip('剪切')
        self.copyAction.setStatusTip('复制')
        self.pasteAction.setStatusTip('粘贴')
        self.deleteAction.setStatusTip('删除')
        self.findAction.setStatusTip('查找')
        self.replaceAction.setStatusTip('替换')

        #  设置工具提示
        self.uodoAction.setToolTip('撤销绘制')
        self.redoAction.setToolTip('重做绘制')
        self.cutAction.setToolTip('剪切')
        self.copyAction.setToolTip('复制')
        self.pasteAction.setToolTip('粘贴')
        self.deleteAction.setToolTip('删除')
        self.findAction.setToolTip('查找')
        self.replaceAction.setToolTip('替换')

        #  添加动作进入编辑菜单
        self.editMenu.addAction(self.uodoAction)
        self.editMenu.addAction(self.redoAction)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.cutAction)
        self.editMenu.addAction(self.copyAction)
        self.editMenu.addAction(self.pasteAction)
        self.editMenu.addAction(self.deleteAction)
        self.editMenu.addSeparator()

        self.findMenu.addAction(self.findAction)
        self.findMenu.addAction(self.replaceAction)

        self.editMenu.addMenu(self.findMenu)

    # 初始化工具菜单列表
    def __initToolsMenu(self):
        self.showNodesMenu = QMenu('显示结点详情', self)
        self.nodeDegreesMenu = QMenu('结点的度', self)
        self.diNodeDegreesMenu = QMenu('有向图的度', self)
        self.parallelEdgesMenu = QMenu('显示平行边', self)
        self.showPathwayMenu = QMenu('显示通路', self)
        self.showLoopMenu = QMenu('显示回路', self)
        self.graphMatrixMenu = QMenu('图的矩阵', self)
        self.specialGraphMenu = QMenu('特殊图', self)
        self.bigraphMenu = QMenu('二部图(偶图)', self)
        self.eulerGraphMenu = QMenu('欧拉图', self)
        self.hamiltonianGraphMenu = QMenu('哈密顿图', self)

        self.showNodeNameAction = QAction('结点名称', self)
        self.showNodeLocationAction = QAction('结点坐标', self)
        self.outputEdgesDataAction = QAction('边详情')
        self.rediNodeDegreesAction = QAction('无向图度', self)
        self.diNodeOutDegreesAction = QAction('出度', self)
        self.diNodeInDegreesAction = QAction('入度', self)
        self.easyGraphAction = QAction('简单图', self)
        self.multipleGraphAction = QAction('多重图', self)
        self.showEasyPathwayAction = QAction('显示简单通路', self)
        self.showComplicatedPathwayAction = QAction('显示复杂通路', self)
        self.showEasyLoopAction = QAction('显示简单回路', self)
        self.showComplicatedLoopAction = QAction('显示复杂回路', self)
        self.outputKeyMatrixAction = QAction('输出关联矩阵', self)
        self.outputAdjacentMatrixAction = QAction('输出邻接矩阵', self)
        self.outputShortestPathAction = QAction('输出最短路径', self)
        self.outputCriticalPathAction = QAction('输出关键路径', self)
        self.graphColorAction = QAction('图的着色', self)
        self.findEulerLoopAction = QAction('寻找欧拉回路', self)
        self.findHamiltonianLoopAction = QAction('寻找哈密顿回路', self)

        self.toolsMenu.addMenu(self.showNodesMenu)

        self.toolsMenu.addAction(self.outputEdgesDataAction)

        self.toolsMenu.addMenu(self.diNodeDegreesMenu)
        self.toolsMenu.addMenu(self.parallelEdgesMenu)
        self.toolsMenu.addMenu(self.showPathwayMenu)
        self.toolsMenu.addMenu(self.showLoopMenu)
        self.toolsMenu.addMenu(self.graphMatrixMenu)

        self.showNodesMenu.addAction(self.showNodeNameAction)
        self.showNodesMenu.addAction(self.showNodeLocationAction)

        self.nodeDegreesMenu.addAction(self.rediNodeDegreesAction)

        self.nodeDegreesMenu.addMenu(self.diNodeDegreesMenu)
        self.diNodeDegreesMenu.addAction(self.diNodeInDegreesAction)
        self.diNodeDegreesMenu.addAction(self.diNodeOutDegreesAction)

        self.parallelEdgesMenu.addAction(self.multipleGraphAction)
        self.parallelEdgesMenu.addAction(self.easyGraphAction)

        self.showPathwayMenu.addAction(self.showEasyPathwayAction)
        self.showPathwayMenu.addAction(self.showComplicatedPathwayAction)

        self.showLoopMenu.addAction(self.showEasyLoopAction)
        self.showLoopMenu.addAction(self.showComplicatedLoopAction)

        self.graphMatrixMenu.addAction(self.outputKeyMatrixAction)
        self.graphMatrixMenu.addAction(self.outputAdjacentMatrixAction)

        self.toolsMenu.addAction(self.outputShortestPathAction)
        self.toolsMenu.addAction(self.outputCriticalPathAction)
        self.toolsMenu.addAction(self.graphColorAction)

        self.toolsMenu.addMenu(self.specialGraphMenu)

        self.specialGraphMenu.addMenu(self.bigraphMenu)
        self.specialGraphMenu.addMenu(self.eulerGraphMenu)
        self.specialGraphMenu.addMenu(self.hamiltonianGraphMenu)

        self.eulerGraphMenu.addAction(self.findEulerLoopAction)
        self.hamiltonianGraphMenu.addAction(self.findHamiltonianLoopAction)

    #  初始化模式菜单
    def __initModeMenu(self):
        self.GraphModeMenu = QMenu('图模式', self)

        self.digraphModeAction = QAction('有向图模式', self, checkable=True)
        self.undigraphModeAction = QAction('无向图模式', self, checkable=True)
        self.treeModeAction = QAction('树模式', self, checkable=True)


        self.digraphModeAction.setStatusTip('有向图模式')
        self.undigraphModeAction.setStatusTip('无向图模式')
        self.treeModeAction.setStatusTip('树模式')

        self.modeMenuGroup=QActionGroup(self)
        self.modeMenuGroup.addAction(self.digraphModeAction)
        self.modeMenuGroup.addAction(self.undigraphModeAction)
        self.modeMenuGroup.addAction(self.treeModeAction)
        self.digraphModeAction.setChecked(True)

        self.digraphModeAction.setShortcut('F1')
        self.undigraphModeAction.setShortcut('F2')
        self.treeModeAction.setShortcut('F3')

        self.GraphModeMenu.addAction(self.digraphModeAction)
        self.GraphModeMenu.addAction(self.undigraphModeAction)

        self.modeMenu.addMenu(self.GraphModeMenu)
        self.modeMenu.addAction(self.treeModeAction)

    #  初始化窗口菜单
    def __initWindowsMenu(self):
        self.maxWindowAction = QAction('最大化', self)
        self.minWindowAction = QAction('最小化', self)
        self.miniWindowAction = QAction('迷你模式', self)

        self.maxWindowAction.setStatusTip('窗口最大化')
        self.minWindowAction.setStatusTip('窗口最小化')
        self.miniWindowAction.setStatusTip('迷你模式')

        self.miniWindowAction.setToolTip('迷你模式只显示画板部分，其余部分将被隐藏')

        self.windowMenu.addAction(self.maxWindowAction)
        self.windowMenu.addAction(self.minWindowAction)
        self.windowMenu.addAction(self.miniWindowAction)

        self.maxWindowAction.triggered.connect(self.setWindowMax)

    #  初始化设置菜单
    def __initSettingMenu(self):
        self.penThicknessAction = QAction('画笔粗细', self)
        self.penColorAction = QAction('画笔颜色', self)
        self.backgroundBoardColorAction = QAction('画板背景色', self)

        self.penThicknessAction.setStatusTip('调整画笔粗细')
        self.penColorAction.setStatusTip('选择画笔颜色')
        self.backgroundBoardColorAction.setStatusTip('选择画板背景色')

        self.settingMenu.addAction(self.penThicknessAction)
        self.settingMenu.addAction(self.penColorAction)
        self.settingMenu.addAction(self.backgroundBoardColorAction)

    #  初始化帮助菜单
    def __initHelpMenu(self):
        self.connectAuthorAction = QAction('联系作者', self)
        self.welcomeUseAction = QAction('欢迎使用', self)
        self.updateSoftwareAction = QAction('检查更新', self)
        self.helpDocAction = QAction('帮助文档', self)

        self.helpDocAction.setShortcut('Ctrl+H')

        self.connectAuthorAction.setStatusTip('联系作者')
        self.welcomeUseAction.setStatusTip('欢迎使用')
        self.updateSoftwareAction.setStatusTip('检查软件版本')
        self.helpDocAction.setStatusTip('使用说明')

        self.helpMenu.addAction(self.connectAuthorAction)
        self.helpMenu.addAction(self.welcomeUseAction)
        self.helpMenu.addAction(self.updateSoftwareAction)
        self.helpMenu.addAction(self.helpDocAction)

    #  右键菜单功能
    def contextMenuEvent(self, event):
        rightMouseMenu = QMenu(self)

        rightMouseMenu.addAction(self.createFileAction)
        rightMouseMenu.addAction(self.openFileAction)
        rightMouseMenu.addAction(self.uodoAction)
        rightMouseMenu.addAction(self.redoAction)
        rightMouseMenu.addAction(self.exitAppAction)




        #  将组件相对坐标转为窗口绝对坐标， exec_显示菜单
        self.action = rightMouseMenu.exec_(self.mapToGlobal(event.pos()))

    #  工具栏菜单
    def __initToolBar(self):
        self.common_toolBar = self.addToolBar('打开')

        self.btn_PenColor = QPushButton()
        self.btn_PenColor.setText('画笔颜色')

        self.btn_PenColor.clicked.connect(QColorDialog.getColor)

        self.common_toolBar.addAction(self.openFileAction)
        self.common_toolBar.addAction(self.createFileAction)
        self.common_toolBar.addAction(self.saveFileAction)
        self.common_toolBar.addWidget(self.btn_PenColor)
        self.common_toolBar.setContentsMargins(5, 5, 5, 5)

    def closeEvent(self, event):

        msgBox = QMessageBox()
        msgBox.setWindowTitle('关闭')
        msgBox.setText("是否保存")
        msgBox.setIcon(QMessageBox.Question)
        btn_Do_notSave = msgBox.addButton('不保存', QMessageBox.AcceptRole)
        btn_cancel = msgBox.addButton('取消', QMessageBox.RejectRole)
        btn_save = msgBox.addButton('保存', QMessageBox.AcceptRole)
        msgBox.setDefaultButton(btn_save)
        msgBox.exec_()

        if msgBox.clickedButton() == btn_Do_notSave:
            event.accept()
        elif msgBox.clickedButton() == btn_cancel:
            event.ignore()
        elif msgBox.clickedButton() == btn_save:
            self.save_file()
            event.accept()

    #  属性栏菜单
    def __initPropertyDock(self):
        self.setDockNestingEnabled(True)
        self.historyDock = QDockWidget("历史记录")
        self.detailPageDock = QDockWidget('详情页')

        self.historyDock.setWidget(self.propertyDock)
        self.detailPageDock.setWidget(self.propertyDock)

        self.historyDock.setFeatures(self.historyDock.DockWidgetFloatable | self.historyDock.DockWidgetMovable)
        self.detailPageDock.setFeatures(self.detailPageDock.DockWidgetFloatable | self.detailPageDock.DockWidgetMovable)
        self.addDockWidget(Qt.RightDockWidgetArea, self.historyDock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.detailPageDock)

    #  状态栏菜单
    def __initStatusBar(self):

        self.statusBar.showMessage('准备就绪')
        self.SoftwareDetailLabel = QLabel("CopyRight @ LiXiaolong 2020")

        self.statusBar.addPermanentWidget(self.SoftwareDetailLabel)

    def setWindowMax(self):
        print(QApplication.desktop())
        self.painterBoard.resize(2560 / 2, 1440 / 2)
        self.showMaximized()

    def resizeEvent(self, event):
        pass

    def setWindowMin(self):
        self.showMinimized()

    def save_file(self):
        savePath, fileType = QFileDialog.getSaveFileName(self, '保存文件', '.\\', '*.graph;;*.json;;*.csv')

        if savePath[0] == "":
            print('Save cancel')
            return

        filename = os.path.basename(savePath)

        if fileType == '*.json':
            pass
            # self.operatorData.save_Json(filename, nodes)
        elif fileType == '*.csv':
            pass
            # self.operatorData.save_Csv(filename, ['point(1)', 'point(2)'], nodes)
        elif fileType == '*.graph':
            self.operatorData.save_Graph(filename, self.painterBoard.GetContentAsGraph())

    def open_file(self):
        dict_file = {}
        openPath, fileType = QFileDialog.getOpenFileName(self, '打开文件', '.\\', '*.graph;;*.json;;*.csv')

        if fileType == '*.json':
            dict_file = self.operatorData.open_Json(openPath)
        elif fileType == '*.csv':
            dict_file = self.operatorData.open_Csv(openPath)
        elif fileType == '*.graph':
            dict_file = self.operatorData.open_Graph(openPath)

        return dict_file


class Wizard(QWizard):

    def __init__(self):
        super(Wizard, self).__init__()

    def initView(self):
        self.addPage(WizardPage())


class WizardPage(QWizardPage):

    def __init__(self):
        super(WizardPage, self).__init__()

    def __initView(self):
        """
        向导页
        """
        self.setTitle("使用指导")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    graph = MainWindow()
    graph.show()
    sys.exit(app.exec_())
