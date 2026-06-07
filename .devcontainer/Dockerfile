FROM --platform=x86_64 python:3.11-bookworm

ENV TZ="Europe/Berlin"

RUN apt-get update -y && \
    apt-get autoremove -y
RUN apt-get install -y software-properties-common bash-completion cmake build-essential iputils-ping rsync p7zip-full libuv1-dev git nlohmann-json3-dev librabbitmq-dev libboost-dev libgtest-dev pybind11-dev

RUN pip install uv

WORKDIR /home

CMD ["bash"]
