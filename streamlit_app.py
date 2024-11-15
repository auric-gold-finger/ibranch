import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import base64

st.set_page_config(layout="wide", page_title="Clinical Trials Visualizer")

def generate_table_html(df):
    df = df.copy()
    df['Objective'] = df['Objective'].apply(lambda x: 
        '<br>'.join([f"<span style='color: #4a5568'>•</span> {item.strip()}" for item in x.split(';')])
    )
    
    html = f"""
    <div style="padding: 1rem; font-family: system-ui, -apple-system, sans-serif;">
        <style>
            .table-container {{
                background: white;
                border-radius: 12px;
                padding: 1.5rem;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                overflow: hidden;
            }}
            table {{
                width: 100%;
                border-collapse: separate;
                border-spacing: 0;
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
                position: sticky;
                top: 0;
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
                color: #1f2937;
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
            .phase-column {{
                font-weight: 600;
                color: #1e40af;
            }}
        </style>
        <div class="table-container">
            {df.to_html(index=False, escape=False, classes='styled-table')}
        </div>
    </div>
    """
    return html

def main():
    st.title("Clinical Trials Table Visualizer")
    st.markdown("""
        <style>
            .stApp {
                background-color: #f8fafc;
            }
            section[data-testid="stSidebar"] {
                background-color: #f1f5f9;
            }
            .stDownloadButton {
                background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%) !important;
                color: white !important;
                border: none !important;
                padding: 0.5rem 1rem !important;
                border-radius: 6px !important;
                font-weight: 600 !important;
                transition: opacity 0.2s !important;
            }
            .stDownloadButton:hover {
                opacity: 0.9 !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
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
    
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.DataFrame(default_data)

    st.dataframe(df, use_container_width=True, hide_index=True)
    
    table_html = generate_table_html(df)
    components.html(table_html, height=600, scrolling=True)
    
    col1, col2 = st.columns(2)
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

if __name__ == "__main__":
    main()