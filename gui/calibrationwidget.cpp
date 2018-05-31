#include "calibrationwidget.h"
#include <QPainter>


CalibrationWidget::CalibrationWidget(QWidget *parent) : QWidget(parent)
{

}

void CalibrationWidget::updateFrame(const QVideoFrame &frame) {
    if (this->m_image != NULL) {
        delete this->m_image;
    }

    QVideoFrame f(frame);

    // in order to access internal data of the videoframe we need to map it
    if (!f.map(QAbstractVideoBuffer::ReadOnly)){
        qDebug() << " [E] I could not map the frane";
        return;
    }
    // used this answer to convert from frame to image
    //  https://stackoverflow.com/questions/27829830/convert-qvideoframe-to-qimage
    QImage::Format imageFormat = QVideoFrame::imageFormatFromPixelFormat(frame.pixelFormat());

    this->m_image = new QImage(f.bits(),
                               frame.width(),
                               frame.height(),
                               frame.bytesPerLine(),
                               imageFormat);
    f.unmap();

    this->update();
}

void CalibrationWidget::paintEvent(QPaintEvent *event)
{
    if (this->m_image == NULL) {
        return;
    }

    QPainter painter(this);

    painter.fillRect(rect(), Qt::black);
    painter.drawImage(0, 0, *this->m_image);
}
