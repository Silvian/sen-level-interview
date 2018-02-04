"""Monitoring app celery tasks."""
import csv

from celery.utils.log import get_task_logger
from django.utils import timezone

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
        for row in reader:
            logger.debug(row)
            _, created = Login.objects.get_or_create(
                server_name=row[0],
                server_ip=row[1],
                username=row[2],
                full_name=row[3],
                contact_number=row[4],
                login_time=timezone.now(),
            )

    # end of file parsing
    file.csv.close()
