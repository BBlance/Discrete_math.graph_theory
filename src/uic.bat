
copy .\QtApp\MainWindow.ui  MainWindow.ui
copy .\QtApp\ThicknessDialog.ui  ThicknessDialog.ui
call pyuic5 -o ui_MainWindow.py  MainWindow.ui
call pyuic5 -o ui_ThicknessDialog.py  ThicknessDialog.ui

call pyrcc5 .\QtApp\res.qrc -o res_rc.py






