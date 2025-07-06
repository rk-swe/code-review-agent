from app.handlers import prefix

# from app.services import github_service
# from app.services import openai_service

prefix.run_prefix()


def main():
    print("Hello from code-review-agent!")

    # openai_service.test()

    # github_service.list_pull_request_files()


if __name__ == "__main__":
    main()
