ARG PYTHON_BASE=3.12-slim
# build stage
FROM python:$PYTHON_BASE AS builder

# install PDM
RUN pip install -U pdm
# disable update check
ENV PDM_CHECK_UPDATE=false
ENV PDM_BUILD_SCM_VERSION=1
# copy files
COPY pyproject.toml pdm.lock README.md config.toml demo.sh /project/
COPY src/ /project/src

# install dependencies and project into the local packages directory
WORKDIR /project
RUN pdm install --check --prod --no-editable

# run stage
FROM python:$PYTHON_BASE
RUN apt-get update && apt-get install -y \
    expect \
    wget \
 && apt-get clean && wget https://github.com/asciinema/asciinema/releases/download/v3.0.0-rc.3/asciinema-x86_64-unknown-linux-gnu && mv asciinema-x86_64-unknown-linux-gnu /usr/local/bin/asciinema && chmod +x /usr/local/bin/asciinema

# retrieve packages from build stage
COPY --from=builder /project/.venv/ /project/.venv
COPY --from=builder /project/config.toml /config.toml
COPY --from=builder /project/demo.sh /demo.sh
ENV PATH="/project/.venv/bin:$PATH"
ENV TERM="xterm"
# set command/entrypoint, adapt to fit your needs
COPY src /project/src
CMD ["/usr/bin/bash", "./demo.sh"]
# CMD ["python", "-m", "cursedtodo", "-c", "./config.toml"]
