# workhour-report-generator
usage: workhour-report-generator.py [-h] [--first FIRST] [--last LAST]
                                    [--institution INSTITUTION]
                                    [--signature SIGNATURE]
                                    FIRSTNAME LASTNAME HOURS YEAR MONTH

Example 1: python3 workhour-report-generator.py John Doe 45 2017 1

Example 2: python3 workhour-report-generator.py --institution 'MyInstitution' --signature mysignatue.svg John Doe 20 2017 1

Example 3: python3 workhour-report-generator.py --first 5 --last 25 John Doe 45 2017 1
