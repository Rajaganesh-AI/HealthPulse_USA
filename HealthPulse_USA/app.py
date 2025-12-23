"""
HealthPulse USA - Multi-Agent US Healthcare Article Generator
Version: 8.3.0 - Real-time Step Progress & Fixed Duplicate ALL
"""

import streamlit as st
import asyncio
import os
import sys
from datetime import datetime
import time

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

# CSS Styles
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
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
    
    /* Dropdown font fixes */
    .stSelectbox [data-baseweb="select"] span,
    .stSelectbox [data-baseweb="select"] div { font-size: 12px !important; }
    [data-baseweb="menu"] li { font-size: 12px !important; padding: 8px 12px !important; }
    [role="option"] div { font-size: 12px !important; }
    
    /* Header */
    .main-header {
        background: linear-gradient(135deg, var(--navy) 0%, var(--navy-light) 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        margin-bottom: 12px;
        border-bottom: 3px solid var(--coral);
    }
    
    .header-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .logo { font-size: 18px; font-weight: 700; }
    .tagline { font-size: 11px; color: var(--coral); font-weight: 600; letter-spacing: 1px; }
    
    /* Progress Steps */
    .progress-bar {
        display: flex;
        align-items: center;
        margin-top: 12px;
        padding-top: 12px;
        border-top: 1px solid rgba(255,255,255,0.15);
    }
    
    .step {
        display: flex;
        align-items: center;
        flex: 1;
    }
    
    .step-dot {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: 700;
        margin-right: 8px;
        flex-shrink: 0;
    }
    
    .step-dot.wait { background: rgba(255,255,255,0.2); color: rgba(255,255,255,0.5); }
    .step-dot.run { background: var(--yellow); color: #000; animation: pulse 1s infinite; }
    .step-dot.ok { background: var(--green); color: white; }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.15); }
    }
    
    .step-text { font-size: 10px; color: rgba(255,255,255,0.7); }
    .step-text.run { color: var(--yellow); font-weight: 600; }
    .step-text.ok { color: var(--green); }
    
    .step-line {
        flex: 1;
        height: 2px;
        background: rgba(255,255,255,0.2);
        margin: 0 10px;
    }
    .step-line.ok { background: var(--green); }
    
    /* Panel */
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
    
    /* Topic Label */
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
    
    /* Check Item */
    .chk { padding: 5px 0; font-size: 11px; }
    
    /* Image Item */
    .img-box {
        padding: 8px 10px;
        background: var(--light);
        border-left: 3px solid var(--navy);
        margin: 5px 0;
        font-size: 11px;
        border-radius: 0 4px 4px 0;
    }
    
    /* Keyword Tag */
    .kw {
        display: inline-block;
        background: var(--navy);
        color: white;
        padding: 4px 10px;
        margin: 3px;
        font-size: 10px;
        border-radius: 4px;
    }
    
    /* Article */
    .art-box {
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        height: calc(100vh - 140px);
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
    
    /* Mode Badge */
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
    
    /* Empty State */
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
    
    /* Generating State */
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

def get_progress_html(agent_num):
    """Generate progress bar HTML for given agent number"""
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
            <div class="header-content">
                <span class="logo">🏥 HealthPulse USA</span>
                <span class="tagline">AI-POWERED HEALTHCARE CONTENT GENERATOR</span>
            </div>
            <div class="progress-bar">{steps_html}</div>
        </div>
    """

def main():
    api_key = st.session_state.api_key
    is_valid = api_key and api_key.startswith('sk-') and len(api_key) > 20
    
    # Determine agent state for display
    if st.session_state.result:
        display_agent = 5  # All done
    elif st.session_state.generating:
        display_agent = st.session_state.agent
    else:
        display_agent = 0
    
    # Header placeholder for dynamic updates
    header_placeholder = st.empty()
    header_placeholder.markdown(get_progress_html(display_agent), unsafe_allow_html=True)
    
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
        
        # FIXED: Only show specific topics if available, no duplicate ALL
        if spec_topics and sub_cat != "ALL":
            # Filter out any "ALL" that might be in spec_topics and add it once at the beginning
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
            
            article_placeholder.markdown(f"""
                <div class="art-box">
                    <div class="art-head">
                        <div class="art-cat">{r.category_path}</div>
                        <div class="art-title">{r.article.title}</div>
                        <div class="art-meta">{datetime.now().strftime("%b %d, %Y")} • {r.article.word_count} words • SEO: {r.seo_validation.overall_score:.0f}% • {st.session_state.mode}</div>
                    </div>
                    <div class="art-desc">{r.article.meta_description}</div>
                    <div class="art-body">{r.article.content}</div>
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
        
        # Update header to show first agent running
        header_placeholder.markdown(get_progress_html(1), unsafe_allow_html=True)
        
        agent_names = ["", "Trend Discovery", "Content Writer", "SEO Examiner", "Consolidator"]
        
        def update_progress(msg, pct):
            """Update progress based on percentage"""
            if pct <= 25:
                new_agent = 1
            elif pct <= 50:
                new_agent = 2
            elif pct <= 80:
                new_agent = 3
            else:
                new_agent = 4
            
            # Only update if agent changed
            if new_agent != st.session_state.agent:
                st.session_state.agent = new_agent
                # Update the header with new progress
                header_placeholder.markdown(get_progress_html(new_agent), unsafe_allow_html=True)
                # Update article panel to show current agent
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
                # Show all complete
                header_placeholder.markdown(get_progress_html(5), unsafe_allow_html=True)
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
