import streamlit as st
import pandas as pd
import base64

def generate_styled_html(df):
    css = """
    <style>
        .clinical-table {
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-size: 0.9em;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
        }
        
        .clinical-table thead tr {
            background-color: #1e3a8a;
            color: #ffffff;
            text-align: left;
            font-weight: bold;
        }
        
        .clinical-table th,
        .clinical-table td {
            padding: 12px 15px;
            border: 1px solid #ddd;
        }
        
        .clinical-table tbody tr {
            border-bottom: 1px solid #dddddd;
        }
        
        .clinical-table tbody tr:nth-of-type(even) {
            background-color: #f3f3f3;
        }
        
        .clinical-table tbody tr:last-of-type {
            border-bottom: 2px solid #1e3a8a;
        }
    </style>
    """
    table_html = df.to_html(classes='clinical-table', index=False, escape=False)
    return css + table_html

def get_table_download_link(df, html_content):
    b64_html = base64.b64encode(html_content.encode()).decode()
    
    # Create SVG version
    svg_content = f'''
    <svg xmlns="http://www.w3.org/2000/svg" width="1000" height="800">
        <foreignObject width="100%" height="100%">
            <div xmlns="http://www.w3.org/1999/xhtml">
                {html_content}
            </div>
        </foreignObject>
    </svg>
    '''
    b64_svg = base64.b64encode(svg_content.encode()).decode()
    
    html_href = f'<a href="data:text/html;base64,{b64_html}" download="table.html">Download HTML</a>'
    svg_href = f'<a href="data:image/svg+xml;base64,{b64_svg}" download="table.svg">Download SVG</a>'
    
    return html_href, svg_href

st.title("Clinical Trials Table Visualizer")

uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    styled_html = generate_styled_html(df)
    st.markdown(styled_html, unsafe_allow_html=True)
    
    html_link, svg_link = get_table_download_link(df, styled_html)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(html_link, unsafe_allow_html=True)
    with col2:
        st.markdown(svg_link, unsafe_allow_html=True)