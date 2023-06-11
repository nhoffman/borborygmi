FROM debian:bookworm-slim
RUN apt-get -y update
RUN apt-get -y install \
    emacs \
    git \
    graphviz \
    python3 \
    python3.11-venv \
    rsync \
    sqlite3

WORKDIR /opt/build

COPY requirements.txt .
RUN python3 -m venv venv
RUN /opt/build/venv/bin/python3 -m pip install -r requirements.txt

COPY org-export /opt/build/org-export
ENV PATH "/opt/build/org-export:$PATH"
ENV ORG_EXPORT_DATA_DIR /opt/build/org-export-data
RUN /opt/build/org-export/org-export cli --show-package-dir
RUN rm /etc/emacs/site-start.d/*

WORKDIR /opt/run
COPY entrypoint.sh /opt/run/entrypoint.sh
RUN chmod +x /opt/run/entrypoint.sh
ENTRYPOINT ["/opt/run/entrypoint.sh"]

