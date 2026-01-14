#!/bin/bash
# Streamlit Cloud 배포 시 Chrome 설치 스크립트

# Chrome 설치 (Ubuntu/Debian 기반)
apt-get update
apt-get install -y wget gnupg

# Google Chrome 저장소 추가
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

# Chrome 설치
apt-get update
apt-get install -y google-chrome-stable

# ChromeDriver 설치 확인
echo "Chrome 설치 완료"
