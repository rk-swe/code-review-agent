import base64

from githubkit import GitHub
from githubkit.utils import UNSET
from githubkit.versions.latest.models import ContentFile, DiffEntry, PullRequest

####


# NOTE: Test value
# repo_owner = "potpie-ai"
# repo = "potpie"
# pr_number = 414


# TODO: Error handling
# owner, repo wrong
# pull_number wrong
# github_token wrong
# rate limit error


####


def list_pull_request_files(
    repo_owner: str,
    repo: str,
    pr_number: str,
    github_token: str | None,
) -> list[DiffEntry]:
    if github_token:
        github = GitHub(github_token)
    else:
        github = GitHub()

    diff_entries: list[DiffEntry] = []

    page = 1
    per_page = 100
    while True:
        response = github.rest.pulls.list_files(
            repo_owner, repo, pr_number, per_page=per_page, page=page
        )
        print(page, len(response.parsed_data))
        if not response.parsed_data:
            break

        diff_entries.extend(
            (
                x
                for x in response.parsed_data
                if x.status not in ["removed", "unchanged"]
            )
        )
        page += 1

    return diff_entries


def get_patch_from_diff_entry(diff_entry: DiffEntry) -> str:
    return diff_entry.patch if diff_entry.patch is not UNSET else ""


####


def get_pull_request(
    repo_owner: str,
    repo: str,
    pr_number: str,
    github_token: str | None = None,
) -> PullRequest:
    if github_token:
        github = GitHub(github_token)
    else:
        github = GitHub()

    pull_request = github.rest.pulls.get(repo_owner, repo, pr_number).parsed_data
    return pull_request


####


def get_file_content(
    repo_owner: str,
    repo: str,
    filename: str,
    ref: str,
    github_token: str,
) -> str:
    if github_token:
        github = GitHub(github_token)
    else:
        github = GitHub()

    response = github.rest.repos.get_content(repo_owner, repo, path=filename, ref=ref)
    file_data = response.parsed_data

    if not isinstance(file_data, ContentFile):
        raise ValueError(f"Unexpected file data type: {type(file_data)}")

    if file_data.encoding != "base64":
        raise ValueError(f"Unsupported encoding: {file_data.encoding}")

    return base64.b64decode(file_data.content).decode("utf-8")


####
