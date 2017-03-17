from bs4 import BeautifulSoup
import requests
from datetime import datetime
from urllib.parse import quote

# return soup from url
def soup_from_url(url):
    result = requests.get(url)
    c = result.content
    soup = BeautifulSoup(c, "html.parser")
    return soup

# returns a tuple of (<user data>) from user_url
def get_user_info(user_url):
    raise NotImplementedError

# returns devpost profiles of contributors for a single project
def get_contributors(project_url):
    soup = soup_from_url(project_url)

    letters = soup.find_all("a", class_="user-profile-link")
    contributors = set([elem['href'] for elem in soup.find_all("a", class_="user-profile-link", href=True)])
    return contributors


# returns list of devpost project links given the submission page
def get_projects_info(submission_url):
    project_infos = []
    num = 1
    soup = soup_from_url(submission_url)
    total_elem = soup.find("span", class_="items_info")
    if total_elem is not None:
        total_proj = int(total_elem.text.split()[-1])
    else:
        total_proj = 0

    # divide by number of submissions per page
    num_pages = int(total_proj/24) + 1

    # urls hold all the submissions pages
    urls = [submission_url]
    for i in range(1, num_pages):
        urls.append(submission_url+ "?page=" + str(i))

    # scrape each submission page
    for url in urls:
        soup = soup_from_url(url)
        project_infos.append([(elem.find('h5').text.strip(), elem['href']) for elem in soup.find_all("a", class_="block-wrapper-link", href=True)])
    
    return [item for sublist in project_infos for item in sublist]

def search_results(base_url, query, page_key="page"):
    page_num = 1
    base_url += "&{}={{}}".format(page_key)
    url = base_url.format(quote(query), page_num)
    page = soup_from_url(url)
    raw_listings = list(filter(lambda x: 'featured' not in x.attrs['class'], page.find_all('article', class_='challenge-listing')))
    while len(page.find_all('div', class_="no-results")) == 0 and len(raw_listings) > 0 and page_num <= 15:
        for listing in raw_listings:
            yield(listing)
        page_num += 1
        url = base_url.format(quote(query), page_num)
        page = soup_from_url(url)
        raw_listings = list(filter(lambda x: 'featured' not in x.attrs['class'], page.find_all('article', class_='challenge-listing')))

# returns a submission url from a hackathon name and start/end date (fuzzy match)
def get_submission_url(name, start, end):
    SEARCH_URL = 'https://devpost.com/hackathons?utf8=%E2%9C%93&search={}&challenge_type=all&sort_by=Recently+Added'
    page_num = 1
    page = soup_from_url(SEARCH_URL.format(quote(name), page_num))
    listings = []
    for listing in search_results(SEARCH_URL, name):
        try:
            l_name = listing.find_all('h2', class_='title')[0].text.strip()
            l_url = listing.find_all('a', class_='clearfix', href=True)[0]['href'].split('devpost.com')[0] + 'devpost.com/submissions'
            l_date_range = listing.find_all('span', class_='date-range')[0].text.strip().split(', ')
            l_year = l_date_range[1]
            l_month, l_day = l_date_range[0].split(' ')[:2]
            date_str = '{} {} {}'.format(l_year, l_month, l_day)
            listings.append({
                'name': l_name,
                'url': l_url,
                'date': datetime.strptime(date_str, '%Y %b %d').date()
            })
        except Exception as err:
            pass
    matches = list(filter(lambda l: abs((start-l['date']).days) < 2, listings))
    return matches[0]['url'] if len(matches) > 0 else None

if __name__=='__main__':
    #print(get_contributors("https://devpost.com/software/persist"))
    print(get_projects_info("https://geauxhack2014.devpost.com/submissions"))
    #print(get_submission_url('hack the north', datetime(2016,9,16), datetime(2016,9,18)))
