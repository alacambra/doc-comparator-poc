# Text Similarity Analyzer

A comprehensive Streamlit application for analyzing semantic similarity between texts using advanced sentence transformer models.

## Features

### Core Functionality
- **Semantic Similarity Analysis**: Uses state-of-the-art Sentence-BERT embeddings for accurate similarity measurement
- **Multiple Model Support**: Choose from 5 different pre-trained models optimized for various use cases
- **Real-time Processing**: Fast similarity calculation with visual feedback
- **Batch Processing**: Upload CSV files for bulk text comparison

### User Interface
- **Clean, Professional Design**: Intuitive interface with responsive layout
- **Interactive Visualizations**: Gauge charts, progress bars, and similarity history graphs
- **File Upload Support**: Direct .txt file upload for both single and batch comparisons
- **Export Capabilities**: Download detailed reports in multiple formats

### Advanced Features
- **Model Caching**: Efficient model loading and caching for improved performance
- **Text Preprocessing**: Optional lowercase conversion and punctuation removal
- **Comparison History**: Track and visualize your last 5 comparisons
- **Color-coded Results**: Visual interpretation of similarity levels

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or download the project**:
   ```bash
   git clone <repository-url>
   cd text_similarity_app
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Access the app**: Open your browser and navigate to `http://localhost:8501`

## Usage Guide

### Single Text Comparison

1. **Select a Model**: Choose from the sidebar dropdown based on your needs:
   - `all-MiniLM-L6-v2`: Best balance of speed and accuracy (recommended)
   - `all-mpnet-base-v2`: Highest accuracy, slower processing
   - `all-distilroberta-v1`: Good for longer texts
   - `paraphrase-multilingual-MiniLM-L12-v2`: Multi-language support
   - `paraphrase-albert-small-v2`: Fastest processing

2. **Input Text**: 
   - Type directly into the text areas, or
   - Upload .txt files using the file uploaders, or
   - Use quick-start examples for demonstration

3. **Configure Options** (optional):
   - Enable text preprocessing (lowercase, punctuation removal)
   - Adjust display options (gauge chart, percentage, processing time)

4. **Analyze**: Click "Analyze Similarity" to process the texts

5. **View Results**:
   - Similarity score (0.000 to 1.000)
   - Percentage equivalent
   - Color-coded interpretation
   - Interactive gauge visualization
   - Processing time

6. **Export**: Download a detailed analysis report

### Batch Processing

1. **Prepare CSV File**: Create a CSV with `text1` and `text2` columns
   ```csv
   text1,text2
   "First text here","Second text here"
   "Another text","Comparison text"
   ```

2. **Upload File**: Use the file uploader in the "Batch Comparison" tab

3. **Process**: Click "Analyze All Pairs" to process all comparisons

4. **Review Results**: View summary statistics, distribution charts, and detailed results table

5. **Export**: Download results as CSV or JSON

### History Tracking

- View your last 5 comparisons in the "History" tab
- See trends in your similarity scores over time
- Clear history when needed

## Model Information

### Available Models

| Model | Speed | Accuracy | Use Case | Dimensions |
|-------|-------|----------|----------|------------|
| MiniLM L6 v2 | Fast | Good | General purpose | 384 |
| MPNet Base v2 | Slow | Excellent | High accuracy needs | 768 |
| DistilRoBERTa v1 | Medium | Good | Longer texts | 768 |
| Multilingual MiniLM | Fast | Good | Multi-language | 384 |
| ALBERT Small v2 | Very Fast | Fair | Speed critical | 768 |

### Similarity Score Interpretation

- **0.8 - 1.0**: Very Similar (Green) - Texts are semantically very close
- **0.6 - 0.8**: Moderately Similar (Yellow) - Texts share significant meaning
- **0.3 - 0.6**: Somewhat Similar (Blue) - Texts have some semantic overlap
- **0.0 - 0.3**: Not Similar (Red) - Texts are semantically distinct

## Technical Details

### Architecture
```
text_similarity_app/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies  
├── README.md             # This file
├── utils/
│   ├── similarity.py     # Core similarity calculation functions
│   └── helpers.py        # UI helpers and utility functions
├── examples/
│   └── sample_texts.py   # Example text pairs for demonstration
└── config/
    └── config.py         # Configuration settings and model info
```

### Performance
- **Model Loading**: < 10 seconds on first run (cached afterwards)
- **Similarity Calculation**: < 3 seconds for typical text pairs
- **Memory Usage**: < 1GB for most models
- **Supported Text Length**: Up to 10,000 characters per text

### Dependencies
- `streamlit`: Web application framework
- `sentence-transformers`: Semantic similarity models
- `numpy`: Numerical computations
- `pandas`: Data manipulation
- `plotly`: Interactive visualizations
- `scikit-learn`: Cosine similarity calculation

## Troubleshooting

### Common Issues

1. **Model Download Slow**: 
   - Models are downloaded on first use
   - Ensure stable internet connection
   - Consider using smaller models for faster startup

2. **Memory Issues**:
   - Use lighter models (MiniLM or ALBERT)
   - Process shorter texts
   - Restart the application if needed

3. **File Upload Errors**:
   - Ensure files are in .txt format
   - Check file encoding (UTF-8 recommended)
   - Verify file is not corrupted

4. **Slow Processing**:
   - Try smaller models
   - Reduce text length
   - Check system resources

### Error Messages

- **"Empty text detected"**: Ensure both text fields contain content
- **"Only .txt files are supported"**: Upload files with .txt extension
- **"CSV must contain 'text1' and 'text2' columns"**: Check CSV format

## Example Use Cases

### Academic Research
- Compare research papers for similarity
- Analyze paraphrasing in student work
- Identify duplicate content

### Content Creation
- Check content originality
- Compare different versions of text
- Analyze competitor content

### Customer Support
- Match customer queries to knowledge base
- Identify similar support tickets
- Automate response suggestions

### Legal & Compliance
- Compare contract versions
- Identify similar legal documents
- Check policy compliance

## Advanced Configuration

### Environment Variables
```bash
# Optional: Set custom model cache directory
export SENTENCE_TRANSFORMERS_HOME=/path/to/cache

# Optional: Set CUDA device for GPU acceleration
export CUDA_VISIBLE_DEVICES=0
```

### Streamlit Configuration
Create `.streamlit/config.toml` for custom settings:
```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"

[server]
maxUploadSize = 50
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

For issues, questions, or feature requests:
1. Check the troubleshooting section above
2. Search existing issues on GitHub
3. Create a new issue with detailed description

## Changelog

### v1.0.0
- Initial release with core similarity functionality
- Support for 5 sentence transformer models
- Single and batch comparison modes
- Interactive visualizations and history tracking
- File upload and export capabilities