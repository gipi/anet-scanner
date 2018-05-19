#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow) {

    ui->setupUi(this);

    qDebug() << "looking for cameras";

    QList<QCameraInfo> cameras = QCameraInfo::availableCameras();

    qDebug() << " [I] found " << cameras.count();

    foreach (const QCameraInfo &cameraInfo, cameras) {
        qDebug() << " [I] " << cameraInfo.deviceName() << " " << cameraInfo.description();
        if (cameraInfo.deviceName() == "mycamera")
            QCamera* camera = new QCamera(cameraInfo);
    }
}

MainWindow::~MainWindow() {
    delete ui;
}
