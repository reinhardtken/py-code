FROM golang:latest
LABEL maintainer="huangxiwen"
RUN mkdir -p /letv/logs/
RUN chmod 777 /letv/logs/
ADD wager /letv/app/

CMD go install /letv/app/


