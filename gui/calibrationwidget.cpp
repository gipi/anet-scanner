#include "calibrationwidget.h"

CalibrationWidget::CalibrationWidget(QWidget *parent) : QWidget(parent)
{

}

void CalibrationWidget::updateFrame(const QVideoFrame &frame) {
    qDebug() << " [I] updateFrame() " << frame;
}
