
copy .\QtApp\MainWindow.ui  MainWindow.ui
copy .\QtApp\ThicknessDialog.ui  ThicknessDialog.ui
copy .\QtApp\CreateFileDialog.ui  CreateFileDialog.ui
call pyside2-uic -o ui_MainWindow.py  MainWindow.ui
call pyside2-uic -o ui_ThicknessDialog.py  ThicknessDialog.ui
call pyside2-uic -o ui_CreateFileDialog.py  CreateFileDialog.ui

call pyside2-rcc .\QtApp\res.qrc -o res_rc.py

del MainWindow.ui ThicknessDialog.ui CreateFileDialog.ui






