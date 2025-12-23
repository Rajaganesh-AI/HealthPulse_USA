"""
HealthPulse USA - Multi-Agent US Healthcare Article Generator
Version: 9.0.0 - Logo, Trending Ticker & Article Images
"""

import streamlit as st
import asyncio
import os
import sys
from datetime import datetime
import random

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    get_main_categories, get_subcategories, get_specific_topics,
    build_topic_query, get_search_keywords
)
from agents import HealthcareAgentOrchestrator
from utils import ArticleExporter, get_download_filename

st.set_page_config(page_title="HealthPulse USA", page_icon="🏥", layout="wide", initial_sidebar_state="collapsed")

# Trending healthcare topics (rotates)
TRENDING_TOPICS = [
    "🔥 Medicare 2025 Premium Changes",
    "📈 ACA Enrollment Hits Record High",
    "💊 Drug Price Negotiations Update",
    "🏥 Hospital Staffing Crisis Deepens",
    "🦠 New COVID Variant Monitoring",
    "💰 Healthcare Costs Rising 7.5%",
    "🩺 Telehealth Usage Surges 40%",
    "⚕️ Mental Health Parity Laws Expand",
    "🔬 AI in Diagnostics Breakthrough",
    "📋 Prior Authorization Reform Bill",
    "🌡️ Flu Season Peaks Early",
    "💉 Vaccine Mandate Updates",
    "🏛️ Medicaid Expansion Debates",
    "👴 Senior Care Costs Soar",
    "🧬 Gene Therapy Approvals 2025",
]

# CSS Styles with Logo, Ticker & Image Styles
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@700;800&display=swap');
    
    :root {
        --navy: #1e3a5f;
        --navy-light: #2d5a87;
        --coral: #ff6b6b;
        --green: #10b981;
        --yellow: #f59e0b;
        --gray: #64748b;
        --light: #f8fafc;
    }
    
    * { font-family: 'Inter', sans-serif !important; }
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    .block-container { padding: 0.5rem 1rem !important; max-width: 100% !important; }
    .stApp { background: #eef2f6; }
    
    /* Dropdown fixes */
    .stSelectbox [data-baseweb="select"] span,
    .stSelectbox [data-baseweb="select"] div { font-size: 12px !important; }
    [data-baseweb="menu"] li { font-size: 12px !important; padding: 8px 12px !important; }
    [role="option"] div { font-size: 12px !important; }
    
    /* ============= HEADER WITH LOGO & TICKER ============= */
    .main-header {
        background: linear-gradient(135deg, var(--navy) 0%, var(--navy-light) 100%);
        color: white;
        padding: 10px 20px 8px 20px;
        border-radius: 8px;
        margin-bottom: 12px;
        border-bottom: 3px solid var(--coral);
        overflow: hidden;
    }
    
    .header-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Logo Section */
    .logo-section {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .logo-icon {
        width: 45px;
        height: 45px;
        background: linear-gradient(135deg, var(--coral) 0%, #ff8e8e 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
        position: relative;
    }
    
    .logo-icon::after {
        content: '';
        position: absolute;
        width: 12px;
        height: 12px;
        background: var(--green);
        border-radius: 50%;
        top: -2px;
        right: -2px;
        border: 2px solid var(--navy);
        animation: pulse-dot 2s infinite;
    }
    
    @keyframes pulse-dot {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.2); opacity: 0.8; }
    }
    
    .logo-text {
        display: flex;
        flex-direction: column;
    }
    
    .logo-title {
        font-family: 'Poppins', sans-serif !important;
        font-size: 22px;
        font-weight: 800;
        letter-spacing: -0.5px;
        line-height: 1.1;
    }
    
    .logo-title span {
        color: var(--coral);
    }
    
    .logo-subtitle {
        font-size: 9px;
        color: rgba(255,255,255,0.7);
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
    }
    
    /* Trending Ticker */
    .ticker-section {
        flex: 1;
        margin-left: 30px;
        overflow: hidden;
        position: relative;
    }
    
    .ticker-label {
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        background: var(--coral);
        color: white;
        padding: 4px 10px;
        font-size: 9px;
        font-weight: 700;
        text-transform: uppercase;
        border-radius: 4px;
        z-index: 2;
        letter-spacing: 0.5px;
    }
    
    .ticker-wrapper {
        margin-left: 80px;
        overflow: hidden;
        mask-image: linear-gradient(to right, transparent, black 10%, black 90%, transparent);
        -webkit-mask-image: linear-gradient(to right, transparent, black 10%, black 90%, transparent);
    }
    
    .ticker-content {
        display: flex;
        animation: ticker 30s linear infinite;
        white-space: nowrap;
    }
    
    .ticker-item {
        display: inline-flex;
        align-items: center;
        padding: 0 25px;
        font-size: 11px;
        color: rgba(255,255,255,0.9);
        font-weight: 500;
    }
    
    .ticker-item::after {
        content: '•';
        margin-left: 25px;
        color: var(--coral);
    }
    
    @keyframes ticker {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }
    
    /* Progress Steps */
    .progress-bar {
        display: flex;
        align-items: center;
        margin-top: 10px;
        padding-top: 10px;
        border-top: 1px solid rgba(255,255,255,0.15);
    }
    
    .step {
        display: flex;
        align-items: center;
        flex: 1;
    }
    
    .step-dot {
        width: 26px;
        height: 26px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 10px;
        font-weight: 700;
        margin-right: 6px;
        flex-shrink: 0;
    }
    
    .step-dot.wait { background: rgba(255,255,255,0.2); color: rgba(255,255,255,0.5); }
    .step-dot.run { background: var(--yellow); color: #000; animation: pulse 1s infinite; }
    .step-dot.ok { background: var(--green); color: white; }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.15); }
    }
    
    .step-text { font-size: 9px; color: rgba(255,255,255,0.7); }
    .step-text.run { color: var(--yellow); font-weight: 600; }
    .step-text.ok { color: var(--green); }
    
    .step-line {
        flex: 1;
        height: 2px;
        background: rgba(255,255,255,0.2);
        margin: 0 8px;
    }
    .step-line.ok { background: var(--green); }
    
    /* ============= PANELS ============= */
    .panel-title {
        font-size: 11px;
        font-weight: 700;
        color: var(--navy);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding-bottom: 8px;
        margin-bottom: 12px;
        border-bottom: 2px solid var(--coral);
    }
    
    .topic-lbl {
        font-size: 11px;
        font-weight: 600;
        color: var(--navy);
        margin-bottom: 4px;
        margin-top: 10px;
    }
    
    /* Stats */
    .stat-item {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        font-size: 12px;
        border-bottom: 1px solid #f0f0f0;
    }
    .stat-lbl { color: var(--gray); }
    .stat-val { font-weight: 600; color: var(--navy); }
    
    /* SEO Circle */
    .seo-box {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 16px auto;
    }
    .seo-box.good { background: linear-gradient(135deg, #d1fae5, #6ee7b7); }
    .seo-box.med { background: linear-gradient(135deg, #fef3c7, #fde047); }
    .seo-box.bad { background: linear-gradient(135deg, #fee2e2, #fca5a5); }
    .seo-num { font-size: 22px; font-weight: 700; }
    .seo-box.good .seo-num { color: var(--green); }
    .seo-box.med .seo-num { color: var(--yellow); }
    .seo-box.bad .seo-num { color: #ef4444; }
    .seo-txt { font-size: 9px; color: var(--gray); }
    
    .chk { padding: 5px 0; font-size: 11px; }
    
    .img-box {
        padding: 8px 10px;
        background: var(--light);
        border-left: 3px solid var(--navy);
        margin: 5px 0;
        font-size: 11px;
        border-radius: 0 4px 4px 0;
    }
    
    .kw {
        display: inline-block;
        background: var(--navy);
        color: white;
        padding: 4px 10px;
        margin: 3px;
        font-size: 10px;
        border-radius: 4px;
    }
    
    /* ============= ARTICLE WITH IMAGES ============= */
    .art-box {
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        height: calc(100vh - 160px);
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }
    
    .art-head {
        background: linear-gradient(135deg, var(--navy) 0%, var(--navy-light) 100%);
        color: white;
        padding: 14px 18px;
    }
    .art-cat { font-size: 10px; color: var(--coral); font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
    .art-title { font-size: 16px; font-weight: 700; margin: 6px 0; line-height: 1.3; }
    .art-meta { font-size: 11px; opacity: 0.8; }
    
    .art-desc {
        background: var(--light);
        border-left: 3px solid var(--coral);
        padding: 12px 16px;
        font-size: 12px;
        font-style: italic;
        color: var(--gray);
    }
    
    .art-body {
        flex: 1;
        overflow-y: auto;
        padding: 16px 18px;
        font-size: 12px;
        line-height: 1.75;
        color: #374151;
    }
    
    .art-body h1, .art-body h2 {
        font-size: 14px;
        color: var(--navy);
        margin: 14px 0 8px 0;
        padding-bottom: 4px;
        border-bottom: 2px solid var(--coral);
    }
    
    .art-body h3 { font-size: 13px; color: var(--coral); margin: 10px 0 6px 0; }
    .art-body p { margin-bottom: 10px; text-align: justify; }
    
    .art-body::-webkit-scrollbar { width: 4px; }
    .art-body::-webkit-scrollbar-thumb { background: var(--coral); border-radius: 2px; }
    
    /* Article Images */
    .art-image-container {
        margin: 16px 0;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .art-image {
        width: 100%;
        height: auto;
        display: block;
    }
    
    .art-image-caption {
        background: var(--light);
        padding: 8px 12px;
        font-size: 10px;
        color: var(--gray);
        border-left: 3px solid var(--coral);
    }
    
    .art-image-credit {
        font-size: 9px;
        color: #999;
        margin-top: 4px;
    }
    
    .art-foot {
        background: var(--light);
        padding: 10px 16px;
        font-size: 10px;
        color: var(--gray);
        border-top: 1px solid #e5e7eb;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--coral) 0%, #ee5a5a 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 20px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
    }
    
    .stDownloadButton > button {
        background: var(--navy) !important;
        color: white !important;
        border: none !important;
        padding: 10px !important;
        font-size: 11px !important;
        border-radius: 6px !important;
    }
    
    .mode-tag {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
        margin: 10px 0;
    }
    .mode-tag.live { background: #d1fae5; color: var(--green); }
    .mode-tag.demo { background: #fef3c7; color: var(--yellow); }
    
    .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        color: #cbd5e1;
        text-align: center;
    }
    .empty-icon { font-size: 60px; margin-bottom: 16px; }
    .empty-text { font-size: 14px; }
    
    .generating-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        color: var(--navy);
        text-align: center;
    }
    .generating-icon { font-size: 50px; margin-bottom: 16px; animation: bounce 1s infinite; }
    .generating-text { font-size: 14px; font-weight: 600; }
    .generating-sub { font-size: 12px; color: var(--gray); margin-top: 8px; }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
</style>
""", unsafe_allow_html=True)

# Healthcare stock images (royalty-free placeholders)
HEALTHCARE_IMAGES = {
    "medicare": [
        ("https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=600", "Senior patient consulting with healthcare provider", "Unsplash"),
        ("https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=600", "Medical professional reviewing patient records", "Unsplash"),
    ],
    "medicaid": [
        ("https://images.unsplash.com/photo-1538108149393-fbbd81895907?w=600", "Community health clinic serving patients", "Unsplash"),
        ("https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=600", "Healthcare accessibility illustration", "Unsplash"),
    ],
    "insurance": [
        ("https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=600", "Health insurance documentation", "Unsplash"),
        ("https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?w=600", "Financial planning for healthcare", "Unsplash"),
    ],
    "hospital": [
        ("https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=600", "Modern hospital facility", "Unsplash"),
        ("https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=600", "Hospital corridor and medical equipment", "Unsplash"),
    ],
    "prescription": [
        ("https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=600", "Prescription medications and pharmacy", "Unsplash"),
        ("https://images.unsplash.com/photo-1587854692152-cbe660dbde88?w=600", "Pharmaceutical drugs close-up", "Unsplash"),
    ],
    "default": [
        ("https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=600", "Healthcare professional at work", "Unsplash"),
        ("https://images.unsplash.com/photo-1551076805-e1869033e561?w=600", "Medical stethoscope and equipment", "Unsplash"),
        ("https://images.unsplash.com/photo-1581595220892-b0739db3ba8c?w=600", "Doctor consultation with patient", "Unsplash"),
    ]
}

def get_article_images(category, title):
    """Get relevant images based on article category and title"""
    title_lower = title.lower()
    category_lower = category.lower()
    
    # Match keywords to image categories
    if "medicare" in title_lower or "medicare" in category_lower:
        images = HEALTHCARE_IMAGES["medicare"]
    elif "medicaid" in title_lower or "medicaid" in category_lower:
        images = HEALTHCARE_IMAGES["medicaid"]
    elif "insurance" in title_lower or "plan" in category_lower:
        images = HEALTHCARE_IMAGES["insurance"]
    elif "hospital" in title_lower or "facility" in title_lower:
        images = HEALTHCARE_IMAGES["hospital"]
    elif "drug" in title_lower or "prescription" in title_lower or "pharma" in title_lower:
        images = HEALTHCARE_IMAGES["prescription"]
    else:
        images = HEALTHCARE_IMAGES["default"]
    
    return images

# Session State
for k, v in [('api_key', os.environ.get('OPENAI_API_KEY', '')), ('model', 'gpt-4o'), 
             ('result', None), ('mode', None), ('agent', 0), ('generating', False)]:
    if k not in st.session_state:
        st.session_state[k] = v

def run_gen(orch, tq, cp, cb):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(orch.generate_article(tq, cp, cb))
    finally:
        loop.close()

def get_header_html(agent_num):
    """Generate header with logo, ticker, and progress"""
    # Build ticker content (duplicate for seamless loop)
    ticker_items = "".join([f'<span class="ticker-item">{t}</span>' for t in TRENDING_TOPICS])
    ticker_html = ticker_items + ticker_items  # Duplicate for seamless animation
    
    # Build progress steps
    steps = ["Trend Discovery", "Content Writer", "SEO Examiner", "Consolidator"]
    steps_html = ""
    
    for i, name in enumerate(steps):
        n = i + 1
        if agent_num == 0:
            dot_cls, txt_cls, line_cls = "wait", "", ""
            icon = str(n)
        elif n < agent_num:
            dot_cls, txt_cls, line_cls = "ok", "ok", "ok"
            icon = "✓"
        elif n == agent_num:
            dot_cls, txt_cls, line_cls = "run", "run", ""
            icon = "⏳"
        else:
            dot_cls, txt_cls, line_cls = "wait", "", ""
            icon = str(n)
        
        steps_html += f'<div class="step"><div class="step-dot {dot_cls}">{icon}</div><span class="step-text {txt_cls}">{name}</span>'
        if i < 3:
            steps_html += f'<div class="step-line {line_cls}"></div>'
        steps_html += '</div>'
    
    return f"""
        <div class="main-header">
            <div class="header-top">
                <div class="logo-section">
                    <div class="logo-icon">💊</div>
                    <div class="logo-text">
                        <div class="logo-title">Health<span>Pulse</span> USA</div>
                        <div class="logo-subtitle">AI Healthcare Content</div>
                    </div>
                </div>
                <div class="ticker-section">
                    <div class="ticker-label">🔥 TRENDING</div>
                    <div class="ticker-wrapper">
                        <div class="ticker-content">{ticker_html}</div>
                    </div>
                </div>
            </div>
            <div class="progress-bar">{steps_html}</div>
        </div>
    """

def insert_images_in_content(content, images):
    """Insert images after first H2 heading in content"""
    if not images:
        return content
    
    # Get first image
    img_url, caption, credit = images[0]
    
    image_html = f"""
    <div class="art-image-container">
        <img src="{img_url}" alt="{caption}" class="art-image" onerror="this.style.display='none'">
        <div class="art-image-caption">
            📷 {caption}
            <div class="art-image-credit">Image: {credit}</div>
        </div>
    </div>
    """
    
    # Insert after first </h2> or after first paragraph
    if "</h2>" in content:
        parts = content.split("</h2>", 1)
        return parts[0] + "</h2>" + image_html + parts[1]
    elif "</p>" in content:
        parts = content.split("</p>", 1)
        return parts[0] + "</p>" + image_html + parts[1]
    
    return image_html + content

def main():
    api_key = st.session_state.api_key
    is_valid = api_key and api_key.startswith('sk-') and len(api_key) > 20
    
    # Determine agent state
    if st.session_state.result:
        display_agent = 5
    elif st.session_state.generating:
        display_agent = st.session_state.agent
    else:
        display_agent = 0
    
    # Header placeholder
    header_placeholder = st.empty()
    header_placeholder.markdown(get_header_html(display_agent), unsafe_allow_html=True)
    
    # Layout
    col1, col2, col3, col4 = st.columns([1, 2.5, 1, 1.2])
    
    # COL 1: Topic Selection
    with col1:
        st.markdown('<div class="panel-title">📋 TOPIC SELECTION</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="topic-lbl">Category</div>', unsafe_allow_html=True)
        main_cat = st.selectbox("c1", get_main_categories(), label_visibility="collapsed")
        
        st.markdown('<div class="topic-lbl">Subcategory</div>', unsafe_allow_html=True)
        sub_cats = get_subcategories(main_cat)
        sub_cat = st.selectbox("c2", sub_cats if sub_cats else ["ALL"], label_visibility="collapsed")
        
        st.markdown('<div class="topic-lbl">Specific Topic</div>', unsafe_allow_html=True)
        spec_topics = get_specific_topics(main_cat, sub_cat)
        
        if spec_topics and sub_cat != "ALL":
            filtered_topics = [t for t in spec_topics if t.upper() != "ALL"]
            spec = st.selectbox("c3", ["ALL"] + filtered_topics, label_visibility="collapsed")
        else:
            spec = None
            st.selectbox("c3d", ["ALL"], label_visibility="collapsed", disabled=True)
        
        topic_query = build_topic_query(main_cat, sub_cat, spec)
        
        # Mode
        mode_cls = "live" if is_valid else "demo"
        mode_txt = "● LIVE MODE" if is_valid else "● DEMO MODE"
        st.markdown(f'<div class="mode-tag {mode_cls}">{mode_txt}</div>', unsafe_allow_html=True)
        
        generate = st.button("🚀 Generate Article", use_container_width=True, disabled=st.session_state.generating)
        
        # Downloads
        if st.session_state.result:
            st.markdown('<div class="panel-title" style="margin-top:20px">⬇️ DOWNLOAD</div>', unsafe_allow_html=True)
            r = st.session_state.result
            exp = ArticleExporter(r.article.title, r.article.content, r.article.meta_description,
                                  r.seo_validation.overall_score, r.article.primary_keywords)
            
            c1, c2 = st.columns(2)
            with c1:
                st.download_button("📄 TXT", exp.export_to_txt(), 
                                   get_download_filename(r.article.title, "txt"), 
                                   "text/plain", use_container_width=True)
            with c2:
                docx = exp.export_to_docx()
                if docx:
                    st.download_button("📘 DOCX", docx, 
                                       get_download_filename(r.article.title, "docx"),
                                       "application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
                                       use_container_width=True)
    
    # COL 2: Article
    with col2:
        article_placeholder = st.empty()
        
        if st.session_state.result:
            r = st.session_state.result
            int_l = ", ".join(r.article.internal_links[:3]) if r.article.internal_links else "-"
            ext_l = ", ".join(r.article.external_links[:3]) if r.article.external_links else "-"
            
            # Get relevant images
            images = get_article_images(r.category_path, r.article.title)
            
            # Insert image into content
            content_with_images = insert_images_in_content(r.article.content, images)
            
            article_placeholder.markdown(f"""
                <div class="art-box">
                    <div class="art-head">
                        <div class="art-cat">{r.category_path}</div>
                        <div class="art-title">{r.article.title}</div>
                        <div class="art-meta">{datetime.now().strftime("%b %d, %Y")} • {r.article.word_count} words • SEO: {r.seo_validation.overall_score:.0f}% • {st.session_state.mode}</div>
                    </div>
                    <div class="art-desc">{r.article.meta_description}</div>
                    <div class="art-body">{content_with_images}</div>
                    <div class="art-foot"><b>Internal:</b> {int_l} | <b>External:</b> {ext_l}</div>
                </div>
            """, unsafe_allow_html=True)
        elif st.session_state.generating:
            agent_names = ["", "Trend Discovery", "Content Writer", "SEO Examiner", "Consolidator"]
            current_name = agent_names[st.session_state.agent] if st.session_state.agent > 0 else "Starting"
            article_placeholder.markdown(f"""
                <div class="art-box">
                    <div class="generating-state">
                        <div class="generating-icon">⚙️</div>
                        <div class="generating-text">Generating Article...</div>
                        <div class="generating-sub">Currently running: {current_name}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            article_placeholder.markdown("""
                <div class="art-box">
                    <div class="empty-state">
                        <div class="empty-icon">📝</div>
                        <div class="empty-text">Select a topic and click<br><b>Generate Article</b></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    # COL 3: Stats
    with col3:
        st.markdown('<div class="panel-title">📊 STATS</div>', unsafe_allow_html=True)
        
        if st.session_state.result:
            r = st.session_state.result
            for lbl, val in [("Words", r.article.word_count), ("Headings", len(r.article.headings)), ("Keywords", len(r.article.primary_keywords))]:
                st.markdown(f'<div class="stat-item"><span class="stat-lbl">{lbl}</span><span class="stat-val">{val}</span></div>', unsafe_allow_html=True)
            
            score = r.seo_validation.overall_score
            cls = "good" if score >= 80 else "med" if score >= 60 else "bad"
            st.markdown(f'<div class="seo-box {cls}"><span class="seo-num">{score:.0f}%</span><span class="seo-txt">SEO SCORE</span></div>', unsafe_allow_html=True)
        else:
            for lbl in ["Words", "Headings", "Keywords"]:
                st.markdown(f'<div class="stat-item"><span class="stat-lbl">{lbl}</span><span class="stat-val">-</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="seo-box" style="background:#f0f0f0"><span class="seo-num" style="color:#ccc">-</span><span class="seo-txt">SEO SCORE</span></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="panel-title" style="margin-top:16px">📷 IMAGES</div>', unsafe_allow_html=True)
        if st.session_state.result and st.session_state.result.article.image_suggestions:
            for i, img in enumerate(st.session_state.result.article.image_suggestions[:3], 1):
                desc = img.get('description', str(img))[:40] if isinstance(img, dict) else str(img)[:40]
                st.markdown(f'<div class="img-box">{i}. {desc}...</div>', unsafe_allow_html=True)
        else:
            st.caption("Generate to see suggestions")
    
    # COL 4: SEO Checklist & Keywords
    with col4:
        st.markdown('<div class="panel-title">✓ SEO CHECKLIST</div>', unsafe_allow_html=True)
        
        if st.session_state.result:
            for item, ok in list(st.session_state.result.seo_validation.validation_checklist.items())[:8]:
                short = item[:24] + "..." if len(item) > 24 else item
                st.markdown(f'<div class="chk">{"✅" if ok else "❌"} {short}</div>', unsafe_allow_html=True)
        else:
            for item in ["Primary keyword in title", "Keyword in first para", "Single H1 present",
                        "5+ H2 headings", "Meta description opt", "Word count >= 1500", "Keyword density 1-3%", "Heading hierarchy"]:
                st.markdown(f'<div class="chk" style="color:#ccc">○ {item[:24]}...</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="panel-title" style="margin-top:16px">🔑 KEYWORDS</div>', unsafe_allow_html=True)
        if st.session_state.result:
            kws = st.session_state.result.article.primary_keywords + st.session_state.result.article.secondary_keywords
            st.markdown("".join([f'<span class="kw">{k}</span>' for k in kws[:6]]), unsafe_allow_html=True)
        else:
            st.caption("Keywords appear after generation")
    
    # ========== Generation Logic ==========
    if generate:
        st.session_state.mode = "LIVE" if is_valid else "DEMO"
        st.session_state.result = None
        st.session_state.generating = True
        st.session_state.agent = 1
        
        header_placeholder.markdown(get_header_html(1), unsafe_allow_html=True)
        
        agent_names = ["", "Trend Discovery", "Content Writer", "SEO Examiner", "Consolidator"]
        
        def update_progress(msg, pct):
            if pct <= 25:
                new_agent = 1
            elif pct <= 50:
                new_agent = 2
            elif pct <= 80:
                new_agent = 3
            else:
                new_agent = 4
            
            if new_agent != st.session_state.agent:
                st.session_state.agent = new_agent
                header_placeholder.markdown(get_header_html(new_agent), unsafe_allow_html=True)
                article_placeholder.markdown(f"""
                    <div class="art-box">
                        <div class="generating-state">
                            <div class="generating-icon">⚙️</div>
                            <div class="generating-text">Generating Article...</div>
                            <div class="generating-sub">Currently running: {agent_names[new_agent]}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        try:
            orch = HealthcareAgentOrchestrator(
                api_key=st.session_state.api_key if is_valid else None,
                model=st.session_state.model
            )
            
            result = run_gen(orch, topic_query, topic_query, update_progress)
            
            if result and hasattr(result, 'article'):
                st.session_state.result = result
                st.session_state.agent = 5
                st.session_state.generating = False
                header_placeholder.markdown(get_header_html(5), unsafe_allow_html=True)
                st.rerun()
            else:
                st.error("Generation failed - please try again")
                st.session_state.generating = False
                st.session_state.agent = 0
        except Exception as e:
            st.error(f"Error: {e}")
            st.session_state.generating = False
            st.session_state.agent = 0

if __name__ == "__main__":
    main()
