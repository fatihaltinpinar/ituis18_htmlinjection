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
