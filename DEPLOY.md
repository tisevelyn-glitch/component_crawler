# 🚀 Streamlit Cloud 배포 가이드

Streamlit Cloud는 Streamlit 앱을 배포하는 가장 쉬운 방법입니다.

## 📋 배포 단계

### 1단계: GitHub에 코드 푸시

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2단계: Streamlit Cloud 접속

1. **Streamlit Cloud 접속**
   - https://streamlit.io/cloud 접속
   - GitHub 계정으로 로그인

2. **앱 배포**
   - "New app" 클릭
   - Repository 선택
   - Branch: `main`
   - Main file: `app.py`
   - "Deploy" 클릭

### 3단계: 완료!

- 자동으로 URL 생성 (예: `https://your-app.streamlit.app`)
- GitHub에 push할 때마다 자동 재배포

---

## ⚙️ 설정

### Python 버전
- Streamlit Cloud는 자동으로 Python 버전 감지
- `requirements.txt`에서 패키지 자동 설치

### 환경 변수 (필요시)
- Streamlit Cloud Dashboard → Settings → Secrets
- 환경 변수 추가 가능

---

## 🔄 재배포

GitHub에 push하면 자동으로 재배포됩니다:

```bash
git add .
git commit -m "Update"
git push
```

---

## 📊 배포 상태 확인

- Streamlit Cloud Dashboard에서 확인
- Logs 탭에서 실시간 로그 확인
- 배포 상태: Deploying → Live

---

## 💡 팁

- 무료 플랜 제공
- 자동 HTTPS 설정
- GitHub 연동으로 자동 배포
- 실시간 로그 확인 가능
