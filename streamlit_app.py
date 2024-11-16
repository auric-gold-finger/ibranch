import streamlit as st
import pandas as pd
from pathlib import Path

def load_css() -> str:
    """Load CSS once at startup."""
    return Path('styles.css').read_text()

def main():
    st.set_page_config(layout="wide", page_title="Clinical Trials Visualizer")
    
    # Load and inject CSS
    css = load_css()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    
    st.title("Clinical Trials Table Visualizer")
    
    if uploaded_file := st.file_uploader("Upload CSV file", type=['csv']):
        df = pd.read_csv(uploaded_file)
        
        # Create and display table
        st.markdown(f"""
            <div class="table-container">
                {df.to_html(index=False, escape=False, classes='styled-table dataframe')}
            </div>
        """, unsafe_allow_html=True)
        
        # Download options
        st.markdown("### Download Options")
        left, right = st.columns(2)
        left.download_button(
            "Download HTML", 
            df.to_html(index=False, escape=False), 
            "table.html", 
            "text/html"
        )
        right.download_button(
            "Download CSV", 
            df.to_csv(index=False), 
            "table.csv", 
            "text/csv"
        )
    else:
        st.warning("Please upload a CSV file to begin.")

if __name__ == "__main__":
    main()