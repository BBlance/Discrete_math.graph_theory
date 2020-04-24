
copy .\QtApp\MainWindow.ui  MainWindow.ui
call pyuic5 -o ui_MainWindow.py  MainWindow.ui

call pyrcc5 .\QtApp\res.qrc -o res_rc.py




