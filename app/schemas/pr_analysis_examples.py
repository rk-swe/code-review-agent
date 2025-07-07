CREATE_PR_ANALSYIS_RESPONSE = {
    200: {
        "description": "A Example response",
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


GET_PR_ANALYSIS_STATUS_RESPONSE = {
    200: {
        "description": "A Example response",
        "content": {
            "application/json": {
                "example": {
                    "task_id": "afb71cdb-00ea-4844-9f84-69f33242c6c8",
                    "repo_url": "https://github.com/rk-swe/code-review-agent",
                    "pr_number": 2,
                    "repo": "code-review-agent",
                    "repo_owner": "rk-swe",
                    "status": "completed",
                    "error": None,
                    "created_at": "2025-07-07T04:42:39.407237",
                    "updated_at": "2025-07-07T04:44:10.634853",
                }
            }
        },
    }
}

GET_PR_ANALYSIS_RESULTS_RESPONSE = {
    200: {
        "description": "A Example response",
        "content": {
            "application/json": {
                "example": {
                    "task_id": "afb71cdb-00ea-4844-9f84-69f33242c6c8",
                    "repo_url": "https://github.com/rk-swe/code-review-agent",
                    "pr_number": 2,
                    "repo": "code-review-agent",
                    "repo_owner": "rk-swe",
                    "status": "completed",
                    "error": None,
                    "results": {
                        "files": [
                            {
                                "name": ".env.example",
                                "issues": [
                                    {
                                        "type": "style",
                                        "line": 5,
                                        "description": "File is missing a trailing newline at the end",
                                        "suggestion": "Add a newline after the last line to adhere to POSIX text file conventions",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 4,
                                        "description": "Placeholder values ‘host:port’ are non-specific",
                                        "suggestion": "Use realistic local-development defaults (e.g. redis://localhost:6379/0 and /1) or clearly document that these must be replaced",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 4,
                                        "description": "No inline documentation for Redis URLs",
                                        "suggestion": "Add comments explaining the purpose of REDIS_BROKER_URL (e.g. Celery broker) and REDIS_BACKEND_URL (e.g. result backend) so new developers know when to configure each",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 1,
                                        "description": "Sensitive credentials can accidentally be committed",
                                        "suggestion": "Ensure that your actual .env file (not .env.example) is added to .gitignore and that only .env.example is tracked in version control",
                                        "is_critical": True,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 3,
                                        "description": "Environment variable naming may differ by framework",
                                        "suggestion": "Verify that your application or any dependencies (e.g. SQLAlchemy, Django) expect DB_URL; if not, consider using the conventional DATABASE_URL or add both for compatibility",
                                        "is_critical": False,
                                    },
                                ],
                            },
                            {
                                "name": "README.md",
                                "issues": [
                                    {
                                        "type": "best_practice",
                                        "line": 1,
                                        "description": "Command ‘fastapi dev’ is ambiguous and not a standard FastAPI startup command.",
                                        "suggestion": "Use a known ASGI server invocation, for example:\n\n```bash\nuvicorn app.main:app --reload\n```",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "style",
                                        "line": 1,
                                        "description": "Commands are added as plain text without Markdown structure.",
                                        "suggestion": "Wrap commands in fenced code blocks and add headings to improve readability. For example:\n\n```markdown\n## Running the FastAPI Server\n```bash\nuvicorn app.main:app --reload\n```",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "bug",
                                        "line": 3,
                                        "description": "Module path for Celery application may be incorrect or overly verbose (`app.celery_app.celery_app`).",
                                        "suggestion": "Verify the Celery app import path. Often it’s enough to refer to the module, for example:\n\n```bash\ncelery -A app.celery_app worker --loglevel=info --queues=default\n```",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 1,
                                        "description": "README is missing context such as prerequisites, environment setup, and dependency installation.",
                                        "suggestion": "Add sections covering prerequisites (Python version), creating a virtual environment, installing requirements (`pip install -r requirements.txt`), and any environment variables needed.",
                                        "is_critical": False,
                                    },
                                ],
                            },
                            {
                                "name": "app/celery_app.py",
                                "issues": [
                                    {
                                        "type": "style",
                                        "line": 3,
                                        "description": "Calling load_dotenv() before module‐level imports breaks PEP8 import order and requires multiple noqa directives.",
                                        "suggestion": "Move all imports to the top of the file, then call load_dotenv() immediately after them, or centralize environment loading in a dedicated configuration module.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 13,
                                        "description": "Environment variables are accessed with os.environ[…] which raises KeyError if missing.",
                                        "suggestion": "Use os.getenv('REDIS_BROKER_URL') with a sensible default or fail fast with a clear error message, or validate and load all config values at startup in a configuration loader.",
                                        "is_critical": True,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 13,
                                        "description": "Inline configuration of Celery broker and backend couples environment resolution to app initialization.",
                                        "suggestion": "Extract configuration into a separate settings module (e.g. config.py) and load it via celery_app.config_from_object(), improving separation of concerns and testability.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "bug",
                                        "line": 28,
                                        "description": "Uncaught exceptions in code_analyzer.analyze_pr will bubble up, causing the Celery worker to mark the task as failed without custom logging or retry logic.",
                                        "suggestion": "Wrap the analyze_pr call in a try/except block, log exceptions with traceback, and consider using Celery’s retry mechanisms (e.g. task.retry) to handle transient errors.",
                                        "is_critical": True,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 27,
                                        "description": "The task is registered with the default name and no retry/timeout settings.",
                                        "suggestion": "Explicitly set a task name and configuration options (@celery_app.task(name='process_pr_analysis', autoretry_for=(Exception,), retry_kwargs={'max_retries':3}, time_limit=300)) to improve clarity and resilience.",
                                        "is_critical": False,
                                    },
                                ],
                            },
                            {
                                "name": "app/handlers/logger.py",
                                "issues": [
                                    {
                                        "type": "bug",
                                        "line": 5,
                                        "description": "Using logger.hasHandlers() checks handlers on this logger and its ancestors, which may cause early exit if the root logger has handlers, preventing your 'app' logger from ever being configured.",
                                        "suggestion": "Check only the handlers attached directly to the 'app' logger by inspecting logger.handlers (e.g. `if logger.handlers: return`).",
                                        "is_critical": True,
                                    },
                                    {
                                        "type": "bug",
                                        "line": 3,
                                        "description": "Concurrent calls to get_logger() may interleave, causing multiple handlers to be added or missing handlers.",
                                        "suggestion": "Protect setup with a module‐level lock or use a once‐only mechanism (e.g. threading.Lock around the handler‐addition logic) to ensure only one configuration pass.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 4,
                                        "description": "By default, your logger propagates to the root logger, which may result in duplicate log entries if the root is also configured.",
                                        "suggestion": "Disable propagation on the 'app' logger after adding your handler: `logger.propagate = False`.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 7,
                                        "description": "Log level is hardcoded to INFO and cannot be overridden by environment or configuration.",
                                        "suggestion": "Allow the log level to be configurable (e.g. via an environment variable or application config) and default to INFO if not specified.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "style",
                                        "line": 3,
                                        "description": "Function name `_set_up_logger` uses an uncommon verb order for Python naming conventions.",
                                        "suggestion": "Rename to `_setup_logger` to follow typical snake_case and common terminology.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "style",
                                        "line": 1,
                                        "description": "Module has no docstring describing its purpose or usage.",
                                        "suggestion": "Add a module‐level docstring explaining that this module provides centralized logger initialization and retrieval.",
                                        "is_critical": False,
                                    },
                                ],
                            },
                            {
                                "name": "app/main.py",
                                "issues": [
                                    {
                                        "type": "style",
                                        "line": 1,
                                        "description": "Multiple `# noqa: E402` comments to suppress import order violations indicate that imports aren’t grouped according to PEP8.",
                                        "suggestion": "Reorder your imports: standard library, third-party, then local. To still load environment variables early, move `load_dotenv()` into a small `config.py` module and import your `settings` before app creation—so you can remove the `# noqa` directives.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 1,
                                        "description": "Environment configuration is being loaded via `load_dotenv()` at module import time.",
                                        "suggestion": "Consider using a Pydantic `BaseSettings` subclass to manage configuration centrally. Invoke `Settings()` once (e.g. in `config.py`) so that you avoid scattering `load_dotenv()` calls.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "style",
                                        "line": 12,
                                        "description": "Exception handler’s signature uses a wildcard `_` for the `Request` parameter, and lacks type annotation on its return value.",
                                        "suggestion": "Name the parameter explicitly (e.g. `request: Request`) and annotate the return type (`-> JSONResponse`) to improve readability and tooling support.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "style",
                                        "line": 12,
                                        "description": "User errors are logged at INFO level.",
                                        "suggestion": 'Log user-facing errors at `WARNING` (or a more appropriate level) so that they stand out in your logs. For example: `logger.warning(f"User error: {exc.message}")`.',
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 20,
                                        "description": 'CORS is open to all origins (`allow_origins=["*"]`), which can be a security risk in production.',
                                        "suggestion": "Drive your CORS settings from environment or configuration and restrict `allow_origins` to a specific list of trusted domains when running in non-development environments.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "performance_improvement",
                                        "line": 1,
                                        "description": "`load_dotenv()` reads and parses the `.env` file on every import.",
                                        "suggestion": "If your application uses a pre-loaded environment (e.g., via container orchestration), you can remove `load_dotenv()` at runtime. Alternatively, call it once in your entrypoint script to avoid redundant parsing.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 6,
                                        "description": "The module-level logger is initialized without contextual naming.",
                                        "suggestion": "Pass `__name__` (or a module-specific name) to your `get_logger()` so that log entries include the module path—for example: `logger = get_logger(__name__)`.",
                                        "is_critical": False,
                                    },
                                ],
                            },
                            {
                                "name": "app/models/models.py",
                                "issues": [
                                    {
                                        "type": "best_practice",
                                        "line": 33,
                                        "description": "Storing `github_token` as a plaintext column in the database is a security risk. Tokens should not be persisted in clear text.",
                                        "suggestion": "Remove the token column or encrypt it before storage. Better yet, retrieve the GitHub token at runtime from a secure store (e.g. Vault, AWS Secrets Manager) or environment variable.",
                                        "is_critical": True,
                                    },
                                    {
                                        "type": "style",
                                        "line": 34,
                                        "description": "Typo in comment: “convinience” is misspelled.",
                                        "suggestion": "Correct the spelling to “convenience” or rewrite the comment for clarity.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "style",
                                        "line": 31,
                                        "description": "Inconsistent formatting of the `mapped_column(String)` call. Simple columns are defined in one line elsewhere.",
                                        "suggestion": "Use a single-line definition: `github_token = mapped_column(String)  # secure handling TBD` or apply consistent multi-line style across all columns.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 86,
                                        "description": "The relationship attribute is named `file`, which shadows Python's built-in type `file`.",
                                        "suggestion": "Rename the attribute to something more descriptive (e.g. `analysis_file`, `pr_file`) to avoid shadowing built-ins and improve clarity.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "performance_improvement",
                                        "line": 31,
                                        "description": "Frequently queried columns (`repo_url`, `pr_number`, `repo_owner`) have no indexes defined.",
                                        "suggestion": "Add `index=True` to these `mapped_column` definitions (or create separate Index constructs) to speed up lookups by repository or PR number.",
                                        "is_critical": False,
                                    },
                                ],
                            },
                            {
                                "name": "app/routers/pr_analysis_router.py",
                                "issues": [
                                    {
                                        "type": "bug",
                                        "line": 60,
                                        "description": "Exposing sensitive data (github_token) in the API response leaks credentials to clients.",
                                        "suggestion": "Remove github_token from the response model or mask it before returning results. Consider storing tokens securely and not returning them in API responses.",
                                        "is_critical": True,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 42,
                                        "description": "Using a plain string for task_id loses built-in validation and type safety.",
                                        "suggestion": "Use UUID type for the path parameter (e.g., `task_id: UUID`) and import `UUID` from the `uuid` module. This enables FastAPI to validate the UUID format automatically.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "bug",
                                        "line": 32,
                                        "description": "No error handling around `celery_app.send_task`, which may raise exceptions if the broker is unavailable.",
                                        "suggestion": "Wrap the task submission in a try/except block. On failure, log the error and return an HTTP 503 or similar to inform the client.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 35,
                                        "description": "Returning the SQLAlchemy model instance (`db_analysis`) directly relies on Pydantic’s ORM mode and may inadvertently expose internal fields.",
                                        "suggestion": "Explicitly convert the model to the response schema (e.g., `PrAnalysisStatusResponse.from_orm(db_analysis)`) or unpack its fields into a dict to control exactly which attributes are returned.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "style",
                                        "line": 38,
                                        "description": "Typo in schema name: `BasicRepsonse` is misspelled.",
                                        "suggestion": "Rename the schema to `BasicResponse` (and update all references) for correct spelling and consistency.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "style",
                                        "line": 56,
                                        "description": "Potential typo in response model: `PrAnalaysisResultResponse` contains a misspelling (‘Analaysis’).",
                                        "suggestion": "Ensure the schema is correctly named `PrAnalysisResultResponse` and update the import and references accordingly.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 14,
                                        "description": "There are no tests covering these endpoints, as indicated by a TODO.",
                                        "suggestion": "Add unit and integration tests for each route, covering success and failure scenarios, to improve code reliability.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 37,
                                        "description": "`delete_all_pr_analysis` unconditionally deletes all records without authentication or confirmation.",
                                        "suggestion": "Protect bulk-deletion endpoints behind authentication/authorization checks or remove this endpoint if not needed in production.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 23,
                                        "description": "Large inline TODO comments outlining business logic clutter the route handler.",
                                        "suggestion": "Refactor the PR analysis logic into a separate service or utility module, and keep route handlers focused on HTTP layer concerns.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 10,
                                        "description": "Logger is instantiated at import time, which can complicate testing and configuration.",
                                        "suggestion": "Inject the logger via dependency or configure logging in the application setup to allow easier overrides in tests.",
                                        "is_critical": False,
                                    },
                                ],
                            },
                            {
                                "name": "app/schemas/pr_analysis_schemas.py",
                                "issues": [
                                    {
                                        "type": "style",
                                        "line": 37,
                                        "description": "Typo in class name 'BasicRepsonse'.",
                                        "suggestion": "Rename 'BasicRepsonse' to 'BasicResponse' for correct spelling and consistency.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "style",
                                        "line": 91,
                                        "description": "Multiple classes have a misspelling 'PrAnalaysis' instead of 'PrAnalysis'.",
                                        "suggestion": "Rename classes (PrAnalaysisResultFileIssue, PrAnalaysisResultFile, PrAnalaysisResultSummary, PrAnalaysisResult, PrAnalaysisResultResponse) to use 'PrAnalysis' consistently.",
                                        "is_critical": True,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 72,
                                        "description": "Repeated definition of common fields (repo_url, pr_number, github_token, repo, repo_owner) across multiple response and read models.",
                                        "suggestion": "Extract these shared fields into a base model or mixin that response and read models can inherit from to reduce duplication.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 49,
                                        "description": "Custom regex validation for GitHub URLs duplicates functionality provided by Pydantic.",
                                        "suggestion": "Use Pydantic's built-in HttpUrl (or AnyUrl with a stricter regex) to validate 'repo_url' instead of a custom regex validator.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 53,
                                        "description": "Using re.match with an anchored pattern. re.fullmatch would more clearly express intent.",
                                        "suggestion": "Replace re.match(pattern, value) with re.fullmatch(pattern, value) for clarity.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "style",
                                        "line": 1,
                                        "description": "Imports are not grouped in standard order (standard library, third-party, local).",
                                        "suggestion": "Group and order imports: first standard library (e.g., datetime, enum, re, typing), then third-party (pydantic), then application modules.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 60,
                                        "description": "Properties 'repo_owner' and 'repo' recompute URL parsing on each call.",
                                        "suggestion": "Consider parsing and storing owner and repo once (e.g., in a private field after validation) or caching the results if these properties are accessed frequently.",
                                        "is_critical": False,
                                    },
                                ],
                            },
                            {
                                "name": "app/services/code_analyzer.py",
                                "issues": [
                                    {
                                        "type": "best_practice",
                                        "line": 18,
                                        "description": "Manual commit calls inside the context manager break transaction atomicity and can lead to partial state persistence.",
                                        "suggestion": "Use SQLAlchemy’s session.begin() or a transactional decorator to wrap the entire task in a single transaction, committing once at the end or rolling back on error.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 28,
                                        "description": "Catching a bare Exception may suppress system-exiting exceptions (e.g., KeyboardInterrupt) and makes it harder to distinguish between expected and unexpected errors.",
                                        "suggestion": "Catch more specific exceptions where possible or re-raise critical exceptions so they bubble up correctly.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "style",
                                        "line": 44,
                                        "description": "Status-update code for PROCESSING, FAILED, and COMPLETED is repetitive and mixed with transaction logic.",
                                        "suggestion": "Extract a helper function (e.g. update_task_status(db, task_id, status, error=None)) to centralize status updates and logging.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "bug",
                                        "line": 67,
                                        "description": "Using .one() on the query will raise an exception if no record or multiple records are found, which may not be handled gracefully.",
                                        "suggestion": "Use .one_or_none() and explicitly handle the None case (e.g., by raising a custom error or setting the task to FAILED with an appropriate message).",
                                        "is_critical": True,
                                    },
                                    {
                                        "type": "performance_improvement",
                                        "line": 125,
                                        "description": "Committing the session after inserting each file’s issues can be inefficient when processing many files.",
                                        "suggestion": "Accumulate inserts and commit once at the end of analyze_pr_with_db (or use session.bulk_insert_mappings) to reduce transaction overhead.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "performance_improvement",
                                        "line": 92,
                                        "description": "GitHub and OpenAI API calls are performed sequentially for each file, which can be slow for large pull requests.",
                                        "suggestion": "Consider using concurrency (e.g., asyncio.gather or a thread pool) to fetch diffs, file contents, and review results in parallel.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "style",
                                        "line": 93,
                                        "description": "Log messages in the loop use comma-separated values which can be unclear in log aggregation tools.",
                                        "suggestion": "Use structured logging with named fields (e.g., logger.info('Processing file', index=index+1, total=len(diff_entries), filename=diff_entry.filename)).",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "style",
                                        "line": 14,
                                        "description": "The TODO comment about adding concurrency is vague and may not be tracked elsewhere.",
                                        "suggestion": "Either implement the concurrency improvements now or replace the comment with a reference to a ticket/issue for prioritization.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 114,
                                        "description": "Inserting issues via raw db.execute and insert can bypass ORM-level validation and defaults.",
                                        "suggestion": "Use Session.bulk_insert_mappings or create PrAnalysisFileIssue ORM instances and add them to the session for better integration with SQLAlchemy’s change tracking.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 95,
                                        "description": "No filtering of diff entries (e.g., binary or very large files) before fetching patches and contents may lead to errors or performance issues.",
                                        "suggestion": "Add logic to skip non-text or oversized files, and handle any exceptions from get_patch_from_diff_entry or get_file_content gracefully.",
                                        "is_critical": False,
                                    },
                                ],
                            },
                            {
                                "name": "app/services/github_service.py",
                                "issues": [
                                    {
                                        "type": "best_practice",
                                        "line": 1,
                                        "description": "Imports are not grouped according to PEP8 (stdlib, third-party, local).",
                                        "suggestion": "Group `import base64` with other stdlib imports, followed by a blank line, then third-party imports (e.g. `githubkit`).",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "style",
                                        "line": 5,
                                        "description": "Leftover placeholder comments (`####` and commented test values) clutter production code.",
                                        "suggestion": "Remove or move test values and separator lines into dedicated tests or examples. Use proper docstrings instead of random comment blocks.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "bug",
                                        "line": 20,
                                        "description": "`github_token` parameter in `list_pull_request_files` is declared without a default, making the API inconsistent with other functions.",
                                        "suggestion": "Provide a default `github_token: str | None = None` so callers can omit it consistently across all service methods.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 22,
                                        "description": "The GitHub client is initialized in every function, leading to duplicated code and potential misconfiguration.",
                                        "suggestion": "Extract client creation into a helper or class constructor that accepts the token once and reuses the `GitHub` instance.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 30,
                                        "description": "Using `print` for pagination logs is not suitable for production.",
                                        "suggestion": "Use the `logging` module (e.g. `logger.debug(...)`) so output can be controlled by log level and redirected appropriately.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "performance_improvement",
                                        "line": 28,
                                        "description": "`per_page=100` is hard-coded, limiting flexibility.",
                                        "suggestion": "Make `per_page` a constant or function parameter so clients can adjust page size according to their needs.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 33,
                                        "description": 'Magic status strings (`"removed"`, `"unchanged"`) are repeated inline.',
                                        "suggestion": 'Define named constants (e.g. `SKIPPED_STATUSES = {"removed","unchanged"}`) to improve readability and reuse.',
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "bug",
                                        "line": 32,
                                        "description": "No error handling around API calls; any HTTP or credential error will bubble up unhandled.",
                                        "suggestion": "Wrap calls to `github.rest.*` in try/except blocks, catch relevant exceptions (e.g. auth errors, rate limits), and translate them into meaningful errors or retry logic.",
                                        "is_critical": True,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 40,
                                        "description": "Public functions lack docstrings describing purpose, parameters, and return types.",
                                        "suggestion": "Add PEP257-compliant docstrings to each function to explain usage, args, returns, and possible exceptions.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "bug",
                                        "line": 70,
                                        "description": "`get_file_content` requires a `github_token` but does not allow `None`, breaking consistency with other helpers.",
                                        "suggestion": "Make `github_token` optional with a default of `None`, similar to other methods, and handle the fallback internally.",
                                        "is_critical": False,
                                    },
                                ],
                            },
                            {
                                "name": "app/services/openai_service.py",
                                "issues": [
                                    {
                                        "type": "bug",
                                        "line": 19,
                                        "description": "Typo in return type annotation: `PrAnalaysisResultFile` is misspelled.",
                                        "suggestion": "Correct the spelling to `PrAnalysisResultFile` (or whatever the actual class name is) to match your schema definition.",
                                        "is_critical": True,
                                    },
                                    {
                                        "type": "bug",
                                        "line": 55,
                                        "description": "Extraneous `full_code:` block repeated at the end of the file, which is invalid syntax and will cause a runtime error.",
                                        "suggestion": "Remove the duplicated `full_code:` snippet outside of any function or comment block.",
                                        "is_critical": True,
                                    },
                                    {
                                        "type": "style",
                                        "line": 8,
                                        "description": "The `test()` function is defined at module level and will run on import, which can be unexpected.",
                                        "suggestion": 'Either remove this helper or guard it under `if __name__ == "__main__":` so it doesn’t execute on import.',
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 10,
                                        "description": "Model name `o4-mini` is hard-coded in multiple places.",
                                        "suggestion": "Extract model names into constants or configuration (e.g. environment variables) so they can be managed centrally.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 16,
                                        "description": "`call_code_review` has no error handling around the API call.",
                                        "suggestion": "Wrap `client.responses.parse(...)` in try/except to handle network failures or invalid responses gracefully.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "performance_improvement",
                                        "line": 16,
                                        "description": "This function uses the synchronous OpenAI client, which may block your application under load.",
                                        "suggestion": "Consider using an asynchronous client (e.g. `AsyncOpenAI`) or offloading the call to a background worker.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "style",
                                        "line": 16,
                                        "description": "`call_code_review` is missing a docstring describing its purpose, parameters, and return value.",
                                        "suggestion": "Add a concise docstring (Google/NumPy style) above the function signature.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 22,
                                        "description": "Building large prompt strings via f-strings can be error-prone and hard to maintain.",
                                        "suggestion": "Use a templating approach or a dedicated prompt-builder utility to manage multi-line system and user prompts more cleanly.",
                                        "is_critical": False,
                                    },
                                ],
                            },
                            {
                                "name": "pyproject.toml",
                                "issues": [
                                    {
                                        "type": "bug",
                                        "line": 3,
                                        "description": 'The `requires-python` field is set to ">=3.13", but Python 3.13 has not yet been released. This may prevent installation in current environments.',
                                        "suggestion": 'Lower the minimum Python version to a stable release (e.g. ">=3.10") or bump later when 3.13 is officially available.',
                                        "is_critical": True,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 7,
                                        "description": "Runtime dependencies (`pytest` and `ruff`) are listed alongside production packages. These are typically development-only tools.",
                                        "suggestion": "Move `pytest` and `ruff` into a dev-dependencies or optional-dependencies group (e.g. `[project.optional-dependencies] dev = [...]`) to avoid installing them in production.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 6,
                                        "description": "`celery` and `redis` have extras to tighten integration (e.g. using Redis as broker/back end).",
                                        "suggestion": 'If you plan to use Redis as your broker/result backend, declare the extra: `"celery[redis]>=5.5.3"` and remove the standalone `redis` if not needed elsewhere.',
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "performance_improvement",
                                        "line": 4,
                                        "description": "All dependencies use open-ended `>=` specifiers without upper bounds. This may lead to unintended upgrades that break compatibility.",
                                        "suggestion": "Consider adding upper bounds (e.g. `>=1.16.2,<2.0.0`) or use compatible release operators (`~=1.16.2`) to guard against breaking changes.",
                                        "is_critical": False,
                                    },
                                ],
                            },
                            {
                                "name": "tests/__init__.py",
                                "issues": [
                                    {
                                        "type": "best_practice",
                                        "line": 1,
                                        "description": "This __init__.py file is empty and serves only to mark the directory as a package.",
                                        "suggestion": "If your project targets Python 3.3 or newer, consider using implicit namespace packages and removing empty __init__.py files to reduce clutter.",
                                        "is_critical": False,
                                    }
                                ],
                            },
                            {
                                "name": "tests/test_pr_analysis_flow.py",
                                "issues": [
                                    {
                                        "type": "best_practice",
                                        "line": 11,
                                        "description": "Hard-coded SQLite file path leads to test pollution and potential conflicts",
                                        "suggestion": "Use an in-memory database URL (`sqlite:///:memory:`) or leverage pytest’s tmp_path fixture to generate a unique database file for each test run",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "bug",
                                        "line": 36,
                                        "description": '`os.remove("./test.db")` will raise if the file does not exist (e.g. on earlier failures)',
                                        "suggestion": "Wrap the removal in a try/except for `OSError` or check `os.path.exists()` before calling `os.remove`",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 31,
                                        "description": "Module-scoped, autouse fixture for DB setup can hide dependencies and interfere with test isolation",
                                        "suggestion": "Scope the fixture to individual tests (function scope) or require explicit inclusion to improve clarity and isolation",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 43,
                                        "description": "Test assumes the asynchronous PR analysis task completes instantly, risking flakiness",
                                        "suggestion": "Either mock the async task to run synchronously in tests, or implement polling with a timeout to wait for task completion before asserting results",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "style",
                                        "line": 44,
                                        "description": 'Unnecessary f-string around a static variable (`f"{url_prefix}"`)',
                                        "suggestion": "Pass `url_prefix` directly to `client.post()` instead of using an f-string",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 26,
                                        "description": "Global override of `get_db` dependency may leak into other test modules",
                                        "suggestion": "Apply the dependency override within a fixture and restore the original `app.dependency_overrides` after the test suite runs",
                                        "is_critical": False,
                                    },
                                ],
                            },
                            {
                                "name": "uv.lock",
                                "issues": [
                                    {
                                        "type": "best_practice",
                                        "line": 17,
                                        "description": "Manual insertion of new [[package]] blocks risks inconsistencies and merge conflicts.",
                                        "suggestion": "Regenerate the lockfile using your package manager (e.g., pip-compile or poetry lock) instead of manual edits to ensure correct dependency resolution, sorting, and checksum integrity.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "style",
                                        "line": 17,
                                        "description": "New package entries are not sorted alphabetically relative to existing ones.",
                                        "suggestion": "Sort [[package]] blocks by name to maintain a predictable order and simplify diffs.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 97,
                                        "description": "The top-level [package.metadata] requires-dist list is out of sync with the [[package]] blocks (e.g., celery and redis added in lock but ensure extras/specifiers match).",
                                        "suggestion": "After regenerating the lockfile, verify that the metadata section matches the declared packages and their version specifiers.",
                                        "is_critical": False,
                                    },
                                    {
                                        "type": "best_practice",
                                        "line": 365,
                                        "description": "Multiple related packages (amqp, billiard, celery, kombu, vine) are added separately and may have interdependent version constraints.",
                                        "suggestion": "Regenerate the entire dependency graph to avoid conflicts and confirm that all transitive requirements align.",
                                        "is_critical": False,
                                    },
                                ],
                            },
                        ],
                        "summary": {
                            "total_files": 15,
                            "total_issues": 92,
                            "critical_issues": 12,
                        },
                    },
                }
            }
        },
    }
}
