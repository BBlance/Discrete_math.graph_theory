#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:


    void on_actionArc_triggered();

    void on_actionStraight_Line_triggered();

    void on_actionPoint_triggered();

    void on_actionEllipse_triggered();

    void on_actionRectangle_triggered();

    void on_actionCircle_triggered();

    void on_actionUodo_triggered();

    void on_actionRedo_triggered();

    void on_actionUndo_triggered();

    void on_actionPen_Color_triggered();

    void on_actionPen_Thickness_triggered();

    void on_actionBackground_Color_triggered();

    void on_actionClues_Color_triggered();

    void on_actionClues_Thickness_triggered();

    void on_actionProperty_And_History_triggered(bool checked);

    void on_actionSave_Image_triggered();

    void on_actionDelete_triggered();

    void on_actionAdd_Annotation_triggered();

    void on_actionRedigraph_s_Degrees_triggered();

    void on_actionDigraph_Mode_triggered();

    void on_actionDigraph_Mode_triggered(bool checked);

    void on_actionRedigraph_Mode_triggered(bool checked);

    void on_actionOut_degree_triggered();

    void on_actionIn_degree_triggered();

private:
    Ui::MainWindow *ui;
};
#endif // MAINWINDOW_H
