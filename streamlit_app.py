import streamlit as st
import pandas as pd
from pathlib import Path

def load_resources() -> tuple[str, str]:
    """Load CSS and JavaScript from files."""
    css = Path('styles.css').read_text()
    js = Path('table.js').read_text()
    return css, js

def format_objective(text: str) -> str:
    """Format semicolon-separated text into bullet points."""
    items = text.split(';')
    return f"<ul>{''.join([f'<li>{item.strip()}</li>' for item in items])}</ul>"

def main():
    st.set_page_config(layout="wide", page_title="Clinical Trials Visualizer")
    
    # Load resources
    css, js = load_resources()
    
    # Inject CSS
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    
    # Inject JavaScript using components
    st.components.v1.html(f"<script>{js}</script>", height=0)
    
    st.title("Clinical Trials Table Visualizer")
    
    if uploaded_file := st.file_uploader("Upload CSV file", type=['csv']):
        df = pd.read_csv(uploaded_file)
        
        # Format the Objective column
        df_display = df.copy()
        df_display['Objective'] = df_display['Objective'].apply(format_objective)
        
        # Display table
        st.markdown(
            f'<div class="table-container">{df_display.to_html(index=False, escape=False, classes="styled-table dataframe")}</div>', 
            unsafe_allow_html=True
        )
        
        # Download options
        st.markdown("### Download Options")
        left, right = st.columns(2)
        
        # For HTML download, use the formatted version
        downloadable_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>{css}</style>
        </head>
        <body>
            <div class="table-container">
                {df_display.to_html(index=False, escape=False, classes='styled-table dataframe')}
            </div>
            <script>{js}</script>
        </body>
        </html>
        """
        
        left.download_button(
            "Download HTML", 
            downloadable_html, 
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