FROM ubuntu:22.04

# 基本ツール
RUN apt update && apt install -y \
    curl git sudo python3 python3-pip nodejs npm

# python-gvm（OpenVASクライアント）
RUN pip3 install python-gvm gvm-tools lxml

# Runner ディレクトリ
RUN mkdir -p /actions-runner
WORKDIR /actions-runner

# GitHub Actions Runner を取得
RUN curl -o actions-runner.tar.gz -L \
  https://github.com/actions/runner/releases/download/v2.309.0/actions-runner-linux-arm64-2.309.0.tar.gz \
  && tar xzf actions-runner.tar.gz \
  && rm actions-runner.tar.gz

# /run/gvmd/gvmd.sock にアクセスする
RUN mkdir -p /run/gvmd
VOLUME ["/run/gvmd"]

# entrypoint をコピー
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]