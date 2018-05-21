#include "mainwindow.h"
#include "ui_mainwindow.h"

Q_DECLARE_METATYPE(QCameraInfo) // like magic

// https://stackoverflow.com/questions/23083352/stream-webcam-video-no-audio-to-a-widget-in-qt5
MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow) {

    ui->setupUi(this);

    qDebug() << " [I] looking for cameras";

    QList<QCameraInfo> cameras = QCameraInfo::availableCameras();

    qDebug() << " [I] found " << cameras.count() << " camera(s)";

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
}

MainWindow::~MainWindow() {
    delete ui;
}

void MainWindow::align(const QVideoFrame &orig_frame) {
    qDebug() << orig_frame;
    QVideoFrame* frame = new QVideoFrame(orig_frame);

    if (true) {
        qDebug() << "is true!!!!";
    }

    if (!frame->map(QAbstractVideoBuffer::ReadWrite)) {
        qDebug() << " [E] failed to map";
       return;
    }

    // now we can act on the bytes
    uchar* buffer = frame->bits();

    if (!frame->isWritable()) {
        qDebug() << "no wrutabe";
    }

    for (unsigned int cycle = 0 ; cycle < 1000 ; cycle++) {
        buffer[cycle] = 0xff;
    }

    frame->unmap();
}
