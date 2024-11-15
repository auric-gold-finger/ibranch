import streamlit as st
import pandas as pd
import base64

st.set_page_config(layout="wide", page_title="Clinical Trials Visualizer")

def generate_html_table(df):
    css = """
    <style>
        .styled-table {
            border-collapse: collapse;
            margin: 25px 0;
            font-size: 0.9em;
            font-family: -apple-system, system-ui, BlinkMacSystemFont;
            width: 100%;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
            border-radius: 5px;
            overflow: hidden;
        }
        .styled-table thead tr {
            background-color: #1e40af;
            color: white;
            text-align: left;
            font-weight: bold;
        }
        .styled-table th,
        .styled-table td {
            padding: 12px 15px;
            border-bottom: 1px solid #dddddd;
        }
        .styled-table tbody tr:nth-of-type(even) {
            background-color: #f8f9ff;
        }
        .styled-table tbody tr:last-of-type {
            border-bottom: 2px solid #1e40af;
        }
        .styled-table tbody tr.active-row {
            font-weight: bold;
            color: #1e40af;
        }
        .objective-list {
            margin: 0;
            padding-left: 20px;
        }
    </style>
    """
    
    df = df.copy()
    df['Objective'] = df['Objective'].apply(lambda x: 
        '<ul class="objective-list">' + 
        ''.join([f'<li>{item.strip()}</li>' for item in x.split(';')]) +
        '</ul>'
    )
    
    table_html = df.to_html(classes='styled-table', index=False, escape=False)
    return css + table_html

def get_download_files(df, html_content):
    html_b64 = base64.b64encode(html_content.encode()).decode()
    
    svg_content = f'''
    <?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800">
        <foreignObject width="100%" height="100%">
            <div xmlns="http://www.w3.org/1999/xhtml">
                {html_content}
            </div>
        </foreignObject>
    </svg>
    '''
    svg_b64 = base64.b64encode(svg_content.encode()).decode()
    
    csv = df.to_csv(index=False).encode()
    csv_b64 = base64.b64encode(csv).decode()
    
    return html_b64, svg_b64, csv_b64

def display_download_buttons(html_b64, svg_b64, csv_b64):
    st.markdown("""
        <style>
        .download-button {
            display: inline-block;
            padding: 10px 20px;
            background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%);
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin: 5px;
            font-weight: bold;
            transition: opacity 0.2s;
        }
        .download-button:hover {
            opacity: 0.9;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'''
            <a href="data:text/html;base64,{html_b64}" 
               download="table.html" 
               class="download-button">
                Download HTML
            </a>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
            <a href="data:image/svg+xml;base64,{svg_b64}" 
               download="table.svg" 
               class="download-button">
                Download SVG
            </a>
        ''', unsafe_allow_html=True)
    with col3:
        st.markdown(f'''
            <a href="data:text/csv;base64,{csv_b64}" 
               download="table.csv" 
               class="download-button">
                Download CSV
            </a>
        ''', unsafe_allow_html=True)

def main():
    st.title("Clinical Trials Table Visualizer")

    default_data = {
        'Phase': ['0', 'I', 'Ib', 'IIa', 'IIb', 'III', 'IIIb', 'IV'],
        'Study Design': [
            'Proof-of-concept subtherapeutic dose',
            'Single-arm dose escalation',
            'Multi-arm dose escalation',
            'Pilot dose-finding',
            'Proof-of-concept case series or randomized controlled trial',
            'Randomized controlled trial',
            'Randomized controlled trial',
            'Post-market surveillance'
        ],
        'Number of Participants': [
            '<15 healthy volunteers or patients with the condition',
            '20-80 healthy volunteers or patients with the condition',
            '20-80 healthy volunteers or patients with the condition',
            '~50 patients with the condition',
            '100-300 patients with the condition',
            '1000-3000 patients with the condition',
            '1000-3000 patients with the condition',
            'Variable'
        ],
        'Trial Duration': [
            '≤14 days',
            'Several months',
            'Several months',
            'Several months up to one year',
            'Several months up to two years',
            'One to four years',
            'One to four years',
            'A few months up to several years'
        ],
        'Objective': [
            'Expedite clinical evaluation of drugs;Demonstrate drug-target effects;Initial pharmakokinetics',
            'Safety;Determine the highest dose without severe side effects',
            'Safety;Determine the highest dose without severe side effects',
            'Test for effective dosage;Determine therapeutic regimen;Continue safety testing;Monitor side effects including drug-drug interactions',
            'Efficacy in achieving the primary outcome;Continue safety testing;Monitor side effects including drug-drug interactions',
            'Evaluate efficacy and side effects;Compare to placebo or other existing treatments',
            'Gather aditional data;Test efficacy in different patient populations',
            'Monitor long-term safety and efficacy'
        ]
    }

    st.markdown("""
        <style>
            .stApp {
                background-color: #f8fafc;
            }
            div[data-testid="stDataFrame"] div[role="cell"] {
                font-family: -apple-system, system-ui, BlinkMacSystemFont !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.DataFrame(default_data)
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    html_content = generate_html_table(df)
    st.markdown("### HTML Table View", unsafe_allow_html=True)
    st.markdown(html_content, unsafe_allow_html=True)
    
    html_b64, svg_b64, csv_b64 = get_download_files(df, html_content)
    st.markdown("### Download Options", unsafe_allow_html=True)
    display_download_buttons(html_b64, svg_b64, csv_b64)

if __name__ == "__main__":
    main()