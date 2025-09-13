import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Any
import io
import json
from datetime import datetime

def create_similarity_gauge(score: float, interpretation: str, color: str) -> go.Figure:
    """Create a gauge chart for similarity score visualization."""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Similarity: {interpretation}"},
        delta = {'reference': 50},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 30], 'color': "lightgray"},
                {'range': [30, 60], 'color': "gray"},
                {'range': [60, 80], 'color': "lightblue"},
                {'range': [80, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        font={'color': "darkblue", 'family': "Arial"}
    )
    
    return fig

def create_history_chart(history: List[Dict]) -> go.Figure:
    """Create a line chart showing similarity history."""
    if not history:
        return None
    
    df = pd.DataFrame(history)
    
    fig = px.line(
        df, 
        x='timestamp', 
        y='similarity_score',
        title='Similarity Score History',
        labels={'similarity_score': 'Similarity Score', 'timestamp': 'Time'},
        markers=True
    )
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def save_comparison_history(text1: str, text2: str, similarity_score: float, 
                          interpretation: str, processing_time: float) -> None:
    """Save comparison to session state history."""
    if 'comparison_history' not in st.session_state:
        st.session_state.comparison_history = []
    
    comparison = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'text1_preview': text1[:50] + '...' if len(text1) > 50 else text1,
        'text2_preview': text2[:50] + '...' if len(text2) > 50 else text2,
        'similarity_score': similarity_score,
        'similarity_percentage': similarity_score * 100,
        'interpretation': interpretation,
        'processing_time': processing_time
    }
    
    st.session_state.comparison_history.insert(0, comparison)
    
    # Keep only last 5 comparisons
    if len(st.session_state.comparison_history) > 5:
        st.session_state.comparison_history = st.session_state.comparison_history[:5]

def generate_report(text1: str, text2: str, similarity_score: float, 
                   interpretation: str, processing_time: float, model_name: str) -> str:
    """Generate a text report of the similarity analysis."""
    report = f"""
Text Similarity Analysis Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Model Used: {model_name}
Processing Time: {processing_time:.3f} seconds

Text 1 (Length: {len(text1)} characters):
{text1[:200]}{'...' if len(text1) > 200 else ''}

Text 2 (Length: {len(text2)} characters):
{text2[:200]}{'...' if len(text2) > 200 else ''}

RESULTS:
Similarity Score: {similarity_score:.3f}
Similarity Percentage: {similarity_score * 100:.1f}%
Interpretation: {interpretation}

Analysis:
The semantic similarity between the two texts is {interpretation.lower()}.
This score indicates that the texts {'share significant semantic content' if similarity_score > 0.6 else 'have limited semantic overlap' if similarity_score > 0.3 else 'are semantically distinct'}.
"""
    return report

def load_file_content(uploaded_file) -> str:
    """Load content from uploaded file."""
    try:
        if uploaded_file.type == "text/plain":
            content = str(uploaded_file.read(), "utf-8")
            return content
        else:
            st.error("Only .txt files are supported")
            return ""
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return ""

def export_batch_results(results: List[Dict], format_type: str = 'csv') -> bytes:
    """Export batch comparison results in specified format."""
    df = pd.DataFrame(results)
    
    if format_type == 'csv':
        output = io.StringIO()
        df.to_csv(output, index=False)
        return output.getvalue().encode()
    elif format_type == 'json':
        return json.dumps(results, indent=2).encode()
    else:
        raise ValueError("Unsupported format type")

def validate_text_input(text: str, min_length: int = 1) -> bool:
    """Validate text input."""
    return len(text.strip()) >= min_length

def get_available_models() -> List[str]:
    """Get list of available sentence transformer models."""
    return [
        'all-MiniLM-L6-v2',
        'all-mpnet-base-v2',
        'all-distilroberta-v1',
        'paraphrase-multilingual-MiniLM-L12-v2',
        'paraphrase-albert-small-v2'
    ]

def display_model_info(model_name: str) -> None:
    """Display information about the selected model."""
    model_info = {
        'all-MiniLM-L6-v2': {
            'description': 'Fast and efficient model, good balance of speed and accuracy',
            'dimensions': 384,
            'max_seq_length': 256
        },
        'all-mpnet-base-v2': {
            'description': 'High-quality model with better accuracy, slower processing',
            'dimensions': 768,
            'max_seq_length': 384
        },
        'all-distilroberta-v1': {
            'description': 'RoBERTa-based model, good for semantic search',
            'dimensions': 768,
            'max_seq_length': 512
        },
        'paraphrase-multilingual-MiniLM-L12-v2': {
            'description': 'Multilingual model supporting 50+ languages',
            'dimensions': 384,
            'max_seq_length': 128
        },
        'paraphrase-albert-small-v2': {
            'description': 'Lightweight model, fastest processing',
            'dimensions': 768,
            'max_seq_length': 100
        }
    }
    
    if model_name in model_info:
        info = model_info[model_name]
        st.sidebar.info(f"""
        **Model Info:**
        - {info['description']}
        - Embedding dimensions: {info['dimensions']}
        - Max sequence length: {info['max_seq_length']}
        """)