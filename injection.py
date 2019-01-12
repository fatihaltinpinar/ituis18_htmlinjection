import json
import requests
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

parsedJSON = 'parsed.json'
dataParsedJson = {}

# Read JSON data into the data variable
try:
    with open(parsedJSON) as json_file:
        dataParsedJson = json.load(json_file)

        # Going through names of repos in order to access dicts in parsed.json :(
        ituisReposURL = "https://github.com/ituis18"

        # Loop through all the pages
        for pageNum in range(1, 12):
            # Open connection, read and close
            repoPage = urlopen(ituisReposURL + "?page=" + str(pageNum))
            repoHTML = repoPage.read()
            repoPage.close()

            # Parse the webpage
            repoSoup = soup(repoHTML, "html.parser")
            # Grab all repo names
            repoNames = repoSoup.findAll("div", {"class": "d-inline-block mb-1"})

            for repoName in repoNames:
                # Find only Assignment 2 repos
                if repoName.a.text[11:13] == "a2":
                    # print(repoName.a.text[11:])
                    # print(repoName)
                    repoOwnerName = re.findall(r'a2-*.*.', repoName.a.text)[0]
                    try:
                        actionLink = dataParsedJson[repoOwnerName]['pageLink'] + dataParsedJson[repoOwnerName]['action']
                    except KeyError:
                        try:
                            actionLink = dataParsedJson[repoOwnerName]['pageLink']
                            pass
                        except KeyError:
                            actionLink = ""
                            pass
                    # If password was successfully found
                    # if dataParsedJson[repoOwnerName]['password'] != "":
                    try:
                        requests.post(actionLink,
                                      data={dataParsedJson[repoOwnerName]['passField']: dataParsedJson[repoOwnerName]['password'],
                                            'comment': 'Hello'})
                    except KeyError:
                        # exitCode = '{} not cracked/found'.format(repoOwnerName)
                        pass
                        # print(re.findall(r'a2-*.*.', repoName.a.text)[0])

except FileNotFoundError:
    exitCode = '''\"{}\" was not found.
    Have you run the following command\:
    python3 parse.py'''.format(parsedJSON)
    exit(exitCode)
