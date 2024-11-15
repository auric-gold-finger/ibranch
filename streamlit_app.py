import streamlit as st
import pandas as pd
import base64
from io import BytesIO
import cairosvg

def generate_styled_html(df):
    css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Avenir:wght@400;700&display=swap');
        
        .clinical-table {
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            font-family: Avenir, sans-serif;
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

def convert_to_svg(html_content):
    # Convert HTML to SVG using cairosvg
    svg_content = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="1000" height="800">
        <foreignObject width="100%" height="100%">
            <div xmlns="http://www.w3.org/1999/xhtml">
                {html_content}
            </div>
        </foreignObject>
    </svg>
    """
    return svg_content

def convert_svg_to_png(svg_content):
    return cairosvg.svg2png(bytestring=svg_content.encode('utf-8'))

def get_download_link(content, filename, text):
    b64 = base64.b64encode(content.encode('utf-8') if isinstance(content, str) else content).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">{text}</a>'

def main():
    st.title("Clinical Trials Table Visualizer")
    
    # File upload
    uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        
        # Display the styled table
        styled_html = generate_styled_html(df)
        st.markdown(styled_html, unsafe_allow_html=True)
        
        # Generate SVG and PNG
        svg_content = convert_to_svg(styled_html)
        png_content = convert_svg_to_png(svg_content)
        
        # Download buttons
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(get_download_link(svg_content, "table.svg", "Download SVG"), unsafe_allow_html=True)
        with col2:
            st.markdown(get_download_link(png_content, "table.png", "Download PNG"), unsafe_allow_html=True)

if __name__ == "__main__":
    main()