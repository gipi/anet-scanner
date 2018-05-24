#ifndef SHOOTCOMPOSER_H
#define SHOOTCOMPOSER_H
/*
 * This class composes the shoots together and generates
 * a unique Image wrt the configurations.
 */
#include <QImage>
#include "scannerconfig.h"


class ShootComposer
{
public:
    ShootComposer(ScannerConfig&);
    QImage* compose(QList<QImage> images);

private:
    ScannerConfig& m_config;
};

#endif // SHOOTCOMPOSER_H
