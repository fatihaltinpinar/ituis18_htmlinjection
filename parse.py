import os
import glob
import re
from bs4 import BeautifulSoup
import requests
import json


root = 'repositories/'
data = []

# TODO:
#  Determine the tree of the data. How it is going to be stored
#  data{
#       'a2-reponame' : {
#                     'pass': 'asdads'
#                     'hashed': '23af2314123sd"
#                     'repoLink': repolink
#                     'pageLink': pageLink
#                     'form1': {
#                              'type': 'post'
#                              'passfield': 'password'
#                              'other_fields': [comment,username,radiothingy,blablabutton]
#                              }
#                     }
#      'a2-reponame2'
#      }

def get_files(base_dir, file_extension):
    return glob.glob(f"{base_dir}/**/*.{file_extension}", recursive=True)


# Taking secret.json file for api mail and api key.
parameters = {}
try:
    with open('secret.json') as f:
        parameters.update(json.load(f))
except FileNotFoundError:
    exitcode = '''Missing secret.json
Create a secret.json file like following'
{
    "email": "yourmail@mailprovider.com",
    "code": "yourkey"
}
You can get your key at https://md5decrypt.net/en/Api/'''
    # I'm using exitcode to print things because they look red. I liked it that's why.
    exit(exitcode)

# Goes over every repository directory
for repo in os.listdir(root):

    # Initialing repo_data
    repoData = {'name': repo,
                'repoLink': 'https://github.com/ituis18/' + repo}

    # Searching heroku link in README.md files.
    readmeFile = glob.glob(f"{root + repo}/README.md")
    if len(readmeFile) != 0:
        with open(readmeFile[0]) as file:
            fileText = file.read()
            # TODO:
            #  Fix required. It finds results such as below.
            #  Excluding symbols like []() should do the job
            # 'pageLink': 'https://www.herokucdn.com/deploy/button.png)](https://my-blg-101-project.herokuapp.com'}
            # 'pageLink': 'https://www.herokucdn.com/deploy/button.png)](https://my-blg-101-project.herokuapp.com'}
            pageLink = re.search(r'https://.*?\.herokuapp\.com.*?|$', fileText).group()
            repoData['pageLink'] = pageLink

    # Searching in python files
    for pyFile in get_files(root + repo, 'py'):
        with open(pyFile) as file:
            fileText = file.read()
            # Looking for form element in html codes
            formHtml = re.findall(r'<form.*?</form>', fileText, flags=re.DOTALL)

            # Looking for 64 character long strings. Character list is defined such as it
            # finds hex. Which is what forms SHA256.
            hashedPass = re.findall(r'[a-fA-F0-9]{64}', fileText)

    # Searching in HTML files

    data.append(repoData)



number = 0
for repoData in data:
    number += 1
    print(number, repoData)
