import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.figure_factory as ff

@st.cache_data
def load_data():
    df = pd.read_csv('data/Merged_Team_and_Marks_Data-1.csv')
    df.set_index('Sno', inplace=True)
    df.replace(0, np.nan, inplace=True)
    df.dropna(inplace=True)
    df['Total'] = pd.to_numeric(df['Total'], errors='coerce')
    df['Phase 1'] = pd.to_numeric(df['Phase 1'], errors='coerce')
    df['Phase 2'] = pd.to_numeric(df['Phase 2'], errors='coerce')
    df['Phase 3'] = pd.to_numeric(df['Phase 3'], errors='coerce')
    return df

df = load_data()
st.title('EL Performance Analysis')
st.sidebar.header('Filter Data')
filter_option = st.sidebar.selectbox('Filter by:', ['Theme', 'Branch'])

if filter_option == 'Theme':
    selected_filter = st.sidebar.selectbox('Select Theme:', ['All'] + list(df['Theme'].unique()))
else:
    selected_filter = st.sidebar.selectbox('Select Branch:', ['All'] + list(df['Branch'].unique()))


if selected_filter != 'All':
    filtered_df = df[df[filter_option] == selected_filter]
    filtered_df = filtered_df.sort_values('Team Name')
else:
    filtered_df = df

st.subheader('Filtered Data')
st.dataframe(filtered_df, use_container_width=True)


with st.container():
    st.subheader('Total Marks Statistics')
    total_stats = filtered_df['Total'].agg(['mean', 'median', 'min', 'max'])
    st.dataframe(total_stats, use_container_width=True)

    st.subheader(f'Average Marks by Phase for {selected_filter}')
    phase_data = filtered_df[['Phase 1', 'Phase 2', 'Phase 3']].mean().reset_index()
    phase_data.columns = ['Phase', 'Average Marks']
    st.bar_chart(phase_data.set_index('Phase'))

with st.container():
    st.subheader('Comparison by Theme')
    themes = df['Theme'].unique()
    hist_data = [df[df['Theme'] == theme]['Total'].dropna().tolist() for theme in themes]
    fig = ff.create_distplot(hist_data, themes, bin_size=[2] * len(themes))

    fig.update_layout(
        title='Distribution of Total Marks by Theme',
        xaxis_title='Total Marks',
        yaxis_title='Density',
        legend_title='Themes'
    )

    st.plotly_chart(fig, use_container_width=True)

    theme_stats = df.groupby('Theme')['Total'].agg(['mean', 'median', 'min', 'max'])
    st.dataframe(theme_stats, use_container_width=True)

# New Streamlit page comparing average and median scores across batches for a particular theme
st.subheader('Comparison by Batch for Selected Theme')
if filter_option == 'Theme' and selected_filter != 'All':
    batch_data = filtered_df.groupby('Batch')['Total'].agg(['mean', 'median']).reset_index()
    batch_data.columns = ['Batch', 'Average Marks', 'Median Marks']
    st.line_chart(batch_data.set_index('Batch'))
else:
    st.write("Please select a specific theme to view batch-wise comparison.")
