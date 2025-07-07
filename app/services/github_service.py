import os

from githubkit import GitHub
from githubkit.exception import (
    AuthCredentialError,
    AuthExpiredError,
    RateLimitExceeded,
    RequestFailed,
)
from githubkit.versions.latest.models import DiffEntry

GITHUB_PAT = os.environ["GITHUB_PAT"]
github = GitHub(GITHUB_PAT)


# TODO: Error handling
# owner, repo wrong
# pull_number wrong
# github_token wrong
# rate limit error


def list_pull_request_files() -> list[DiffEntry]:
    owner = "potpie-ai"
    repo = "potpie"
    pull_number = 414

    diff_entries: list[DiffEntry] = []

    page = 1
    per_page = 100
    try:
        while True:
            response = github.rest.pulls.list_files(
                owner, repo, pull_number, per_page=per_page, page=page
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
    except RateLimitExceeded:
        raise
    except RequestFailed:
        raise
    except AuthCredentialError:
        raise
    except AuthExpiredError:
        raise
    except Exception:
        raise

    return diff_entries
