import os
import glob
import re
from bs4 import BeautifulSoup

fileTypesToSearch = ('*.py', '*.html')
root = 'repositories/'
count = 0


def get_files(base_dir, file_extension):
    return glob.glob(f"{base_dir}/**/*.{file_extension}", recursive=True)


for repo in os.listdir(root):

    for pyFile in get_files(root + repo, 'py'):

        with open(pyFile) as file:
            fileText = file.read()

            formHtml = re.findall(r'<form.*?</form>', fileText, flags=re.DOTALL)

    for htmlFile in get_files(root + repo, 'html'):

        with open(htmlFile) as file:
            fileText = file.read()

            formHtml.extend(re.findall(r'<form.*?</form>', fileText, flags=re.DOTALL))

    if len(formHtml) != 0:
        print(formHtml)

    for form in formHtml:
        soup = BeautifulSoup(form, "html")

        # finds every element that has a name attribute in html
        formInputs = soup.findAll(attrs={"name": True})

        # goes over every element that has a name attribute
        for x in formInputs:

            # gets all attributes of these elements and looks for what type they are
            if x.attrs.get('type') == 'password':

                # since people can put different names but will put type as password(to make field invisible while
                # typing) we can find password's name that'll be used in post method.
                count += 1
                print(x.attrs['name'])

            # TODO: 1
            #  Now we need to take all the other attributes. Homework requires a checkbox, radio thingy, things that you
            #  choose. We need a way to choose one of them it doesn't mater what it is.

            # TODO: 2
            #  Another problem: If people did not use post method they will be using get method in their code, Since
            #  we know url has a limit, we have to write our javascript code clean, short, or we can inject a code
            #  that runs a javascript code from another hijacked user available if they are using get method.
            #  I don't know if this is possible.


print('this many password fields found', count)