import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def clean_title(title_html):
    # BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(title_html, 'html.parser')
    # mark 태그 제거
    for mark in soup.find_all('mark'):
        mark.unwrap()
    return soup.get_text().strip()

def search_naver_blog(keyword, max_pages=1):
    # 검색 결과를 저장할 리스트
    results = []
    
    # Selenium 설정
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    
    
    driver = webdriver.Chrome(options=options)
    
    try:
        for page in range(1, max_pages + 1):
            # 네이버 블로그 검색 URL
            url = f"https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query={keyword}&start={((page-1)*10)+1}"
            driver.get(url)
            
            # 페이지 로딩 대기
            time.sleep(2)
            
            # 블로그 포스트 목록 찾기
            posts = driver.find_elements(By.CSS_SELECTOR, "#main_pack > section > div.api_subject_bx > ul > li.bx")
            
            for post in posts:
                try:
                    # print(post.get_attribute('innerHTML'))
                    # 작성자 ID 추출
                    author_element = post.find_element(By.CSS_SELECTOR, ".user_box .user_info a.name")
                    author_id = author_element.text

                    # 제목 추출 (HTML 포함)
                    title_element = post.find_element(By.CSS_SELECTOR,  ".detail_box .title_area a.title_link")
                    title_html = title_element.get_attribute('innerHTML')
                    title = clean_title(title_html)
                    
                    # 링크 추출
                    link = title_element.get_attribute("href")
                    
                    results.append({
                        'author_id': author_id,
                        'title': title,
                        'link': link
                    })
                except Exception as e:
                    print(f"게시물 처리 중 오류 발생: {e}")
                    continue
            
            print(f"페이지 {page} 처리 완료")
    
    finally:
        driver.quit()
    
    return results

def main():
    # data 디렉토리 생성
    os.makedirs('/app/data', exist_ok=True)
    
    # 검색할 키워드 입력
    keyword = input("검색할 키워드를 입력하세요: ")
    
    # 블로그 검색 실행
    print(f"'{keyword}' 키워드로 네이버 블로그 검색을 시작합니다...")
    results = search_naver_blog(keyword)
    
    # 결과를 DataFrame으로 변환
    df = pd.DataFrame(results)
    
    # 결과 출력
    print("\n검색 결과:")
    print(df)
    
    # 결과를 CSV 파일로 저장
    filename = f"/app/data/naver_blog_{keyword}.csv"
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"\n결과가 {filename} 파일에 저장되었습니다.")

if __name__ == "__main__":
    main() 