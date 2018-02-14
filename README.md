# workhour-report-generator

usage: workhour-report-generator.py [-h] [--first FIRST] [--last LAST]
                                    [--institution INSTITUTION]
                                    [--signature SIGNATURE]
                                    FIRSTNAME LASTNAME HOURS YEAR MONTH

Create workhour reports.

positional arguments:
  FIRSTNAME             your first name
  LASTNAME              your last name
  HOURS                 number of working hours
  YEAR                  which Year
  MONTH                 which month

optional arguments:
  -h, --help            show this help message and exit
  --first FIRST         earliest working day of the month
  --last LAST           latest working day of the month
  --institution INSTITUTION
                        the institute where you work
  --signature SIGNATURE
                        path and filename of signature picture

Example 1: python3 workhour-report-generator.py John Doe 45 2017 1

Example 2: python3 workhour-report-generator.py --institution 'MyInstitution' --signature mysignatue.svg John Doe 20 2017 1

Example 3: python3 workhour-report-generator.py --first 5 --last 25 John Doe 45 2017 1
