CREATE_PR_ANALSYIS_RESPONSE = {
    200: {
        "description": "A Sample response",
        "content": {
            "application/json": {
                "example": {
                    "task_id": "afb71cdb-00ea-4844-9f84-69f33242c6c8",
                    "repo_url": "https://github.com/rk-swe/code-review-agent",
                    "pr_number": 2,
                    "repo": "code-review-agent",
                    "repo_owner": "rk-swe",
                    "status": "pending",
                    "error": None,
                    "created_at": "2025-07-07T04:42:39.407237",
                    "updated_at": None,
                }
            }
        },
    }
}

CREATE_PR_ANALSYIS_REQUEST = [
    {
        "repo_url": "https://github.com/rk-swe/code-review-agent",
        "pr_number": 2,
        "github_token": "your-github_token",
    },
]
