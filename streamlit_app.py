import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

st.set_page_config(layout="wide", page_title="Clinical Trials Visualizer")

def generate_table_html(df):
    """Generate HTML table with bullet points for objectives."""
    df = df.copy()
    df['Objective'] = df['Objective'].apply(lambda x: 
        '<div class="bullet-container">' + 
        '<br>'.join([f"<span class='bullet'>•</span><span class='bullet-text'>{item.strip()}</span>" 
                    for item in x.split(';')]) +
        '</div>'
    )
    
    html = f"""
    <div style="padding: 2rem;">
        <link rel="stylesheet" type="text/css" href="styles.css">
        <div class="table-container">
            {df.to_html(index=False, escape=False, classes='styled-table dataframe')}
        </div>
    </div>
    """
    return html

# Place this before your main function or at the top of your script
def load_css(css_file):
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    
    load_css('styles.css')

    st.title("Clinical Trials Table Visualizer")
    
    # File upload
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    
    if uploaded_file is None:
        st.warning("Please upload a CSV file to begin.")
        return
        
    df = pd.read_csv(uploaded_file)
    
    # Display table
    table_html = generate_table_html(df)
    components.html(table_html, height=600, scrolling=True)
    
    # Download options
    st.markdown("### Download Options")
    col1, col2 = st.columns([1,1])
    
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