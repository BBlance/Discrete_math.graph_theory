
copy .\QtApp\MainWindow.ui  MainWindow.ui
copy .\QtApp\ThicknessDialog.ui  ThicknessDialog.ui
copy .\QtApp\ShowMatrix.ui  ShowMatrix.ui
copy .\QtApp\DataDetails.ui  DataDetails.ui

pyside2-uic -o ui_MainWindow.py  MainWindow.ui
pyside2-uic -o ui_ThicknessDialog.py  ThicknessDialog.ui
pyside2-uic -o ui_ShowMatrix.py  ShowMatrix.ui
pyside2-uic -o ui_DataDetails.py  DataDetails.ui

pyside2-rcc .\QtApp\res.qrc -o res_rc.py

del ThicknessDialog.ui ShowMatrix.ui DataDetails.ui







