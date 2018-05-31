#ifndef PRINTERCONTROLLER_H
#define PRINTERCONTROLLER_H
/*
 * This class interfaces to the printer to execute various actions:
 * moving, homing, etc...
 *
 *
 */
#include <QThread>


class PrinterController : public QThread
{
public:
    void run();
};

#endif // PRINTERCONTROLLER_H
