# What is this repository

This repository contains backend code for a code review agent.
It has apis to take a github repository and pull request number and github token and give code review as response.
The api creates a background celery task that goes to a celery worker through a redis broker.

## Table of Contents

1. [How to setup and run the code](#how-to-setup-and-run-the-code)
2. [Explanation of design and decisions](#explanation-of-design-and-decisions)
3. [Some things in the repo to better understand the repo](#some-things-in-the-repo-to-better-understand-the-repo)
4. [Things that needs Improvements](#things-that-needs-improvements)
5. [What is not there yet but am currently doing it](#what-is-not-there-yet-but-am-currently-doing-it)

## How to setup and run the code

Install uv, see [uv documentation](https://docs.astral.sh/uv/).

Go inside base folder.

`uv sync`

Create .env file following .env.example file.
Setup postgres, redis, openai api key and put the url there.

To setup db

`run alembic upgrade head`

To run api service

For dev

`fastapi dev`

For prod

`fastapi run`

To run celery worker

`celery -A app.celery_app.celery_app worker --loglevel=info --queues=default`

To run tests

`pytest`

To deploy in a vm or cloud, install docker and docker compose. The .env file should be updated slightly to add host of postgres and redis to be just postgres and redis. Also need to keep postgres db name to be postgres. And then from inside base of the folder run

`docker compose up -d --build`

# Explanation of design and decisions

I should have clarified the requirements beforehand.

What did async code mean here? Is it using asyncio or doing things concurrently and parrallely. For first phase of the code I wanted to write sync apis and background task to test the logic. And later make changes to speed things up. Unfortunately I could not complete it in time. I would have used a threadpool and can make each file run in seperate thread and also manage openai api rate limit. Once i have that then in next phase it made sense to use asyncio.

Also what did a code review agent mean here. My default first idea which is what i implemented was to treat each file independently and get the whole file and diff and pass it to llm to get code review
since openai models are already good at coding related tasks well.

The next step to be much better is to have additional prompt hints for different languages
based on file type This was in my scope but could not do in time.

What improvements can we do at this stage, i think we can do deep research , chain of thought
to be absolutelty sure and get better quality results.

One more thing i thought of was using tools like ruff, pylint for python
and other language specific tools to use with llm
So llm can call the tool and get output and again make another llm call to get an answer.

I feel using a llm agent framework would make things more complex. But some ideas I thought of were seperating each issue type and having specific agents
with sepecific tools for each issue type.
This could be like a style agent, bug agent etc and can act parallelly and then we can aggregate and combine and maybe even use another llm call at the end.

# Some things in the repo to better understand the repo

In [app/schemas/pr_analysis_examples.py](app/schemas/pr_analysis_examples.py), I have added the example input request_body and reponse_body which also has code review of a pr from this repository.

# Things that needs Improvements

Error handling I do have a very nice context manager for the background task
but i could have handled each exception nicely and gave proper messages.

# What is not there yet but am currently doing it

Updating the README.md to be more readable and do markdown syntax correctly.

I need to add a test for background_task - coming in a few more minutes.

live deployment link - coming in a few more minutes.

rate limiting - coming in a few more minutes.

response caching - will take some more time.

---
