import streamlit as st
import pandas as pd
from pathlib import Path

def load_css() -> str:
    """Load CSS once at startup."""
    return Path('styles.css').read_text()

def format_objective(text: str) -> str:
    """Format semicolon-separated text into bullet points."""
    items = text.split(';')
    return f"<ul>{''.join([f'<li>{item.strip()}</li>' for item in items])}</ul>"

def create_table_html(df: pd.DataFrame, css: str) -> str:
    """Create HTML table with embedded CSS for downloads."""
    df = df.copy()
    df['Objective'] = df['Objective'].apply(format_objective)
    
    return f"""
    <style>{css}</style>
    <div class="table-container">
        {df.to_html(index=False, escape=False, classes='styled-table dataframe')}
    </div>
    """

def main():
    st.set_page_config(layout="wide", page_title="Clinical Trials Visualizer")
    
    # Load CSS
    css = load_css()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    
    st.title("Clinical Trials Table Visualizer")
    
    if uploaded_file := st.file_uploader("Upload CSV file", type=['csv']):
        df = pd.read_csv(uploaded_file)
        
        # Display table
        table_html = create_table_html(df, css)
        components.html(table_html, height=600, scrolling=True)
        
        # Download options
        st.markdown("### Download Options")
        left, right = st.columns(2)
        left.download_button(
            "Download HTML", 
            table_html, 
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