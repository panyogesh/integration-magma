from github import Github
from datetime import datetime
g = Github('ghp_JhDuidfV0Iy8ToG8vcUdqGepHgbVG52bW11119')
#date = datetime(2022, 9, 1, 0, 0)
date = datetime(2023, 1, 1, 0, 0)
repo = g.get_repo("magma/magma")
open_issues = repo.get_issues(state='open', since=date)
for issue in open_issues:
    user = issue.user
    print("{}$ {}$ {}$ {}".format(issue.number, issue.title, issue.created_at, user.login))
