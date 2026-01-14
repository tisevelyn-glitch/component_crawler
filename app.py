#!/usr/bin/env python3
"""
웹사이트 컴포넌트 크롤러 - 웹 인터페이스
Streamlit 기반 웹 애플리케이션
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from urllib.parse import urlparse
import io
from component_crawler import ComponentCrawler

# 페이지 설정
st.set_page_config(
    page_title="웹사이트 컴포넌트 크롤러",
    page_icon="🕷️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #e8f4f8;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border: 2px solid #1f77b4;
        color: #1a1a1a;
    }
    .info-box h3 {
        color: #0d5a8f;
        margin-top: 0;
    }
    .info-box p {
        color: #2c2c2c;
        line-height: 1.6;
    }
    .info-box ul {
        color: #2c2c2c;
    }
    .info-box li {
        color: #2c2c2c;
        margin: 0.5rem 0;
    }
    .info-box strong {
        color: #0d5a8f;
    }
    .info-box code {
        background-color: #d4e9f7;
        color: #c7254e;
        padding: 0.2rem 0.4rem;
        border-radius: 0.3rem;
        font-weight: bold;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        color: #155724;
    }
    .stat-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        border: 1px solid #e0e0e0;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
        line-height: 1.2;
        margin-bottom: 0.5rem;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #4a4a4a;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    /* 메인 영역 배경색 */
    .main .block-container {
        background-color: #f7f7f7 !important;
        padding: 2rem;
    }
    .stApp {
        background-color: #f7f7f7 !important;
    }
    section[data-testid="stAppViewContainer"] {
        background-color: #f7f7f7 !important;
    }
    .main {
        background-color: #f7f7f7 !important;
    }
    /* 헤더 배경색 */
    header[data-testid="stHeader"] {
        background-color: #f7f7f7 !important;
    }
    /* 사이드바 스타일 개선 */
    .css-1d391kg {
        background-color: #ffffff;
    }
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 2px solid #e0e0e0;
    }
    section[data-testid="stSidebar"] p {
        color: #2c2c2c !important;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #1a1a1a !important;
    }
    section[data-testid="stSidebar"] code {
        background-color: #f5f5f5;
        color: #d63384;
        padding: 0.2rem 0.4rem;
        border-radius: 0.3rem;
        font-weight: 600;
    }
    section[data-testid="stSidebar"] .stCheckbox label {
        color: #2c2c2c !important;
        font-weight: 500;
    }
    /* 구분선 스타일 */
    section[data-testid="stSidebar"] hr {
        border-top: 2px solid #dee2e6;
        margin: 1.5rem 0;
    }
    /* 메인 영역 텍스트 스타일 */
    .stApp p, .stApp span, .stApp div {
        color: #2c2c2c;
    }
    /* 입력 필드 레이블 */
    .stTextInput label {
        color: #2c2c2c !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
    }
    /* 마크다운 텍스트 */
    .stMarkdown p {
        color: #2c2c2c !important;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #1a1a1a !important;
    }
    /* 버튼 텍스트 개선 */
    .stButton button {
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# 메인 헤더
st.markdown('<div class="main-header">🕷️ 웹사이트 컴포넌트 크롤러</div>', unsafe_allow_html=True)

# 사이드바
with st.sidebar:
    st.markdown("""
    <h2 style="color: #1f77b4; border-bottom: 3px solid #1f77b4; padding-bottom: 0.5rem;">
        ⚙️ 설정
    </h2>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <h3 style="color: #2c2c2c; margin-top: 1.5rem; margin-bottom: 0.5rem;">
        📋 크롤링 옵션
    </h3>
    """, unsafe_allow_html=True)
    headless_mode = st.checkbox("🖥️ 백그라운드 모드", value=True, help="브라우저를 보이지 않게 실행")
    
    st.markdown("---")
    
    st.markdown("""
    <h3 style="color: #2c2c2c; margin-top: 1rem; margin-bottom: 1rem;">
        📖 사용 방법
    </h3>
    <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 0.5rem; border-left: 3px solid #1f77b4;">
        <p style="color: #2c2c2c; margin: 0.5rem 0; font-size: 0.95rem;">
            <strong style="color: #0d5a8f;">1️⃣ URL 입력:</strong><br>
            <span style="color: #4a4a4a;">크롤링할 웹사이트 주소 입력</span>
        </p>
        <p style="color: #2c2c2c; margin: 0.5rem 0; font-size: 0.95rem;">
            <strong style="color: #0d5a8f;">2️⃣ 크롤링 시작:</strong><br>
            <span style="color: #4a4a4a;">버튼 클릭</span>
        </p>
        <p style="color: #2c2c2c; margin: 0.5rem 0; font-size: 0.95rem;">
            <strong style="color: #0d5a8f;">3️⃣ 결과 확인:</strong><br>
            <span style="color: #4a4a4a;">테이블에서 결과 확인</span>
        </p>
        <p style="color: #2c2c2c; margin: 0.5rem 0; font-size: 0.95rem;">
            <strong style="color: #0d5a8f;">4️⃣ 다운로드:</strong><br>
            <span style="color: #4a4a4a;">엑셀 파일로 저장</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <h3 style="color: #2c2c2c; margin-top: 1rem; margin-bottom: 1rem;">
        🎯 컴포넌트 패턴
    </h3>
    """, unsafe_allow_html=True)
    st.code("AA##- 또는 AAA##-", language="text")
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 0.5rem;">
        <p style="color: #2c2c2c; margin: 0.3rem 0; font-size: 0.9rem;">
            <strong style="color: #0d5a8f;">✅ 예시:</strong>
        </p>
        <p style="color: #4a4a4a; margin: 0.3rem 0; margin-left: 1rem; font-size: 0.9rem;">
            🔹 <code style="background-color: #e8f4f8; color: #c7254e; padding: 0.2rem 0.4rem; border-radius: 0.3rem;">hd08-hero-kv-home</code>
        </p>
        <p style="color: #4a4a4a; margin: 0.3rem 0; margin-left: 1rem; font-size: 0.9rem;">
            🔹 <code style="background-color: #e8f4f8; color: #c7254e; padding: 0.2rem 0.4rem; border-radius: 0.3rem;">co76-feature-kv</code>
        </p>
        <p style="color: #4a4a4a; margin: 0.3rem 0; margin-left: 1rem; font-size: 0.9rem;">
            🔹 <code style="background-color: #e8f4f8; color: #c7254e; padding: 0.2rem 0.4rem; border-radius: 0.3rem;">co78-recommended-carousel</code>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <h3 style="color: #2c2c2c; margin-top: 1rem; margin-bottom: 1rem;">
        💡 팁
    </h3>
    <div style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #ffc107;">
        <p style="color: #856404; margin: 0; font-weight: 500; font-size: 0.95rem;">
        💡 <strong>Samsung, LG</strong> 등의 컴포넌트 라이브러리를 분석할 때 유용합니다!
        </p>
    </div>
    """, unsafe_allow_html=True)

# 메인 컨텐츠
st.markdown("""
<p style="color: rgb(13, 90, 143) !important; font-size: 18px; font-weight: 600; margin-bottom: 0.5rem;">
    🔗 크롤링할 URL을 입력하세요
</p>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    url_input = st.text_input(
        "URL",
        placeholder="https://www.example.com",
        help="http:// 또는 https://로 시작하는 전체 URL을 입력해주세요",
        label_visibility="collapsed"
    )

with col2:
    crawl_button = st.button("🚀 크롤링 시작", type="primary", use_container_width=True)

# 세션 스테이트 초기화
if 'results' not in st.session_state:
    st.session_state.results = None
if 'url' not in st.session_state:
    st.session_state.url = None
if 'crawl_time' not in st.session_state:
    st.session_state.crawl_time = None

# 크롤링 실행
if crawl_button:
    if not url_input:
        st.error("❌ URL을 입력해주세요!")
    else:
        # URL 검증 및 보정
        url = url_input.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        st.session_state.url = url
        
        # 진행 상황 표시
        with st.spinner('🔍 크롤링 중... 잠시만 기다려주세요.'):
            try:
                # 크롤러 실행
                crawler = ComponentCrawler(headless=headless_mode)
                
                # 진행 단계 표시
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("🌐 페이지 로딩 중...")
                progress_bar.progress(25)
                
                # 크롤링 실행
                results = crawler.crawl_divs(url)
                
                status_text.text("📊 데이터 추출 중...")
                progress_bar.progress(75)
                
                # 크롤러 종료
                crawler.close()
                
                status_text.text("✅ 완료!")
                progress_bar.progress(100)
                
                # 결과 저장
                if results:
                    st.session_state.results = pd.DataFrame(results)
                    st.session_state.crawl_time = datetime.now()
                    st.success(f"✅ 크롤링 완료! 총 {len(results)}개의 컴포넌트를 발견했습니다.")
                else:
                    st.warning("⚠️ 컴포넌트 패턴에 맞는 결과를 찾지 못했습니다.")
                    st.session_state.results = None
                
            except Exception as e:
                st.error(f"❌ 오류 발생: {str(e)}")
                st.session_state.results = None
            
            finally:
                # 진행 상황 표시 제거
                progress_bar.empty()
                status_text.empty()

# 결과 표시
if st.session_state.results is not None:
    df = st.session_state.results
    
    st.markdown("---")
    
    # 통계 정보
    st.markdown("""
    <h2 style="color: #1a1a1a !important; border-bottom: 3px solid #1f77b4; padding-bottom: 0.5rem; margin-top: 2rem; font-weight: 700; background-color: transparent;">
        📊 크롤링 결과
    </h2>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{len(df)}</div>
            <div class="stat-label">총 컴포넌트</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        site_code = df['Site Code'].iloc[0] if 'Site Code' in df.columns and len(df) > 0 else "N/A"
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{site_code}</div>
            <div class="stat-label">Site Code</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        page_type = df['Page Type'].iloc[0] if 'Page Type' in df.columns and len(df) > 0 else "N/A"
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{page_type}</div>
            <div class="stat-label">Page Type</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        if st.session_state.crawl_time:
            time_str = st.session_state.crawl_time.strftime('%H:%M:%S')
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value" style="font-size: 1.5rem;">{time_str}</div>
                <div class="stat-label">크롤링 시간</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="stat-card">
                <div class="stat-value" style="font-size: 1.5rem;">--:--:--</div>
                <div class="stat-label">크롤링 시간</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 컴포넌트 분류별 개수
    st.markdown("""
    <h3 style="color: #1a1a1a !important; margin-top: 2rem; margin-bottom: 1rem; font-weight: 700; background-color: transparent;">
        📈 컴포넌트별 통계
    </h3>
    """, unsafe_allow_html=True)
    
    # 컴포넌트명별 집계 (이미 그룹화되어 있음)
    component_counts = df[['컴포넌트명', 'Display']].copy()
    component_counts['클래스 개수'] = df['전체 클래스 목록'].apply(lambda x: len(x.split(', ')))
    component_counts = component_counts[['컴포넌트명', '클래스 개수', 'Display']]
    component_counts.columns = ['컴포넌트명', '클래스 개수', 'Display 현황']
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.dataframe(
            component_counts,
            hide_index=True,
            use_container_width=True,
            height=300
        )
    
    with col2:
        st.bar_chart(
            component_counts.set_index('컴포넌트명')['클래스 개수'],
            use_container_width=True,
            height=300
        )
    
    # 결과 테이블
    st.markdown("""
    <h3 style="color: #1a1a1a !important; margin-top: 2rem; margin-bottom: 1rem; font-weight: 700; background-color: transparent;">
        📋 전체 컴포넌트 목록
    </h3>
    """, unsafe_allow_html=True)
    
    # 검색 기능
    st.markdown("""
    <p style="color: #1a1a1a !important; font-size: 1rem; font-weight: 600; margin-bottom: 0.5rem; background-color: transparent;">
        🔍 컴포넌트 검색
    </p>
    """, unsafe_allow_html=True)
    search_term = st.text_input(
        "검색",
        placeholder="검색어 입력...",
        label_visibility="collapsed"
    )
    
    if search_term:
        filtered_df = df[
            df['컴포넌트명'].str.contains(search_term, case=False, na=False) | 
            df['전체 클래스 목록'].str.contains(search_term, case=False, na=False)
        ]
        st.markdown(f"""
        <div style="background-color: #d1ecf1; padding: 0.8rem; border-radius: 0.5rem; border-left: 4px solid #0c5460; margin-bottom: 1rem;">
            <p style="color: #0c5460; margin: 0; font-weight: 500;">
            🔍 검색 결과: {len(filtered_df)}개 컴포넌트
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        filtered_df = df
    
    # 데이터프레임 표시
    st.dataframe(
        filtered_df,
        hide_index=True,
        use_container_width=True,
        height=400,
        column_config={
            "Display": st.column_config.TextColumn(
                "Display",
                width="small",
            )
        }
    )
    
    # 다운로드 버튼
    st.markdown("""
    <h3 style="color: #1a1a1a !important; margin-top: 2rem; margin-bottom: 1rem; font-weight: 700; background-color: transparent;">
        💾 다운로드
    </h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 엑셀 다운로드
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            filtered_df.to_excel(writer, index=False, sheet_name='Components')
        
        domain = urlparse(st.session_state.url).netloc.replace('www.', '').replace('.', '_')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{domain}_components_{timestamp}.xlsx"
        
        st.download_button(
            label="📥 엑셀 다운로드 (.xlsx)",
            data=output.getvalue(),
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    with col2:
        # CSV 다운로드
        csv = filtered_df.to_csv(index=False, encoding='utf-8-sig')
        csv_filename = filename.replace('.xlsx', '.csv')
        
        st.download_button(
            label="📥 CSV 다운로드 (.csv)",
            data=csv,
            file_name=csv_filename,
            mime="text/csv",
            use_container_width=True
        )

else:
    # 초기 화면
    st.markdown("---")
    st.markdown("""
    <div class="info-box">
        <h3>👋 환영합니다!</h3>
        <p>이 도구는 웹사이트의 <strong>div 요소</strong>에서 특정 패턴(<code>AA##-</code> 또는 <code>AAA##-</code>)을 따르는 
        <strong>컴포넌트 클래스</strong>를 자동으로 추출합니다.</p>
        <br>
        <p>🎯 <strong>주요 기능:</strong></p>
        <ul>
            <li>✅ JavaScript 렌더링 페이지 지원 (Selenium 사용)</li>
            <li>✅ 컴포넌트 패턴 자동 인식 및 필터링</li>
            <li>✅ 실시간 통계 및 시각화</li>
            <li>✅ 엑셀/CSV 파일 다운로드</li>
            <li>✅ 컴포넌트 검색 기능</li>
        </ul>
        <br>
        <p>💡 <strong>시작하기:</strong> 위의 URL 입력 필드에 크롤링할 웹사이트 주소를 입력하고 <strong>크롤링 시작</strong> 버튼을 클릭하세요!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 예시 이미지 또는 데모
    st.markdown("""
    <p style="color: rgb(13, 90, 143) !important; font-size: 18px; font-weight: 600; margin-top: 2rem; margin-bottom: 1rem; background-color: transparent;">
        📸 예시 결과
    </p>
    """, unsafe_allow_html=True)
    
    example_data = {
        '번호': [1, 2, 3, 4, 5],
        'Site Code': ['UK'] * 5,
        'Page Type': ['Home'] * 5,
        'URL': ['https://www.samsung.com/uk/'] * 5,
        '컴포넌트명': [
            'hd08-hero-kv-home',
            'co76-feature-kv',
            'co73-feature-cards',
            'co78-recommended-product-carousel',
            'nv16-country-selector'
        ],
        '전체 클래스 목록': [
            'hd08-hero-kv-home',
            'co76-feature-kv',
            'co73-feature-cards',
            'co78-recommended-product-carousel',
            'nv16-country-selector__content-wrap, nv16-country-selector__content, nv16-country-selector__menu'
        ],
        'Display': ['Y:1 / N:0', 'Y:1 / N:0', 'Y:1 / N:0', 'Y:1 / N:0', 'Y:2 / N:1']
    }
    
    st.dataframe(
        pd.DataFrame(example_data),
        hide_index=True,
        use_container_width=True
    )

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #4a4a4a; padding: 2rem 0;">
    <p style="font-size: 0.95rem; font-weight: 500;">Made with ❤️ for AUX Component Analysis | Powered by Selenium & Streamlit</p>
</div>
""", unsafe_allow_html=True)
