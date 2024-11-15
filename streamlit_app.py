import streamlit as st

# Page config
st.set_page_config(layout="wide")

# Data
data = [
    {
        "phase": "0",
        "design": "Proof-of-concept, subtherapeutic dose",
        "participants": "<15 healthy volunteers or patients with the condition",
        "duration": "≤14 days",
        "objectives": [
            "Expedite clinical evaluation of drugs",
            "Demonstrate drug-target effects", 
            "Initial pharmakokinetics"
        ]
    },
    # ... add remaining phases data here
]

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Avenir:wght@400;700&display=swap');
    
    .clinical-table {
        width: 100%;
        border-collapse: collapse;
        margin: 25px 0;
        font-family: Avenir, sans-serif;
        font-size: 0.9em;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
    }
    
    .clinical-table thead tr {
        background-color: #1e3a8a;
        color: #ffffff;
        text-align: left;
        font-weight: bold;
    }
    
    .clinical-table th,
    .clinical-table td {
        padding: 12px 15px;
        border: 1px solid #ddd;
    }
    
    .clinical-table tbody tr {
        border-bottom: 1px solid #dddddd;
    }
    
    .clinical-table tbody tr:nth-of-type(even) {
        background-color: #f3f3f3;
    }
    
    .clinical-table tbody tr:last-of-type {
        border-bottom: 2px solid #1e3a8a;
    }
    
    .objectives-list {
        list-style-type: disc;
        margin: 0;
        padding-left: 20px;
    }
    
    .phase-cell {
        font-weight: bold;
        color: #1e3a8a;
    }
</style>
""", unsafe_allow_html=True)

# Generate HTML table
html = """
<table class="clinical-table">
    <thead>
        <tr>
            <th>Phase</th>
            <th>Study Design</th>
            <th>Number of Participants</th>
            <th>Trial Duration</th>
            <th>Objective</th>
        </tr>
    </thead>
    <tbody>
"""

for item in data:
    objectives_html = "\n".join([f"<li>{obj}</li>" for obj in item["objectives"]])
    html += f"""
        <tr>
            <td class="phase-cell">{item["phase"]}</td>
            <td>{item["design"]}</td>
            <td>{item["participants"]}</td>
            <td>{item["duration"]}</td>
            <td><ul class="objectives-list">{objectives_html}</ul></td>
        </tr>
    """

html += """
    </tbody>
</table>
"""

# Display
st.title("Clinical Trial Phases")
st.markdown(html, unsafe_allow_html=True)
