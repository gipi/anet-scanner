#include "printercontroller.h"
#include <time.h>
#include <QDebug>


void PrinterController::run() {
    while (true) {
        qDebug() << ".";
        sleep(1);
    }
}
