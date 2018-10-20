FROM python:3-alpine

RUN python -m pip install pip --upgrade
RUN pip install requests

RUN  mkdir /app

COPY . /app

ENV ENABLE_PUSHOVER=false
ENV PUSHOVER_USER=
ENV PUSHOVER_TOKEN=
ENV REDDIT_USERNAME=random_user

CMD ["python", "-u", "new_subreddits.py"]
