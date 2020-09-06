from indeed_scrapper import get_indeed_jobs
from so_scrapper import get_so_jobs
from save_result import save_to_file


def nomad_job_scrapper(word):
    indeed_jobs = get_indeed_jobs(word)
    so_jobs = get_so_jobs(word)
    jobs = indeed_jobs + so_jobs
    return jobs
