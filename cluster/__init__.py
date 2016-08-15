import re

from subprocess import check_output
from time import sleep


def job_running(job_name):
    """
    Checks if a specific job is still running on a cluster using the qstat command

    :param job_name: name of the submitted script/jobname
    :return: boolean true if the job is still running or in the queue
    """
    qstat = check_output(["qstat", "-r"]).decode("utf-8")

    pattern = "Full jobname:\s*" + job_name

    running_jobs = re.findall(pattern, qstat)

    if len(running_jobs) > 0:
        print('Still %d jobs running.' % len(running_jobs), end='\r')
    else:
        print('\nDone!\n')

    return bool(len(running_jobs) > 0)


def wait_for_job(job_name, sleep_time=5):
    """
    Checks if a job is running and sleeps for a set number of minutes if it is

    :param job_name: name of the job to check
    :param sleep_time: time to sleep between polls (in minutes, default = 5)
    """
    while job_running(job_name):
        sleep(sleep_time*60)
