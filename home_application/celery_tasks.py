from celery import task
from blueapps.utils.logger import logger
import datetime, time
from .models import Doinfo


@task
def async_status(client, data, biz_id, obj, ip_id):
    num = 0
    tag = True
    job_id = data['job_instance_id']
    kwargs2 = {"bk_biz_id": biz_id,
               "job_instance_id": job_id}
    while True:
        job_data = client.job.get_job_instance_status(kwargs2)
        if job_data.get('result', False):
            is_finished = job_data['data']['is_finished']
            job_instance = job_data['data']['job_instance']
            status = job_instance['status']
            create_time = job_instance['create_time'][:-6]
            start_time = job_instance['start_time'][:-6]
            if job_instance.get('endtime', ''):
                end_time = job_instance['end_time'][:-6]
            else:
                end_time = datetime.datetime.now()
            if int(status) == 2:
                time.sleep(5)
            else:
                tag = True
                break
        else:
            logger.error(u"request failed")
            num += 1
            if num > 5:
                tag = False
                break
            time.sleep(5)
    if tag:
        Doinfo.objects.create(
            businessname=biz_id,
            username="admin",
            script=obj,
            create_time=create_time,
            starttime=start_time,
            endtime=end_time,
            ipcount=len(ip_id),
            details=is_finished,
            jobid=job_id,
            status=status,
        )
