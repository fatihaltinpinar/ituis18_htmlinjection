import requests
import json

parameters = {}

# Taking secret.json file for api mail and api key.
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

# hash_type is required in api thus we add it to parameters
parameters['hash_type'] = 'sha256'

passwords = []

try:
    with open('hashes.txt') as hashes:
        print('\nReading hashes.txt')
        for line in hashes:
            # From every line we extract the owner repository's name and the hash itself
            hashed_pass = line[-1:-66:-1][::-1].replace('\n', '')

            # Getting owner of the hashes
            pass_owner = line[15:]
            pass_owner = pass_owner[:pass_owner.find('/')]

            # We add hash to the dict in order to be used in a request.
            parameters['hash'] = hashed_pass

            # Requesting answer from the api via.
            try:
                print('\nLooking for password of ', pass_owner)
                response = requests.get('https://md5decrypt.net/en/Api/api.php', params=parameters)

                # Response from the server comes as bytes we convert it back to the utf-8 in order to be able to read it
                password = response.content.decode('utf-8')

                # Server returns empty string if password can not be found
                # WE NEED TO ADD ERROR CODES HERE! Provided at https://md5decrypt.net/en/Api/#erreurs
                errcode_check = {
                        'ERROR CODE : 001' : 'You exceeded the 400 allowed request per day',
                        'ERROR CODE : 002' : 'There is an error in your email / code',
                        'ERROR CODE : 003' : 'Your request includes more than 400 hashes',
                        'ERROR CODE : 004' : 'hash_type is not valid',
                        'ERROR CODE : 005' : 'Your hash doesn\'t match hash_type',
                        'ERROR CODE : 006' : 'You didn\'t provide all the arguments, or you mispell one of them',
                        'ERROR CODE : 007' : 'The premium code you entered is not valid',
                        'ERROR CODE : 008' : 'The premium variable is not correct, it must be 1',
                        'ERROR CODE : 009' : 'Your premium account ran out of time',
                }

                if password != '' and errcode_check.get(password,'no_error') == 'no_error':
                    print('Found password {}:{}'.format(pass_owner, password))
                    passwords.append({
                        'pass_owner': pass_owner,
                        'password': password,
                        'hash = ': hashed_pass,
                        'link': 'https://github.com/ituis18/' + pass_owner
                    })
                elif errcode_check.get(password,'no_error') != 'no_error':
                    print('Got an error: {}'.format(errcode_check.get(password)))
                else:
                    print('{}\'s password is way too strong!'.format(pass_owner))

                    passwords.append({
                        'pass_owner': pass_owner,
                        'hash = ': hashed_pass,
                        'link': 'https://github.com/ituis18/' + pass_owner
                    })
            except requests.exceptions as e:
                print('Error:{} \nWhile trying to solve {}'.format(e,pass_owner))

except FileNotFoundError:
    exitcode = '''
    Missing hashes.txt
    In order to find every hash in repositories run following command in a terminal

grep -ronE "[a-fA-F0-9]{64}" ./repositories/ > hashes.txt

    '''
    # I'm using exitcode to print things because they look red. I liked it that's why.
    exit(exitcode)

try:
    with open('passwords.json', 'w') as output_file:
        print('\nDumping passwords into json file')
        json.dump(passwords, output_file, indent=2)
except EnvironmentError as e:
    print(e)
