import sys
import re
import string

FILE_PATH = "/home/matej/Dropbox/matej/workarea/nw.work"


class NoDayInit(Exception):
    pass


def findint(inputstr, start=0):
    if not inputstr[start].isdigit():
        raise NoDayInit()
    stop = start
    while inputstr[stop].isdigit():
        stop += 1
    return start, stop


def clocktohrs(inputstr):
    a = inputstr.split(':')
    if len(a) == 2:
        h = float(a[0])
        m = float(a[1])
        return h + m / 60.0
    else:
        return float(a[0])


def gethours(inputstr):
    chunks = inputstr.split('+')
    hours = 0.0
    for chunk in chunks:
        nums = chunk.split('..')
        if len(nums) == 2:
            begin = clocktohrs(nums[0])
            end = clocktohrs(nums[1])
            if begin <= end:
                hours += end - begin
            else:
                hours += 24 - begin + end
        else:
            hours += clocktohrs(nums[0])
    return hours


def dayandhours(line):
    day_end = line.find('=')
    try:
        day = int(line[0:day_end])
    except ValueError:
        raise NoDayInit()
    else:
        return day, gethours(line[day_end + 1:])


def rm_whitespace(line):
    return re.sub(r"\s", "", line)


def print_end(month, days, hours):
    overall = False if month else True

    print "{0} total days: {1}, total hours: {2}\n".format(
        "overall\n\t" if overall else "}} month: {0},".format(month),
        days,
        hours
    )


def parse_file(filepath, arg_month, arg_day):
    """
        TODO:
        - work.py <filename> [month] [day]
    """
    i_month = None
    i_months = 0
    i_days = 0
    i_hours = 0.0
    daysinmonth = 0
    hoursinmonth = 0.0
    in_month = False
    arg_day = int(arg_day) if arg_day else 0
    dayfound = False

    with open(filepath) as workfile:
        for line in workfile:

            try:
                is_month = re.search("^\s*\[.+\]\s*$", line)
                is_day = re.search("^\s*\d*\s*=\s*.+$", line)

                if dayfound:
                    if is_month or is_day:
                        break
                    else:
                        print string.rstrip(line)
                        continue

                # search for month
                if is_month:
                    line = rm_whitespace(line)
                    if not i_months == 0:
                        if in_month and not arg_day:
                            print_end(i_month, daysinmonth, hoursinmonth)
                        daysinmonth = 0
                        hoursinmonth = 0.0
                        i_month = line[1:-1]
                        in_month = not arg_month or i_month == arg_month
                        if in_month and not arg_day:
                            print "{0} {{".format(i_month)
                    else:
                        i_month = line[1:-1]
                        in_month = not arg_month or i_month == arg_month
                        if in_month and not arg_day:
                            print "{0} {{".format(i_month)

                    i_months += 1
                    continue

                # search for day init string
                if in_month and is_day:
                    line = rm_whitespace(line)
                    day, hours = dayandhours(line)
                    if day == arg_day:
                        dayfound = True
                        continue
                    i_days += 1
                    daysinmonth += 1
                    i_hours += hours
                    hoursinmonth += hours
                    if not arg_day:
                        print "\tday {0}, {1}hrs".format(day, hours)
                    continue

            except NoDayInit:
                continue

    if in_month and not arg_day:
        print_end(i_month, daysinmonth, hoursinmonth)

    if not arg_month:
        print_end(arg_month, i_days, i_hours)


arg_month = None
arg_day = None
if len(sys.argv) > 1:
    arg_month = sys.argv[1]
    if len(sys.argv) > 2:
        arg_day = sys.argv[2]

parse_file(FILE_PATH, arg_month, arg_day)
