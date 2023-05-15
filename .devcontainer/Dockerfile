# FROM mcr.microsoft.com/devcontainers/base:ubuntu
# # Install the xz-utils package
# RUN apt-get update && apt-get install -y xz-utils

ARG VARIANT=0-3.10
FROM mcr.microsoft.com/devcontainers/python:${VARIANT}
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y traceroute 

RUN apt-get update \
&& apt-get install -y git curl zsh

#  Add Git user
RUN git config --global user.email "ezanardo@stellab.it"
RUN git config --global user.name "enricozanardo"


# Add Node 18
RUN apt-get update \
&& apt-get install -y curl ca-certificates \
&& curl -fsSL https://deb.nodesource.com/setup_18.x | bash \
&& apt-get install -y nodejs \
&& node -v \
&& npm -v

RUN apt-get update \
&& npm install -g ganache-cli 