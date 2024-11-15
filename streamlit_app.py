import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import base64

st.set_page_config(layout="wide", page_title="Clinical Trials Visualizer")

def generate_table_html(df):
    df = df.copy()
    df['Objective'] = df['Objective'].apply(lambda x: 
        '<br>'.join([f"<span class='bullet'>•</span> {item.strip()}" for item in x.split(';')])
    )
    
    html = f"""
    <div style="padding: 2rem;">
        <style>
            @import url('https://fonts.cdnfonts.com/css/avenir');
            
            .table-container {{
                background: #f0f2f5;
                padding: 1px;
                box-shadow: 
                    0 4px 6px -1px rgba(0, 0, 0, 0.1),
                    0 2px 4px -1px rgba(0, 0, 0, 0.06);
                max-width: 1400px;
                margin: 0 auto;
                position: relative;
            }}
            
            table {{
                width: 100%;
                border-collapse: separate;
                border-spacing: 2px;
                font-family: 'Avenir', system-ui, sans-serif;
                background: #f0f2f5;
            }}
            
            thead {{
                position: sticky;
                top: 0;
                z-index: 1;
            }}
            
            th {{
                background: #1e3a8a;
                color: white;
                padding: 16px 20px;
                text-align: left;
                font-weight: 500;
                font-size: 0.85rem;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            
            /* Column widths */
            th:nth-child(1) {{ width: 8%; }}
            th:nth-child(2) {{ width: 22%; }}
            th:nth-child(3) {{ width: 20%; }}
            th:nth-child(4) {{ width: 15%; }}
            th:nth-child(5) {{ width: 35%; }}
            
            td {{
                padding: 14px 20px;
                font-size: 0.9rem;
                color: #1a1a1a;
                line-height: 1.5;
                vertical-align: top;
                background: white;
                box-shadow: 
                    0 2px 4px rgba(0, 0, 0, 0.04),
                    0 1px 2px rgba(0, 0, 0, 0.06);
                transition: all 0.2s ease;
            }}
            
            tr:hover td {{
                transform: translateY(-1px);
                box-shadow: 
                    0 4px 6px rgba(0, 0, 0, 0.06),
                    0 2px 4px rgba(0, 0, 0, 0.08);
            }}
            
            /* Phase column */
            td:first-child {{
                font-weight: 600;
                color: #1e3a8a;
                white-space: nowrap;
                text-align: center;
                background: white;
            }}
            
            /* Enhanced bullets */
            .bullet {{
                display: inline-block;
                color: #1e3a8a;
                font-weight: bold;
                margin-right: 8px;
                width: 12px;
                height: 12px;
                line-height: 12px;
                text-align: center;
            }}
            
            /* List styling */
            td ul {{
                margin: 0;
                padding: 0;
                list-style: none;
            }}
            
            td li {{
                margin: 8px 0;
                padding-left: 20px;
                position: relative;
            }}
            
            /* Scrollbar styling */
            ::-webkit-scrollbar {{
                width: 10px;
                height: 10px;
            }}
            
            ::-webkit-scrollbar-track {{
                background: #f0f2f5;
            }}
            
            ::-webkit-scrollbar-thumb {{
                background: #c1c1c1;
                border: 2px solid #f0f2f5;
            }}
            
            ::-webkit-scrollbar-thumb:hover {{
                background: #a1a1a1;
            }}
            
            /* Corner treatment */
            ::-webkit-scrollbar-corner {{
                background: #f0f2f5;
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
                background-color: #f8f9fa;
            }
            .stDownloadButton {
                background: #1e3a8a !important;
                color: white !important;
                border: none !important;
                padding: 0.5rem 1rem !important;
                font-weight: 500 !important;
                font-family: 'Avenir', system-ui, sans-serif !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
            }
            .stDownloadButton:hover {
                opacity: 0.9 !important;
                box-shadow: 0 4px 6px rgba(0,0,0,0.15) !important;
                transform: translateY(-1px) !important;
            }
            .stTitle {
                font-family: 'Avenir', system-ui, sans-serif !important;
                color: #1e3a8a !important;
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