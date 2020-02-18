FROM ubuntu:19.04
COPY * /home/plugin/
RUN sed -i "s/archive.ubuntu.com/mirrors.aliyun.com/g" /etc/apt/sources.list \ 
	&& sed -i "s/security.ubuntu.com/mirrors.aliyun.com/g" /etc/apt/sources.list \ 
	&& apt-get update \ 
	&& mkdir -p /home/plugin/data \ 
	&& mkdir -p /home/plugin/result 
RUN apt install g++ -y \  
        && apt install gcc -y \ 