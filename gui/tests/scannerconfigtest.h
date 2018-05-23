#ifndef SCANNERCONFIGTEST_H
#define SCANNERCONFIGTEST_H

#include <QObject>
#include <QtTest/QtTest>
#include <QTemporaryDir>


class ScannerConfigTest : public QObject
{
    Q_OBJECT
private slots:
    void initTestCase();

    void testWithoutFile();
    void testReadFile();

    void cleanupTestCase();
private:
    QTemporaryDir* m_temp_dir;
};

#endif // SCANNERCONFIGTEST_H
