from bs4 import BeautifulSoup
import requests


def extract_jobs(term):
    result = []
    url = f"https://remoteok.com/remote-{term}-jobs"
    request = requests.get(url, headers={"User-Agent": "Kimchi"})
    if request.status_code == 200:
        soup = BeautifulSoup(request.text, "html.parser")
        jobs = soup.find_all(
            'td', class_="company position company_and_position")
        for jobs_detail in jobs:
            job_posts = jobs_detail.find_all('a', class_="preventLink")
            for post in job_posts:
                link = post['href']
                link_url = (f"https://remoteok.com{link}")
                position = jobs_detail.find('h2', itemprop="title")
                company_name = jobs_detail.find('h3', itemprop="name")
                locations = jobs_detail.find_all('div', class_="location")
                location = "None"
                salary = "None"
                partTime = "None"
                for location_detail in locations:
                    if location is not None and not location_detail.string.startswith('💰') and not location_detail.string.startswith('⏰'):
                        location = location_detail.string.strip()
                    elif location is not None and location_detail.string.startswith('💰'):
                        salary = location_detail.string.strip()
                    elif location is not None and location_detail.string.startswith('⏰'):
                        partTime = location_detail.string.strip()

                job_data = {
                    'company': company_name.string.strip(),
                    'position': position.string.strip(),
                    'region': location,
                    'salary': salary,
                    'etc' : partTime,
                    'url': link_url
                }
                result.append(job_data)
        for results in result:
            print(results)
            print("////////////")

    else:
        print("Can't get jobs.")

# Search by receiving user input.
term = input("Enter a search term: ")
extract_jobs(term)
