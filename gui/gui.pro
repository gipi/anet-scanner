#-------------------------------------------------
#
# Project created by QtCreator 2018-05-19T17:45:51
#
#-------------------------------------------------

QT       += core gui multimedia multimediawidgets

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = gui
TEMPLATE = app
DESTDIR = build

# The following define makes your compiler emit warnings if you use
# any feature of Qt which has been marked as deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS

# You can also make your code fail to compile if you use deprecated APIs.
# In order to do so, uncomment the following line.
# You can also select to disable deprecated APIs only up to a certain version of Qt.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0


SOURCES += \
        mainwindow.cpp \
    calibrationwidget.cpp \
    calibrationencoder.cpp \
    scannerconfig.cpp \
    shootcomposer.cpp \
    printercontroller.cpp


HEADERS += \
        mainwindow.h \
    calibrationwidget.h \
    calibrationencoder.h \
    scannerconfig.h \
    shootcomposer.h \
    printercontroller.h

FORMS += \
        mainwindow.ui


# Here we are creating two different configuration build
# for the project
#
# Use the following to generate the test app and run it
#
#   $ qmake /path/to/project "CONFIG+=test"
#   $ make check
#
# For more info look at the following links
# - https://stackoverflow.com/questions/12154980/how-to-structure-project-while-unit-testing-qt-app-by-qtestlib
# - http://xilexio.org/?p=125

test{
    message(Configuring test build...)

    TEMPLATE = app
    TARGET = tests

    CONFIG += testcase
    QT += testlib

    HEADERS += \
        tests/shootcomposertest.h \
        tests/scannerconfigtest.h

    SOURCES += \
        tests/test_main.cpp \
        tests/shootcomposertest.cpp \
        tests/scannerconfigtest.cpp

# https://larry-price.com/blog/2013/11/14/copy-data-using-qmake/
    FIXTURES += \
        tests/fixtures/
    QMAKE_POST_LINK += $$quote(cp -rf $${PWD}/$${FIXTURES} $$DESTDIR)
    QMAKE_CLEAN += -r $$FIXTURES


}else{
    message(Configuring normal build...)

    SOURCES += \
        main.cpp
}
