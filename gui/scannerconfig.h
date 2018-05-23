#ifndef SCANNERCONFIG_H
#define SCANNERCONFIG_H
/*
 * It represents the configuration of the scanner.
 *
 * This comprehends
 *
 *  - number of columns/rows
 *  - overlap between shoots
 *  - distance between shoots
 *
 * It can be configured via GUI and its state it's stored
 * via a JSON file.
 *
 * TODO: make possible saving more session of scanning.
 */

#include <QString>


class ScannerConfig
{
public:
    ScannerConfig(const QString&);
private:
    unsigned int m_cols;
    unsigned int m_rows;
    unsigned int m_step_distance; /* mm */
    unsigned int m_shoots_overlap_x; /* pixels */
    unsigned int m_shoots_overlap_y; /* pixels */
};

#endif // SCANNERCONFIG_H
