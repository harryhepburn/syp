import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

# Load the dataset
@st.cache_data
def load_data():
    data = pd.read_csv('SYP.csv')
    return data

def predict_syp(df, rainfall_zone, soil_class, topography, year):
    """
    Predict Site Yield Potential based on input parameters
    """
    # Validate inputs
    filtered_df = df[
        (df['Zon Taburan Hujan'] == rainfall_zone) & 
        (df['Kelas Tanah'] == soil_class) & 
        (df['Topografi'] == topography)
    ]
    
    if filtered_df.empty:
        return None
    
    # Find closest year or interpolate
    closest_year_row = filtered_df.iloc[(filtered_df['Tahun Tuai'] - year).abs().argsort()[:1]]
    
    return closest_year_row['Potensi Hasil'].values[0]

def main():
    st.title('Palm Oil Site Yield Potential (SYP) Calculator')
    
    # Load data
    df = load_data()
    
    # Sidebar for input
    st.sidebar.header('Input Parameters')
    
    # Rainfall Zone Selection
    rainfall_zones = df['Zon Taburan Hujan'].unique()
    rainfall_zone = st.sidebar.selectbox('Rainfall Zone', rainfall_zones)
    
    # Soil Class Selection
    soil_classes = df['Kelas Tanah'].unique()
    soil_class = st.sidebar.selectbox('Soil Class', soil_classes)
    
    # Topography Selection
    topographies = df['Topografi'].unique()
    topography = st.sidebar.selectbox('Topography', topographies)
    
    # Year Selection
    max_year = df['Tahun Tuai'].max()
    min_year = df['Tahun Tuai'].min()
    year = st.sidebar.slider('Planting Year', min_value=min_year, max_value=max_year, value=min_year)
    
    # Predict SYP
    if st.sidebar.button('Calculate SYP'):
        syp = predict_syp(df, rainfall_zone, soil_class, topography, year)
        
        if syp is not None:
            st.success(f'Estimated Site Yield Potential: {syp:.2f} metric tons per hectare')
            
            # Additional Visualization
            st.subheader('Performance Trend')
            year_data = df[
                (df['Zon Taburan Hujan'] == rainfall_zone) & 
                (df['Kelas Tanah'] == soil_class) & 
                (df['Topografi'] == topography)
            ]
            st.line_chart(year_data.set_index('Tahun Tuai')['Potensi Hasil'])
        else:
            st.error('No matching data found. Please adjust your parameters.')
    
    # Dataset Information
    st.sidebar.markdown('### Dibangunkan oleh Rafizan Samian, Jabatan Strategi & Transformasi FELDA')


###



def create_interactive_performance_chart(df, rainfall_zone, soil_class, topography):
    # Filter data based on selected parameters
    year_data = df[
        (df['Zon Taburan Hujan'] == rainfall_zone) & 
        (df['Kelas Tanah'] == soil_class) & 
        (df['Topografi'] == topography)
    ]
    
    # Create interactive Plotly line chart
    fig = px.line(
        year_data, 
        x='Tahun Tuai', 
        y='Potensi Hasil',
        title=f'Performance Trend: {rainfall_zone}, {soil_class}, {topography}',
        labels={
            'Tahun Tuai': 'Harvest Year',
            'Potensi Hasil': 'Potential Yield'
        },
        markers=True
    )
    
    # Customize hover template
    fig.update_traces(
        hovertemplate='<b>Year</b>: %{x}<br><b>Potential Yield</b>: %{y}<extra></extra>'
    )
    
    # Adjust layout for better readability
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        )
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)



if __name__ == '__main__':
    main()
