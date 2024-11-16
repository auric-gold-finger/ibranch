import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from pathlib import Path

def load_resources() -> tuple[str, str]:
    """Load CSS and JavaScript resources."""
    css = Path('styles.css').read_text()
    js = Path('table.js').read_text()
    return css, js

def format_objective(text: str) -> str:
    """Format semicolon-separated text into HTML bullet points."""
    bullets = [f"<span class='bullet'>•</span><span class='bullet-text'>{item.strip()}</span>" 
              for item in text.split(';')]
    return f"<div class='bullet-container'>{'<br>'.join(bullets)}</div>"

def create_table_html(df: pd.DataFrame, css: str, js: str) -> str:
    """Create HTML table with styling and interactivity."""
    df = df.copy()
    df['Objective'] = df['Objective'].apply(format_objective)
    
    return f"""
    <div style="padding: 2rem;">
        <style>{css}</style>
        <script>{js}</script>
        <div class="table-container">
            {df.to_html(index=False, escape=False, classes='styled-table dataframe')}
        </div>
    </div>
    """

def main():
    st.set_page_config(layout="wide", page_title="Clinical Trials Visualizer")
    st.title("Clinical Trials Table Visualizer")
    
    try:
        css, js = load_resources()
    except FileNotFoundError as e:
        st.error(f"Required resource files not found: {e}")
        return
    
    if uploaded_file := st.file_uploader("Upload CSV file", type=['csv']):
        df = pd.read_csv(uploaded_file)
        table_html = create_table_html(df, css, js)
        
        components.html(table_html, height=600, scrolling=True)
        
        # Download options in columns
        st.markdown("### Download Options")
        left, right = st.columns(2)
        left.download_button("Download HTML", table_html, "table.html", "text/html")
        right.download_button("Download CSV", df.to_csv(index=False), "table.csv", "text/csv")
    else:
        st.warning("Please upload a CSV file to begin.")

if __name__ == "__main__":
    main()