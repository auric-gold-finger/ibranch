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
                max-width: 1400px;
                margin: 0 auto;
                position: relative;
            }}
            
            table {{
                width: 100%;
                border-collapse: separate;
                border-spacing: 4px;  /* Slightly increased for shadow */
                font-family: 'Avenir', system-ui, sans-serif;
                background: #f0f2f5;
            }}
            
            table, th, td {{
                border: none !important;
            }}
            
            thead {{
                position: sticky;
                top: 0;
                z-index: 1;
            }}
            
            th {{
                background: #000000;
                color: white;
                padding: 16px 20px;
                text-align: left;
                font-weight: 500;
                font-size: 0.85rem;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                box-shadow: 
                    2px 2px 4px rgba(0, 0, 0, 0.2),
                    4px 4px 8px rgba(0, 0, 0, 0.1);
            }}
            
            th:nth-child(1) {{ width: 8%; }}
            th:nth-child(2) {{ width: 22%; }}
            th:nth-child(3) {{ width: 20%; }}
            th:nth-child(4) {{ width: 15%; }}
            th:nth-child(5) {{ width: 35%; }}
            
            td {{
                background: white;
                padding: 14px 20px;
                font-size: 0.9rem;
                color: #000000;
                line-height: 1.5;
                vertical-align: middle;  /* Changed from 'top' to 'middle' */
                box-shadow: 
                    2px 2px 4px rgba(0, 0, 0, 0.07),
                    3px 3px 6px rgba(0, 0, 0, 0.03);
                position: relative;
                transform: translate(-1px, -1px);
                transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
            }}
            
            tr:hover td {{
                transform: translate(-2px, -2px);
                box-shadow: 
                    3px 3px 6px rgba(0, 0, 0, 0.15),
                    5px 5px 12px rgba(0, 0, 0, 0.1);
            }}
            
            td:first-child {{
                font-weight: 600;
                color: #000000;
                white-space: nowrap;
                text-align: center;
            }}
            
            .bullet {{
                display: inline-block;
                color: #1e3a8a;
                margin-right: 8px;
                width: 12px;
                height: 12px;
                line-height: 12px;
                text-align: center;
            }}
            
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
            
            .dataframe {{
                border: none !important;
            }}
            
            .dataframe th, 
            .dataframe td {{
                border: none !important;
            }}
            
            ::-webkit-scrollbar {{
                width: 8px;
                height: 8px;
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
        </style>
        <div class="table-container">
            {df.to_html(index=False, escape=False, classes='styled-table dataframe')}
        </div>
    </div>
    """
    return html

def get_svg_download(table_html):
    # Simplified SVG wrapper with CDATA section to protect HTML content
    svg_wrapper = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800">
  <foreignObject width="100%" height="100%">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <![CDATA[
        <style>
          @import url('https://fonts.cdnfonts.com/css/avenir');
          table {{ border-collapse: separate; border-spacing: 4px; width: 100%; }}
          th {{ background: #000000; color: white; padding: 16px; }}
          td {{ background: white; padding: 14px; }}
        </style>
        {table_html}
      ]]>
    </div>
  </foreignObject>
</svg>'''
    return svg_wrapper

def add_png_download_button():
    js_code = """
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <style>
        .png-download-btn {
            background: #000000;
            color: white;
            padding: 0.5rem 1rem;
            font-family: 'Avenir', system-ui, sans-serif;
            font-weight: 500;
            border: none;
            cursor: pointer;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: all 0.2s ease;
        }
        .png-download-btn:hover {
            opacity: 0.9;
            box-shadow: 0 4px 6px rgba(0,0,0,0.25);
            transform: translateY(-1px);
        }
    </style>
    
    <button class="png-download-btn" onclick="downloadTableAsPNG()">Download PNG</button>
    
    <script>
    async function downloadTableAsPNG() {
        try {
            // Add loading state
            const button = document.querySelector('.png-download-btn');
            button.innerHTML = 'Generating PNG...';
            button.style.opacity = '0.7';
            
            // Find the table in the iframe
            const iframes = document.querySelectorAll('iframe');
            let table;
            for (const iframe of iframes) {
                const doc = iframe.contentDocument || iframe.contentWindow.document;
                table = doc.querySelector('.table-container');
                if (table) break;
            }
            
            if (!table) {
                console.error('Table not found');
                button.innerHTML = 'Error - Try Again';
                return;
            }

            // Create canvas
            const canvas = await html2canvas(table, {
                scale: 2,
                backgroundColor: '#f0f2f5',
                logging: true,
                useCORS: true,
                allowTaint: true,
                foreignObjectRendering: true
            });
            
            // Create download link
            const image = canvas.toDataURL('image/png', 1.0);
            const link = document.createElement('a');
            link.download = 'clinical_trials_table.png';
            link.href = image;
            link.click();
            
            // Reset button
            button.innerHTML = 'Download PNG';
            button.style.opacity = '1';
        } catch (error) {
            console.error('Error generating PNG:', error);
            const button = document.querySelector('.png-download-btn');
            button.innerHTML = 'Error - Try Again';
        }
    }
    </script>
    """
    return components.html(js_code, height=50)

def main():
    st.title("Clinical Trials Table Visualizer")
    st.markdown("""
        <style>
            .stApp {
                background-color: #f8f9fa;
            }
            .stDownloadButton {
                background: #000000 !important;
                color: black !important;
                border: none !important;
                padding: 0.5rem 1rem !important;
                font-weight: 500 !important;
                font-family: 'Avenir', system-ui, sans-serif !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
            }
            .stDownloadButton:hover {
                opacity: 0.9 !important;
                box-shadow: 0 4px 6px rgba(0,0,0,0.25) !important;
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

    #st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Display table
    table_html = generate_table_html(df)
    components.html(table_html, height=600, scrolling=True)
    
    # Download options
    st.markdown("### Download Options")
    col1, col2, col3 = st.columns([1,1,1])
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
        add_png_download_button()


if __name__ == "__main__":
    main()