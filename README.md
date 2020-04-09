# workhour-report-generator

Create workhour reports.

## Installation

### Pre Install
Fedora:
`dnf install wkhtmltopdf`
Ubuntu/Debian:
`apt-get install wkhtmltopdf`

### Clone Repository
with SSH:
`git clone git@github.com:tosterkamp/workhour-report-generator.git`
with HTTPS:
`git clone https://github.com/tosterkamp/workhour-report-generator.git`

### Install
create virtual environment:
`python3 -m venv ./venv`

source venv file:
`source venv/bin/activate`

install python requirements:
`pip install -r requirements.txt`


## Usage

usage: workhour-report-generator.py [-h] [--first FIRST] [--last LAST] [--institution INSTITUTION] [--signature SIGNATURE] FIRSTNAME LASTNAME HOURS YEAR MONTH

#### non optional arguments:
* FIRSTNAME ---> your first name
* LASTNAME ---> your last name
* HOURS ---> number of working hours
* YEAR ---> which Year
* MONTH ---> which month

#### optional arguments:
* -h, --help ---> show this help message and exit
* --first FIRST ---> earliest working day of the month
* --last LAST ---> latest working day of the month
* --institution INSTITUTION ---> the institute where you work
* --signature SIGNATURE ---> path and filename of signature picture


Example 1: `<python3 workhour-report-generator.py John Doe 45 2017 1>`

Example 2: `<python3 workhour-report-generator.py --institution 'MyInstitution' --signature mysignature.svg John Doe 20 2017 1>`

Example 3: `<python3 workhour-report-generator.py --first 5 --last 25 John Doe 45 2017 1>`
