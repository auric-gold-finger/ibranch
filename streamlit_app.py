import streamlit as st
import pandas as pd
import base64

# Page config
st.set_page_config(layout="wide", page_title="Clinical Trials Visualizer")

def generate_styled_html(df):
    css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
        
        .container {
            padding: 2rem;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .clinical-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin: 25px 0;
            font-family: 'Inter', sans-serif;
            font-size: 0.9em;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .clinical-table thead tr {
            background: linear-gradient(90deg, #1e3a8a 0%, #2563eb 100%);
            color: #ffffff;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85em;
            letter-spacing: 0.5px;
        }
        
        .clinical-table th,
        .clinical-table td {
            padding: 16px 20px;
            border-bottom: 1px solid #e5e7eb;
        }
        
        .clinical-table th {
            border: none;
        }
        
        .clinical-table tbody tr {
            transition: all 0.2s ease;
        }
        
        .clinical-table tbody tr:hover {
            background-color: #f8fafc;
        }
        
        .clinical-table tbody tr:nth-of-type(even) {
            background-color: #f8f9ff;
        }
        
        .clinical-table tbody tr:last-of-type td {
            border-bottom: none;
        }
        
        .phase-cell {
            font-weight: 600;
            color: #1e3a8a;
        }
        
        .objectives-list {
            margin: 0;
            padding-left: 20px;
            list-style-type: disc;
        }
        
        .download-btn {
            display: inline-block;
            padding: 10px 20px;
            background: linear-gradient(90deg, #1e3a8a 0%, #2563eb 100%);
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-family: 'Inter', sans-serif;
            font-weight: 500;
            margin: 10px;
            transition: all 0.2s ease;
        }
        
        .download-btn:hover {
            opacity: 0.9;
            transform: translateY(-1px);
        }
    </style>
    """
    
    # Convert semicolon-separated objectives to HTML lists
    df = df.copy()
    df['Objective'] = df['Objective'].apply(lambda x: f"<ul class='objectives-list'><li>{'</li><li>'.join(x.split(';'))}</li></ul>")
    
    # Add phase-cell class to Phase column
    table_html = df.to_html(classes='clinical-table', index=False, escape=False)
    table_html = table_html.replace('<td>', '<td class="phase-cell">', 1)
    
    return f"<div class='container'>{css}{table_html}</div>"

def get_table_download_link(df, html_content):
    b64_html = base64.b64encode(html_content.encode()).decode()
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
    
    html_href = f'<a class="download-btn" href="data:text/html;base64,{b64_html}" download="table.html">Download HTML</a>'
    svg_href = f'<a class="download-btn" href="data:image/svg+xml;base64,{b64_svg}" download="table.svg">Download SVG</a>'
    
    return html_href, svg_href

def main():
    st.markdown("""
        <style>
            .stApp {
                background-color: #f1f5f9;
            }
            .main .block-container {
                padding-top: 2rem;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("Clinical Trials Table Visualizer")
    st.markdown("Upload a CSV file to generate a beautifully formatted table.")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        styled_html = generate_styled_html(df)
        st.markdown(styled_html, unsafe_allow_html=True)
        
        html_link, svg_link = get_table_download_link(df, styled_html)
        st.markdown(f"<div style='text-align: center'>{html_link}{svg_link}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()