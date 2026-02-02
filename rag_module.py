import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 환경 변수 로드
load_dotenv()

def create_report_rag_chain(
    pdf_path, 
    report_type="업무 보고서",
    chunk_size=500, 
    chunk_overlap=100, 
    top_k=3,
    temperature=0.0
):
    """
    World Vision 보고서 생성 특화 RAG 체인 생성
    
    Args:
        pdf_path: PDF 파일 경로
        report_type: 보고서 유형 (업무 보고서, 회의록 요약 등)
        chunk_size: 문서 분할 크기
        chunk_overlap: 청크 간 중복 크기
        top_k: 검색할 관련 문서 수
        temperature: LLM 창의성 (0=정확, 1=창의적)
    
    Returns:
        RAG Chain 객체
    """
    
    print(f"[RAG 초기화] 보고서 유형: {report_type}")
    print(f"[설정] chunk_size={chunk_size}, overlap={chunk_overlap}, k={top_k}, temp={temperature}")
    
    # =====================================
    # [1단계] 문서 로드 (Document Load)
    # =====================================
    loader = PyMuPDFLoader(pdf_path)
    docs = loader.load()
    print(f"[1단계 완료] 문서 로드: {len(docs)}페이지")
    
    # =====================================
    # [2단계] 문서 분할 (Text Split)
    # =====================================
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]  # 한국어 고려 구분자
    )
    split_documents = text_splitter.split_documents(docs)
    print(f"[2단계 완료] 청크 분할: {len(split_documents)}개 청크")
    
    # =====================================
    # [3~4단계] 임베딩 및 벡터 DB 저장
    # =====================================
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")  # 최신 임베딩 모델
    vectorstore = FAISS.from_documents(documents=split_documents, embedding=embeddings)
    print(f"[3-4단계 완료] 벡터 DB 생성")
    
    # =====================================
    # [5단계] 검색기 (Retriever) 생성
    # =====================================
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": top_k}
    )
    print(f"[5단계 완료] 검색기 생성 (k={top_k})")
    
    # =====================================
    # [6단계] 프롬프트 템플릿 설정
    # 프롬프트 엔지니어링 기법 적용:
    # - 역할 지정 기법 (Role Playing)
    # - 형식 지정 기법 (Format Specification)
    # - Chain of Thought 유도
    # =====================================
    
    # 보고서 유형별 프롬프트 커스터마이징
    role_description = {
        "업무 보고서": "World Vision의 업무 보고서 작성 전문가",
        "회의록 요약": "효율적인 회의록 요약 전문가",
        "프로젝트 현황": "프로젝트 관리 및 현황 분석 전문가",
        "데이터 분석 보고서": "데이터 기반 인사이트 도출 전문가"
    }
    
    template = f"""# 당신의 역할
당신은 {role_description.get(report_type, 'World Vision의 보고서 작성 전문가')}입니다.
주어진 문서를 기반으로 정확하고 구조화된 답변을 제공해야 합니다.

# 제약조건
- 제공된 문서(Context)의 내용만을 기반으로 답변하세요
- 추측이나 외부 지식을 사용하지 마세요
- 답변은 한국어로 작성하세요
- 비즈니스 관점에서 핵심을 간결하게 전달하세요
- 전문적이고 공식적인 어조를 유지하세요

# 문서 내용 (Context)
{{context}}

# 질문 (Question)
{{question}}

# 답변 작성 지침
1. 먼저 질문의 핵심을 파악하세요
2. 문서에서 관련 정보를 찾으세요
3. 정보를 논리적으로 구조화하세요
4. 간결하고 명확하게 답변하세요

# 한국어 답변:"""

    prompt = ChatPromptTemplate.from_template(template)
    print(f"[6단계 완료] 프롬프트 생성 ({report_type} 특화)")
    
    # =====================================
    # [7단계] LLM 설정
    # =====================================
    llm = ChatOpenAI(
        model_name="gpt-4o",  # 최신 GPT-4o 모델
        temperature=temperature,
        max_tokens=2000  # 충분한 보고서 생성을 위한 토큰
    )
    print(f"[7단계 완료] LLM 설정 (GPT-4o, temp={temperature})")
    
    # =====================================
    # [8단계] RAG 체인 생성
    # =====================================
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    print(f"[8단계 완료] RAG 체인 생성 완료")
    
    return rag_chain


def create_advanced_report_prompt(report_type, additional_instructions=""):
    """
    고급 보고서 생성 프롬프트 템플릿
    
    Args:
        report_type: 보고서 유형
        additional_instructions: 추가 지시사항
    
    Returns:
        프롬프트 문자열
    """
    
    base_prompt = f"""
# 명령문
당신은 World Vision의 {report_type} 작성 전문가입니다.
업로드된 문서를 철저히 분석하여 구조화된 보고서를 작성해주세요.

# 제약조건
- 문서의 내용만을 기반으로 작성하세요
- 비즈니스 임팩트 중심으로 서술하세요
- 데이터나 수치가 있다면 반드시 포함하세요
- 전문적이고 객관적인 어조를 유지하세요
- 불필요한 수식어는 제거하고 간결하게 작성하세요

{additional_instructions}

# 입력문
업로드된 문서의 전체 내용을 기반으로 {report_type}를 작성하시오.

# 출력형식
"""
    
    # 보고서 유형별 출력 형식
    format_templates = {
        "업무 보고서": """
## 업무 보고서

### 1. 개요
- [주요 목적 및 배경]

### 2. 추진 내용
- [주요 활동 1]: [상세 내용]
- [주요 활동 2]: [상세 내용]
- [주요 활동 3]: [상세 내용]

### 3. 주요 성과
- [정량적 성과]: [구체적 수치]
- [정성적 성과]: [핵심 성과]

### 4. 이슈 및 대응 방안
- [이슈 1]: [대응 방안]
- [이슈 2]: [대응 방안]

### 5. 향후 계획
- [단기 계획]
- [중장기 계획]
""",
        
        "회의록 요약": """
## 회의록 요약

### 📋 회의 정보
- 회의명: [회의 제목]
- 일시: [날짜/시간]
- 참석자: [주요 참석자]

### 💬 주요 논의 사항
1. [논의 주제 1]
   - 핵심 내용: [요약]
   - 결정 사항: [결론]

2. [논의 주제 2]
   - 핵심 내용: [요약]
   - 결정 사항: [결론]

### ✅ 액션 아이템
- [ ] [담당자]: [업무 내용] (마감: [날짜])
- [ ] [담당자]: [업무 내용] (마감: [날짜])

### 📌 차기 회의 안건
- [다음 회의에서 다룰 주제]
""",
        
        "프로젝트 현황": """
## 프로젝트 현황 보고서

### 📊 프로젝트 개요
- 프로젝트명: [이름]
- 기간: [시작일 ~ 종료일]
- 진행률: [X%]

### 🎯 주요 마일스톤
| 마일스톤 | 계획일 | 완료일 | 상태 |
|---------|--------|--------|------|
| [항목1] | [날짜] | [날짜] | ✅/🔄/⏸️ |
| [항목2] | [날짜] | [날짜] | ✅/🔄/⏸️ |

### 💡 주요 성과
- [성과 1]: [상세 설명]
- [성과 2]: [상세 설명]

### ⚠️ 리스크 및 이슈
- [리스크 1]: [대응 방안]
- [리스크 2]: [대응 방안]

### 📅 향후 일정
- [주요 일정 1]
- [주요 일정 2]
""",
        
        "데이터 분석 보고서": """
## 데이터 분석 보고서

### 📈 분석 개요
- 분석 목적: [목적]
- 분석 기간: [기간]
- 데이터 소스: [출처]

### 🔍 주요 발견 사항
1. **[인사이트 1]**
   - 데이터: [구체적 수치]
   - 해석: [의미]
   
2. **[인사이트 2]**
   - 데이터: [구체적 수치]
   - 해석: [의미]

### 💡 비즈니스 시사점
- [시사점 1]: [상세 설명]
- [시사점 2]: [상세 설명]

### 📋 권장 사항
1. [권장 액션 1]
2. [권장 액션 2]
3. [권장 액션 3]

### 📊 추가 분석 필요 영역
- [향후 분석 주제]
"""
    }
    
    output_format = format_templates.get(report_type, format_templates["업무 보고서"])
    
    return base_prompt + output_format


# 테스트용 함수
if __name__ == "__main__":
    print("RAG Module for World Vision Report Agent")
    print("=" * 50)
    
    # 프롬프트 테스트
    test_prompt = create_advanced_report_prompt("업무 보고서")
    print(test_prompt)
