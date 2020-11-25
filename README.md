# gc-python-flask-api
flask api that runs in google cloud functions that can calculate the number of business seconds between any 2 input datetimes. Pass start_time and end_time as query string parameters

Name: Francois Van Graan

Example Endpoint: https://europe-west2-recomed-294109.cloudfunctions.net/calculate-business-seconds?start_time=2020-09-18T08:00:00.000Z&end_time=2020-09-25T17:00:00.000Z

* The provided endpoint constains query string parameters for Friday 18 September 2020 to Friday 25 September 2020. This is period that contains 5 work days, a weekend and one public holiday, Thursday 24 September. The response is supposed to be 45 hours or 162000 seconds. There are many different other test cases in the test folder

* The code is hosted in my personal google cloud instance but you can set up your own instance by following the deployment instructions and using the deploy.sh script.

* The test folder contains an exported Postman collection with several test cases. They are configured to point to the endpoint provided above but you can obviously update them with your own. I've provided instructions on how to run the tests in test instructions.txt

* added quick deploy script that only deploys the function.
* added a test script for quick local debugging

# Problem analysis and approach
--------------------------------

* use python datetime arithmetic with TimeDelta objects. Use the fact that TimeDeltas can be negative to determine if thresholds are exceeded.
* remember that a work day has a max of 32400 work seconds.
* make work day start and end times dynamic. convert these to python datetime so you can use them in calculations.
* standardize to time-zone naive date objects, so strip this after parsing the querystring parameters

on a high level, there's the following cases:

    1. fraction of 24 hours but on 1 day
    2. fraction of 48 hours but on consecutive days
    3. 2 or more full days with with fractional days before and/or after

    check total days, iterate through days n days

    case 1. less than 1 day (n==0) and on the same day. start.day==end.day
    case 1.1. if it's a weekend (start.weekday() >= 5) or public holiday (south_african_holidays.get(start)) don't count the seconds
    case 1.2. if not case 1.1. convert work day paramters to datetime.datetime, if end <= work_day_start or start >= work_day_end, don't count the seconds
              if not case 1.2. possible cases are: start <= work_day_start < end <= work_day_end. count seconds between work_day_start, end
                                                   work_day_start < start < end <= work_day_end. count seconds between start, end
                                                   work_day_start < start < work_day_end <= end. count seconds between start, work_day_end
                                                   start <= work_day_start < work_day_end <= end. count seconds between work_day_start, work_day_end

    case 2. less than 2 day (n<=1>) but over 2 days, (start.day + 1)==end.day
    case 2.1. check both days for weekend and public holidays
    case 2.2. start only matters on the first day and end only matters on the second day. work_day_end and work_day_start becomes end and start for day 1 and 2. value of timedelta becomes negative as the start/end time moves across the working day start/end time.

    case 3. more than 2 days (n > 2). This is the long term case and can be generalized as case 2 but with full days in the middle. just check if they are valid working days before you count them.