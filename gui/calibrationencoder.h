#ifndef CALIBRATIONMONITOR_H
#define CALIBRATIONMONITOR_H
/*
 * This class receives and manipulates frames
 * in order to place a calibration mask over them.
 */
#include <QDebug>
#include <QVideoFrame>
#include <QAbstractVideoSurface>


class CalibrationEncoder : public QAbstractVideoSurface
{
   Q_OBJECT
public:
    CalibrationEncoder();
    bool present(const QVideoFrame &frame);
    QList<QVideoFrame::PixelFormat> supportedPixelFormats(
               QAbstractVideoBuffer::HandleType handleType) const;
signals:
    void videoFrameProcessed(const QVideoFrame& frame);
};

#endif // CALIBRATIONMONITOR_H
