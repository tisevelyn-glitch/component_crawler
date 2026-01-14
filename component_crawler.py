#!/usr/bin/env python3
"""
웹사이트 컴포넌트 크롤러
특정 URL의 div class 명을 추출하여 엑셀 파일로 저장하는 프로그램
"""

import re
from datetime import datetime
from urllib.parse import urlparse
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class ComponentCrawler:
    """웹사이트 컴포넌트 크롤러 클래스"""
    
    def __init__(self, headless=True):
        """
        초기화
        Args:
            headless (bool): 브라우저를 보이지 않게 실행할지 여부
        """
        self.headless = headless
        self.driver = None
        
    def setup_driver(self):
        """Chrome 드라이버 설정"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)
        
    def extract_component_name(self, class_string):
        """
        class 문자열에서 주요 컴포넌트 이름 추출
        Samsung 컴포넌트 네이밍 규칙: AA##- 또는 AAA##- 패턴
        예: hd08-hero-kv-home, co76-feature-kv, co78-recommended-product-carousel
        
        Args:
            class_string (str): class 속성 문자열
        Returns:
            str: 주요 컴포넌트 클래스명 (패턴에 맞지 않으면 None)
        """
        if not class_string:
            return None
        
        classes = class_string.split()
        
        # AA##- 또는 AAA##- 패턴을 따르는 컴포넌트만 찾기
        # 예: hd08-, co76-, srd19- 등
        component_pattern = re.compile(r'^[a-z]{2,3}\d{2}-')
        
        for cls in classes:
            if component_pattern.match(cls):
                return cls
        
        # 패턴에 맞는 컴포넌트가 없으면 None 반환
        return None
    
    def extract_bem_component(self, class_name):
        """
        BEM 패턴에서 컴포넌트명 추출
        예: nv16-country-selector__content-wrap -> nv16-country-selector
        
        Args:
            class_name (str): 클래스명
        Returns:
            str: 컴포넌트명 (BEM의 Block 부분)
        """
        if not class_name:
            return class_name
        
        # __ 기준으로 분리 (BEM의 Block__Element 패턴)
        if '__' in class_name:
            return class_name.split('__')[0]
        
        # -- 기준으로 분리 (BEM의 Block--Modifier 패턴)
        if '--' in class_name:
            return class_name.split('--')[0]
        
        return class_name
    
    def extract_site_code(self, url):
        """
        URL에서 Site Code 추출
        예: https://www.samsung.com/uk/ -> UK
        
        Args:
            url (str): URL
        Returns:
            str: Site Code (대문자)
        """
        try:
            parsed = urlparse(url)
            path_parts = [p for p in parsed.path.split('/') if p]
            if path_parts:
                return path_parts[0].upper()
            return "GLOBAL"
        except:
            return "UNKNOWN"
    
    def extract_page_type(self):
        """
        페이지 타입 추출
        digitalData.page.pageInfo.pageTrack 값을 읽어옴
        
        Returns:
            str: Page Type (예: home, pdp, plp 등)
        """
        try:
            # digitalData.page.pageInfo.pageTrack 값 가져오기
            page_track = self.driver.execute_script("""
                try {
                    if (typeof digitalData !== 'undefined' && 
                        digitalData.page && 
                        digitalData.page.pageInfo && 
                        digitalData.page.pageInfo.pageTrack) {
                        return digitalData.page.pageInfo.pageTrack;
                    }
                } catch (e) {
                    return null;
                }
                return null;
            """)
            
            if page_track:
                # Camel 형태로 변환 (첫 글자만 대문자)
                return page_track.capitalize()
            
            return "Unknown"
            
        except Exception as e:
            print(f"   ⚠️  Page Type 추출 실패: {str(e)}")
            return "Unknown"
    
    def crawl_divs(self, url):
        """
        URL의 div 요소들의 class 추출
        Args:
            url (str): 크롤링할 URL
        Returns:
            list: div 정보가 담긴 딕셔너리 리스트
        """
        print(f"🔍 크롤링 시작: {url}")
        
        try:
            if not self.driver:
                self.setup_driver()
            
            # 페이지 로드
            self.driver.get(url)
            
            # 페이지 로딩 대기
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "div"))
            )
            
            # 추가 로딩 시간 (동적 콘텐츠)
            import time
            time.sleep(3)
            
            # Site Code 추출
            site_code = self.extract_site_code(url)
            print(f"🌍 Site Code: {site_code}")
            
            # Page Type 추출
            page_type = self.extract_page_type()
            print(f"📄 Page Type: {page_type}")
            
            # 모든 div 요소 찾기
            divs = self.driver.find_elements(By.TAG_NAME, "div")
            
            print(f"✅ 총 {len(divs)}개의 div 요소 발견")
            
            # 컴포넌트별로 데이터를 수집하기 위한 딕셔너리
            components_data = {}
            processed_classes = set()  # 중복 제거를 위한 세트 (클래스명 기준)
            
            for idx, div in enumerate(divs, 1):
                class_attr = div.get_attribute("class")
                
                if class_attr and class_attr.strip():
                    component_class = self.extract_component_name(class_attr)
                    
                    # 컴포넌트 패턴에 맞는 것만 추출
                    if component_class:
                        # 중복 체크 (클래스명 기준)
                        if component_class in processed_classes:
                            continue
                        
                        processed_classes.add(component_class)
                        
                        # display 스타일 체크
                        display_style = div.value_of_css_property("display")
                        is_displayed = display_style != "none"
                        
                        # BEM 컴포넌트명 추출
                        component_name = self.extract_bem_component(component_class)
                        
                        # 컴포넌트별로 데이터 그룹화
                        if component_name not in components_data:
                            components_data[component_name] = {
                                'classes': [],
                                'display_y': 0,
                                'display_n': 0,
                                'all_classes': set()
                            }
                        
                        components_data[component_name]['classes'].append(component_class)
                        
                        if is_displayed:
                            components_data[component_name]['display_y'] += 1
                        else:
                            components_data[component_name]['display_n'] += 1
                        
                        # 전체 클래스 목록 수집
                        for cls in class_attr.split():
                            components_data[component_name]['all_classes'].add(cls)
            
            # 결과 리스트 생성 (코드 내 순서대로)
            results = []
            for idx, (component_name, data) in enumerate(components_data.items(), 1):
                results.append({
                    '번호': idx,
                    'Site Code': site_code,
                    'Page Type': page_type,
                    'URL': url,
                    '컴포넌트명': component_name,
                    '전체 클래스 목록': ', '.join(data['classes']),
                    'Display': f"Y:{data['display_y']} / N:{data['display_n']}"
                })
            
            total_classes = sum(len(data['classes']) for data in components_data.values())
            total_y = sum(data['display_y'] for data in components_data.values())
            total_n = sum(data['display_n'] for data in components_data.values())
            
            print(f"📊 총 {len(results)}개의 고유 컴포넌트")
            print(f"   └ 총 클래스 수: {total_classes}개")
            print(f"   └ Display Y: {total_y}개")
            print(f"   └ Display N: {total_n}개")
            return results
            
        except Exception as e:
            print(f"❌ 에러 발생: {str(e)}")
            return []
    
    def save_to_excel(self, data, url):
        """
        데이터를 엑셀 파일로 저장
        Args:
            data (list): 저장할 데이터
            url (str): 크롤링한 URL
        Returns:
            str: 저장된 파일명
        """
        if not data:
            print("⚠️  저장할 데이터가 없습니다.")
            return None
        
        # 파일명 생성
        domain = urlparse(url).netloc.replace('www.', '').replace('.', '_')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{domain}_components_{timestamp}.xlsx"
        
        # DataFrame 생성
        df = pd.DataFrame(data)
        
        # 엑셀 파일로 저장
        try:
            df.to_excel(filename, index=False, engine='openpyxl')
            print(f"✅ 파일 저장 완료: {filename}")
            return filename
        except Exception as e:
            # Excel 저장 실패시 CSV로 저장
            csv_filename = filename.replace('.xlsx', '.csv')
            df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
            print(f"✅ CSV 파일로 저장 완료: {csv_filename}")
            return csv_filename
    
    def close(self):
        """드라이버 종료"""
        if self.driver:
            self.driver.quit()
            print("🔒 브라우저 종료")


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("🕷️  웹사이트 컴포넌트 크롤러")
    print("=" * 60)
    print()
    
    # URL 입력
    url = input("크롤링할 URL을 입력하세요: ").strip()
    
    if not url:
        print("❌ URL이 입력되지 않았습니다.")
        return
    
    # http/https 프로토콜 체크
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    print()
    print(f"🎯 대상 URL: {url}")
    print()
    
    # 크롤러 실행
    crawler = ComponentCrawler(headless=True)
    
    try:
        # div 크롤링
        results = crawler.crawl_divs(url)
        
        if results:
            # 엑셀 저장
            filename = crawler.save_to_excel(results, url)
            
            if filename:
                print()
                print("=" * 60)
                print(f"🎉 크롤링 완료!")
                print(f"📁 저장 파일: {filename}")
                print(f"📊 총 {len(results)}개의 컴포넌트 클래스 추출")
                print("=" * 60)
        else:
            print("⚠️  추출된 데이터가 없습니다.")
    
    except KeyboardInterrupt:
        print("\n⚠️  사용자에 의해 중단되었습니다.")
    
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
    
    finally:
        crawler.close()


if __name__ == "__main__":
    main()
