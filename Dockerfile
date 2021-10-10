FROM ubuntu

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get install -y \
            python3-pip \
            p7zip-full \
            gramps \
            git
