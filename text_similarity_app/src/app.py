import streamlit as st
import pandas as pd
import plotly.express as px
from utils.similarity import calculate_similarity, calculate_batch_similarity, get_similarity_color
from utils.helpers import (
    create_similarity_gauge, create_history_chart, save_comparison_history,
    generate_report, load_file_content, export_batch_results, validate_text_input,
    get_available_models, display_model_info
)
from examples.sample_texts import get_example_pairs
from config.config import DEFAULT_CONFIG
import io

def main():
    st.set_page_config(
        page_title="Text Similarity Analyzer",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("📊 Text Similarity Analyzer")
    st.markdown("### Compare the semantic similarity between two texts using advanced AI models")
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")
    
    # Model selection
    available_models = get_available_models()
    selected_model = st.sidebar.selectbox(
        "Select Model",
        available_models,
        index=0,
        help="Choose the sentence transformer model for analysis"
    )
    
    display_model_info(selected_model)
    
    # Processing options
    st.sidebar.subheader("Text Processing Options")
    lowercase = st.sidebar.checkbox("Convert to lowercase", value=False)
    remove_punctuation = st.sidebar.checkbox("Remove punctuation", value=False)
    
    preprocess_options = {
        'lowercase': lowercase,
        'remove_punctuation': remove_punctuation
    }
    
    # Display options
    st.sidebar.subheader("Display Options")
    show_gauge = st.sidebar.checkbox("Show similarity gauge", value=True)
    show_percentage = st.sidebar.checkbox("Show percentage", value=True)
    show_processing_time = st.sidebar.checkbox("Show processing time", value=True)
    
    # Main interface tabs
    tab1, tab2, tab3 = st.tabs(["📝 Single Comparison", "📁 Batch Comparison", "📈 History"])
    
    with tab1:
        single_comparison_interface(selected_model, preprocess_options, show_gauge, 
                                  show_percentage, show_processing_time)
    
    with tab2:
        batch_comparison_interface(selected_model)
    
    with tab3:
        history_interface()

def single_comparison_interface(model_name, preprocess_options, show_gauge, 
                              show_percentage, show_processing_time):
    """Interface for single text comparison."""
    
    # Example texts section
    st.subheader("📋 Quick Start Examples")
    example_pairs = get_example_pairs()
    
    cols = st.columns(len(example_pairs))
    for i, (name, pair) in enumerate(example_pairs.items()):
        with cols[i]:
            if st.button(f"Load {name}", key=f"example_{i}"):
                st.session_state.text1 = pair[0]
                st.session_state.text2 = pair[1]
    
    # Text input section
    st.subheader("📝 Text Input")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Text 1**")
        text1 = st.text_area(
            "Enter first text",
            height=300,
            placeholder="Enter your first text here...",
            key="text1",
            label_visibility="collapsed"
        )
        
        # File upload for text 1
        uploaded_file1 = st.file_uploader(
            "Upload file for Text 1",
            type=['txt'],
            key="upload1"
        )
        
        if uploaded_file1:
            file_content1 = load_file_content(uploaded_file1)
            if file_content1:
                st.session_state.text1 = file_content1
                st.rerun()
        
        if text1:
            st.caption(f"Characters: {len(text1)}")
    
    with col2:
        st.markdown("**Text 2**")
        text2 = st.text_area(
            "Enter second text",
            height=300,
            placeholder="Enter your second text here...",
            key="text2",
            label_visibility="collapsed"
        )
        
        # File upload for text 2
        uploaded_file2 = st.file_uploader(
            "Upload file for Text 2",
            type=['txt'],
            key="upload2"
        )
        
        if uploaded_file2:
            file_content2 = load_file_content(uploaded_file2)
            if file_content2:
                st.session_state.text2 = file_content2
                st.rerun()
        
        if text2:
            st.caption(f"Characters: {len(text2)}")
    
    # Control buttons
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        analyze_button = st.button("🔍 Analyze Similarity", type="primary")
    
    with col2:
        clear_button = st.button("🗑️ Clear All")
    
    if clear_button:
        st.session_state.text1 = ""
        st.session_state.text2 = ""
        st.rerun()
    
    # Analysis and results
    if analyze_button:
        if not validate_text_input(text1) or not validate_text_input(text2):
            st.error("Please enter text in both fields before analyzing.")
        else:
            with st.spinner("Analyzing similarity..."):
                similarity_score, processing_time, interpretation, token_info = calculate_similarity(
                    text1, text2, model_name, preprocess_options
                )
                
                # Save to history
                save_comparison_history(text1, text2, similarity_score, interpretation, processing_time)
                
                # Display results
                display_single_results(similarity_score, interpretation, processing_time, 
                                     get_similarity_color(similarity_score), show_gauge, 
                                     show_percentage, show_processing_time, token_info)
                
                # Download report
                report = generate_report(text1, text2, similarity_score, interpretation, 
                                       processing_time, model_name)
                
                st.download_button(
                    label="📄 Download Report",
                    data=report,
                    file_name=f"similarity_report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )

def display_single_results(similarity_score, interpretation, processing_time, color, 
                          show_gauge, show_percentage, show_processing_time, token_info=None):
    """Display results for single comparison."""
    
    st.subheader("📊 Results")
    
    # Main metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Similarity Score",
            value=f"{similarity_score:.3f}"
        )
    
    with col2:
        if show_percentage:
            st.metric(
                label="Percentage",
                value=f"{similarity_score * 100:.1f}%"
            )
    
    with col3:
        st.metric(
            label="Interpretation",
            value=interpretation
        )
    
    with col4:
        if show_processing_time:
            st.metric(
                label="Processing Time",
                value=f"{processing_time:.3f}s"
            )
    
    # Progress bar
    st.progress(min(similarity_score, 1.0), text=f"Similarity: {similarity_score:.1%}")
    
    # Token information
    if token_info:
        st.subheader("🔢 Token Analysis")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Text 1 Tokens",
                value=token_info['text1_tokens']
            )
        
        with col2:
            st.metric(
                label="Text 2 Tokens", 
                value=token_info['text2_tokens']
            )
        
        with col3:
            st.metric(
                label="Total Tokens",
                value=token_info['total_tokens']
            )
        
        with col4:
            st.metric(
                label="Model Limit",
                value=token_info['max_seq_length']
            )
        
    
    # Gauge chart
    if show_gauge:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            gauge_fig = create_similarity_gauge(similarity_score, interpretation, color)
            st.plotly_chart(gauge_fig, use_container_width=True)

def batch_comparison_interface(model_name):
    """Interface for batch text comparison."""
    
    st.subheader("📁 Batch Text Comparison")
    st.markdown("Upload a CSV file with 'text1' and 'text2' columns for batch processing.")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload CSV file",
        type=['csv'],
        help="CSV should have 'text1' and 'text2' columns"
    )
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            
            if 'text1' not in df.columns or 'text2' not in df.columns:
                st.error("CSV file must contain 'text1' and 'text2' columns")
                return
            
            st.success(f"Loaded {len(df)} text pairs")
            
            if st.button("🔍 Analyze All Pairs", type="primary"):
                with st.spinner("Processing batch comparison..."):
                    text_pairs = [(row['text1'], row['text2']) for _, row in df.iterrows()]
                    results = calculate_batch_similarity(text_pairs, model_name)
                    
                    # Display results
                    results_df = pd.DataFrame(results)
                    
                    st.subheader("📊 Batch Results")
                    st.dataframe(results_df, use_container_width=True)
                    
                    # Summary statistics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Pairs", len(results))
                    with col2:
                        st.metric("Avg Similarity", f"{results_df['similarity_score'].mean():.3f}")
                    with col3:
                        st.metric("Max Similarity", f"{results_df['similarity_score'].max():.3f}")
                    with col4:
                        st.metric("Min Similarity", f"{results_df['similarity_score'].min():.3f}")
                    
                    # Visualization
                    fig = px.histogram(
                        results_df, 
                        x='similarity_score',
                        nbins=20,
                        title="Distribution of Similarity Scores"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Download options
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        csv_data = export_batch_results(results, 'csv')
                        st.download_button(
                            label="📄 Download CSV",
                            data=csv_data,
                            file_name=f"batch_results_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                    
                    with col2:
                        json_data = export_batch_results(results, 'json')
                        st.download_button(
                            label="📄 Download JSON",
                            data=json_data,
                            file_name=f"batch_results_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
        
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

def history_interface():
    """Interface for viewing comparison history."""
    
    st.subheader("📈 Comparison History")
    
    if 'comparison_history' not in st.session_state or not st.session_state.comparison_history:
        st.info("No comparison history available. Perform some comparisons to see history here.")
        return
    
    history = st.session_state.comparison_history
    
    # Display history table
    history_df = pd.DataFrame(history)
    st.dataframe(history_df, use_container_width=True)
    
    # History chart
    if len(history) > 1:
        chart_fig = create_history_chart(history)
        if chart_fig:
            st.plotly_chart(chart_fig, use_container_width=True)
    
    # Clear history button
    if st.button("🗑️ Clear History"):
        st.session_state.comparison_history = []
        st.rerun()

if __name__ == "__main__":
    main()