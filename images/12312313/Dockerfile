FROM registry.cn-hangzhou.aliyuncs.com/icuhub/ubuntu:20.04
COPY * /home/plugin/
RUN sed -i "s/archive.ubuntu.com/mirrors.aliyun.com/g" /etc/apt/sources.list \ 
	&& sed -i "s/security.ubuntu.com/mirrors.aliyun.com/g" /etc/apt/sources.list \ 
	&& apt-get update 
RUN apt install iftop -y \ 