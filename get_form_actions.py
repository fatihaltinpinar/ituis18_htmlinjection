import os
import glob
import re

file_types_to_search = ('*.py', '*.html')
root = 'repositories/'


def get_files(base_dir, filetype_extension):
    return glob.glob(f"{base_dir}/**/*.{filetype_extension}", recursive=True)


for repo in os.listdir(root):

    for pyfile in get_files(root + repo, 'py'):
        with open(pyfile) as file:
            # 'asdf=5;(.*)123jasd'
            file_text = file.read()
            a = re.findall(r'(<form.*?</form>)', file_text, flags=re.DOTALL)


            # ADD HTNL PARSING ALL THE INPUTS
            if len(a) != 0:
                print('lengt = ' , len(a), a)
            # forms = re.findall(r'<forms(.+?)</forms>', file_text)
    for htmlfile in get_files(root + repo, 'html'):
        with open(htmlfile) as file:
            # 'asdf=5;(.*)123jasd'
            file_text = file.read()
            a = re.findall(r'(<form.*?</form>)', file_text, flags=re.DOTALL)

            # ADD HTNL PARSING ALL THE INPUTS
            if len(a) != 0:
                print('lengt = ', len(a), a)
            # forms = re.findall(r'<forms(.+?)</forms>', file_text)
