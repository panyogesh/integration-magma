from github import Github
from datetime import datetime
g = Github('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')
#date = datetime(2022, 9, 1, 0, 0)
date = datetime(2023, 1, 1, 0, 0)
repo = g.get_repo("magma/magma")
open_issues = repo.get_issues(state='open', since=date)
for issue in open_issues:
    print("{}- {}".format(issue.number, issue.title))
