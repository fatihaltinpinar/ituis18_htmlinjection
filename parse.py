import os
import glob
import re
from bs4 import BeautifulSoup
import requests
import json


root = 'repositories/'
data = {}

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
    repoData = {'repoLink': 'https://github.com/ituis18/' + repo}

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
            pageLink = re.search(r'https://[^w].*?\.herokuapp\.com.*?|$', fileText).group()
            repoData['pageLink'] = pageLink

    # Searching in python files
    allForms = []
    for pyFile in get_files(root + repo, 'py'):
        with open(pyFile) as file:
            fileText = file.read()
            # Looking for form element in html codes
            formHtml = re.findall(r'<form.*?</form>', fileText, flags=re.DOTALL)

            # Looking for 64 character long strings. Character list is defined such as it
            # finds hex. Which is what forms SHA256.
            hashedPass = re.findall(r'[a-fA-F0-9]{64}', fileText)

        allForms.extend(formHtml)
        # print('formHTML of', repo, allForms)
    repoData['raw'] = allForms
    for form in allForms:
        soup = BeautifulSoup(form, 'html.parser')
        formInputs = soup.findAll(attrs={"name": True})
        inputList = []
        for formInput in formInputs:
            if formInput.attrs.get('type') == 'password':
                repoData['passfield'] = formInput.attrs.get('name')
            else:
                inputList.append(formInput.attrs.get('name'))
        repoData['nonpassfields'] = inputList

    data[repo] = repoData

with open('test.txt', 'w') as f:
    #  json.dump(passwords, output_file, indent=2)
    json.dump(data, f, indent=2)
