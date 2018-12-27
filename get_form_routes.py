import glob
import os
import re

count = 0
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
        routeOfForm_m1 = re.findall(r'@post\([\"\'](.+?)[\"\']', read_pyFile)
        routeOfForm_m2 = re.findall(r'@route\([\"\'](.+?)[\"\'].+?method=[\"\']POST[\"\']', read_pyFile)

        # Print only non empty lists
        if len(routeOfForm_m1) != 0:
            print(repoName, ':', routeOfForm_m1)
            count += 1
        elif len(routeOfForm_m2) != 0:
            print(repoName, ':', routeOfForm_m2)
            count += 1

    reposPath = reposPath_orig

# Additional info on number of repos with forms
print("\nFound {} repos with forms".format(count))
