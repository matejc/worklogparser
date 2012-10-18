=============
WorkLogParser
=============

Sample::

    [october]
    1 = 10..17:30
        working on ticket #239
        ticket #228: fixed minor errors
        went for a drink
    2 = 13..17
        working on #239
        same error found for "Normal" quality option


Explanation of sample:

    **[october]**:

        month tag

    **1 = 10..17:30**:

        **1**:
            day number in the month
        **10..17:30**:
            hours from 10 to 17:30


Samples of hours (after the equals sign):

    **10..17:30**:
        from 10 to 17:30

    **8**:
        just a number, number of hours

    **0.5+3.5+15..17:30**:
        translates to 6.5h


Command example::

    python work.py october


Command Output::

    october {
        day 1, 7.5hrs
        day 2, 4.0hrs
    } month: october, total days: 2, total hours: 11.5


Known Issues::

    Work log file is hardcoded, will fix eventually
