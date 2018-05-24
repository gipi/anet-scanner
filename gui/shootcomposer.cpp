#include "shootcomposer.h"
#include <QPainter>
#include <QDebug>


ShootComposer::ShootComposer(ScannerConfig& config) :
    m_config(config)
{

}

/*
 * Generates a new image compositing the input images
 * using the configuration.
 *
 * TODO: check and raise exception if images are not all equal.
 */
QImage* ShootComposer::compose(QList<QImage> images)
{
    QImage model_image = images.at(0); // take an image as reference for the calculations

    unsigned int single_width = model_image.width() - this->m_config.overlapX();
    unsigned int single_height = model_image.height() - this->m_config.overlapY();

    unsigned int width = ((this->m_config.columns()  - 1) * single_width) + model_image.width();
    unsigned int height = ((this->m_config.rows() - 1)    * single_height) + model_image.height();

    // I don't know why, but the model_image has monochrome format set
    // so I must set ARGB32 explicitely to make all this works
    //qDebug() << model_image.format();
    QImage* composed_image = new QImage(width, height, QImage::Format_ARGB32);

    QPainter painter(composed_image);
    composed_image->fill(Qt::white);

    unsigned int index = 0;

    foreach(QImage image, images) {
        unsigned int x = (index % this->m_config.columns()) * single_width;
        unsigned int y = (index / this->m_config.rows()) * single_height;

        painter.drawImage(x, y, image);

        index++;
    }
    painter.end();

    return composed_image;
}
