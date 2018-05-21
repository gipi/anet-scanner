#include "calibrationencoder.h"

CalibrationEncoder::CalibrationEncoder()
{

}

QList<QVideoFrame::PixelFormat> CalibrationEncoder::supportedPixelFormats(
           QAbstractVideoBuffer::HandleType handleType = QAbstractVideoBuffer::NoHandle) const
{
       Q_UNUSED(handleType);

       // Return the formats you will support
       return QList<QVideoFrame::PixelFormat>() << QVideoFrame::Format_RGB565;
}

bool CalibrationEncoder::present(const QVideoFrame &frame) {
    qDebug() << " [I] present(): " << frame;

    emit videoFrameProcessed(frame);

    return true;
}
