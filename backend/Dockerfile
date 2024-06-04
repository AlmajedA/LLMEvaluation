FROM python:3.9
LABEL maintainer="backend-server"

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get install git-lfs && \
    python -m venv /py && \
    /py/bin/pip install --upgrade pip

COPY ./requirements.txt /requirements.txt

RUN /py/bin/pip install -r /requirements.txt

COPY ./app /app
COPY ./scripts /scripts

# Ensure the script has Unix line endings and executable permissions
RUN apt-get install -y dos2unix && \
    dos2unix /scripts/run.sh && \
    chmod +x /scripts/run.sh

RUN adduser --disabled-password --no-create-home user && \
    mkdir -p /vol/web/static && \
    chown -R user:user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

EXPOSE 8000

CMD ["run.sh"]
