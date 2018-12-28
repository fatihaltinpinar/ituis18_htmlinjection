import os
import glob
import re
from bs4 import BeautifulSoup

file_types_to_search = ('*.py', '*.html')
root = 'repositories/'


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
        soup = BeautifulSoup(form, 'html')
        form_inputs = soup.findAll(attrs={"name": True})

        # forms_inputs.attrs can be used in here
        print(form_inputs)

