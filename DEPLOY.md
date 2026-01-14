# 🚀 배포 가이드

## 방법 1: Streamlit Cloud (추천 ⭐)

Streamlit 앱을 배포하는 가장 쉬운 방법입니다.

### 단계:

1. **GitHub에 코드 푸시**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

2. **Streamlit Cloud 접속**
   - https://streamlit.io/cloud 접속
   - GitHub 계정으로 로그인

3. **앱 배포**
   - "New app" 클릭
   - Repository 선택
   - Branch: `main`
   - Main file: `app.py`
   - "Deploy" 클릭

4. **완료!**
   - 자동으로 URL 생성 (예: `https://your-app.streamlit.app`)

---

## 방법 2: Vercel 배포

⚠️ **주의**: Streamlit은 서버리스 환경에 최적화되지 않아 Vercel에서는 제한적입니다.

### 단계:

1. **Vercel CLI 설치**
   ```bash
   npm i -g vercel
   ```

2. **Vercel 로그인**
   ```bash
   vercel login
   ```

3. **프로젝트 배포**
   ```bash
   vercel
   ```

4. **프로덕션 배포**
   ```bash
   vercel --prod
   ```

### 문제점:
- Streamlit은 장시간 실행되는 서버가 필요
- Vercel의 Serverless Functions는 10초 제한
- Selenium 크롤링은 더 오래 걸릴 수 있음

---

## 방법 3: Railway (추천 대안 🚂)

Python 앱에 최적화된 플랫폼입니다.

### 단계:

1. **Railway 계정 생성**
   - https://railway.app 접속
   - GitHub로 로그인

2. **프로젝트 생성**
   - "New Project" 클릭
   - "Deploy from GitHub repo" 선택
   - Repository 선택

3. **설정**
   - Start Command: `streamlit run app.py --server.port $PORT`
   - Environment Variables: 필요시 추가

4. **배포 완료!**

---

## 방법 4: Render

무료 티어가 있는 좋은 대안입니다.

### 단계:

1. **Render 계정 생성**
   - https://render.com 접속

2. **New Web Service**
   - GitHub repo 연결
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

3. **배포 완료!**

---

## 환경 변수 설정 (필요시)

모든 플랫폼에서 공통:

```bash
# .env 파일 생성
CHROME_DRIVER_PATH=/path/to/chromedriver
HEADLESS=true
```

---

## 추천 순서

1. ⭐ **Streamlit Cloud** - 가장 쉬움, 무료, Streamlit 공식
2. 🚂 **Railway** - Python 앱에 최적화, 무료 티어
3. 🌐 **Render** - 무료 티어, 안정적
4. ⚡ **Vercel** - 제한적이지만 가능
