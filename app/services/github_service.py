import os

from githubkit import GitHub
from githubkit.versions.latest.models import DiffEntry

GITHUB_PAT = os.environ["GITHUB_PAT"]
github = GitHub(GITHUB_PAT)


def test():
    owner = "potpie-ai"
    repo = "potpie"
    pull_number = 414

    diff_entries: list[DiffEntry] = []

    page = 1
    per_page = 100

    while True:
        response = github.rest.pulls.list_files(
            owner, repo, pull_number, per_page=per_page, page=page
        )
        print(page, len(response.parsed_data))
        if not response.parsed_data:
            break

        diff_entries.extend(response.parsed_data)
        page += 1

    print(diff_entries)
