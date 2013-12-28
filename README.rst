=============
WorkLogParser
=============

Work Log Parser, can parse log file with specific syntax, and outputs JSON
directly or you can use jinja template to export to whatever format you like.
There are three default HTML templates to choose from (long_report.jinja,
short_report.jinja and weekly_report.jinja) but you can write your own.

Remember:
    one log file has to have max 12 non-repeatable sections/months and
    is used per one year.


Simple example of log file::

    [october]
    1 = 10..17:30 [tag1, tag2]
        working on ticket #239
        ticket #228: fixed minor errors
    2 = 13..17 [tag3]
        working on #239
            same error found for "Normal" quality option


Explanation of sample:

    **[october]**

        month section

    **1 = 10..17:30**

        **1**
            day number in the month
        **10..17:30**
            hours from 10 to 17:30


Samples of hours (after the equals sign):

    **10..17:30**
        from 10 to 17:30

    **8**
        just a number, number of hours

    **0.5+3.5+15..17:30**
        translates to 6.5h


Tags (after hours):

    **... [ill, at_home]**
        Those tags will be parsed and grouped
        to be used with *--template* option


Command line options:

    **worklogparser** [-h] [-m MONTH] [-e END_MONTH] [-d DAY] [-c DAY_COUNT]
                     [-j] [-jm] [-t TEMPLATE] [-g GROUP_TODOS]
                     FILEPATH

    **-h, --help**            show this help message and exit
    **-m MONTH, --month MONTH**:
        Retrieve content by (start) month (ex: november)
    **-e END_MONTH, --end-month END_MONTH**:
        Retrieve content from MONTH to END_MONTH month (ex: december)
    **-d DAY, --day DAY**:
         Retrieve content by (start) day in month (ex: 2)
    **-c DAY_COUNT, --day-count DAY_COUNT**:
        Retrieve content by day range from DAY inclusive to
        DAY+DAY_COUNT exclusive in month
    **-j, --json**:
        Export to stdout as JSON format
    **-jm, --json-min**:
        Export to stdout as JSON format (minified)
    **-t TEMPLATE, --template TEMPLATE**:
        Export to stdout by this Jinja2 template file
    **-g, --group-todos**
        Group all "TODO:*" lines to be accessed in template file


Command example - weekly report::

    worklogparser ./work-2013.txt --month december \
        --day 16 --day-count 7 --template weekly_report.jinja

    Explanation:
        *./work-2013.txt* is a log file
        *--month december* where to start the month parsing
        *--day 16* which day to start parsing in month
        *--day-count 7* 7 days is one week
        *--template weekly_report.jinja* included weekly HTML template output


Command example - JSON::

    worklogparser ./work-2013.txt --month december \
        --day 16 --day-count 7 --json

    Explanation:
        *--json* raw output of JSON without any template
