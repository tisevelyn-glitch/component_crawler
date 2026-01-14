# 🕷️ 웹사이트 컴포넌트 크롤러

웹사이트의 div 요소 class 명을 추출하여 엑셀 파일로 저장하는 Python 프로그램입니다.

## 📋 기능

- ✅ 특정 URL의 모든 div 요소 크롤링
- ✅ div class 명 자동 추출
- ✅ 주요 컴포넌트 클래스명 파싱
- ✅ 엑셀 파일(.xlsx) 또는 CSV 파일로 자동 저장
- ✅ 중복 class 자동 제거
- ✅ 타임스탬프가 포함된 파일명 자동 생성

## 🚀 설치 방법

### 1. Python 설치
Python 3.8 이상이 필요합니다.

### 2. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

또는 개별 설치:

```bash
pip install selenium pandas openpyxl webdriver-manager
```

## 💻 사용 방법

### 기본 실행

```bash
python component_crawler.py
```

프로그램 실행 후 크롤링할 URL을 입력하세요:

```
크롤링할 URL을 입력하세요: https://www.samsung.com/uk/
```

### Python 코드에서 직접 사용

```python
from component_crawler import ComponentCrawler

# 크롤러 생성
crawler = ComponentCrawler(headless=True)

# div 크롤링
results = crawler.crawl_divs("https://www.example.com")

# 엑셀 저장
crawler.save_to_excel(results, "https://www.example.com")

# 종료
crawler.close()
```

## 📊 출력 파일 형식

생성되는 엑셀 파일은 다음 컬럼을 포함합니다:

| 번호 | URL | 주요 컴포넌트 클래스 | 전체 클래스 목록 |
|------|-----|---------------------|-----------------|
| 1 | https://... | hd08-hero-kv-home | hd08-hero-kv-home, bg-black, ... |
| 2 | https://... | co76-feature-kv | co76-feature-kv, bg-white, ... |

### 파일명 형식

```
[도메인]_components_[날짜]_[시간].xlsx
```

예: `samsung_com_components_20260114_143025.xlsx`

## ⚙️ 주요 기능 설명

### 1. 컴포넌트 이름 추출 규칙

프로그램은 다음 우선순위로 주요 컴포넌트 클래스를 추출합니다:

1. BEM 패턴 (예: `hd08-hero-kv-home`)
2. 일반 하이픈 패턴 (예: `feature-card`)
3. 첫 번째 클래스명

### 2. 중복 제거

동일한 class 조합을 가진 div는 한 번만 기록됩니다.

### 3. 동적 콘텐츠 지원

Selenium을 사용하여 JavaScript로 렌더링되는 동적 웹사이트도 크롤링 가능합니다.

## 🔧 커스터마이징

### headless 모드 변경

브라우저를 실제로 보면서 크롤링하려면:

```python
crawler = ComponentCrawler(headless=False)
```

### 대기 시간 조정

`component_crawler.py`의 `crawl_divs` 메서드에서:

```python
time.sleep(3)  # 이 값을 조정하여 페이지 로딩 대기 시간 변경
```

### section 또는 다른 태그 크롤링

`crawl_divs` 메서드를 복사하여 다음 부분을 수정:

```python
# div 대신 section 크롤링
divs = self.driver.find_elements(By.TAG_NAME, "section")
```

## 🛠️ 문제 해결

### Chrome 드라이버 오류

자동으로 최신 Chrome 드라이버를 다운로드합니다. Chrome 브라우저가 설치되어 있어야 합니다.

### 엑셀 파일 저장 실패

openpyxl 설치 실패 시 자동으로 CSV 파일로 저장됩니다.

### 페이지 로딩이 느린 경우

`time.sleep(3)` 값을 늘려보세요 (예: `time.sleep(5)`).

## 📝 예제

### Samsung UK 사이트 크롤링

```bash
python component_crawler.py
# 입력: https://www.samsung.com/uk/
```

### Apple 사이트 크롤링

```bash
python component_crawler.py
# 입력: https://www.apple.com
```

## ⚠️ 주의사항

- 웹사이트의 이용 약관과 robots.txt를 확인하세요
- 과도한 크롤링은 서버에 부담을 줄 수 있습니다
- 개인정보나 저작권이 있는 콘텐츠 수집에 주의하세요

## 📄 라이선스

MIT License

## 👨‍💻 개발자

Created for AUX Component Analysis Project
