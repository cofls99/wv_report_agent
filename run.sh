#!/bin/bash

echo "============================================"
echo "World Vision 보고서 생성 AI 에이전트"
echo "============================================"
echo ""

# 가상환경 활성화
echo "[1/3] 가상환경 활성화 중..."
source venv/bin/activate

# 패키지 확인
echo ""
echo "[2/3] 패키지 확인 중..."
python -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "패키지가 설치되지 않았습니다. 설치를 시작합니다..."
    pip install -r requirements.txt
fi

# Streamlit 실행
echo ""
echo "[3/3] 애플리케이션 실행 중..."
echo "브라우저가 자동으로 열립니다."
echo "종료하려면 Ctrl+C를 누르세요."
echo ""
streamlit run app.py
