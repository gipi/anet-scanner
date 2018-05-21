#ifndef CALIBRATIONWIDGET_H
#define CALIBRATIONWIDGET_H

#include <QDebug>
#include <QWidget>
#include <QVideoFrame>


class CalibrationWidget : public QWidget
{
    Q_OBJECT
public:
    explicit CalibrationWidget(QWidget *parent = nullptr);

signals:

public slots:
    void updateFrame(const QVideoFrame&);
};

#endif // CALIBRATIONWIDGET_H
