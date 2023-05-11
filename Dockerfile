FROM python:3.10-slim-buster as base
RUN apt-get update
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

FROM base as dependencies
RUN apt-get install -y --no-install-recommends gcc
COPY ./requirements.in .
RUN python -m venv $VIRTUAL_ENV && \
    . /opt/venv/bin/activate && \
    pip install pip-tools && \
    pip-compile requirements.in > requirements.txt && \
    pip-sync


FROM base as development
ENV ENV=development \
    PATH="${VENV_PATH}/bin:${PATH}"
COPY --from=dependencies $VENV_PATH $VENV_PATH
WORKDIR /app


FROM base as release
ENV ENV=production
COPY --from=dependencies $VENV_PATH $VENV_PATH
WORKDIR /app
COPY ./src ./src