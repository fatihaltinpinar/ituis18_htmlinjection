import glob
import os
import re

reposPath_orig = 'repositories/'
reposPath = reposPath_orig

# Create path of every repo in /repositories
for repoName in os.listdir(reposPath):
    reposPath += repoName + '/'
    # Reaching every .py file using glob
    for pyFile in glob.glob(os.path.join(reposPath, '*.py')):
        # Read the python file
        read_pyFile = open(pyFile).read()
        # Find the lines with post method
        routeOfForm_m1 = re.findall(r'@post\((.+?)\)', read_pyFile)
        routeOfForm_m2 = re.findall(r'@route\((.+?)method="POST"\)', read_pyFile)
        # Print only non empty lists
        if len(routeOfForm_m1) != 0:
            print(routeOfForm_m1)
        if len(routeOfForm_m2) != 0:
            print(routeOfForm_m2)
        # print(open(fileName).read())
        # with open(fileName) as openedFile:
        #     if 'String' in myfile.read():
        # print(fileName)

    reposPath = reposPath_orig
