import streamlit as st
import pandas as pd
import numpy as np
from typing import List, Tuple, Dict

def detect_and_format_lists(df: pd.DataFrame, 
                         threshold: float = 0.5,
                         delimiters: List[str] = [';', '|', ',']) -> Tuple[pd.DataFrame, List[str]]:
   """
   Detects and formats list-like columns in the DataFrame.
   """
   list_columns = []
   formatted_df = df.copy()
   
   for col in formatted_df.columns:
       if pd.api.types.is_numeric_dtype(formatted_df[col]):
           continue
           
       delimiter_counts = [
           formatted_df[col].astype(str).apply(lambda x: delim in x).sum() / len(formatted_df[col])
           for delim in delimiters
       ]
       
       if any(count > threshold for count in delimiter_counts):
           list_columns.append(col)
           primary_delimiter = delimiters[np.argmax(delimiter_counts)]
           
           formatted_df[col] = formatted_df[col].apply(
               lambda x: format_list_cell(x, primary_delimiter)
               if pd.notna(x) else '<ul><li></li></ul>'
           )
   
   return formatted_df, list_columns

def format_list_cell(cell_value: str, delimiter: str) -> str:
    """Formats a single cell value as an HTML unordered list."""
    if pd.isna(cell_value):
        return '-'  # or return whatever you want for NaN values in non-list cells
    items = [item.strip() for item in str(cell_value).split(delimiter) if item.strip()]
    if not items:
        return '-'  # or return whatever you want for empty lists
    return '<ul>' + ''.join([f'<li>{item}</li>' for item in items]) + '</ul>'            

def get_table_styles(column_settings: Dict, 
                   header_border_radius: int = 4, 
                   cell_border_radius: int = 4, 
                   header_font_size: int = 20, 
                   cell_font_size: int = 18,
                   cell_spacing: int = 6, 
                   header_bgcolor: str = '#333333',
                   header_font_color: str = '#FFFFFF',
                   zebra_stripe: bool = False, 
                   list_style: str = 'square',
                   line_height: float = 1.3,
                   default_header_align: str = 'center',
                   default_cell_align: str = 'center') -> str:
   """Returns custom CSS styles for the table."""
   
   # Generate column-specific styles
   column_styles = "\n".join([
       f"""
       td:nth-child({i+1}), th:nth-child({i+1}) {{
           width: {settings['width']}%;
       }}
       td:nth-child({i+1}) {{
           text-align: {settings['align'] if settings['align'] != 'default' else default_cell_align};
       }}
       """
       for i, settings in enumerate(column_settings.values())
   ])
   
   return f"""
   <style>
   /* Import fonts */
   @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600&display=swap');
   @import url('https://fonts.googleapis.com/css2?family=Avenir&display=swap');

   /* Table styling */
   table {{ 
       border-collapse: separate;
       border-spacing: {cell_spacing}px;
       width: 100%; 
       box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
       border-radius: {cell_border_radius}px;
       overflow: hidden;
       table-layout: fixed;
   }}
   th {{
       background-color: {header_bgcolor};
       color: {header_font_color};
       font-family: 'Cormorant Garamond', serif;
       font-size: {header_font_size}px;
       font-weight: bold;
       padding: 12px;
       border-radius: {header_border_radius}px;
       line-height: {line_height};
       overflow: hidden;
       text-overflow: ellipsis;
       text-align: {default_header_align};
   }}
   td {{
       background-color: #f9f9f9;
       border-collapse: separate;
       border-style: none;
       border: 0;
       font-family: 'Avenir', sans-serif;
       font-size: {cell_font_size}px;
       padding: 10px;
       border-radius: {cell_border_radius}px;
       box-shadow: 2px 3px 4px rgba(0, 0, 0, 0.15);
       line-height: {line_height};
       overflow: hidden;
       text-overflow: ellipsis;
       text-align: {default_cell_align};
   }}
   {'''
   tr:nth-child(even) td {
       background-color: #f0f0f0;
   }
   ''' if zebra_stripe else ''}
   td ul {{
       margin: 0;
       list-style-type: {list_style};
   }}
   td ul li {{
       font-size: {cell_font_size}px !important;
       font-weight: normal !important;
       line-height: {line_height} !important;
   }}
   td:has(ul) {{
       font-weight: normal !important;
   }}
   
   /* Column-specific styles */
   {column_styles}
   </style>
   """

def main():
   st.set_page_config(page_title="Enhanced CSV Viewer", page_icon="📊", layout="wide")
   st.title("Enhanced CSV Table Viewer")

   # Initialize session state
   if 'column_settings' not in st.session_state:
       st.session_state.column_settings = {}

   # File upload
   uploaded_file = st.file_uploader("Upload CSV file", type="csv")

   if uploaded_file:
       try:
           # Load data first
           df = pd.read_csv(uploaded_file)
           
           # Initialize column settings if new file uploaded
           if 'current_file' not in st.session_state or st.session_state.current_file != uploaded_file.name:
                st.session_state.current_file = uploaded_file.name
                # Ensure each column gets at least 5% width, adjust if needed
                base_width = max(5, 100 // len(df.columns))
                st.session_state.column_settings = {
                    col: {
                        'width': base_width,
                        'align': 'default'
                    } for col in df.columns
                }

           # Global Controls Sidebar
           with st.sidebar:
               st.header("Global Settings")
               
               st.subheader("Table Settings")
               cell_spacing = st.number_input("Cell Spacing", min_value=0, max_value=20, value=6)
               
               st.subheader("Borders")
               header_border_radius = st.number_input("Header Border Radius", min_value=0, max_value=20, value=4)
               cell_border_radius = st.number_input("Cell Border Radius", min_value=0, max_value=20, value=4)
               
               st.subheader("Typography")
               header_font_size = st.number_input("Header Font Size", min_value=12, max_value=28, value=20)
               cell_font_size = st.number_input("Cell Font Size", min_value=12, max_value=24, value=18)
               line_height = st.number_input("Line Height", min_value=1.0, max_value=3.0, value=1.3, step=0.1)

               st.subheader("Default Alignment")
               default_header_align = st.selectbox(
                   "Header Text Alignment",
                   options=['left', 'center', 'right'],
                   index=1,  # center default
                   help="Default alignment for all headers unless overridden"
               )
               default_cell_align = st.selectbox(
                   "Cell Text Alignment",
                   options=['left', 'center', 'right'],
                   index=1,  # left default
                   help="Default alignment for all cells unless overridden"
               )
               
               st.subheader("Colors")
               header_bgcolor = st.color_picker("Header Background", value='#333333')
               header_font_color = st.color_picker("Header Font Color", value='#FFFFFF')
               
               st.subheader("List Style")
               list_style = st.selectbox(
                   "Bullet Style",
                   options=['square', 'circle', 'disc', 'decimal', 'decimal-leading-zero', 
                           'lower-roman', 'upper-roman', 'lower-alpha', 'upper-alpha', 'none']
               )
               
               zebra_stripe = st.checkbox("Zebra Striping", value=True)
           
           # Column controls
           with st.sidebar.expander("Column Settings"):
               for col in df.columns:
                   st.subheader(f"Column: {col}")
                   # Width control
                   st.session_state.column_settings[col]['width'] = st.number_input(
                       f"Width % - {col}",
                       min_value=5,
                       max_value=100,
                       value=st.session_state.column_settings[col]['width'],
                       step=5,
                       key=f"width_{col}"
                   )
                   # Alignment control
                   st.session_state.column_settings[col]['align'] = st.selectbox(
                       f"Alignment - {col}",
                       options=['default', 'left', 'center', 'right'],
                       index=['default', 'left', 'center', 'right'].index(st.session_state.column_settings[col]['align']),
                       key=f"align_{col}"
                   )
                   st.markdown("---")
           
           # Show total width as a sanity check
           total_width = sum(settings['width'] for settings in st.session_state.column_settings.values())
           if total_width != 100:
               st.sidebar.warning(f"Total width: {total_width}% (should be 100%)")

           # Show basic file info
           st.write(f"**Rows:** {len(df)} | **Columns:** {len(df.columns)}")
           
           # Process and display data
           formatted_df, list_cols = detect_and_format_lists(df)
           formatted_df = formatted_df.fillna('')
           
           if list_cols:
               st.info(f"📝 Detected list columns: {', '.join(list_cols)}")
           
           # Style and display table
           styled_df = formatted_df.style.format(precision=0).hide(axis='index')
           
           # Apply custom styling
           st.markdown(
               get_table_styles(
                   column_settings=st.session_state.column_settings,
                   header_border_radius=header_border_radius,
                   cell_border_radius=cell_border_radius,
                   header_font_size=header_font_size,
                   cell_font_size=cell_font_size,
                   cell_spacing=cell_spacing,
                   header_bgcolor=header_bgcolor,
                   header_font_color=header_font_color,
                   zebra_stripe=zebra_stripe,
                   list_style=list_style,
                   line_height=line_height,
                   default_header_align=default_header_align,
                   default_cell_align=default_cell_align
               ), 
               unsafe_allow_html=True
           )
           
           # Display table
           st.write(styled_df.to_html(escape=False, index=False), unsafe_allow_html=True)
           
           # Download button
           html_string = f"""
           <!DOCTYPE html>
           <html>
           <head>
           {get_table_styles(
               column_settings=st.session_state.column_settings,
               header_border_radius=header_border_radius,
               cell_border_radius=cell_border_radius,
               header_font_size=header_font_size,
               cell_font_size=cell_font_size,
               cell_spacing=cell_spacing,
               header_bgcolor=header_bgcolor,
               header_font_color=header_font_color,
               zebra_stripe=zebra_stripe,
               list_style=list_style,
               line_height=line_height,
               default_header_align=default_header_align,
               default_cell_align=default_cell_align
           )}
           </head>
           <body>
           {styled_df.to_html(escape=False, index=False)}
           </body>
           </html>
           """
           
           st.sidebar.download_button(
               label="Download HTML Table",
               data=html_string,
               file_name="styled_table.html",
               mime="text/html"
           )
           
       except Exception as e:
           st.error(f"Error processing file: {str(e)}")
           st.exception(e)
           st.write("Please ensure your CSV file is properly formatted and try again.")

if __name__ == "__main__":
   main()