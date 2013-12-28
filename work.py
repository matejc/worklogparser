#!/usr/bin/env python

import argparse
import calendar
import json
import re
import traceback


def month_to_num(month_name):
    for i in range(1, 13):
        if month_name.lower() == calendar.month_name[i].lower():
            return i
    return None


def days_in_month(year, month):
    if type(month) == str:
        month_num = month_to_num(month)
    return calendar.monthrange(year, month_num)[1]


def days_range(year, year_stop, month, day, day_count):
    if type(month) == str:
        month = month_to_num(month)
    days = []
    days_used = 0
    first_month = True
    while True:
        if first_month:
            day_max = min(
                day + day_count - 1,
                calendar.monthrange(year, month)[1]
            )
        else:
            day_max = min(
                day_count - days_used,
                calendar.monthrange(year, month)[1]
            )
        day_range = range(day, day_max + 1)
        days += [{
            'year': year,
            'month': month,
            'days': day_range
        }]
        days_used += len(day_range)
        if days_used == day_count:
            break
        else:
            if month == 12:
                month = 1
                year += 1
                if year > year_stop:
                    break
            else:
                month += 1
            day = 1
        first_month = False
    return days


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


def rm_whitespace(line):
    return re.sub(r"\s", "", line)


def get_month_dict(months, month):
    if type(month) == int:
        month = calendar.month_name[month].lower()
    for m_dict in months:
        if month == m_dict['month'].lower():
            return m_dict
    return None


def get_day_dict(months, month, day):
    if type(month) == int:
        month = calendar.month_name[month].lower()
    for m_dict in months:
        if month == m_dict['month']:
            for d_dict in m_dict['days']:
                if day == d_dict['day']:
                    return d_dict
    return None


def parse_file(filepath):
    result = []
    current_month = None
    current_day = None
    configuration = {}
    line_no = 0
    line_text = None

    with open(filepath) as workfile:
        try:
            for line in workfile:
                line_no += 1
                line_text = line

                match = re.search('^\s*#\s*(\{.*\})\s*$', line)
                if match:
                    configuration.update(json.loads(match.groups()[0]))
                    if line_no == 1:
                        global_config = configuration.copy()
                    continue

                line_stripped = rm_whitespace(line)
                match = re.search("^\[(.+)\]$", line_stripped)
                month = None
                if match:
                    month = match.groups()[0]

                match = re.search("^(\d+)=(.+)\[(.+)\]$", line_stripped) or \
                    re.search("^(\d+)=(.+)$", line_stripped)
                day = None
                if match:
                    day = int(match.groups()[0])
                    hours = gethours(match.groups()[1])
                    if len(match.groups()) == 3:
                        day_tags = match.groups()[2].lower().split(',')
                    else:
                        day_tags = []

                if month:
                    tmp_month_dict = {
                        'month': month,
                        'month_num': month_to_num(month),
                        'days': [],
                    }
                    tmp_month_dict.update(configuration.copy())
                    result += [tmp_month_dict]
                    current_month = month

                elif day:
                    get_month_dict(result, current_month)['days'] += [{
                        'day': day,
                        'hours': hours,
                        'lines': [],
                        'tags': day_tags
                    }]
                    current_day = day

                else:
                    match = re.search('^(\s*)(.+)$', line)
                    if match:
                        depth = len(match.groups()[0])
                        line = match.groups()[1]
                        get_day_dict(
                            result, current_month, current_day
                        )['lines'] += [
                            {'depth': depth, 'line': line}
                        ]
        except:
            traceback.print_exc()
            print 'EXCEPTION ON LINE: {}, TEXT: "{}"'.format(
                line_no,
                line_text.strip()
            )
            exit(1)

    for month_dict in result:
        for day_dict in month_dict['days']:
            prev_level = 0
            prev_depth = 0
            for line_dict in day_dict['lines']:
                depth = line_dict['depth']
                if depth > prev_depth:
                    prev_level += 1
                elif depth < prev_depth:
                    prev_level -= 1
                line_dict['depth'] = prev_level
                prev_depth = depth

    return result, global_config


def get_months(root, month_range):
    if month_range[0] and month_range[1]:
        months = []
        inside_range = False
        for month_dict in root:
            if month_dict['month'] == month_range[0]:
                months += [month_dict]
                inside_range = True
            elif month_dict['month'] == month_range[1]:
                months += [month_dict]
                break
            elif inside_range:
                months += [month_dict]
        return months

    elif month_range[0]:
        return [get_month_dict(root, month_range[0])]

    else:
        return root


def get_days_in_month(month_dict, day, count):
    days = []
    for day_dict in month_dict['days']:
        if day <= day_dict['day'] < day + count:
            days += [day_dict]
    return days


def filter_by(root, month_range, day, day_count, group_todos=False):
    if day is None:
        return get_months(root, month_range)
    else:
        out_months = []
        month_dict = get_month_dict(root, month_range[0])
        days_nums = days_range(
            month_dict['year'],
            root[-1]['year'],
            month_dict['month'],
            day,
            day_count
        )

        for month_nums in days_nums:
            month_dict = get_month_dict(root, month_nums['month'])
            days = []
            for day_num in month_nums['days']:
                day_dict = get_day_dict(root, month_nums['month'], day_num)
                if day_dict:
                    days += [day_dict]
            if days:
                tmp_month_dict = month_dict.copy()
                tmp_month_dict.update({
                    'days': days,
                })
                out_months += [tmp_month_dict]

        return out_months


def get_statistics(months):
    stats = {
        'total_hours': 0,
        'total_days': 0,
        'year_start': months[0]['year'],
        'year_end': months[-1]['year'],
        'month_start': months[0]['month'],
        'month_num_start': months[0]['month_num'],
        'month_end': months[-1]['month'],
        'month_num_end': months[-1]['month_num'],
        'day_start': months[0]['days'][0]['day'],
        'day_end': months[-1]['days'][-1]['day'],
        'tags': {},
    }

    for month_dict in months:
        for day_dict in month_dict['days']:
            stats['total_days'] += 1
            stats['total_hours'] += day_dict['hours']

            # record tag stats
            for tag in day_dict['tags']:
                if tag in stats['tags']:
                    stats['tags'][tag]['days'] += 1
                    stats['tags'][tag]['hours'] += day_dict['hours']
                else:
                    stats['tags'][tag] = {
                        'days': 1, 'hours': day_dict['hours']
                    }
    return stats


def extract_todos(months):
    todos = []
    for month_dict in months:
        for day_dict in month_dict['days']:
            for i in reversed(range(len(day_dict['lines']))):
                line = day_dict['lines'][i]['line']
                match = re.match('^TODO:\s*(.*)$', line)
                if match:
                    todos += [match.groups()[0]]
                    del day_dict['lines'][i]
    return todos


def export_json_by(root, month_range, day, day_count, minified=False):
    months = filter_by(root, month_range, day, day_count)
    if minified:
        return json.dumps(months)
    else:
        return json.dumps(months, indent=4, sort_keys=True)


def export_template_by(root, config, template, month_range, day, day_count,
        group_todos=False):
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader('templates'))
    jinja_template = env.get_template(template)

    months = filter_by(root, month_range, day, day_count)

    todos = []
    if group_todos:
        todos = extract_todos(months)

    stats = get_statistics(months)

    return jinja_template.render(
        months=months,
        stats=stats,
        config=config,
        todos=todos
    )


parser = argparse.ArgumentParser(description='WorkLogParser')
parser.add_argument('filepath', metavar='FILEPATH', type=str,
    help='Work log file to parse')
parser.add_argument('-m', '--month', metavar='MONTH', type=str,
    help='Retrieve content by (start) month (ex: november)')
parser.add_argument(
    '-e', '--end-month',
    metavar='END_MONTH', type=str, default=None,
    help='Retrieve content from MONTH to END_MONTH month (ex: december)'
)
parser.add_argument(
    '-d', '--day', metavar='DAY', type=int, default=None,
    help='Retrieve content by (start) day in month (ex: 2)'
)
parser.add_argument(
    '-c', '--day-count', metavar='DAY_COUNT', type=int, default=None,
    help='Retrieve content by day range from DAY inclusive to DAY+DAY_COUNT '
    'exclusive in month'
)
parser.add_argument(
    '-j', '--json', action='store_true',
    help='Export to stdout as JSON format'
)
parser.add_argument(
    '-jm', '--json-min', action='store_true',
    help='Export to stdout as JSON format (minified)'
)
parser.add_argument(
    '-t', '--template', type=str,
    help='Export to stdout by this Jinja2 template file'
)
parser.add_argument(
    '-g', '--group-todos', type=str,
    help='Group all "TODO:*" lines to be accessed in template file'
)
args = parser.parse_args()

root, configuration = parse_file(args.filepath)

if args.month:
    month_range = (args.month, args.end_month)

    if args.day:
        day = args.day
        day_count = args.day_count

    else:  # export whole month(s)
        day = None
        day_count = None

else:  # export all
    month_range = (None, None)
    day = None
    day_count = None

if args.json or args.json_min:
    print export_json_by(
        root, month_range, day, day_count,
        minified=args.json_min
    )

elif args.template:
    print export_template_by(
        root, configuration,
        args.template, month_range, day, day_count,
        group_todos=True if 'group_todos' in args else False
    )
