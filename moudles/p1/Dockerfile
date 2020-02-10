FROM python3.7:basic
COPY sources.list /etc/apt/
COPY * /home/plugin/
RUN apt-get update \ 
 && mkdir -p /home/plugin/data \ 
 && mkdir -p /home/plugin/result 