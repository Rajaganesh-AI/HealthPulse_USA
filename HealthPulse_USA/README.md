# 🏥 HealthPulse USA

## Multi-Agent US Healthcare Trending Article Generator

A comprehensive, SEO-optimized content generation platform powered by Microsoft AutoGen's multi-agent framework with Round-Robin orchestration.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-red)
![AutoGen](https://img.shields.io/badge/AutoGen-0.4+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🌟 Features

### Multi-Agent Architecture
- **4 Specialized AI Agents** working in Round-Robin orchestration
- **Trend Discovery Agent**: Fetches latest trending US healthcare topics
- **Content Writer Agent**: Generates SEO-optimized long-form articles
- **SEO Examiner Agent**: Validates content against SEO best practices
- **Consolidator Agent**: Merges outputs into publication-ready format

### Topic Selection
- **Hierarchical Dropdown System** with 6 main categories:
  - Government Plans (Medicare, Medicaid, ACA)
  - Commercial Plans (HMO, PPO, EPO, POS, HDHP)
  - Supplemental Plans (Dental, Vision, Prescription)
  - Exchange (On-Exchange, Off-Exchange)
  - Medical Codes (ICD-10, CPT, HCPCS, DRG, etc.)
  - All Categories Combined

### SEO Optimization
- **Keyword density optimization** (1-3%)
- **Proper heading structure** (H1-H3)
- **Meta description generation**
- **Readability scoring**
- **Topic relevance validation**
- **Search intent alignment**

### Export Options
- **PDF** - Professional document format
- **DOCX** - Microsoft Word compatible
- **TXT** - Plain text format

### Trusted Sources
Content is informed by authoritative US healthcare sources:
- CMS (Centers for Medicare & Medicaid Services)
- CDC (Centers for Disease Control and Prevention)
- HHS (Department of Health and Human Services)
- NIH (National Institutes of Health)
- Kaiser Family Foundation
- Healthcare.gov
- AMA (American Medical Association)
- AHA (American Hospital Association)

---

## 📁 Project Structure

```
healthpulse_usa/
├── app.py                    # Main Streamlit application
├── config.py                 # Topic hierarchy and SEO configuration
├── requirements.txt          # Python dependencies
├── README.md                 # This file
│
├── agents/
│   ├── __init__.py          # Package exports
│   ├── definitions.py       # Agent system prompts and data classes
│   └── orchestrator.py      # AutoGen Round-Robin orchestration
│
└── utils/
    ├── __init__.py          # Package exports
    └── document_export.py   # PDF, DOCX, TXT export utilities
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11.0
- OpenAI API key (optional - demo mode available)

### Installation

1. **Clone/Download the project**
   ```bash
   cd healthpulse_usa
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   - Navigate to `http://localhost:8501`

---

## 💡 Usage

### 1. Configure API Key (Optional)
- Enter your OpenAI API key in the sidebar
- Without an API key, the app runs in demo mode with simulated content

### 2. Select Topic
- Choose a **Main Category** (e.g., "GOVERNMENT PLANS")
- Select a **Subcategory** (e.g., "Medicare")
- Optionally choose a **Specific Topic** (e.g., "Part D")

### 3. Generate Article
- Click **"🚀 Generate SEO Article"**
- Watch the multi-agent pipeline progress
- View the completed article with SEO metrics

### 4. Review & Download
- **Article Tab**: Full content with SEO score
- **SEO Report Tab**: Detailed validation checklist
- **Trending Topic Tab**: Source information
- **Downloads Tab**: Export in PDF, DOCX, or TXT

---

## 🔧 Configuration

### Environment Variables
```bash
OPENAI_API_KEY=your-api-key-here
```

### Model Selection
Choose from available OpenAI models:
- `gpt-4o` (recommended)
- `gpt-4-turbo`
- `gpt-3.5-turbo`

### SEO Scoring Weights
Configured in `config.py`:
```python
SEO_WEIGHTS = {
    "keyword_usage": 20,      # Primary & secondary keyword placement
    "heading_structure": 15,  # H1-H3 hierarchy
    "content_length": 15,     # 1500-3000 words target
    "readability": 15,        # Grade 8-12 reading level
    "topic_relevance": 15,    # Content matches selection
    "search_intent": 10,      # Actionable value
    "meta_elements": 10       # Title & description
}
```

---

## 🏗️ Architecture

### Agent Workflow (Round-Robin)

```
┌─────────────────────────────────────────────────────────────┐
│                     User Input                               │
│              (Topic Selection via Dropdown)                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              AGENT 1: Trend Discovery                        │
│  • Analyzes selected category                                │
│  • Identifies trending topics                                │
│  • Provides keywords and sources                             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              AGENT 2: Content Writer                         │
│  • Generates 1500-3000 word article                          │
│  • Applies SEO best practices                                │
│  • Creates meta description and headings                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              AGENT 3: SEO Examiner                           │
│  • Validates keyword usage                                   │
│  • Checks heading structure                                  │
│  • Calculates SEO score                                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              AGENT 4: Consolidator                           │
│  • Merges all agent outputs                                  │
│  • Prepares final package                                    │
│  • Enables downloads                                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   Streamlit Frontend                         │
│  • Displays article                                          │
│  • Shows SEO score gauge                                     │
│  • Provides download options                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 SEO Validation Criteria

| Category | Max Points | Criteria |
|----------|------------|----------|
| Keyword Usage | 20 | Primary keyword in title, first paragraph, headings |
| Heading Structure | 15 | Single H1, 5+ H2s, proper hierarchy |
| Content Length | 15 | 1500-3000 words |
| Readability | 15 | Short paragraphs, active voice, grade 8-12 |
| Topic Relevance | 15 | Matches selection, comprehensive coverage |
| Search Intent | 10 | Answers questions, actionable content |
| Meta Elements | 10 | 150-160 char description with keywords |

**Pass Threshold: 70/100**

---

## 🔐 Security Notes

- API keys are stored in session state only (not persisted)
- No data is saved to disk by default
- All processing happens locally or via OpenAI API

---

## 📝 License

MIT License - See LICENSE file for details.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📞 Support

For issues or questions:
- Open a GitHub issue
- Reference the AutoGen documentation: https://microsoft.github.io/autogen/stable/

---

## 🙏 Acknowledgments

- **Microsoft AutoGen** - Multi-agent framework
- **Streamlit** - Frontend framework
- **OpenAI** - Language models
- **US Healthcare Sources** - CMS, CDC, HHS, NIH, KFF

---

*Built with ❤️ for healthcare content creators*
