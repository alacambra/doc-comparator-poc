# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a text similarity analysis tool built with Streamlit that compares semantic similarity between texts using sentence transformer models. The main application is located in `text_similarity_app/` directory.

## Development Commands

### Running the Application
```bash
cd text_similarity_app
streamlit run app.py
```

### Setting up Development Environment
```bash
cd text_similarity_app
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Docker Deployment
```bash
cd text_similarity_app
docker build -t text-similarity-app:latest .
docker run -p 8501:8501 text-similarity-app:latest
```

### Kubernetes Deployment
```bash
cd text_similarity_app
kubectl apply -f k8s-deployment.yaml
kubectl apply -f k8s-service.yaml
```

## Architecture

### Core Components

**Main Application (`app.py`)**
- Streamlit UI orchestration and page configuration
- Tab management for Single Comparison, Batch Processing, and History
- Sidebar configuration for model selection and processing options
- Integration point for all utilities and components

**Similarity Engine (`utils/similarity.py`)**
- Model loading and caching using `@st.cache_resource`
- Core similarity calculation with sentence transformers
- Text preprocessing (lowercase, punctuation removal)
- Batch processing for multiple text pairs
- Returns similarity scores, processing time, and interpretation

**UI Helpers (`utils/helpers.py`)**
- Plotly visualizations (gauge charts, history graphs)
- File I/O operations for text and CSV uploads
- Report generation and export functionality
- Model information display utilities

**Configuration (`config/config.py`)**
- Centralized settings for thresholds, colors, and display options
- Model descriptions and capabilities
- Default preprocessing and UI configurations

**Sample Data (`examples/sample_texts.py`)**
- Predefined text pairs for demonstration
- CSV sample content for batch processing examples

### Data Flow

1. **Model Selection**: User chooses from 5 available sentence transformer models via sidebar
2. **Text Input**: Single text pairs via text areas or file upload, batch via CSV upload
3. **Preprocessing**: Optional lowercase conversion and punctuation removal
4. **Similarity Calculation**: 
   - Load/cache model using `@st.cache_resource`
   - Generate embeddings for input texts
   - Calculate cosine similarity between embeddings
   - Interpret score using predefined thresholds
5. **Visualization**: Gauge charts, percentage displays, and color-coded results
6. **History Tracking**: Store last 5 comparisons with trend visualization
7. **Export**: Generate detailed reports and batch results

### Model Architecture

The application supports 5 sentence transformer models:
- `all-MiniLM-L6-v2`: General purpose, balanced speed/accuracy (384 dimensions)
- `all-mpnet-base-v2`: Highest accuracy (768 dimensions) 
- `all-distilroberta-v1`: Good for longer texts (768 dimensions)
- `paraphrase-multilingual-MiniLM-L12-v2`: Multi-language support (384 dimensions)
- `paraphrase-albert-small-v2`: Fastest processing (768 dimensions)

### Caching Strategy

- Models are cached using Streamlit's `@st.cache_resource` to avoid reloading
- First model load takes ~10 seconds, subsequent uses are instant
- Cache persists across user sessions

### Configuration Files

**Streamlit Configuration (`.streamlit/config.toml`)**
- Theme settings with custom colors
- Upload size limits (50MB)
- Security settings (CORS, XSRF protection)

**Docker Configuration**
- Multi-stage build not used - single Python 3.11-slim base
- Exposes port 8501 with health checks
- Copies requirements first for better layer caching

**Kubernetes Configuration**
- Deployment with 2 replicas, resource limits, health probes
- LoadBalancer service exposing port 80 → 8501
- No persistent volumes - stateless application

## Working with This Codebase

### Adding New Models
1. Add model configuration to `MODEL_DESCRIPTIONS` in `config/config.py`
2. Update `get_available_models()` in `utils/helpers.py`
3. Test model loading and similarity calculation

### Modifying Similarity Thresholds
- Update `similarity_thresholds` in `DEFAULT_CONFIG` 
- Adjust corresponding colors in `colors` section
- Update interpretation logic in `get_similarity_interpretation()`

### Adding New Visualizations
- Create new chart functions in `utils/helpers.py` using Plotly
- Follow existing pattern: return `go.Figure` object
- Add to appropriate tab in `app.py`

### File Upload Handling
- Text files: Use `load_file_content()` from helpers
- CSV files: Validate columns 'text1' and 'text2' exist
- All file operations include error handling and user feedback