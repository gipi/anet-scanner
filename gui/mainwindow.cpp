#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "printercontroller.h"


Q_DECLARE_METATYPE(QCameraInfo) // like magic


// https://stackoverflow.com/questions/23083352/stream-webcam-video-no-audio-to-a-widget-in-qt5
MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow) {

    ui->setupUi(this);

    qDebug() << " [I] looking for cameras";

    QList<QCameraInfo> cameras = QCameraInfo::availableCameras();

    unsigned int cameras_n = cameras.count();

    qDebug() << " [I] found " << cameras_n << " camera(s)";

    if (cameras_n < 1)
        return;

    QCamera* camera;

    QActionGroup *videoDevicesGroup = new QActionGroup(this);
    videoDevicesGroup->setExclusive(true);

    foreach (const QCameraInfo &cameraInfo, cameras) {
        qDebug() << " [I] " <<
                    cameraInfo.deviceName() << " " << cameraInfo.description();
        QAction *videoDeviceAction =
                new QAction(cameraInfo.description(), videoDevicesGroup);
        videoDeviceAction->setCheckable(true);
        videoDeviceAction->setData(QVariant::fromValue(cameraInfo));

        camera = new QCamera(cameraInfo); // FIXME

        ui->menuBar->addAction(videoDeviceAction);
    }

    //connect(camera, &QCameraImageCapture::imageCaptured, this, &Camera::processCapturedImage);

    //camera->setViewfinder(ui->monitor);
    CalibrationEncoder* ce = new CalibrationEncoder();
    camera->setViewfinder(ce);
    /*
     * Here we use a VideoProbe instance to manipulate
     * the frame before visualization
     *
     * See <https://doc.qt.io/qt-5/videooverview.html>
     */
    /*QVideoProbe* videoProbe = new QVideoProbe(this);
    if (videoProbe->setSource(camera)) {
        connect(videoProbe, &QVideoProbe::videoFrameProbed,
                this, &MainWindow::align);
    }*/
    connect(ce, &CalibrationEncoder::videoFrameProcessed,
            ui->monitor, &CalibrationWidget::updateFrame);
    camera->start();

    this->m_thread = new PrinterController;
    this->m_thread->start();
}

MainWindow::~MainWindow() {
    delete ui;
}

