from PySide2.QtCore import QModelIndex, QAbstractItemModel, Qt
from PySide2.QtWidgets import QStyledItemDelegate, QWidget, QStyleOptionViewItem, QDoubleSpinBox


class WeightSpinDelegate(QStyledItemDelegate):
    def __init__(self, minV=0, maxV=1000, digi=2, parent=None):
        super().__init__(parent)
        self.__min = minV
        self.__max = maxV
        self.__decimals = digi

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        editor = QDoubleSpinBox(parent)
        editor.setFrame(False)
        editor.setRange(self.__min, self.__max)
        editor.setDecimals(self.__decimals)
        return editor

    def setEditorData(self, editor: QWidget, index: QModelIndex):
        model = index.model()
        text = model.data(index, Qt.EditRole)
        editor.setValue(float(text))

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex):
        value = editor.value()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        editor.setGeometry(option.rect)
