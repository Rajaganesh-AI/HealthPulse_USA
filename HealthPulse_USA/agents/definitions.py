"""
Multi-Agent System Definitions
Implements the 4 specialized agents using AutoGen AgentChat framework
"""

import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

# Agent Response Data Classes
@dataclass
class TrendingTopic:
    """Represents a trending topic discovered by the Search Agent"""
    title: str
    keywords: List[str]
    source: str
    relevance_score: float
    description: str
    trending_reason: str

@dataclass
class SEOArticle:
    """Represents an SEO-optimized article from the Content Writer"""
    title: str
    meta_description: str
    content: str
    primary_keywords: List[str]
    secondary_keywords: List[str]
    headings: List[Dict[str, str]]
    word_count: int
    image_suggestions: List[Dict[str, str]]
    internal_links: List[str]
    external_links: List[str]

@dataclass
class SEOValidation:
    """Represents SEO validation results from the SEO Examiner"""
    overall_score: float
    keyword_score: float
    heading_score: float
    length_score: float
    readability_score: float
    relevance_score: float
    intent_score: float
    validation_checklist: Dict[str, bool]
    recommendations: List[str]
    pass_status: bool

@dataclass
class ConsolidatedOutput:
    """Final consolidated output from the Consolidator Agent"""
    article: SEOArticle
    seo_validation: SEOValidation
    trending_topic: TrendingTopic
    generation_timestamp: str
    category_path: str
    download_ready: bool = True

# Agent System Prompts
SEARCH_AGENT_PROMPT = """You are the TREND DISCOVERY AGENT, a specialized US healthcare content intelligence expert.

YOUR MISSION:
Discover and curate the latest trending topics in US healthcare based on the user's topic selection.

RESPONSIBILITIES:
1. Analyze the selected healthcare category/subcategory
2. Identify current trending topics from trusted US healthcare sources
3. Focus ONLY on topics relevant to the selected category
4. Provide keywords optimized for SEO

TRUSTED SOURCES TO REFERENCE:
- CMS (Centers for Medicare & Medicaid Services)
- CDC (Centers for Disease Control and Prevention)  
- HHS (Department of Health and Human Services)
- NIH (National Institutes of Health)
- Kaiser Family Foundation
- Healthcare.gov
- AMA (American Medical Association)
- AHA (American Hospital Association)

OUTPUT FORMAT:
Provide your response as a structured trending topic analysis with:
- TOPIC TITLE: Clear, SEO-friendly title
- PRIMARY KEYWORDS: 3-5 main keywords
- SECONDARY KEYWORDS: 5-8 supporting keywords
- TRENDING REASON: Why this is trending now
- SOURCE REFERENCES: Which trusted sources support this topic
- RELEVANCE SCORE: 1-100 based on current relevance
- BRIEF DESCRIPTION: 2-3 sentences about the topic

CATEGORY-SPECIFIC FOCUS:
- For CODES topics: Focus on coding updates, changes, compliance
- For GOVERNMENT PLANS: Focus on policy changes, enrollment, benefits
- For COMMERCIAL PLANS: Focus on market trends, pricing, coverage changes
- For SUPPLEMENTAL: Focus on added value, gaps in coverage
- For EXCHANGE: Focus on marketplace updates, enrollment periods

Be specific and factual. Reference current year (2024-2025) developments."""

CONTENT_WRITER_PROMPT = """You are the SEO CONTENT WRITER AGENT, a healthcare content specialist.

YOUR MISSION:
Generate a comprehensive, SEO-optimized article on US healthcare topics.

ARTICLE REQUIREMENTS:
1. Word count: 1500-3000 words
2. Professional, authoritative healthcare tone
3. Data-driven insights with statistics where relevant
4. US healthcare context throughout

SEO BEST PRACTICES TO FOLLOW:
- Use H1 for main title (only one per article)
- Use H2 for major sections (5-8 recommended)
- Use H3 for subsections as needed
- Keyword density: 1-3% for primary keywords
- Include primary keyword in:
  * Title (H1)
  * First paragraph
  * At least 2 H2 headings
  * Meta description
  * Conclusion
- Natural keyword integration (no stuffing)
- Short paragraphs (2-4 sentences each)
- Use bullet points for lists
- Include transition phrases between sections

ARTICLE STRUCTURE:
1. META DESCRIPTION: 150-160 characters, compelling, keyword-rich
2. TITLE (H1): Under 60 characters, includes primary keyword
3. INTRODUCTION: Hook + topic overview + what reader will learn
4. BODY SECTIONS (H2s):
   - Each section addresses a key aspect
   - Include relevant statistics/data points
   - Reference trusted sources
5. SUBSECTIONS (H3s): Detailed breakdowns as needed
6. CONCLUSION: Key takeaways + call to action
7. IMAGE SUGGESTIONS: Descriptions with alt-text for 3-5 images

FORMAT YOUR RESPONSE:
---
META_DESCRIPTION: [description]
---
TITLE: [H1 title]
---
PRIMARY_KEYWORDS: [comma-separated list]
SECONDARY_KEYWORDS: [comma-separated list]
---
ARTICLE_CONTENT:
[Full article with proper heading markup using ## for H2 and ### for H3]
---
IMAGE_SUGGESTIONS:
1. [Description] | Alt-text: [alt text]
2. [etc.]
---
INTERNAL_LINK_SUGGESTIONS: [topics to link to]
EXTERNAL_LINK_SUGGESTIONS: [authoritative sources to cite]
---

Write in an authoritative but accessible style suitable for healthcare professionals and informed consumers."""

SEO_EXAMINER_PROMPT = """You are the SEO EXAMINER AGENT, a technical SEO analyst for healthcare content.

YOUR MISSION:
Validate articles against SEO best practices and provide actionable feedback.

VALIDATION CRITERIA:

1. KEYWORD USAGE (20 points max):
   - Primary keyword in title: 5 points
   - Primary keyword in first paragraph: 3 points
   - Primary keyword in H2s: 4 points
   - Keyword density 1-3%: 4 points
   - No keyword stuffing: 4 points

2. HEADING STRUCTURE (15 points max):
   - Single H1 present: 3 points
   - 5+ H2 headings: 4 points
   - Logical hierarchy (H1>H2>H3): 4 points
   - Keywords in headings: 4 points

3. CONTENT LENGTH (15 points max):
   - 1500+ words: 5 points
   - 2000+ words: 5 points
   - 2500+ words: 5 points

4. READABILITY (15 points max):
   - Short paragraphs: 4 points
   - Transition words: 3 points
   - Active voice predominant: 4 points
   - Grade level 8-12: 4 points

5. TOPIC RELEVANCE (15 points max):
   - Matches requested topic: 5 points
   - Comprehensive coverage: 5 points
   - Accurate information: 5 points

6. SEARCH INTENT (10 points max):
   - Answers user questions: 4 points
   - Actionable content: 3 points
   - Clear value proposition: 3 points

7. META ELEMENTS (10 points max):
   - Meta description present: 3 points
   - Meta description length (150-160): 3 points
   - Meta includes primary keyword: 4 points

OUTPUT FORMAT:
---
OVERALL_SCORE: [X/100]
---
CATEGORY_SCORES:
- Keyword Usage: [X/20]
- Heading Structure: [X/15]
- Content Length: [X/15]
- Readability: [X/15]
- Topic Relevance: [X/15]
- Search Intent: [X/10]
- Meta Elements: [X/10]
---
VALIDATION_CHECKLIST:
✓/✗ Primary keyword in title
✓/✗ Primary keyword in first paragraph
✓/✗ Single H1 present
✓/✗ 5+ H2 headings
✓/✗ Meta description present and optimized
✓/✗ Word count >= 1500
✓/✗ Keyword density 1-3%
✓/✗ Proper heading hierarchy
✓/✗ Topic matches request
✓/✗ Actionable content present
---
PASS_STATUS: [PASS/FAIL] (Pass requires 70+ overall score)
---
RECOMMENDATIONS:
1. [Specific improvement suggestion]
2. [etc.]
---

Be thorough and objective in your assessment."""

CONSOLIDATOR_PROMPT = """You are the CONSOLIDATOR AGENT, the orchestrator of the content generation pipeline.

YOUR MISSION:
Merge outputs from all agents into a cohesive, ready-to-publish package.

CONSOLIDATION TASKS:
1. Verify all agent outputs are present and complete
2. Ensure article content aligns with trending topic
3. Validate SEO score meets threshold (70+)
4. Format final output for frontend display and download

OUTPUT FORMAT:
---
GENERATION_SUMMARY:
- Topic Category: [category path]
- Generated: [timestamp]
- Word Count: [count]
- SEO Score: [score]%
- Status: [APPROVED/NEEDS_REVISION]
---
TRENDING_TOPIC_SUMMARY:
[Brief summary of the trending topic selected]
---
FINAL_ARTICLE:
[Complete article content with all formatting preserved]
---
SEO_REPORT:
- Overall Score: [X]%
- Key Metrics:
  * Keywords: [score]
  * Structure: [score]
  * Readability: [score]
  * Relevance: [score]
---
QUALITY_NOTES:
[Any additional observations or recommendations]
---
DOWNLOAD_READY: [YES/NO]
---

Ensure the final package is professional and publication-ready."""


def get_agent_prompts() -> Dict[str, str]:
    """Return all agent system prompts"""
    return {
        "search_agent": SEARCH_AGENT_PROMPT,
        "content_writer": CONTENT_WRITER_PROMPT,
        "seo_examiner": SEO_EXAMINER_PROMPT,
        "consolidator": CONSOLIDATOR_PROMPT
    }


class AgentOutputParser:
    """Parses structured outputs from agents"""
    
    @staticmethod
    def parse_trending_topic(response: str) -> TrendingTopic:
        """Parse Search Agent output into TrendingTopic"""
        lines = response.split('\n')
        topic_data = {
            'title': '',
            'keywords': [],
            'source': '',
            'relevance_score': 0.0,
            'description': '',
            'trending_reason': ''
        }
        
        current_section = None
        for line in lines:
            line = line.strip()
            if line.startswith('TOPIC TITLE:'):
                topic_data['title'] = line.replace('TOPIC TITLE:', '').strip()
            elif line.startswith('PRIMARY KEYWORDS:'):
                keywords = line.replace('PRIMARY KEYWORDS:', '').strip()
                topic_data['keywords'] = [k.strip() for k in keywords.split(',')]
            elif line.startswith('TRENDING REASON:'):
                topic_data['trending_reason'] = line.replace('TRENDING REASON:', '').strip()
            elif line.startswith('SOURCE REFERENCES:'):
                topic_data['source'] = line.replace('SOURCE REFERENCES:', '').strip()
            elif line.startswith('RELEVANCE SCORE:'):
                try:
                    score_str = line.replace('RELEVANCE SCORE:', '').strip()
                    topic_data['relevance_score'] = float(score_str.split('/')[0])
                except:
                    topic_data['relevance_score'] = 75.0
            elif line.startswith('BRIEF DESCRIPTION:'):
                topic_data['description'] = line.replace('BRIEF DESCRIPTION:', '').strip()
        
        return TrendingTopic(**topic_data)
    
    @staticmethod
    def parse_seo_article(response: str) -> SEOArticle:
        """Parse Content Writer output into SEOArticle"""
        article_data = {
            'title': '',
            'meta_description': '',
            'content': '',
            'primary_keywords': [],
            'secondary_keywords': [],
            'headings': [],
            'word_count': 0,
            'image_suggestions': [],
            'internal_links': [],
            'external_links': []
        }
        
        sections = response.split('---')
        
        for section in sections:
            section = section.strip()
            if section.startswith('META_DESCRIPTION:'):
                article_data['meta_description'] = section.replace('META_DESCRIPTION:', '').strip()
            elif section.startswith('TITLE:'):
                article_data['title'] = section.replace('TITLE:', '').strip()
            elif section.startswith('PRIMARY_KEYWORDS:'):
                lines = section.split('\n')
                for line in lines:
                    if line.startswith('PRIMARY_KEYWORDS:'):
                        keywords = line.replace('PRIMARY_KEYWORDS:', '').strip()
                        article_data['primary_keywords'] = [k.strip() for k in keywords.split(',')]
                    elif line.startswith('SECONDARY_KEYWORDS:'):
                        keywords = line.replace('SECONDARY_KEYWORDS:', '').strip()
                        article_data['secondary_keywords'] = [k.strip() for k in keywords.split(',')]
            elif section.startswith('ARTICLE_CONTENT:'):
                content = section.replace('ARTICLE_CONTENT:', '').strip()
                article_data['content'] = content
                article_data['word_count'] = len(content.split())
                
                # Extract headings
                for line in content.split('\n'):
                    if line.startswith('## '):
                        article_data['headings'].append({'level': 'H2', 'text': line.replace('## ', '')})
                    elif line.startswith('### '):
                        article_data['headings'].append({'level': 'H3', 'text': line.replace('### ', '')})
            elif section.startswith('IMAGE_SUGGESTIONS:'):
                lines = section.replace('IMAGE_SUGGESTIONS:', '').strip().split('\n')
                for line in lines:
                    if '|' in line and line.strip():
                        parts = line.split('|')
                        if len(parts) >= 2:
                            article_data['image_suggestions'].append({
                                'description': parts[0].strip(),
                                'alt_text': parts[1].replace('Alt-text:', '').strip()
                            })
            elif 'INTERNAL_LINK' in section:
                article_data['internal_links'] = [l.strip() for l in section.split('\n') if l.strip() and not l.startswith('INTERNAL')]
            elif 'EXTERNAL_LINK' in section:
                article_data['external_links'] = [l.strip() for l in section.split('\n') if l.strip() and not l.startswith('EXTERNAL')]
        
        return SEOArticle(**article_data)
    
    @staticmethod
    def parse_seo_validation(response: str) -> SEOValidation:
        """Parse SEO Examiner output into SEOValidation"""
        validation_data = {
            'overall_score': 0.0,
            'keyword_score': 0.0,
            'heading_score': 0.0,
            'length_score': 0.0,
            'readability_score': 0.0,
            'relevance_score': 0.0,
            'intent_score': 0.0,
            'validation_checklist': {},
            'recommendations': [],
            'pass_status': False
        }
        
        lines = response.split('\n')
        in_recommendations = False
        in_checklist = False
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('OVERALL_SCORE:'):
                try:
                    score_str = line.replace('OVERALL_SCORE:', '').strip()
                    validation_data['overall_score'] = float(score_str.split('/')[0])
                except:
                    validation_data['overall_score'] = 75.0
            elif 'Keyword Usage:' in line:
                try:
                    validation_data['keyword_score'] = float(line.split(':')[1].strip().split('/')[0])
                except:
                    pass
            elif 'Heading Structure:' in line:
                try:
                    validation_data['heading_score'] = float(line.split(':')[1].strip().split('/')[0])
                except:
                    pass
            elif 'Content Length:' in line:
                try:
                    validation_data['length_score'] = float(line.split(':')[1].strip().split('/')[0])
                except:
                    pass
            elif 'Readability:' in line:
                try:
                    validation_data['readability_score'] = float(line.split(':')[1].strip().split('/')[0])
                except:
                    pass
            elif 'Topic Relevance:' in line:
                try:
                    validation_data['relevance_score'] = float(line.split(':')[1].strip().split('/')[0])
                except:
                    pass
            elif 'Search Intent:' in line:
                try:
                    validation_data['intent_score'] = float(line.split(':')[1].strip().split('/')[0])
                except:
                    pass
            elif line.startswith('PASS_STATUS:'):
                validation_data['pass_status'] = 'PASS' in line.upper()
            elif line.startswith('VALIDATION_CHECKLIST:'):
                in_checklist = True
                in_recommendations = False
            elif line.startswith('RECOMMENDATIONS:'):
                in_recommendations = True
                in_checklist = False
            elif in_checklist and ('✓' in line or '✗' in line):
                passed = '✓' in line
                item_name = line.replace('✓', '').replace('✗', '').strip()
                validation_data['validation_checklist'][item_name] = passed
            elif in_recommendations and line and line[0].isdigit():
                rec = line.split('.', 1)[-1].strip() if '.' in line else line
                validation_data['recommendations'].append(rec)
        
        return SEOValidation(**validation_data)
