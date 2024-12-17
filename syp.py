import streamlit as st
import pandas as pd
import plotly.express as px

# Function to load SYP.csv
@st.cache_data
def load_data():
    try:
        data = pd.read_csv('SYP.csv')
        return data
    except FileNotFoundError:
        st.error("File 'SYP.csv' not found. Please ensure the file is in the correct directory.")
        return None

# Function to predict Site Yield Potential
def predict_syp(df, rainfall_zone, soil_class, topography, year):
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

# Function to create performance trend chart
def create_performance_trend_chart(year_data):
    fig = px.line(
        year_data, 
        x='Tahun Tuai', 
        y='Potensi Hasil',
        title='Performance Trend',
        labels={'Tahun Tuai': 'Year', 'Potensi Hasil': 'Yield Potential (MT/ha)'},
        markers=True
    )
    return fig

def get_topography_table():
    data = {
        "TOPOGRAFI": ["Beralun Lemah", "Beralun Sederhana", "Berbukit"],
        "KOD": ["G", "M", "H"],
        "KETERANGAN": ["Kurang Daripada Empat (4) Darjah", "Lima (5) Hingga Dua Belas (12) Darjah", "Melebihi Dua Belas (12) Darjah"],
        
    }
    return pd.DataFrame(data)

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
    year = st.slider("Planting Year", int(df['Tahun Tuai'].min()), int(df['Tahun Tuai'].max()))

    if st.button("Calculate Site Yield Potential"):
        syp = predict_syp(df, rainfall_zone, soil_class, topography, year)
        if syp:
            st.success(f"Estimated Yield Potential: {syp:.2f} MT/ha")
        else:
            st.error("No matching data found.")
    
    # Display Soil Class Table
    st.subheader("Maklumat Topografi")
    topo_df = get_topography_table()
    st.dataframe(topo_df)

    st.markdown("### Developed by Rafizan Samian - FELDA Strategy & Transformation Department")

if __name__ == "__main__":
    main()
