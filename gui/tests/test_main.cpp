#include "scannerconfigtest.h"
#include "shootcomposertest.h"

/*
 * Main accesso point for the unit tests of the project.
 *
 *  https://www.slideshare.net/ICSinc/qt-test-framework
 */
int main(int argc, char *argv[])
{
    ShootComposerTest st;
    ScannerConfigTest sct;

    QTest::qExec(&st);
    QTest::qExec(&sct);
}
