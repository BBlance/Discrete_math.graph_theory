#include "CreateFileDialog.h"
#include "ui_CreateFileDialog.h"

CreateFileDialog::CreateFileDialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::CreateFileDialog)
{
    ui->setupUi(this);
}

CreateFileDialog::~CreateFileDialog()
{
    delete ui;
}
