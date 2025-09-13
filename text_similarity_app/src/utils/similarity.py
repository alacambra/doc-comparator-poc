import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import time
from typing import Tuple, Optional

@st.cache_resource
def load_model(model_name: str) -> SentenceTransformer:
    """Load and cache the sentence transformer model."""
    return SentenceTransformer(model_name)

def preprocess_text(text: str, lowercase: bool = False, remove_punctuation: bool = False) -> str:
    """Preprocess text based on selected options."""
    if lowercase:
        text = text.lower()
    
    if remove_punctuation:
        import string
        text = text.translate(str.maketrans('', '', string.punctuation))
    
    return text.strip()

def calculate_similarity(text1: str, text2: str, model_name: str = 'all-MiniLM-L6-v2', 
                        preprocess_options: dict = None) -> Tuple[float, float, str, dict]:
    """
    Calculate semantic similarity between two texts using sentence transformers.
    
    Returns:
        tuple: (similarity_score, processing_time, interpretation, token_info)
    """
    if not text1.strip() or not text2.strip():
        return 0.0, 0.0, "Empty text detected", {}
    
    start_time = time.time()
    
    # Preprocess texts if options provided
    if preprocess_options:
        text1 = preprocess_text(text1, **preprocess_options)
        text2 = preprocess_text(text2, **preprocess_options)
    
    # Load model
    model = load_model(model_name)
    
    # Tokenize texts to get token counts
    tokenizer = model.tokenizer
    tokens1 = tokenizer.encode(text1)
    tokens2 = tokenizer.encode(text2)
    
    # Get model's max sequence length
    max_seq_length = model.get_max_seq_length()
    
    # Create token info
    token_info = {
        'text1_tokens': len(tokens1),
        'text2_tokens': len(tokens2),
        'total_tokens': len(tokens1) + len(tokens2),
        'max_seq_length': max_seq_length
    }
    
    # Generate embeddings
    embeddings = model.encode([text1, text2])
    
    # Calculate cosine similarity
    similarity_matrix = cosine_similarity([embeddings[0]], [embeddings[1]])
    similarity_score = float(similarity_matrix[0][0])
    
    processing_time = time.time() - start_time
    
    # Interpret similarity score
    interpretation = get_similarity_interpretation(similarity_score)
    
    return similarity_score, processing_time, interpretation, token_info

def get_similarity_interpretation(score: float) -> str:
    """Get human-readable interpretation of similarity score."""
    if score > 0.8:
        return "Very Similar"
    elif score > 0.6:
        return "Moderately Similar"
    elif score > 0.3:
        return "Somewhat Similar"
    else:
        return "Not Similar"

def get_similarity_color(score: float) -> str:
    """Get color code for similarity score visualization."""
    if score > 0.8:
        return "#28a745"  # Green
    elif score > 0.6:
        return "#ffc107"  # Yellow
    elif score > 0.3:
        return "#17a2b8"  # Blue
    else:
        return "#dc3545"  # Red

def calculate_batch_similarity(text_pairs: list, model_name: str = 'all-MiniLM-L6-v2') -> list:
    """Calculate similarity for multiple text pairs."""
    results = []
    model = load_model(model_name)
    
    for i, (text1, text2) in enumerate(text_pairs):
        if text1.strip() and text2.strip():
            start_time = time.time()
            embeddings = model.encode([text1, text2])
            similarity_matrix = cosine_similarity([embeddings[0]], [embeddings[1]])
            similarity_score = float(similarity_matrix[0][0])
            processing_time = time.time() - start_time
            
            results.append({
                'pair_id': i + 1,
                'text1': text1[:100] + '...' if len(text1) > 100 else text1,
                'text2': text2[:100] + '...' if len(text2) > 100 else text2,
                'similarity_score': similarity_score,
                'similarity_percentage': similarity_score * 100,
                'interpretation': get_similarity_interpretation(similarity_score),
                'processing_time': processing_time
            })
        else:
            results.append({
                'pair_id': i + 1,
                'text1': text1[:100] + '...' if len(text1) > 100 else text1,
                'text2': text2[:100] + '...' if len(text2) > 100 else text2,
                'similarity_score': 0.0,
                'similarity_percentage': 0.0,
                'interpretation': 'Empty text detected',
                'processing_time': 0.0
            })
    
    return results