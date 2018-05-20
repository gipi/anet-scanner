#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QtDebug>
#include <QCamera>
#include <QCameraInfo>
#include <QActionGroup>
#include <QAction>
#include <QVideoProbe>


namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

public slots:
    void align(const QVideoFrame& frame);

private:
    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
