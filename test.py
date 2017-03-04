from bs4 import BeautifulSoup
import urllib

r = urllib.urlopen('https://devpost.com/hackathons?utf8=%E2%9C%93&search=&challenge_type=all&sort_by=Submission+Deadline').read()

soup = BeautifulSoup(r)

letters = soup.find_all("h2", class_="title")


print type(soup)
# print soup.prettify()
print letters
