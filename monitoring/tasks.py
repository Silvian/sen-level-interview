"""Monitoring app celery tasks."""
import csv
from datetime import datetime

from celery.utils.log import get_task_logger

from servers.celery import app

logger = get_task_logger(__name__)


@app.task
def process_csv_task(file_id):
    """Celery task to process the imported csv files."""
    from monitoring.models import CSVUpload, Login
    file = CSVUpload.objects.get(pk=file_id)

    logger.info("Processing file {}".format(file))

    with file.csv.open(mode="rt") as f:
        reader = csv.reader(f)
        next(reader)  # skip the first row containing the headers

        for row in reader:
            logger.debug(row)

            # define the csv rows layout:
            server_name = row[0]
            server_ip = row[1]
            username = row[2]
            full_name = row[3]
            contact = row[4]
            login_time = row[5]

            # TODO: Current Limitations to be addressed
            """
            Currently there is no check to check every single date both ways assumptions are made that:
            if there is a back slash we expect the date to be in dd-mm-yy or dd-mm-YYYY
            if there is a pipe divider we expect the same as a backslash
            if there is a forward slash then we expect the date to be in YYYY/mm/dd or yy/mm/dd
            if there is a dash then we expect to be standar YYYY-mm-dd format only

            Note: All of these could be swapped around and there could be further ambiguity in reading date.
            Some dates could be in the future as a result of this issue.

            For any date not confined to any of the above we try to keep the entry but roll the date back to
            Unix start date i.e. 01-01-1970 00:00:00
            """

            try:
                # 12\10\2016
                if "\"" in login_time:
                    if len(login_time) < 10:
                        login_time = datetime.strptime(login_time, '%d\%m\%y')
                    else:
                        login_time = datetime.strptime(login_time, '%d\%m\%Y')

                # 10|12|2016
                elif "|" in login_time:
                    if len(login_time) < 10:
                        login_time = datetime.strptime(login_time, '%d|%m|%y')
                    else:
                        login_time = datetime.strptime(login_time, '%d|%m|%Y')

                # 2016/10/12
                elif "/" in login_time:
                    if len(login_time) < 10:
                        login_time = datetime.strptime(login_time, '%y/%m/%d')
                    else:
                        login_time = datetime.strptime(login_time, '%Y/%m/%d')

                # 2016-10-12 12:00:00.000000
                elif "-" and ":" in login_time:
                    login_time = datetime.strptime(login_time, '%Y-%m-%d %H:%M:%S.%f')

                # 2016-10-12
                elif "-" in login_time and login_time != "login-time":
                    login_time = datetime.strptime(login_time, '%Y-%m-%d')

                else:
                    login_time = datetime.strptime('2017-12-12', '%Y-%m-%d')

            # dates such as 17\19\06 or 17/19/06 don't make sense and will be defaulted back to start of unix time.
            except ValueError:
                login_time = datetime.strptime('1970-01-01', '%Y-%m-%d')
                pass

            # figure out if the contact detail is an email or number
            # assuming that if its not an email then it must be a number
            contact_email = ""
            contact_number = ""
            if "@" in contact:
                contact_email = contact
            else:
                contact_number = contact

            # process the data into the Login model
            _, created = Login.objects.get_or_create(
                server_ip=server_ip,
                username=username,
                full_name=full_name,
                login_time=login_time,
                defaults={
                    'server_name': server_name,
                    'contact_email': contact_email,
                    'contact_number': contact_number,
                }
            )

    # end of file parsing
    file.csv.close()
