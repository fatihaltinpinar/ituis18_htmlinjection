from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

ituisReposURL = "https://github.com/ituis18"
nameFile = open("repoNames.txt","w+")
repoNumber = 0

# Loop through all the pages
for pageNum in range(1, 12):
    # Open connection, read and close
    repoPage = urlopen(ituisReposURL+"?page="+str(pageNum))
    repoHTML = repoPage.read()
    repoPage.close()

    # Parse the webpage
    repoSoup = soup(repoHTML, "html.parser")
    # Grab all repo names
    repoNames = repoSoup.findAll("div",{"class":"d-inline-block mb-1"})

    for repoName in repoNames:
        # Find only Assignment 2 repos
        if repoName.a.text[11:13] == "a2":
            # print(repoName.a.text[11:])
            # print(repoName)
            repoNumber += 1
            nameFile.write("{}) {}".format(repoNumber,repoName.a.text[11:]))
