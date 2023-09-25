# Install : pip install PyGithub
# Script for fetching pull requests for open PRs 
from github import Github
g = Github('Your Token')
repo = g.get_repo("magma/magma")
pulls = repo.get_pulls(state='open', sort='created', base='master')
for pr in pulls:
   author=repo.get_pull(pr.number)
   print('{}, {}, {}'.format(pr.number, pr.title, author.user.login))
