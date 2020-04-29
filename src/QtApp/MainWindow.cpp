#include "MainWindow.h"
#include "ui_MainWindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}



void MainWindow::on_actionArc_triggered()
{

}

void MainWindow::on_actionStraight_Line_triggered()
{

}



void MainWindow::on_actionClues_Color_triggered()
{

}

void MainWindow::on_actionClues_Thickness_triggered()
{

}

void MainWindow::on_actionBackground_Color_triggered()
{

}
