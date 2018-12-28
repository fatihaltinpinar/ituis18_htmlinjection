import os
import glob
import re
from bs4 import BeautifulSoup

file_types_to_search = ('*.py', '*.html')
root = 'repositories/'
count = 0

def get_files(base_dir, file_extension):
    return glob.glob(f"{base_dir}/**/*.{file_extension}", recursive=True)


for repo in os.listdir(root):

    for py_file in get_files(root + repo, 'py'):

        with open(py_file) as file:
            file_text = file.read()

            form_html = re.findall(r'<form.*?</form>', file_text, flags=re.DOTALL)

    for html_file in get_files(root + repo, 'html'):

        with open(html_file) as file:
            file_text = file.read()

            form_html.extend(re.findall(r'<form.*?</form>', file_text, flags=re.DOTALL))

    if len(form_html) != 0:
        print(form_html)

    for form in form_html:
        soup = BeautifulSoup(form, "html")

        # finds every element that has a name attribute in html
        form_inputs = soup.findAll(attrs={"name": True})

        # goes over every element that has a name attribute
        for x in form_inputs:

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


        # forms_inputs.attrs can be used in here
        # print(form_inputs)

print('this many password fields found', count)