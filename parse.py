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
            pageLink = re.search(r'https://.*?\.herokuapp\.com.*?|$', fileText).group()
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

        # allForms contains all the form elements of a single repo user.(Only from .py files)
        allForms.extend(formHtml)

    # goes over every form element that we found per repo.
    for form in allForms:

        # We parse our string with BeautifulSoup since we have it as txt.
        # We get a BeautifulSoup object that has all the information about html file.
        # It allows us to find elements, their attributes, children, parents with ease.
        soup = BeautifulSoup(form, 'html.parser')

        # Fields is where we hold 'name' attributes of every input in a form.
        fields = []

        # Since a html input has to have a name attribute in order to be sent to the server
        # we look for inputs wia this tag. It returns a list of objects which are html elements that
        # have 'name' attribute.
        formInputs = soup.findAll(attrs={"name": True})

        # We need to find 'action' attribute of the form. Thus we need the object that represents
        # the form itself. formAction is a object that represents form element that has a 'action' attribute
        # We already go over forms but I was not able to find the value of 'action' attribute. This one
        # worked so I don't care :)
        formAction = soup.find(attrs={"action": True})

        # We go over every input element we found
        for formInput in formInputs:

            # We only look for forms that has a password field. We check if any of the inputs
            # has 'type' attribute that is set to 'password'
            if formInput.attrs.get('type') == 'password':

                # In HTML if you do not write 'action' attribute it'll be set to '/' by default.
                if formAction is None:
                    repoData['action'] = '/'
                else:
                    # We set the action in our dictionary to it's value in HTML
                    repoData['action'] = formAction.attrs.get('action')

                # Since this part are in the if block formInput will be representing the input that is
                # password input. We need the name to send password to the server.
                passField = formInput.attrs.get('name')
                repoData['passField'] = passField

                # I had to go over every input again. Sad but I can not find a solution
                # for this now.
                for formI in formInputs:
                    fields.append(formI.attrs.get('name'))
                fields.remove(passField)
                repoData['fields'] = fields
                repoData['raw'] = form
    # Adds repo's data to all data.
    data[repo] = repoData

# Dumping into a json file
with open('parsed.json', 'w') as f:
    #  json.dump(passwords, output_file, indent=2)
    json.dump(data, f, indent=2)
