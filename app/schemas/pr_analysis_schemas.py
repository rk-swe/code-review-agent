from enum import StrEnum
from typing import Self

from pydantic import BaseModel

####


class TaskStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class CodeIssueType(StrEnum):
    STYLE = "style"
    BUG = "bug"
    PERFORMANCE = "performance_improvement"
    BEST_PRACTICE = "best_practice"


####


class PrAnalysisCreate(BaseModel):
    repo_url: str
    pr_number: int
    github_token: str | None = None

    @property
    def owner(self: Self) -> str:
        return self.repo_url.removeprefix("https://github.com/").split("/")[0]

    @property
    def repo(self: Self) -> str:
        return self.repo_url.removeprefix("https://github.com/").split("/")[1]


####


class PrAnalaysisResultFileIssue(BaseModel):
    type: CodeIssueType
    line: int
    description: str
    suggestion: str


class PrAnalaysisResultFile(BaseModel):
    name: str
    issues: list[PrAnalaysisResultFileIssue]


class PrAnalaysisResultSummary(BaseModel):
    total_files: int
    total_issues: int
    critical_issues: int


class PrAnalaysisResult(BaseModel):
    files: list[PrAnalaysisResultFile]
    summary: PrAnalaysisResultSummary


class PrAnalaysisResultResponse(BaseModel):
    task_id: str
    status: TaskStatus
    results: PrAnalaysisResult


####
