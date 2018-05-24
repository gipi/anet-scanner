#ifndef SHOOTCOMPOSERTEST_H
#define SHOOTCOMPOSERTEST_H

#include <QObject>
#include <QImage>
#include <QtTest/QtTest>


class ShootComposerTest : public QObject
{
    Q_OBJECT
private slots:
    void initTestCase();
    void test_compose();
private:
    QList<QImage>* m_images = new QList<QImage>();
};

#endif // SHOOTCOMPOSERTEST_H
