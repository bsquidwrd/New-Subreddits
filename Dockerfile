FROM python:3-alpine

RUN python -m pip install pip --upgrade --no-cache-dir
RUN pip install requests --no-cache-dir

RUN  mkdir /app

COPY . /app

ENV ENABLE_PUSHOVER=false
ENV PUSHOVER_USER=
ENV PUSHOVER_TOKEN=
ENV REDDIT_USERNAME=random_user

CMD ["python", "-u", "new_subreddits.py"]
