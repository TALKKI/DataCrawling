FROM python:3.10-slim

WORKDIR /app

# 필요한 시스템 라이브러리 설치
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxcb1 \
    libxkbcommon0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# 크롬 설치 (압축 해제 방식)
RUN wget -q https://storage.googleapis.com/chrome-for-testing-public/136.0.7103.49/linux64/chrome-linux64.zip
RUN unzip chrome-linux64.zip
RUN mv chrome-linux64 /opt/chrome
RUN ln -s /opt/chrome/chrome /usr/bin/google-chrome
RUN rm chrome-linux64.zip

# 크롬 버전 확인
RUN google-chrome --version

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"] 