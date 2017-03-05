from bs4 import BeautifulSoup
import requests

def soup_from_url(url):
    result = requests.get(url)
    c = result.content
    soup = BeautifulSoup(c)
    return soup


# returns devpost profiles of contributors for a single project
def get_contributors(project_url):
    soup = soup_from_url(project_url)

    letters = soup.find_all("a", class_="user-profile-link")
    for letter in letters:
        each = (str(letter)).split("\n")
        contributors = set([elem['href'] for elem in soup.find_all("a", class_="user-profile-link", href=True)])
    return contributors

# returns list of devpost project links given the submission page
def get_project_links(submission_url):
    project_links = []
    num = 1
    soup = soup_from_url(submission_url)
    letters = soup.find("span", class_="items_info").find_all('b')

    for letter in letters:
        # (yamini) lol sorry this is gross
        total = (((str(letters)).split("b")[3]).split(">"))[1].split("<")[0]

    # divide by number of submissions per page
    num_pages = int(total)/24

    # urls hold all the submissions pages
    urls = [submission_url]
    for i in range(num_pages + 1):
        urls.append(submission_url+ "?page=" + str(i))

    # scrape each submission page
    for each_url in urls:
        soup = soup_from_url(each_url)
        project_links.append([elem['href'] for elem in soup.find_all("a", class_="block-wrapper-link fade link-to-software", href=True)])

    return [item for sublist in project_links for item in sublist]

# main

get_project_links("https://hackgt2016.devpost.com/submissions")
