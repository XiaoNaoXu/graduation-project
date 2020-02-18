#!/bin/bash

apt update && apt install python3.7 -y && apt install python3-pip -y && pip3 install shadowsocks -y
echo "{ \
	"server": "0.0.0.0", \
	"port_password": { \
	"30001": "password1", \
	"30002": "password2", \
	"30003": "password3", \
	"30004": "password4" \
	}, \
	"timeout": 300, \
	"method": "aes-256-cfb" \
	}" \
	> /etc/shadowsocks.json
systemctl stop firewalld.service
sed -i "s/cleanup/reset/g" /usr/local/lib/python3.7/dist-packages/shadowsocks/crypto/openssl.py
ssserver -c /etc/shadowsocks.json -d start
