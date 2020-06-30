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

void MainWindow::on_actionAdjacent_Matrix_Digraph_triggered()
{

}

void MainWindow::on_actionReachable_Matrix_triggered()
{

}

void MainWindow::on_actionIncidence_Matrix_Undigraph_triggered()
{

}

void MainWindow::on_actionNew_triggered()
{

}

void MainWindow::on_actionEdge_s_Weight_triggered()
{

}

void MainWindow::on_actionEasy_Pathway_triggered()
{

}

void MainWindow::on_tabWidget_currentChanged(int index)
{

}

void MainWindow::on_tabWidget_tabCloseRequested(int index)
{

}

void MainWindow::on_actionDigraph_Mode_toggled(bool arg1)
{

}

void MainWindow::on_action_EdgeNum_triggered()
{

}

void MainWindow::on_actionWeight_triggered()
{

}

void MainWindow::on_actionEasy_Loop_triggered()
{

}

void MainWindow::on_actionPrimary_Pathway_triggered()
{

}

void MainWindow::on_actionPrimary_Loop_triggered()
{

}

void MainWindow::on_actionShowNodesWeight_toggled(bool arg1)
{

}

void MainWindow::on_actionConnectivity_triggered()
{

}

void MainWindow::on_actionCompleteGraph_triggered()
{

}

void MainWindow::on_actionMultipleOrSimple_triggered()
{

}

void MainWindow::on_actionShortest_Path_triggered()
{

}

void MainWindow::on_actionSave_triggered()
{

}

void MainWindow::on_actionOpen_triggered()
{

}

void MainWindow::on_actionHideControlPoint_triggered()
{

}

void MainWindow::on_actionHideControlPoint_toggled(bool arg1)
{

}

void MainWindow::on_actionHelp_Document_triggered()
{

}

void MainWindow::on_actionOutputData_triggered()
{

}

void MainWindow::on_actionImportData_triggered()
{

}

void MainWindow::on_actionSave_As_triggered()
{

}
