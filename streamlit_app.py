import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import base64
import cairosvg
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import io

st.set_page_config(layout="wide", page_title="Clinical Trials Visualizer")

def generate_table_html(df):
    df = df.copy()
    df['Objective'] = df['Objective'].apply(lambda x: 
        '<br>'.join([f"• {item.strip()}" for item in x.split(';')])
    )
    
    html = f"""
    <div style="padding: 1rem;">
        <style>
            .table-container {{
                background: white;
                border-radius: 12px;
                padding: 1.5rem;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            }}
            table {{
                width: 100%;
                border-collapse: separate;
                border-spacing: 0;
                font-family: system-ui, -apple-system, sans-serif;
            }}
            th {{
                background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
                color: white;
                padding: 16px;
                text-align: left;
                font-weight: 600;
                font-size: 0.95rem;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                border-bottom: 2px solid #2563eb;
            }}
            th:first-child {{
                border-top-left-radius: 8px;
            }}
            th:last-child {{
                border-top-right-radius: 8px;
            }}
            td {{
                padding: 16px;
                border-bottom: 1px solid #e5e7eb;
                line-height: 1.6;
                font-size: 0.95rem;
                transition: all 0.2s ease;
            }}
            tr:hover td {{
                background-color: #f8fafc;
            }}
            tr:nth-child(even) {{
                background: #f1f5f9;
            }}
            tr:last-child td {{
                border-bottom: none;
            }}
            tr:last-child td:first-child {{
                border-bottom-left-radius: 8px;
            }}
            tr:last-child td:last-child {{
                border-bottom-right-radius: 8px;
            }}
        </style>
        <div class="table-container">
            {df.to_html(index=False, escape=False, classes='styled-table')}
        </div>
    </div>
    """
    return html

def convert_to_png(html_content):
    # Convert HTML to SVG
    svg_content = f"""
    <svg width="1200" height="800" xmlns="http://www.w3.org/2000/svg">
        <foreignObject width="100%" height="100%">
            <div xmlns="http://www.w3.org/1999/xhtml">
                {html_content}
            </div>
        </foreignObject>
    </svg>
    """
    
    # Convert SVG to PNG using reportlab
    drawing = svg2rlg(io.StringIO(svg_content))
    bio = io.BytesIO()
    renderPM.drawToFile(drawing, bio, fmt="PNG", dpi=300)
    return bio.getvalue()

def main():
    st.title("Clinical Trials Table Visualizer")
    
    # Your existing default_data dictionary here...
    
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.DataFrame(default_data)

    st.dataframe(df, use_container_width=True, hide_index=True)
    
    table_html = generate_table_html(df)
    components.html(table_html, height=600, scrolling=True)
    
    # Generate downloads
    html_b64 = base64.b64encode(table_html.encode()).decode()
    csv_b64 = base64.b64encode(df.to_csv(index=False).encode()).decode()
    png_data = convert_to_png(table_html)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(
            label="Download HTML",
            data=table_html,
            file_name="table.html",
            mime="text/html"
        )
    with col2:
        st.download_button(
            label="Download CSV",
            data=df.to_csv(index=False),
            file_name="table.csv",
            mime="text/csv"
        )
    with col3:
        st.download_button(
            label="Download PNG",
            data=png_data,
            file_name="table.png",
            mime="image/png"
        )

if __name__ == "__main__":
    main()