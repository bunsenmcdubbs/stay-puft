from bs4 import BeautifulSoup
import requests


def get_num_contributors(url):
    result = requests.get(url)
    c = result.content
    soup = BeautifulSoup(c)

    contributors = 0
    letters = soup.find_all("a", class_="user-profile-link")
    for letter in letters:
        each = (str(letter)).split("\n")
        for word in each:
            word_split = word.split()
            if len(word_split) == 4:
                contributors = contributors + 1

    return contributors


# main
print get_num_contributors("https://devpost.com/software/persist")
