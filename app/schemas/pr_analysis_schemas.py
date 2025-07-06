from typing import Self

from pydantic import BaseModel


class PrAnalysis(BaseModel):
    repo_url: str
    pr_number: int
    github_token: str | None = None

    @property
    def owner(self: Self) -> str:
        return self.repo_url.removeprefix("https://github.com/").split("/")[0]

    @property
    def repo(self: Self) -> str:
        return self.repo_url.removeprefix("https://github.com/").split("/")[1]
