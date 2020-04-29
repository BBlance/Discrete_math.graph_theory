#ifndef THICKNESSDIALOG_H
#define THICKNESSDIALOG_H

#include <QDialog>

namespace Ui {
class ThicknessDialog;
}

class ThicknessDialog : public QDialog
{
    Q_OBJECT

public:
    explicit ThicknessDialog(QWidget *parent = nullptr);
    ~ThicknessDialog();

private slots:
    void on_btnCancel_clicked();

    void on_btnOk_clicked();

private:
    Ui::ThicknessDialog *ui;
};

#endif // THICKNESSDIALOG_H
