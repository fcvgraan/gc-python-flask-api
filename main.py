import datetime
from datetime import timedelta
import holidays as pyholidays
import dateutil.parser
import pytz

work_day_start_hour = 8
work_day_end_hour = 17
sa_holidays = pyholidays.ZA()

def http_trigger(request):
    """ HTTP Cloud Function
    Arg: request (flask.Request)
    Res: arg(s) for flask.make_response
    """
    if request.method == 'GET':
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')

        if start_time == None or end_time == None:
            return 'Parameters are missing, please provide start_time and end_time in ISO-8601 format'
        else:
            try: 
                start_time_parsed = dateutil.parser.parse(start_time).replace(tzinfo=None)
                end_time_parsed = dateutil.parser.parse(end_time).replace(tzinfo=None)

                business_seconds = calculate_business_time(start_time_parsed, end_time_parsed)
                return str(business_seconds)

            except ValueError:
                return 'start_time or end_time is not a valid date string. Please provide them in ISO-8601 format'
    else:
        return 'Request method is {}, only GET is allowed'.format(request.method)

def celculate_delta(start, day_end, end, day_start):
    
    if None not in [start,day_end]:
        if (None == sa_holidays.get(start)) and (start.weekday() < 5):
            delta = (day_end - start).total_seconds()
            if 32400 >= delta > 0:
                return delta
            if 32400 < delta:
                return 32400
        else:
            return 0
    else: 
        if (None == sa_holidays.get(end)) and (end.weekday() < 5):
            delta = (end - day_start).total_seconds()
            if 32400 >= delta > 0:
                return delta
            if 32400 < delta:
                return 32400
        else:
            return 0

def calculate_business_time(start, end):

    period = end - start

    work_day_start = datetime.datetime(start.year, start.month, start.day, work_day_start_hour, 0, 0)
    work_day_end = datetime.datetime(end.year, end.month, end.day, work_day_end_hour, 0, 0)

    if (period.days == 0) and (start.day == end.day):
        if (sa_holidays.get(start) == None) and (start.weekday() < 5):
            if start <= work_day_start < end <= work_day_end:
                return int((end - work_day_start).total_seconds())
            if start <= work_day_start < work_day_end <= end:
                return int((work_day_end - work_day_start).total_seconds())
            if work_day_start < start < end <= work_day_end:
                return int((end - start).total_seconds())
            if work_day_start < start < work_day_end <= end:
                return int((work_day_end - start).total_seconds())
            else:
                return 0
        else:
            return 0
    
    if (period.days <= 1) and ((start.day + 1) == end.day):
        seconds = 0
        for day in [0, 1]:
            if day == 0:
                seconds += celculate_delta(start, work_day_end, None, None)
            else:
                seconds += celculate_delta(None, None, end, work_day_start)
        return int(seconds)
    
    if (period.days >= 2):
        seconds = 0
        for day in range(period.days + 1):
            if day == 0:
                seconds += celculate_delta(start, work_day_end, None, None)
            if 0 < day <= period.days:
                current_day = start + timedelta(days=day)
                if (None == sa_holidays.get(current_day)) and (current_day.weekday() < 5):
                    seconds += 32400
            if day == period.days + 1:
                seconds += celculate_delta(None, None, end, work_day_start)
        return int(seconds)