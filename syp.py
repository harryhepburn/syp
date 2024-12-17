import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

# Function to load SYP.csv with improved error handling
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data():
    try:
        data = pd.read_csv('SYP.csv', encoding='utf-8')
        # Additional data validation
        required_columns = ['Zon Taburan Hujan', 'Kelas Tanah', 'Topografi', 'Tahun Tuai', 'Potensi Hasil']
        for col in required_columns:
            if col not in data.columns:
                st.error(f"Missing required column: {col}")
                return None
        return data
    except FileNotFoundError:
        st.error("File 'SYP.csv' not found. Please ensure the file is in the correct directory.")
        return None
    except pd.errors.EmptyDataError:
        st.error("The CSV file is empty.")
        return None
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")
        return None

# Function to predict Site Yield Potential
def predict_syp(df, rainfall_zone, soil_class, topography, year):
    try:
        filtered_df = df[
            (df['Zon Taburan Hujan'] == rainfall_zone) & 
            (df['Kelas Tanah'] == soil_class) & 
            (df['Topografi'] == topography)
        ]
        
        if filtered_df.empty:
            return None
        
        # Find closest year
        closest_row = filtered_df.iloc[(filtered_df['Tahun Tuai'] - year).abs().argsort()[:1]]
        return closest_row['Potensi Hasil'].values[0]
    except Exception as e:
        st.error(f"Error in prediction: {e}")
        return None

def create_performance_trend_chart(year_data):
    """
    Create an interactive Plotly line chart for performance trend
    """
    # Create interactive Plotly line chart
    fig = px.line(
        year_data, 
        x='Tahun Tuai', 
        y='Potensi Hasil',
        title='Performance Trend',
        labels={
            'Tahun Tuai': 'Planting Year',
            'Potensi Hasil': 'Site Yield Potential (metric tons/hectare)'
        },
        markers=True
    )
    
    # Customize hover template
    fig.update_traces(
        hovertemplate='<b>Planting Year</b>: %{x}<br><b>Yield Potential</b>: %{y:.2f} metric tons/hectare<extra></extra>',
        line=dict(width=3),
        marker=dict(size=8)
    )
    
    # Adjust layout for better readability
    fig.update_layout(
        hovermode='closest',
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        ),
        xaxis_title='Planting Year',
        yaxis_title='Site Yield Potential (metric tons/hectare)',
        height=450
    )
    
    return fig

# Function to get topography table
def get_topography_table():
    data = {
        "TOPOGRAFI": ["Beralun Lemah", "Beralun Sederhana", "Berbukit"],
        "KOD": ["G", "M", "H"],
        "KETERANGAN": [
            "Kurang Daripada Empat (4) Darjah", 
            "Lima (5) Hingga Dua Belas (12) Darjah", 
            "Melebihi Dua Belas (12) Darjah"
        ]
    }
    return pd.DataFrame(data)

# Main application function
def main():
    st.title("Palm Oil Site Yield Potential (SYP) Calculator")
    
    # Load SYP Data
    df = load_data()
    if df is None:
        return
    
    # User Input: Rainfall Zone, Soil Class, Topography, Year
    col1, col2, col3 = st.columns(3)
    with col1:
        rainfall_zone = st.selectbox("Rainfall Zone", df['Zon Taburan Hujan'].unique())
    with col2:
        soil_class = st.selectbox("Soil Class", df['Kelas Tanah'].unique())
    with col3:
        topography = st.selectbox("Topography", df['Topografi'].unique())
    
    year = st.slider(
        "Planting Year", 
        min_value=int(df['Tahun Tuai'].min()), 
        max_value=int(df['Tahun Tuai'].max()),
        value=int(df['Tahun Tuai'].min())
    )
    
    if st.button("Calculate Site Yield Potential"):
        syp = predict_syp(df, rainfall_zone, soil_class, topography, year)
        if syp is not None:
            st.success(f"Estimated Yield Potential: {syp:.2f} MT/ha")
        else:
            st.warning("No matching data found for the selected criteria.")
    
            # Additional Visualization with Plotly
            st.subheader('Performance Trend')
            year_data = df[
                (df['Zon Taburan Hujan'] == rainfall_zone) & 
                (df['Kelas Tanah'] == soil_class) & 
                (df['Topografi'] == topography)
            ]
            
            # Create and display Plotly chart
            fig = create_performance_trend_chart(year_data)
            st.plotly_chart(fig, use_container_width=True)
            
            # Optional: Add some additional insights
            if not year_data.empty:
                min_yield = year_data['Potensi Hasil'].min()
                max_yield = year_data['Potensi Hasil'].max()
                avg_yield = year_data['Potensi Hasil'].mean()
                
                st.markdown(f"""
                ### Yield Insights
                - **Minimum Yield**: {min_yield:.2f} metric tons/hectare
                - **Maximum Yield**: {max_yield:.2f} metric tons/hectare
                - **Average Yield**: {avg_yield:.2f} metric tons/hectare
                """)
        else:
            st.error('No matching data found. Please adjust your parameters.')
   
    
    # Display Topography Table
    st.subheader("Maklumat Topografi")
    topo_df = get_topography_table()
    st.dataframe(topo_df)
    
    st.markdown("### Developed by Rafizan Samian - FELDA Strategy & Transformation Department")

# Run the main application
if __name__ == "__main__":
    main()


