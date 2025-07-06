from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import DeclarativeBase, mapped_column

from app.schemas.pr_analysis_schemas import CodeIssueType, TaskStatus


class Base(DeclarativeBase):
    pass


def str_uuid4() -> str:
    return str(uuid4())


class PrAnalysis(Base):
    __tablename__ = "pr_analysis"

    task_id = mapped_column(String, primary_key=True, default=str_uuid4)

    repo_url = mapped_column(String)
    repo = mapped_column(String)
    owner = mapped_column(String)
    pr_number = mapped_column(Integer)
    github_token = mapped_column(String)

    status = mapped_column(Enum(TaskStatus))
    error = mapped_column(String)

    created_at = mapped_column(DateTime, default=datetime.utcnow())
    updated_at = mapped_column(DateTime, onupdate=datetime.utcnow())
    # completed_at

    # Check if prev task exists. if it does check pr last updated_at vs last task created_at
    # If pr did not change use prev result
    # If it has changed check unchanged files and use that
    # Compute for changed files
    # Reuse files from prev task if it has not changed

    # relationships


class PrAnalysisFile(Base):
    __tablename__ = "pr_analysis_file"

    id = mapped_column(String, primary_key=True, default=str_uuid4)
    task_id = mapped_column(String, ForeignKey(PrAnalysis.task_id))

    name = mapped_column(String)
    # diff
    # content hashing or diff fingerprinting
    # full file_content

    # status
    # error

    created_at = mapped_column(DateTime, default=datetime.utcnow())
    updated_at = mapped_column(DateTime, onupdate=datetime.utcnow())
    # completed_at


class PrAnalysisFileIssue(Base):
    __tablename__ = "pr_analysis_file_issue"

    id = mapped_column(String, primary_key=True, default=str_uuid4)
    file_id = mapped_column(String, ForeignKey(PrAnalysisFile.id))

    type = mapped_column(Enum(CodeIssueType))
    line = mapped_column(Integer)
    description = mapped_column(String)
    suggestion = mapped_column(String)
    is_critical = mapped_column(Boolean)

    created_at = mapped_column(DateTime, default=datetime.utcnow())
