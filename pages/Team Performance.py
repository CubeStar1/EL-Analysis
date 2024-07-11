import streamlit as st
import pandas as pd

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv('data/Merged_Team_and_Marks_Data-1.csv')

data = load_data()

st.title('Team Performance Dashboard')

# Sidebar for team selection
selected_team = st.sidebar.selectbox('Select a Team', data['Team Name'].unique())

# Filter data for the selected team
team_data = data[data['Team Name'] == selected_team]

# Display team information
st.subheader(f"Team: {selected_team}")
st.write(f"Theme: {team_data['Theme'].iloc[0]}")
st.write(f"Topic: {team_data['Topic'].iloc[0]}")
st.write(f'''Team Leader: {team_data["Team Leader's Name"].iloc[0]}''')

# Prepare data for the chart
phases = ['Phase 1', 'Phase 2', 'Phase 3']
marks = team_data[phases].iloc[0].tolist()

# Create a line chart
st.subheader('Performance Across Phases')
chart_data = pd.DataFrame({
    'Phase': ['Phase 1', 'Phase 2', 'Phase 3'],
    'Marks': marks
})
st.line_chart(chart_data.set_index('Phase'))

# Display total marks
st.subheader('Total Performance')
total_marks = team_data['Total'].iloc[0]
st.metric(label="Total Marks", value=f"{total_marks}/100")

# Calculate and display percentage
percentage = (total_marks / 100) * 100
st.progress(percentage / 100)
st.write(f"Overall Percentage: {percentage:.2f}%")