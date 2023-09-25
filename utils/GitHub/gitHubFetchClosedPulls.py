from github import Github
import datetime

g = Github('-Your Token-')
repo = g.get_repo("magma/magma")
cutdate=datetime.datetime(2023, 1, 1)
pulls = repo.get_pulls(state='closed', sort='created', direction='desc', base='master')
for pr in pulls:
   author=repo.get_pull(pr.number)
   if pr.merged == False and pr.closed_at > cutdate and 'dependabot' in author.user.login:
       print('{}, {}, {}, {}'.format(pr.number, pr.title, author.user.login, pr.closed_at))
