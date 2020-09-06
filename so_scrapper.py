import requests
from bs4 import BeautifulSoup


def so_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "s-pagination"})
    pages = pagination.find_all("a")
    last_page = pages[-2].get_text(strip=True)

    return int(last_page)


def extract_jobs(html):
    title = html.find("h2", {"class": "mb4"}).find("a")["title"]
    company_span = html.find(
        "h3", {"class": "fc-black-700"}).find_all("span", recursive=False)
    company = company_span[0].get_text(strip=True)
    location = company_span[1].get_text(strip=True)
    job_id = html["data-jobid"]
    return {"title": title, "company": company, "location": location, "link": f"https://stackoverflow.com/jobs/{job_id}"}


def extract_so_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping StackOverFlow :: page {page+1}")
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_jobs(result)
            jobs.append(job)
    return jobs


def get_so_jobs(word):
    url = f"https://stackoverflow.com/jobs?q={word}"
    last_page = so_last_page(url)
    so_jobs = extract_so_jobs(last_page, url)

    return so_jobs


if __name__ == "__main__":
    word = "python"
    xx = get_so_jobs(word)
    print(xx)
