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

def add_png_download_button():
    """Add a button to download the table as PNG."""
    js_code = """
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html-to-image/1.11.11/html-to-image.min.js"></script>
    <button class="png-download-btn" onclick="downloadTableAsPNG()">Download PNG</button>
    
    <script>
    function downloadTableAsPNG() {
        const button = document.querySelector('.png-download-btn');
        button.innerHTML = 'Generating PNG...';
        
        const streamlitDoc = document.querySelector('iframe[title="streamlit_html_sandbox"]').contentDocument;
        const targetNode = streamlitDoc.querySelector('.table-container');
        
        if (!targetNode) {
            button.innerHTML = 'Error - Table Not Found';
            return;
        }
        
        htmlToImage.toPng(targetNode, {
            quality: 1.0,
            pixelRatio: 2,
            backgroundColor: '#f0f2f5'
        })
        .then(function (dataUrl) {
            const link = document.createElement('a');
            link.download = 'clinical_trials_table.png';
            link.href = dataUrl;
            link.click();
            button.innerHTML = 'Download PNG';
        })
        .catch(function (error) {
            console.error('Error:', error);
            button.innerHTML = 'Error - Try Again';
        });
    }
    </script>
    """
    return components.html(js_code, height=50)

def main():
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