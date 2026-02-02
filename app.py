import streamlit as st
import os
from rag_module import create_report_rag_chain

# 페이지 설정
st.set_page_config(
    page_title="World Vision 보고서 생성 에이전트",
    page_icon="📊",
    layout="wide"
)

# 헤더
st.title("📊 World Vision AI 보고서 생성 에이전트")
st.markdown("""
> **80% 업무시간 단축을 위한 AI 자동화 솔루션**  
> 회의록, 프로젝트 문서를 업로드하면 구조화된 보고서를 자동으로 생성합니다.
""")

# 사이드바 설정
with st.sidebar:
    st.header("⚙️ 설정")
    
    # 파일 업로드
    uploaded_file = st.file_uploader(
        "📄 문서 업로드 (PDF)", 
        type=['pdf'],
        help="회의록, 프로젝트 문서, 데이터 보고서 등을 업로드하세요"
    )
    
    st.divider()
    
    # 보고서 유형 선택
    report_type = st.selectbox(
        "📋 보고서 유형",
        ["업무 보고서", "회의록 요약", "프로젝트 현황", "데이터 분석 보고서"],
        help="생성할 보고서 유형을 선택하세요"
    )
    
    # 고급 설정 (접이식)
    with st.expander("🔧 고급 설정"):
        chunk_size = st.slider("Chunk Size", 200, 1000, 500, 50)
        chunk_overlap = st.slider("Chunk Overlap", 0, 200, 100, 20)
        top_k = st.slider("검색 문서 수 (k)", 1, 10, 3, 1)
        temperature = st.slider("창의성 (Temperature)", 0.0, 1.0, 0.0, 0.1)
    
    st.divider()
    st.caption("💡 World Vision AI Platform v1.0")

# 메인 영역
if uploaded_file:
    # 임시 파일 저장
    temp_path = f"temp_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # RAG 체인 초기화 (세션 상태 활용)
    if "rag_chain" not in st.session_state or st.session_state.get("last_settings") != (chunk_size, chunk_overlap, top_k, temperature, report_type):
        with st.spinner("📚 문서 분석 중..."):
            st.session_state.rag_chain = create_report_rag_chain(
                temp_path, 
                report_type=report_type,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                top_k=top_k,
                temperature=temperature
            )
            st.session_state.last_settings = (chunk_size, chunk_overlap, top_k, temperature, report_type)
        st.success("✅ 분석 완료! 이제 질문하거나 보고서 생성을 요청하세요.")
    
    # 탭 구성
    tab1, tab2 = st.tabs(["💬 대화형 질문", "📝 보고서 자동 생성"])
    
    # 탭1: 대화형 질문
    with tab1:
        st.markdown("### 문서에 대해 질문하세요")
        
        # 메시지 이력 초기화
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # 기존 대화 표시
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # 사용자 입력
        if prompt := st.chat_input("질문을 입력하세요 (예: 이 문서의 핵심 내용은?)"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("🤔 답변 생성 중..."):
                    response = st.session_state.rag_chain.invoke(prompt)
                    st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    # 탭2: 보고서 자동 생성
    with tab2:
        st.markdown("### 원클릭 보고서 생성")
        st.info("💡 아래 버튼을 클릭하면 업로드한 문서를 기반으로 구조화된 보고서를 자동 생성합니다.")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            generate_button = st.button("📊 보고서 생성", type="primary", use_container_width=True)
        
        if generate_button:
            with st.spinner("📝 보고서 생성 중... (약 10-20초 소요)"):
                # 보고서 생성 전용 프롬프트
                report_prompt = f"""
# 명령문
당신은 World Vision의 업무 보고서 작성 전문가입니다. 
업로드된 문서를 분석하여 '{report_type}' 형식의 구조화된 보고서를 작성해주세요.

# 제약조건
- 비즈니스 관점에서 핵심 내용을 간결하게 작성
- 전문적이고 공식적인 어조 유지
- 문장은 간결하게 작성하되 핵심 정보는 누락하지 않음
- 다른 문장이나 설명은 출력하지 않음

# 입력문
업로드된 문서의 전체 내용을 분석하여 {report_type}를 작성하시오.

# 출력형식
## [제목]
{report_type} - [문서명 또는 주제]

## 1. 요약
- 핵심 내용 3-5줄 요약

## 2. 주요 내용
- 중요 포인트 1
- 중요 포인트 2  
- 중요 포인트 3
(추가 포인트 자유롭게)

## 3. 액션 아이템 (해당 시)
- [ ] 조치 사항 1
- [ ] 조치 사항 2

## 4. 결론 및 제언
- 종합 의견 및 다음 단계

---
*생성일시: [자동 기입]*
"""
                
                report = st.session_state.rag_chain.invoke(report_prompt)
                
                st.markdown("---")
                st.markdown("### 생성된 보고서")
                st.markdown(report)
                
                # 다운로드 버튼
                st.download_button(
                    label="📥 보고서 다운로드 (TXT)",
                    data=report,
                    file_name=f"WV_Report_{uploaded_file.name.replace('.pdf', '')}.txt",
                    mime="text/plain"
                )

else:
    # 안내 메시지
    st.info("👈 왼쪽 사이드바에서 PDF 파일을 업로드하여 시작하세요.")
    
    # 사용 예시
    with st.expander("📖 사용 가이드"):
        st.markdown("""
        ### 사용 방법
        
        1. **문서 업로드**: 왼쪽 사이드바에서 PDF 파일 업로드
        2. **보고서 유형 선택**: 생성할 보고서 형식 선택
        3. **대화형 질문 또는 자동 생성 선택**:
           - 💬 대화형: 문서에 대해 자유롭게 질문
           - 📝 자동 생성: 원클릭으로 구조화된 보고서 생성
        
        ### 활용 사례
        - ✅ 회의록을 업로드하여 핵심 내용 자동 요약
        - ✅ 프로젝트 문서를 현황 보고서로 변환
        - ✅ 데이터 분석 결과를 경영진 보고서로 정리
        - ✅ 다국어 문서를 한국어 보고서로 번역 및 요약
        
        ### 고급 기능
        - 🔧 Chunk Size: 문서 분할 크기 조정 (작을수록 정밀, 클수록 문맥 유지)
        - 🔧 Overlap: 청크 간 중복 비율 (높을수록 문맥 연결성 향상)
        - 🔧 Top K: 검색할 관련 문서 수 (많을수록 풍부하지만 느림)
        - 🔧 Temperature: AI 창의성 (0=정확, 1=창의적)
        """)
    
    # 데모 영상 또는 스크린샷 공간
    st.markdown("---")
    st.caption("World Vision AI Platform | Powered by GPT-4o & LangChain")
