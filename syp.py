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

@st.cache_data
def load_soil_class_data():
    data = pd.read_csv('KELASTANAH.csv')
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
            'Tahun Tuai': 'Tahun Tuaian',
            'Potensi Hasil': 'Potensi Hasil (SYP) (metric tan/hektar)'
        },
        markers=True
    )
    
    # Customize hover template
    fig.update_traces(
        hovertemplate='<b>Tahun Tuai</b>: %{x}<br><b>SYP</b>: %{y:.2f} metrik tan/hektar<extra></extra>',
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
        xaxis_title='Tahun Tuaian',
        yaxis_title='Site Yield Potential (metrik tan/hektar)',
        height=450
    )
    
    return fig
    
def get_topography_table():
    datatopo = {
        "TOPOGRAFI": ["Beralun Lemah", "Beralun Sederhana", "Berbukit"],
        "KOD": ["G", "M", "H"],
        "KETERANGAN": [
            "Kurang Daripada Empat (4) Darjah", 
            "Lima (5) Hingga Dua Belas (12) Darjah", 
            "Melebihi Dua Belas (12) Darjah"
        ]
    }
    return pd.DataFrame(datatopo)

def get_rainfall_table():
    datahujan = {
        "ZON TABURAN HUJAN": ["Lembap", "Sederhana Lembap", "Kering"],
        "KOD": ["W", "M", "D"],
        "KETERANGAN": [
            "Menerima Hujan Melebihi 2500mm Setahun", 
            "Menerima Hujan di Antara 1800mm - 2500mm Setahun", 
            "Menerima Hujan kurang daripada 1800mm Setahun"
        ]
    }
    return pd.DataFrame(datahujan)
    
def get_soilclass_table():
    datatanah = {
        "KELAS TANAH": ["Kelas 1", "Kelas 2", "Kelas 3"],
        "KUMPULAN TANAH": ["1 dan 2", "3 dan 4", "5 dan 6"],
        "KETERANGAN": [
            "Sangat Sesuai untuk Tanaman Sawit", 
            "Sesuai untuk Tanaman Sawit", 
            "Kurang Sesuai untuk Tanaman Sawit"
        ]
    }
    return pd.DataFrame(datatanah)
    
def main():
    st.title('Kalkulator Potensi Hasil Sawit')
    st.subheader('_Site Yield Potential_ (SYP) _Calculator_')
    # Load data
    df = load_data()
    soil_class_df = load_soil_class_data()

    
    
    # Create columns for input
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Rainfall Zone Selection
        rainfall_zones = df['Zon Taburan Hujan'].unique()
        rainfall_zone = st.selectbox('Zon Taburan Hujan', rainfall_zones)
    
    with col2:
         # Topography Selection
        topographies = df['Topografi'].unique()
        topography = st.selectbox('Topografi', topographies)
       
    with col3:
        # Soil Class Selection
        soil_classes = df['Kelas Tanah'].unique()
        soil_class = st.selectbox('Kelas Tanah', soil_classes)

    
    # Year Selection
    max_year = df['Tahun Tuai'].max()
    min_year = df['Tahun Tuai'].min()
    year = st.slider('Tahun Tuaian', min_value=min_year, max_value=max_year, value=min_year)
    
    # Calculate Button
    if st.button('Kira SYP'):
        syp = predict_syp(df, rainfall_zone, soil_class, topography, year)
        
        if syp is not None:
            st.success(f'Anggaran SYP: {syp:.2f} metrik tan per hektar')
            
            # Additional Visualization with Plotly
            st.subheader('Tren Potensi Hasil (SYP) Untuk 25 Tahun')
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
                ### Rumusan SYP
                - **Hasil Minimum**: {min_yield:.2f} metrik tan/hektar
                - **Hasil Maximum**: {max_yield:.2f} metrik tan/hektar
                - **Hasil Purata**: {avg_yield:.2f} metrik tan/hektar
                """)
        else:
            st.error('Tiada Data Ditemui. Ubah parameter anda.')

    # Display Rainfall Table
    st.subheader("Maklumat Zon Taburan Hujan")
    rain_df = get_rainfall_table()
    st.dataframe(rain_df)
    
    # Display Topography Table
    st.subheader("Maklumat Topografi")
    topo_df = get_topography_table()
    st.dataframe(topo_df)

    # Display Soil Class Table
    st.subheader("Maklumat Kelas Tanah")
    soil_df = get_soilclass_table()
    st.dataframe(soil_df)

    if st.checkbox('Tampilkan Data Mentah'):
        st.subheader('Soil Classification Lookup')
        
            # Create columns for filtering
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Kelas Tanah Filter
            kelas_tanah_options = ['All'] + list(soil_class_df['Kelas Tanah'].unique())
            selected_kelas_tanah = st.selectbox('Soil Class', kelas_tanah_options)
        
        with col2:
            # Jenis Tanah Filter
            jenis_tanah_options = ['All'] + list(soil_class_df['Jenis Tanah'].unique())
            selected_jenis_tanah = st.selectbox('Soil Type', jenis_tanah_options)
        
        with col3:
            # Kod Filter
            kod_options = ['All'] + list(soil_class_df['Kod'].unique())
            selected_kod = st.selectbox('Soil Code', kod_options)
        
        with col4:
            # Kumpulan Filter
            kumpulan_options = ['All'] + list(map(str, soil_class_df['Kumpulan'].unique()))
            selected_kumpulan = st.selectbox('Group', kumpulan_options)
        
        # Apply Filters
        filtered_df = soil_class_df.copy()
        
        if selected_kelas_tanah != 'All':
            filtered_df = filtered_df[filtered_df['Kelas Tanah'] == selected_kelas_tanah]
        
        if selected_jenis_tanah != 'All':
            filtered_df = filtered_df[filtered_df['Jenis Tanah'] == selected_jenis_tanah]
        
        if selected_kod != 'All':
            filtered_df = filtered_df[filtered_df['Kod'] == selected_kod]
        
        if selected_kumpulan != 'All':
            filtered_df = filtered_df[filtered_df['Kumpulan'] == int(selected_kumpulan)]
        
        # Display Filtered Results
        st.dataframe(filtered_df, use_container_width=True)
        
    
    # Footer
    # st.markdown('### Dibangunkan oleh Rafizan Samian - Jabatan Strategi & Transformasi FELDA')

    st.sidebar.markdown("""
    ## Kalkulator Potensi Hasil Sawit
    ## _Site Yield Potential (SYP) Calculator_

    ### 🎯 Objektif
    Aplikasi membantu pekerja industri kelapa sawit dalam:
    - Mengira potensi hasil tapak
    - Mencari maklumat klasifikasi tanah
    - Menganalisis trend prestasi

    ### ✨ Ciri Utama
    - Kalkulator Potensi Hasil
    - Pencarian Klasifikasi Tanah
    - Visualisasi Trend Prestasi

    ### 👤 Pembangunan
    **Dibangunkan oleh:**
    Rafizan Samian
    Jabatan Strategi & Transformasi
    FELDA

    ### ℹ️ Perhatian
    *Keputusan adalah anggaran berdasarkan data terdahulu (historical data).*
    """)

    # Optional: Add a visual element or logo
    #st.sidebar.image("/path/to/felda_logo.png", use_column_width=True)

if __name__ == '__main__':
    main()
