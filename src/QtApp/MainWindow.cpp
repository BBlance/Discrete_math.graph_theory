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

void MainWindow::on_actionProperty_And_History_triggered(bool checked)
{

}

void MainWindow::on_actionSave_Image_triggered()
{

}

void MainWindow::on_actionUndo_triggered()
{

}

void MainWindow::on_actionDelete_triggered()
{

}

void MainWindow::on_actionAdd_Annotation_triggered()
{

}

void MainWindow::on_actionRedigraph_s_Degrees_triggered()
{

}

void MainWindow::on_actionDigraph_Mode_triggered(bool checked)
{

}

void MainWindow::on_actionRedigraph_Mode_triggered(bool checked)
{

}

void MainWindow::on_actionOut_degree_triggered()
{

}

void MainWindow::on_actionIn_degree_triggered()
{

}
