"""
HealthPulse USA - Multi-Agent US Healthcare Article Generator
Version: 2.1.0 - Simplified and Reliable
"""

import streamlit as st
import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

# Load .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    get_main_categories,
    get_subcategories,
    get_specific_topics,
    build_topic_query,
    get_search_keywords,
    TRUSTED_SOURCES,
    SEO_WEIGHTS
)
from agents import HealthcareAgentOrchestrator
from utils import ArticleExporter, get_download_filename

# Page config
st.set_page_config(
    page_title="HealthPulse USA",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0066CC, #003366);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }
    .main-header h1 { margin: 0; font-size: 2rem; }
    .main-header p { margin: 0.5rem 0 0 0; opacity: 0.9; }
    
    .metric-box {
        background: #f0f9ff;
        border: 1px solid #bae6fd;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .metric-value { font-size: 2rem; font-weight: bold; color: #0066cc; }
    .metric-label { color: #64748b; font-size: 0.85rem; }
    
    .agent-status {
        padding: 0.5rem 1rem;
        border-radius: 6px;
        margin: 0.3rem 0;
        border-left: 4px solid #e2e8f0;
    }
    .agent-working { background: #eff6ff; border-left-color: #3b82f6; }
    .agent-done { background: #f0fdf4; border-left-color: #22c55e; }
    
    .info-box {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'api_key' not in st.session_state:
    st.session_state.api_key = os.environ.get('OPENAI_API_KEY', '')
if 'model' not in st.session_state:
    st.session_state.model = os.environ.get('OPENAI_MODEL', 'gpt-4o')
if 'result' not in st.session_state:
    st.session_state.result = None
if 'mode' not in st.session_state:
    st.session_state.mode = None


def run_generation(orchestrator, topic_query, category_path, progress_callback):
    """Run the async generation synchronously"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(
            orchestrator.generate_article(topic_query, category_path, progress_callback)
        )
        return result
    finally:
        loop.close()


def main():
    # Header
    st.markdown("""
        <div class="main-header">
            <h1>🏥 HealthPulse USA</h1>
            <p>AI-Powered Multi-Agent Healthcare Content Generator</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key
        st.subheader("🔑 OpenAI API Key")
        api_input = st.text_input(
            "API Key",
            type="password",
            value=st.session_state.api_key,
            placeholder="sk-..."
        )
        st.session_state.api_key = api_input
        
        # Check validity
        is_valid = api_input and api_input.startswith('sk-') and len(api_input) > 20
        
        if is_valid:
            st.success("🟢 LIVE MODE")
        else:
            st.warning("🟡 DEMO MODE")
            st.caption("Enter API key for AI generation")
        
        st.divider()
        
        # Model
        st.subheader("🤖 Model")
        st.session_state.model = st.selectbox(
            "Model",
            ["gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]
        )
        
        st.divider()
        
        # Help
        with st.expander("📖 Setup Help"):
            st.markdown("""
            **Create .env file:**
            ```
            OPENAI_API_KEY=sk-your-key
            OPENAI_MODEL=gpt-4o
            ```
            
            **Or enter API key above**
            
            Get key: [platform.openai.com](https://platform.openai.com)
            """)
        
        st.divider()
        st.caption("Sources: CMS • CDC • HHS • NIH")
    
    # Main area - Mode indicator
    is_valid = st.session_state.api_key and st.session_state.api_key.startswith('sk-') and len(st.session_state.api_key) > 20
    
    if is_valid:
        st.success(f"🟢 **LIVE MODE** - Using OpenAI {st.session_state.model}")
    else:
        st.warning("🟡 **DEMO MODE** - Template content (add API key for AI generation)")
    
    st.divider()
    
    # Topic Selection
    st.subheader("📋 Select Topic")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        main_cat = st.selectbox("Main Category", get_main_categories())
    
    with col2:
        subs = get_subcategories(main_cat)
        sub_cat = st.selectbox("Subcategory", subs if subs else ["ALL"])
    
    with col3:
        specs = get_specific_topics(main_cat, sub_cat)
        if specs and sub_cat != "ALL":
            spec = st.selectbox("Specific", ["ALL"] + specs)
        else:
            spec = None
            st.selectbox("Specific", ["N/A"], disabled=True)
    
    topic_query = build_topic_query(main_cat, sub_cat, spec)
    keywords = get_search_keywords(main_cat, sub_cat)
    
    st.markdown(f"""
    <div class="info-box">
        <strong>📍 Topic:</strong> {topic_query}<br>
        <strong>🔑 Keywords:</strong> {', '.join(keywords[:5])}
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Generate Button
    col_btn = st.columns([1, 2, 1])[1]
    with col_btn:
        generate = st.button("🚀 Generate Article", use_container_width=True, type="primary")
    
    # Generation
    if generate:
        st.divider()
        st.subheader("🔄 Multi-Agent Generation")
        
        col_prog, col_agents = st.columns([2, 1])
        
        with col_prog:
            progress_bar = st.progress(0)
            status_text = st.empty()
        
        with col_agents:
            st.markdown("**Agent Status:**")
            a1 = st.empty()
            a2 = st.empty()
            a3 = st.empty()
            a4 = st.empty()
            
            a1.markdown('<div class="agent-status">🔍 Trend Discovery - Waiting</div>', unsafe_allow_html=True)
            a2.markdown('<div class="agent-status">✍️ Content Writer - Waiting</div>', unsafe_allow_html=True)
            a3.markdown('<div class="agent-status">📊 SEO Examiner - Waiting</div>', unsafe_allow_html=True)
            a4.markdown('<div class="agent-status">📦 Consolidator - Waiting</div>', unsafe_allow_html=True)
        
        def update_progress(msg, pct):
            progress_bar.progress(pct)
            status_text.markdown(f"**{msg}**")
            
            if pct <= 25:
                a1.markdown('<div class="agent-status agent-working">🔍 Trend Discovery - Working...</div>', unsafe_allow_html=True)
            elif pct <= 50:
                a1.markdown('<div class="agent-status agent-done">🔍 Trend Discovery - Done ✓</div>', unsafe_allow_html=True)
                a2.markdown('<div class="agent-status agent-working">✍️ Content Writer - Working...</div>', unsafe_allow_html=True)
            elif pct <= 80:
                a2.markdown('<div class="agent-status agent-done">✍️ Content Writer - Done ✓</div>', unsafe_allow_html=True)
                a3.markdown('<div class="agent-status agent-working">📊 SEO Examiner - Working...</div>', unsafe_allow_html=True)
            else:
                a3.markdown('<div class="agent-status agent-done">📊 SEO Examiner - Done ✓</div>', unsafe_allow_html=True)
                a4.markdown('<div class="agent-status agent-working">📦 Consolidator - Working...</div>', unsafe_allow_html=True)
        
        # Set mode
        st.session_state.mode = "LIVE" if is_valid else "DEMO"
        
        try:
            orchestrator = HealthcareAgentOrchestrator(
                api_key=st.session_state.api_key if is_valid else None,
                model=st.session_state.model
            )
            
            result = run_generation(orchestrator, topic_query, topic_query, update_progress)
            
            # Simplified validation - just check if result exists
            if result is not None and hasattr(result, 'article'):
                st.session_state.result = result
                
                # Final status
                a1.markdown('<div class="agent-status agent-done">🔍 Trend Discovery - Done ✓</div>', unsafe_allow_html=True)
                a2.markdown('<div class="agent-status agent-done">✍️ Content Writer - Done ✓</div>', unsafe_allow_html=True)
                a3.markdown('<div class="agent-status agent-done">📊 SEO Examiner - Done ✓</div>', unsafe_allow_html=True)
                a4.markdown('<div class="agent-status agent-done">📦 Consolidator - Done ✓</div>', unsafe_allow_html=True)
                
                st.success(f"✅ Article generated in **{st.session_state.mode} MODE**!")
            else:
                st.error(f"❌ Generation returned: {type(result)}")
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
    
    # Display Results
    if st.session_state.result:
        result = st.session_state.result
        
        st.divider()
        
        if st.session_state.mode == "DEMO":
            st.info("📝 DEMO MODE content - Add API key for AI-generated articles")
        
        st.subheader("📄 Generated Article")
        
        # Metrics
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f'<div class="metric-box"><div class="metric-value">{result.article.word_count}</div><div class="metric-label">WORDS</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-box"><div class="metric-value">{len(result.article.headings)}</div><div class="metric-label">HEADINGS</div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-box"><div class="metric-value">{len(result.article.primary_keywords)}</div><div class="metric-label">KEYWORDS</div></div>', unsafe_allow_html=True)
        with m4:
            score = result.seo_validation.overall_score
            color = "#22c55e" if score >= 80 else "#f59e0b" if score >= 60 else "#ef4444"
            st.markdown(f'<div class="metric-box"><div class="metric-value" style="color:{color}">{score:.0f}%</div><div class="metric-label">SEO SCORE</div></div>', unsafe_allow_html=True)
        
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📝 Article", "📊 SEO Report", "🔍 Topic", "⬇️ Download"])
        
        with tab1:
            st.markdown(f"**Meta:** _{result.article.meta_description}_")
            st.divider()
            st.markdown(result.article.content)
        
        with tab2:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Scores:**")
                st.progress(result.seo_validation.keyword_score/20, f"Keywords: {result.seo_validation.keyword_score:.0f}/20")
                st.progress(result.seo_validation.heading_score/15, f"Headings: {result.seo_validation.heading_score:.0f}/15")
                st.progress(result.seo_validation.length_score/15, f"Length: {result.seo_validation.length_score:.0f}/15")
                st.progress(result.seo_validation.readability_score/15, f"Readability: {result.seo_validation.readability_score:.0f}/15")
            with c2:
                st.markdown("**Checklist:**")
                for item, ok in result.seo_validation.validation_checklist.items():
                    st.markdown(f"{'✅' if ok else '❌'} {item}")
        
        with tab3:
            st.markdown(f"**Title:** {result.trending_topic.title}")
            st.markdown(f"**Relevance:** {result.trending_topic.relevance_score}%")
            st.markdown(f"**Reason:** {result.trending_topic.trending_reason}")
            st.markdown(f"**Sources:** {result.trending_topic.source}")
        
        with tab4:
            exporter = ArticleExporter(
                title=result.article.title,
                content=result.article.content,
                meta_description=result.article.meta_description,
                seo_score=result.seo_validation.overall_score,
                keywords=result.article.primary_keywords
            )
            
            c1, c2 = st.columns(2)
            
            with c1:
                try:
                    st.download_button(
                        "📄 Download TXT",
                        exporter.export_to_txt(),
                        get_download_filename(result.article.title, "txt"),
                        "text/plain",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"TXT error")
            
            with c2:
                try:
                    docx = exporter.export_to_docx()
                    if docx:
                        st.download_button(
                            "📘 Download DOCX",
                            docx,
                            get_download_filename(result.article.title, "docx"),
                            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"DOCX error")
            
            
            
            st.divider()
            st.json({
                "mode": st.session_state.mode,
                "model": st.session_state.model,
                "topic": result.category_path,
                "words": result.article.word_count,
                "seo_score": f"{result.seo_validation.overall_score:.1f}%"
            })
    
    # Footer
    st.divider()
    st.caption("🏥 HealthPulse USA v2.1 | Multi-Agent Healthcare Content Generator")


if __name__ == "__main__":
    main()
