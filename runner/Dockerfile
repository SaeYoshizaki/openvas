FROM ubuntu:22.04

RUN apt update && apt install -y \
    curl git sudo python3 python3-pip nodejs npm

RUN pip3 install python-gvm gvm-tools lxml

RUN mkdir -p /actions-runner
WORKDIR /actions-runner

RUN curl -o actions-runner.tar.gz -L \
  https://github.com/actions/runner/releases/download/v2.309.0/actions-runner-linux-arm64-2.309.0.tar.gz \
  && tar xzf actions-runner.tar.gz \
  && rm actions-runner.tar.gz

RUN mkdir -p /run/gvmd
VOLUME ["/run/gvmd"]

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]