import git
import json


def get_repositories(repo_data):

    # Taking repo_data.json and loading it into a dictionary
    with open(repo_data) as repo_json:
        repo_dict = json.load(repo_json)

    # Going over every key-value pair in dictionary.
    for repo_name, repo_address in repo_dict.items():

        # Trying to clone every repository
        try:
            print('Cloning {}'.format(repo_name))
            git.Repo.clone_from(repo_address, './repositories/' + repo_name)
            print('Cloned {}'.format(repo_name))

        # If cannot copy the repository either it
        except git.exc.GitCommandError as e:

            # does not exist on GitHub:
            if 'remote: Repository not found' in e.stderr:
                print('{}\'s repository does not exist'.format(repo_name))

            # already cloned:
            elif 'fatal: destination path' in e.stderr:

                print('{} exists, pulling...'.format(repo_name))

                # If a repository is copied already, we pull the changes
                # from GitHub
                git.Repo('./repositories/' + repo_name).remotes.origin.pull()
                print('Pulled {}'.format(repo_name))

            # In case anything else:
            else:
                print('Non handled error: ', e)


# For calling function directly
if __name__ == '__main__':
    get_repositories('repo_data.json')




# except git.exc.GitCommandError as e:
#     print('no repo ', e)

# git.Repo.clone_from(repo_dict[repo_keys[2]], './'+repo_keys[2])
# git.Git('./').clone(repo_dict[repo_keys[x]])


# searching through
# with open('repo_data.json') as repo_json:
#     repo_dict = json.load(repo_json)
# i = 0
# for repo_name in repo_dict:
#     print(i, " ", repo_name)
#     i = i + 1

#
#     repo = git.Repo('a2-batuhanfaik')
#     o = repo.remote.origin
#     o.pull()
# except git.exc.NoSuchPathError:
#     print("cloning")
#     git.Repo.clone_from('https://github.com/ituis18/a2-batuhanfaik.git', './batuhanfaik/')
#