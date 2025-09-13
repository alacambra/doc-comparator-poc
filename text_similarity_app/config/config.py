DEFAULT_CONFIG = {
    "default_model": "all-MiniLM-L6-v2",
    "max_text_length": 10000,
    "similarity_thresholds": {
        "very_similar": 0.8,
        "moderately_similar": 0.6,
        "somewhat_similar": 0.3
    },
    "colors": {
        "very_similar": "#28a745",
        "moderately_similar": "#ffc107", 
        "somewhat_similar": "#17a2b8",
        "not_similar": "#dc3545"
    },
    "display_options": {
        "show_gauge_default": True,
        "show_percentage_default": True,
        "show_processing_time_default": True,
        "max_history_items": 5
    },
    "preprocessing": {
        "lowercase_default": False,
        "remove_punctuation_default": False
    }
}

STREAMLIT_CONFIG = {
    "page_title": "Text Similarity Analyzer",
    "page_icon": "📊",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

MODEL_DESCRIPTIONS = {
    "all-MiniLM-L6-v2": {
        "name": "MiniLM L6 v2",
        "description": "Fast and efficient model, good balance of speed and accuracy",
        "dimensions": 384,
        "max_seq_length": 256,
        "recommended_for": "General purpose, quick comparisons"
    },
    "all-mpnet-base-v2": {
        "name": "MPNet Base v2", 
        "description": "High-quality model with better accuracy, slower processing",
        "dimensions": 768,
        "max_seq_length": 384,
        "recommended_for": "High accuracy requirements"
    },
    "all-distilroberta-v1": {
        "name": "DistilRoBERTa v1",
        "description": "RoBERTa-based model, good for semantic search",
        "dimensions": 768,
        "max_seq_length": 512,
        "recommended_for": "Semantic search, longer texts"
    },
    "paraphrase-multilingual-MiniLM-L12-v2": {
        "name": "Multilingual MiniLM",
        "description": "Multilingual model supporting 50+ languages",
        "dimensions": 384,
        "max_seq_length": 128,
        "recommended_for": "Multi-language text comparison"
    },
    "paraphrase-albert-small-v2": {
        "name": "ALBERT Small v2",
        "description": "Lightweight model, fastest processing",
        "dimensions": 768,
        "max_seq_length": 100,
        "recommended_for": "Speed-critical applications"
    }
}