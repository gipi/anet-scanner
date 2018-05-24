#include "scannerconfig.h"

/*
 * Constructor that reads the content of the path passed as argument
 * and populate the object.
 */
ScannerConfig::ScannerConfig(const QString& path)
{

}

ScannerConfig::ScannerConfig(unsigned int columns, unsigned int rows, unsigned int overlap_x, unsigned int overlap_y):
    m_cols(columns), m_rows(rows), m_shoots_overlap_x(overlap_x), m_shoots_overlap_y(overlap_y)
{

}

unsigned int ScannerConfig::columns()
{
    return m_cols;
}

unsigned int ScannerConfig::rows()
{
    return m_rows;
}

unsigned int ScannerConfig::overlapX()
{
    return m_shoots_overlap_x;
}

unsigned int ScannerConfig::overlapY()
{
    return m_shoots_overlap_y;
}
