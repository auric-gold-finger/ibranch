import streamlit as st
import pandas as pd
from pathlib import Path
import streamlit.components.v1 as components

def load_resources() -> tuple[str, str]:
    """Load CSS and JavaScript from files."""
    css = Path('styles.css').read_text()
    js = Path('table.js').read_text()
    return css, js

def should_convert_to_list(text: str) -> bool:
    """Determine if text should be converted to bullet points."""
    if not isinstance(text, str) or pd.isna(text):
        return False
    semicolon_count = text.count(';')
    has_spaced_semicolons = '; ' in text
    return semicolon_count > 1 or has_spaced_semicolons

def format_semicolon_text(text: str, force_list: bool = False) -> str:
    """Format text into bullet points if it's a list or forced to be one."""
    if pd.isna(text) or not isinstance(text, str):
        return ""
    if force_list or should_convert_to_list(text):
        if ';' in text:
            items = text.split(';')
        else:
            items = [text]  # Single item list
        return f"<ul>{''.join([f'<li>{item.strip()}</li>' for item in items])}</ul>"
    return text

def render_original_table(df: pd.DataFrame, css: str, js: str):
    """Render table using original HTML/CSS/JS approach."""
    df_display = df.copy()
    for column in df_display.columns:
        # Check if ANY row in this column has semicolon list format
        if df_display[column].astype(str).str.contains(';').any() and \
        df_display[column].apply(should_convert_to_list).any():
            # If yes, format ALL entries in this column as lists
            df_display[column] = df_display[column].apply(lambda x: format_semicolon_text(x, force_list=True))
    
    # Display table
    st.components.v1.html(f"<script>{js}</script>", height=0)
    st.markdown(
        f'<div class="table-container">{df_display.to_html(index=False, escape=False, classes="styled-table dataframe")}</div>', 
        unsafe_allow_html=True
    )
    
    return df_display

def render_styled_table(df: pd.DataFrame):
    """Render table using Pandas Styler approach."""
    # Style the DataFrame
    df_display = df.copy()
    for column in df_display.columns:
        if df_display[column].astype(str).str.contains(';').any():
            df_display[column] = df_display[column].apply(format_semicolon_text)
            
    styled_df = df_display.style\
        .hide(axis='index')\
        .set_properties(**{
            'text-align': 'center',
            'vertical-align': 'middle'
        })\
        .format(na_rep="")\
        .set_table_styles([
            {'selector': 'td', 'props': [
                ('text-align', 'center'),
                ('vertical-align', 'middle')
            ]},
            {'selector': 'td > *', 'props': [
                ('display', 'inline-block'),
                ('text-align', 'center'),
                ('margin', '0 auto')
            ]}
        ])
    
    st.write(styled_df.to_html(escape=False), unsafe_allow_html=True)
    return styled_df

def main():
    st.set_page_config(layout="wide", page_title="Clinical Trials Visualizer")
    
    # Load resources
    css, js = load_resources()
    
    # Inject CSS
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    
    st.title("Clinical Trials Table Visualizer")
    
    if uploaded_file := st.file_uploader("Upload CSV file", type=['csv']):
        # Read CSV and fill NaN values with empty string
        df = pd.read_csv(uploaded_file).fillna("")
        
        # Create tabs
        tab1, tab2 = st.tabs(["Original Style", "Pandas Style"])
        
        with tab1:
            df_display = render_original_table(df, css, js)
            
            # Download options
            st.markdown("### Download Options")
            left, right = st.columns(2)
            
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
            
            # Original style downloads
            left.download_button(
                "Download HTML", 
                downloadable_html, 
                "table.html", 
                "text/html",
                key="html_download_original"  # Add this
            )
            
            right.download_button(
                "Download CSV", 
                df.to_csv(index=False), 
                "table.csv", 
                "text/csv",
                key="csv_download_original"  # Add this
            )
            
        with tab2:
            
            styled_df = render_styled_table(df)
            
            # Download options
            st.markdown("### Download Options")
            left, right = st.columns(2)
            
            styled_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>{css}</style>
            </head>
            <body>
                {styled_df.to_html(escape=False, index=False)}
            </body>
            </html>
            """
            
            # Pandas style downloads
            left.download_button(
                "Download HTML", 
                styled_html, 
                "table_styled.html", 
                "text/html",
                key="html_download_styled"  # Add this
            )
            
            right.download_button(
                "Download CSV", 
                df.to_csv(index=False), 
                "table.csv", 
                "text/csv",
                key="csv_download_styled"  # Add this
            )
    else:
        st.warning("Please upload a CSV file to begin.")

if __name__ == "__main__":
    main()