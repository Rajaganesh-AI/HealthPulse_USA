"""
Healthcare Topics Configuration
Defines the hierarchical dropdown structure for topic selection
"""

from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class TopicCategory:
    """Represents a topic category with subcategories"""
    name: str
    subcategories: Dict[str, List[str]]
    
    def get_all_topics(self) -> List[str]:
        """Get all topics including subcategories"""
        all_topics = []
        for sub_name, topics in self.subcategories.items():
            all_topics.extend(topics)
        return all_topics

# Trusted US Healthcare Sources
TRUSTED_SOURCES = [
    "CMS (Centers for Medicare & Medicaid Services)",
    "CDC (Centers for Disease Control and Prevention)",
    "HHS (Department of Health and Human Services)",
    "NIH (National Institutes of Health)",
    "Kaiser Family Foundation",
    "Healthcare.gov",
    "AMA (American Medical Association)",
    "AHA (American Hospital Association)",
    "AHRQ (Agency for Healthcare Research and Quality)",
    "FDA (Food and Drug Administration)"
]

# Healthcare Topic Hierarchy
TOPIC_HIERARCHY = {
    "GOVERNMENT PLANS": {
        "ALL": ["Medicare", "Medicaid", "ACA"],
        "Medicare": {
            "ALL": ["Part A", "Part B", "Part C (Medicare Advantage)", "Part D", "Medigap", "Tricare", "VA Healthcare"],
            "Part A": ["Hospital Insurance", "Inpatient Care", "Skilled Nursing", "Hospice"],
            "Part B": ["Medical Insurance", "Outpatient Care", "Preventive Services", "Durable Medical Equipment"],
            "Part C (Medicare Advantage)": ["HMO Plans", "PPO Plans", "Special Needs Plans", "Private Fee-for-Service"],
            "Part D": ["Prescription Drug Coverage", "Formulary", "Coverage Gap", "Extra Help Program"],
            "Medigap": ["Supplement Insurance", "Policy Types", "Enrollment Periods"],
            "Tricare": ["Military Healthcare", "Tricare Prime", "Tricare Select", "Tricare for Life"],
            "VA Healthcare": ["Veterans Benefits", "Priority Groups", "VA Medical Centers"]
        },
        "Medicaid": {
            "ALL": ["Medicaid Expansion", "CHIP"],
            "Medicaid Expansion": ["State Programs", "Eligibility", "Covered Services"],
            "CHIP": ["Children's Health Insurance", "State CHIP Programs", "Eligibility Requirements"]
        },
        "ACA": ["Marketplace Plans", "Essential Health Benefits", "Subsidies", "Open Enrollment"]
    },
    "COMMERCIAL PLANS": {
        "ALL": ["HMO", "PPO", "EPO", "POS", "HDHP", "Catastrophic Plans"],
        "HMO": ["Health Maintenance Organization", "Network Requirements", "Primary Care Physician", "Referral System"],
        "PPO": ["Preferred Provider Organization", "In-Network vs Out-of-Network", "Flexibility Options"],
        "EPO": ["Exclusive Provider Organization", "Network-Only Coverage", "Cost Structure"],
        "POS": ["Point of Service", "Hybrid Plans", "Referral Options"],
        "HDHP": ["High Deductible Health Plans", "HSA Compatibility", "Cost Savings", "Preventive Care"],
        "Catastrophic Plans": ["Young Adult Coverage", "Hardship Exemptions", "Essential Benefits"]
    },
    "SUPPLEMENTAL PLANS": {
        "ALL": ["Dental", "Vision", "Prescription Drugs Only"],
        "Dental": ["Dental Insurance", "Preventive Care", "Major Services", "Orthodontics"],
        "Vision": ["Vision Insurance", "Eye Exams", "Glasses and Contacts", "LASIK Coverage"],
        "Prescription Drugs Only": ["Standalone Drug Plans", "Formulary Tiers", "Prior Authorization"]
    },
    "EXCHANGE": {
        "ALL": ["On-Exchange", "Off-Exchange"],
        "On-Exchange": ["Marketplace Plans", "Premium Tax Credits", "Cost-Sharing Reductions", "Special Enrollment"],
        "Off-Exchange": ["Private Plans", "Direct Enrollment", "Broker-Sold Plans"]
    },
    "CODES": {
        "ALL": ["ICD-10-CM", "CPT", "HCPCS", "ICD-10-PCS", "NDC", "DRG", "Revenue Codes", "CDT", "Modifiers"],
        "Diagnosis – ICD-10-CM": ["Diagnosis Coding", "ICD-10-CM Updates", "Clinical Documentation", "Coding Guidelines"],
        "Procedures – CPT": ["Procedure Codes", "Evaluation and Management", "Surgical Codes", "CPT Updates"],
        "Supplies – HCPCS": ["Medical Supplies", "Durable Medical Equipment", "Level II Codes", "Billing Guidelines"],
        "InPatient – ICD-10-PCS": ["Inpatient Procedure Coding", "Body Systems", "Root Operations", "Device Coding"],
        "Drugs – NDC": ["National Drug Code", "Drug Identification", "FDA Database", "Reimbursement"],
        "Payment – DRG": ["Diagnosis Related Groups", "Hospital Reimbursement", "Case Mix Index", "Severity Levels"],
        "Facility – Revenue Codes": ["Revenue Cycle", "UB-04 Billing", "Charge Capture", "Payer Requirements"],
        "Dental – CDT": ["Dental Procedure Codes", "ADA Codes", "Dental Documentation"],
        "Rules – Modifiers": ["CPT Modifiers", "HCPCS Modifiers", "Correct Modifier Usage", "Modifier Guidelines"]
    },
    "ALL": {
        "ALL": ["Government Plans", "Commercial Plans", "Supplemental Plans", "Exchange", "Codes"]
    }
}

def get_main_categories() -> List[str]:
    """Get list of main category names"""
    return list(TOPIC_HIERARCHY.keys())

def get_subcategories(main_category: str) -> List[str]:
    """Get subcategories for a main category"""
    if main_category in TOPIC_HIERARCHY:
        return list(TOPIC_HIERARCHY[main_category].keys())
    return []

def get_specific_topics(main_category: str, subcategory: str) -> List[str]:
    """Get specific topics for a subcategory"""
    if main_category in TOPIC_HIERARCHY:
        category_data = TOPIC_HIERARCHY[main_category]
        if subcategory in category_data:
            sub_data = category_data[subcategory]
            if isinstance(sub_data, dict):
                return list(sub_data.keys())
            elif isinstance(sub_data, list):
                return sub_data
    return []

def get_detailed_topics(main_category: str, subcategory: str, specific: str) -> List[str]:
    """Get detailed topics for a specific selection"""
    if main_category in TOPIC_HIERARCHY:
        category_data = TOPIC_HIERARCHY[main_category]
        if subcategory in category_data:
            sub_data = category_data[subcategory]
            if isinstance(sub_data, dict) and specific in sub_data:
                return sub_data[specific]
    return []

def build_topic_query(main_category: str, subcategory: str = "ALL", 
                      specific: str = None, detailed: str = None) -> str:
    """Build a comprehensive topic query string for agents"""
    parts = [main_category]
    
    if subcategory and subcategory != "ALL":
        parts.append(subcategory)
    
    if specific and specific != "ALL":
        parts.append(specific)
        
    if detailed:
        parts.append(detailed)
    
    return " - ".join(parts)

def get_search_keywords(main_category: str, subcategory: str = "ALL") -> List[str]:
    """Get relevant search keywords based on selection"""
    keywords = ["US healthcare", "2024", "2025", "latest", "trending"]
    
    category_keywords = {
        "GOVERNMENT PLANS": ["Medicare", "Medicaid", "ACA", "federal healthcare", "government insurance"],
        "COMMERCIAL PLANS": ["private insurance", "employer coverage", "health plans", "insurance market"],
        "SUPPLEMENTAL PLANS": ["supplemental coverage", "ancillary benefits", "additional insurance"],
        "EXCHANGE": ["marketplace", "health insurance exchange", "open enrollment", "ACA marketplace"],
        "CODES": ["medical coding", "billing codes", "healthcare coding", "reimbursement codes"]
    }
    
    if main_category in category_keywords:
        keywords.extend(category_keywords[main_category])
    
    subcategory_keywords = {
        "Medicare": ["Medicare benefits", "senior healthcare", "65+ insurance"],
        "Medicaid": ["Medicaid eligibility", "state healthcare", "low-income coverage"],
        "ACA": ["Affordable Care Act", "Obamacare", "marketplace plans"],
        "HMO": ["managed care", "network doctors", "HMO benefits"],
        "PPO": ["preferred providers", "out-of-network", "PPO flexibility"],
        "ICD-10-CM": ["diagnosis codes", "clinical classification", "ICD updates"],
        "CPT": ["procedure codes", "CPT changes", "AMA coding"],
        "DRG": ["hospital payment", "case mix", "inpatient reimbursement"]
    }
    
    if subcategory in subcategory_keywords:
        keywords.extend(subcategory_keywords[subcategory])
    
    return keywords

# SEO Configuration
SEO_CONFIG = {
    "min_word_count": 1500,
    "max_word_count": 3000,
    "keyword_density_min": 1.0,
    "keyword_density_max": 3.0,
    "min_headings": 5,
    "max_headings": 12,
    "meta_description_length": 160,
    "title_length_max": 60,
    "readability_target": "grade_8_12",
    "internal_links_min": 3,
    "external_links_min": 2
}

# SEO Scoring Weights
SEO_WEIGHTS = {
    "keyword_usage": 20,
    "heading_structure": 15,
    "content_length": 15,
    "readability": 15,
    "topic_relevance": 15,
    "search_intent": 10,
    "meta_elements": 10
}
