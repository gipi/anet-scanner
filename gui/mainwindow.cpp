#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow) {

    ui->setupUi(this);

    qDebug() << " [I] looking for cameras";

    QList<QCameraInfo> cameras = QCameraInfo::availableCameras();

    qDebug() << " [I] found " << cameras.count();

    QCamera* camera;

    foreach (const QCameraInfo &cameraInfo, cameras) {
        qDebug() << " [I] " << cameraInfo.deviceName() << " " << cameraInfo.description();
            camera = new QCamera(cameraInfo);
    }

    camera->setViewfinder(ui->monitor);
    camera->start();
}

MainWindow::~MainWindow() {
    delete ui;
}
