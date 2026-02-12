# ⚡ AWS 배포 퀵스타트 (5단계)

RIN님이 가장 빠르게 AWS에 배포하는 방법입니다!

---

## 🎯 선택: GitHub 방식 (가장 간단) ⭐ 추천

### 준비물
- [ ] AWS 계정
- [ ] GitHub 계정
- [ ] OpenAI API Key

### 소요 시간: 약 30분

---

## 📋 Step 1: GitHub 리포지토리 생성 (5분)

### 1-1. GitHub에 새 리포지토리 생성
```
https://github.com/new

Repository name: wv-report-agent-v2
Description: World Vision AI Report Generator
Public 또는 Private 선택
```

### 1-2. 코드 업로드
```bash
# 프로젝트 폴더에서
cd wv_report_agent_v2

git init
git add .
git commit -m "Initial commit - v2.0"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/wv-report-agent-v2.git
git push -u origin main
```

---

## 🔐 Step 2: AWS 계정 준비 (10분)

### 2-1. AWS 가입
```
https://aws.amazon.com/
→ "Create an AWS Account" 클릭
→ 이메일, 비밀번호 입력
→ 결제 정보 입력 (프리티어 대부분 무료)
→ 본인 확인
```

### 2-2. AWS Console 접속
```
https://console.aws.amazon.com/
→ 로그인
```

---

## 🚀 Step 3: App Runner 서비스 생성 (10분)

### 3-1. App Runner 서비스 페이지 이동
```
https://console.aws.amazon.com/apprunner/
→ "Create service" 클릭
```

### 3-2. Source 설정
```
Repository type: Source code repository
Provider: GitHub
→ "Add new" 클릭
→ GitHub 로그인 및 권한 허용
→ 리포지토리 선택: wv-report-agent-v2
→ Branch: main
→ Deployment trigger: Automatic (또는 Manual)
```

### 3-3. Build 설정
```
Configuration file: Configure all settings here (기본값)

Runtime: Python 3
Build command: pip install -r requirements.txt
Start command: streamlit run app.py --server.port=8501 --server.address=0.0.0.0
Port: 8501
```

### 3-4. Service 설정
```
Service name: wv-report-agent
CPU: 1 vCPU
Memory: 2 GB
```

### 3-5. 환경 변수 설정 ⚠️ 중요!
```
Environment variables:
  Key: OPENAI_API_KEY
  Value: sk-proj-여기에-실제-API-키-입력
```

### 3-6. 배포 시작
```
→ "Create & deploy" 클릭
→ 3-5분 대기
```

---

## ✅ Step 4: URL 확인 및 테스트 (3분)

### 4-1. 배포 완료 확인
```
Status: Running (초록색)
```

### 4-2. URL 복사
```
예시: https://abc123xyz.us-east-1.awsapprunner.com
```

### 4-3. 브라우저에서 접속
```
→ URL 접속
→ PDF 업로드 테스트
→ 질문/보고서 생성 테스트
```

---

## 📝 Step 5: 과제 제출 (2분)

### 5-1. 제출 내용
```
1. 코드: 2주차_프로토타입_ver2_RIN.zip (이미 준비됨)
2. 배포 URL: https://abc123xyz.us-east-1.awsapprunner.com
```

### 5-2. URL 제출 형식
```
AWS 주소: https://wv-report-agent-abc123.us-east-1.awsapprunner.com
```

---

## 💰 비용 안내

### 프리티어 (12개월)
- App Runner: **월 300시간 무료**
- 테스트용으로 충분!

### 예상 비용
- 24시간 운영 시: 월 $50-70
- 테스트만 (하루 2시간): **거의 무료**

### 💡 비용 절감 팁
```
1. 과제 제출 후 서비스 일시 중지
2. 필요할 때만 재시작
3. Auto scaling 최소값으로 설정
```

---

## 🐛 트러블슈팅

### "Build failed" 오류
```
해결:
1. requirements.txt 확인
2. Build command 확인:
   pip install -r requirements.txt
```

### "502 Bad Gateway" 오류
```
해결:
1. Start command 확인:
   streamlit run app.py --server.port=8501 --server.address=0.0.0.0
2. Port: 8501 확인
3. 메모리를 3GB로 증가
```

### 환경 변수 오류
```
해결:
1. AWS Console → App Runner → Service
2. Configuration → Edit
3. Environment variables 확인:
   OPENAI_API_KEY=sk-proj-...
```

### GitHub 연결 오류
```
해결:
1. GitHub 권한 재확인
2. 리포지토리가 Public인지 확인
3. Branch 이름 확인 (main)
```

---

## 📊 배포 체크리스트

- [ ] AWS 계정 생성 완료
- [ ] GitHub 리포지토리 생성 완료
- [ ] 코드 푸시 완료
- [ ] App Runner 서비스 생성 완료
- [ ] 환경 변수 (OPENAI_API_KEY) 설정 완료
- [ ] 배포 상태 "Running" 확인
- [ ] URL 접속 테스트 완료
- [ ] PDF 업로드 테스트 완료
- [ ] 질문/답변 테스트 완료
- [ ] 보고서 생성 테스트 완료

---

## 🎓 다음 단계

### 배포 완료 후
1. URL을 과제 제출 양식에 입력
2. 스크린샷 캡처 (선택)
3. 제출 완료!

### 서비스 관리
```
AWS Console → App Runner → wv-report-agent

→ "Pause service" (일시 중지)
→ "Resume service" (재시작)
→ "Delete service" (삭제)
```

---

## 🆘 도움이 필요하면?

### AWS 공식 문서
```
https://docs.aws.amazon.com/apprunner/
```

### 카카오톡 오픈채팅방
```
멘토님께 질문하기!
```

---

**작성일**: 2026.01.26  
**예상 소요 시간**: 30분  
**난이도**: ⭐⭐☆☆☆

**화이팅입니다!** 🚀
