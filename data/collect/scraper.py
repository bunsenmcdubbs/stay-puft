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
    soup = soup_from_url(submission_url)
    
    return [elem['href'] for elem in soup.find_all("a", class_="block-wrapper-link fade link-to-software", href=True)]


# main

print get_contributors("https://devpost.com/software/persist")
print get_project_links("https://hackillinois-2017.devpost.com/submissions")
