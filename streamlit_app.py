import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="Clinical Trials Visualizer")

def style_dataframe(df):
    # Custom CSS for the table
    st.markdown("""
    <style>
        .stDataFrame {
            font-family: 'Inter', -apple-system, sans-serif;
        }
        .dataframe {
            border-collapse: collapse;
            margin: 25px 0;
            font-size: 0.9em;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
            border-radius: 8px;
            overflow: hidden;
            width: 100%;
        }
        .dataframe thead tr {
            background: linear-gradient(90deg, #1e3a8a 0%, #2563eb 100%);
            color: white;
            text-align: left;
            font-weight: bold;
        }
        .dataframe th,
        .dataframe td {
            padding: 12px 15px !important;
            border: 1px solid #ddd;
        }
        .dataframe tbody tr {
            border-bottom: 1px solid #dddddd;
        }
        .dataframe tbody tr:nth-of-type(even) {
            background-color: #f8f9ff;
        }
        .dataframe tbody tr:last-of-type {
            border-bottom: 2px solid #1e3a8a;
        }
        .dataframe tbody tr:hover {
            background-color: #f3f4f6;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Apply custom formatting to objectives column
    df['Objective'] = df['Objective'].str.split(';').apply(lambda x: "\n• " + "\n• ".join(x))
    
    # Display the styled dataframe
    st.dataframe(df, use_container_width=True, hide_index=True)

def main():
    st.title("Clinical Trials Table Visualizer")
    
    # Sample data if no file is uploaded
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
    
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.DataFrame(default_data)
    
    style_dataframe(df)
    
    # Add download button for CSV
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="clinical_trials.csv",
        mime="text/csv",
        key='download-csv'
    )

if __name__ == "__main__":
    main()