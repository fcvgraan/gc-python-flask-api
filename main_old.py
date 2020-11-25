import datetime
import businesstimedelta
import holidays as pyholidays
import dateutil.parser

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
                start_time_parsed = dateutil.parser.parse(start_time)
                end_time_parsed = dateutil.parser.parse(end_time)

                business_seconds = calculate_business_time(start_time_parsed, end_time_parsed)
                return str(business_seconds)

            except ValueError:
                return 'start_time or end_time is not a valid date string. Please provide them in ISO-8601 format'
            
    
    else:
        return 'Request method is {}, only GET is allowed'.format(request.method)

def calculate_business_time(start, end):

    # Define a working day
    workday = businesstimedelta.WorkDayRule(
    start_time=datetime.time(8),
    end_time=datetime.time(17),
    working_days=[0, 1, 2, 3, 4])

    south_african_holidays = pyholidays.ZA()
    holidays = businesstimedelta.HolidayRule(south_african_holidays)
    business_hours_object = businesstimedelta.Rules([workday, holidays])

    start_date_time = datetime.datetime(start.year, start.month, start.day, start.hour, start.minute, start.second)
    end_date_time = datetime.datetime(end.year, end.month, end.day, end.hour, end.minute, end.second)

    business_hours = business_hours_object.difference(start_date_time, end_date_time).hours
    business_seconds = business_hours_object.difference(start_date_time, end_date_time).seconds

    total_seconds = (business_hours*60*60) + (business_seconds)

    return total_seconds