#include <QDebug>
#include <QDir>
#include <QStringList>
#include <QColor>

#include "shootcomposertest.h"
#include "shootcomposer.h"
#include "scannerconfig.h"


void ShootComposerTest::initTestCase()
{
    // loads all the pngs (100x100)
    QDir fixtures_dir("fixtures");
    QStringList filters;
    filters << "*.png";
    fixtures_dir.setNameFilters(filters);

    QStringList pngs = fixtures_dir.entryList();

    qDebug() << pngs;

    foreach (const QString file, pngs) {
        QImage png(fixtures_dir.filePath(file));
        this->m_images->append(png);
    }
}

void ShootComposerTest::test_compose()
{
    ScannerConfig config(2, 2, 10, 5);
    ShootComposer composer(config);
    QImage* result = composer.compose(*this->m_images);

    /*
     * we have 4 images placed in a grid 2x2
     */
    QVERIFY(result->width() == ((100 - 10) + 100));
    QVERIFY(result->height() == ((100 - 5) + 100));

    //result->save("/tmp/compose.png");

    QRgb blue = qRgb(0, 0, 0xff);
    QRgb red  = qRgb(0xff, 0, 0);

    QCOMPARE(result->pixel(0, 0), blue);
    QCOMPARE(result->pixel((100 - 10), (100 - 5)), red);

}
