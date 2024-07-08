# Use a imagem Debian Slim como base
FROM debian:buster-slim
ARG SIPP_VERSION="3.7.2"

WORKDIR /sipp
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential cmake wget libssl-dev libpcap-dev libsctp-dev libncurses5-dev && \
    wget --no-check-certificate "https://github.com/SIPp/sipp/releases/download/v$SIPP_VERSION/sipp-$SIPP_VERSION.tar.gz" && \
    tar -xzf sipp-$SIPP_VERSION.tar.gz -C . && \
    cd sipp-$SIPP_VERSION && \
    ./build.sh --full && \
    ./sipp -sn uas -bg

EXPOSE 5060

CMD ["/bin/bash"]