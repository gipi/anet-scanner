#include "scannerconfigtest.h"
#include "scannerconfig.h"


/*
 * Generate data necessary for the following tests
 */
void ScannerConfigTest::initTestCase()
{
    this->m_temp_dir = new QTemporaryDir();
    qDebug() << "generated temporary directory " << m_temp_dir->path();
    qDebug() << __FILE__;
}

void ScannerConfigTest::cleanupTestCase()
{
    this->m_temp_dir->remove();
}

void ScannerConfigTest::testWithoutFile()
{
    ScannerConfig config();
}

void ScannerConfigTest::testReadFile()
{
    QFile config_file(this->m_temp_dir->filePath("config.json"));
    QVERIFY(config_file.open(QIODevice::ReadWrite | QIODevice::Text));
    config_file.close();

    ScannerConfig config(config_file.fileName());

}

