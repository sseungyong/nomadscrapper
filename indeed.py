import requests
from bs4 import BeautifulSoup

LIMIT = 50
INDEED_URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"


def extract_indeed_pages():
    result = requests.get(INDEED_URL)
    soup = BeautifulSoup(result.text, "html.parser")

    pagination = soup.find("div", {"class": "pagination"})

    links = pagination.find_all("a")

    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]

    return max_page


def extract_jobs(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    company_span = html.find("span", {"class": "company"})
    company_anchor = company_span.find("a")
    if company_anchor is not None:
        company = str(company_anchor.string)
    else:
        company = str(company_span.string)
    company = company.strip()
    location = html.find("span", {"class": "location"}).string
    job_id = html["data-jk"]
    return {"title": title, "company": company, "location": location, "link": f"https://www.indeed.com/viewjob?jk={job_id}"}


def extract_indeed_jobs(last_page):
    jobs = []
    for page in range(last_page):
        result = requests.get(f"{INDEED_URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            job = extract_jobs(result)
            jobs.append(job)
    return jobs


def get_indeed_jobs():
    max_indeed_pages = extract_indeed_pages()
    indeed_jobs = extract_indeed_jobs(max_indeed_pages)

    return indeed_jobs


if __name__ == "__main__":
    xx = extract_indeed_jobs(0)
    print(xx)
