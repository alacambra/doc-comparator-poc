def get_example_pairs():
    """Return example text pairs for demonstration."""
    
    examples = {
        "Identical": [
            "The quick brown fox jumps over the lazy dog.",
            "The quick brown fox jumps over the lazy dog."
        ],
        
        "Paraphrased": [
            "Climate change is one of the most pressing issues of our time, requiring immediate global action.",
            "Global warming represents a critical challenge that demands urgent worldwide intervention."
        ],
        
        "Similar Topic": [
            "Machine learning algorithms can process vast amounts of data to identify patterns and make predictions.",
            "Artificial intelligence systems use computational methods to analyze information and forecast outcomes."
        ],
        
        "Different": [
            "The recipe calls for two cups of flour, one egg, and a pinch of salt.",
            "The stock market experienced significant volatility due to economic uncertainty."
        ]
    }
    
    return examples

def get_sample_csv_content():
    """Return sample CSV content for batch processing demonstration."""
    
    csv_content = """text1,text2
"The weather is beautiful today.","Today's weather is lovely."
"I love reading books in my spare time.","Reading novels is my favorite hobby."
"The cat sat on the mat.","A feline rested on the rug."
"Technology is advancing rapidly.","Scientific progress is accelerating."
"The ocean waves crashed against the shore.","Grocery shopping can be time-consuming."
"""
    
    return csv_content