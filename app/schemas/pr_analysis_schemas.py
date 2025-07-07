import re
from datetime import datetime
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, field_validator

from app.schemas import pr_analysis_examples


class CustomBaseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        str_strip_whitespace=True,
    )


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


class BasicRepsonse(CustomBaseModel):
    message: str


####


class PrAnalysisCreate(CustomBaseModel):
    repo_url: str
    pr_number: int
    github_token: str | None = None

    @field_validator("repo_url")
    @classmethod
    def validate_github_repo_url(cls, value: str) -> str:
        pattern = r"^https://github\.com/[^/]+/[^/]+/?$"
        if not re.match(pattern, value):
            raise ValueError(
                "repo_url must be a valid GitHub repo URL like https://github.com/owner/repo"
            )

        return value.rstrip("/")

    @property
    def repo_owner(self: Self) -> str:
        return self.repo_url.removeprefix("https://github.com/").split("/")[0]

    @property
    def repo(self: Self) -> str:
        return self.repo_url.removeprefix("https://github.com/").split("/")[1]

    model_config = {
        "json_schema_extra": {
            "examples": pr_analysis_examples.CREATE_PR_ANALSYIS_REQUEST
        }
    }


####


class PrAnalysisStatusResponse(CustomBaseModel):
    task_id: str

    repo_url: str
    pr_number: int
    repo: str
    repo_owner: str

    status: TaskStatus
    error: str | None

    created_at: datetime
    updated_at: datetime | None


####


class PrAnalaysisResultFileIssue(CustomBaseModel):
    type: CodeIssueType
    line: int
    description: str
    suggestion: str
    is_critical: bool


class PrAnalaysisResultFile(CustomBaseModel):
    name: str
    issues: list[PrAnalaysisResultFileIssue]


class PrAnalaysisResultSummary(CustomBaseModel):
    total_files: int
    total_issues: int
    critical_issues: int


class PrAnalaysisResult(CustomBaseModel):
    files: list[PrAnalaysisResultFile]
    summary: PrAnalaysisResultSummary


class PrAnalaysisResultResponse(CustomBaseModel):
    task_id: str

    repo_url: str
    pr_number: int
    repo: str
    repo_owner: str

    status: TaskStatus
    error: str | None

    results: PrAnalaysisResult


####


class PrAnalysisReadData(CustomBaseModel):
    repo_url: str
    pr_number: int
    github_token: str | None
    repo: str
    repo_owner: str


####
