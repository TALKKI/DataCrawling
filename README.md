# 웹 크롤링 프로젝트

이 프로젝트는 도커 기반의 웹 크롤링 환경을 제공합니다.

## 사용된 주요 라이브러리
- requests: HTTP 요청
- BeautifulSoup4: HTML 파싱
- Selenium: 동적 웹페이지 크롤링
- Pandas: 데이터 처리

## 실행 방법

1. 도커 이미지 빌드
```bash
docker build -t web-crawler .
```

2. 도커 컨테이너 실행
```bash
docker run web-crawler
```

## 프로젝트 구조
- `main.py`: 메인 크롤링 코드
- `requirements.txt`: 파이썬 패키지 의존성
- `Dockerfile`: 도커 환경 설정 