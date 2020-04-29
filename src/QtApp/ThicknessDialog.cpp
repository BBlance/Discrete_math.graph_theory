#include "ThicknessDialog.h"
#include "ui_ThicknessDialog.h"

ThicknessDialog::ThicknessDialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::ThicknessDialog)
{
    ui->setupUi(this);
}

ThicknessDialog::~ThicknessDialog()
{
    delete ui;
}

void ThicknessDialog::on_btnCancel_clicked()
{

}

void ThicknessDialog::on_btnOk_clicked()
{

}

void ThicknessDialog::on_penStyleComboBox_currentIndexChanged(int index)
{

}
