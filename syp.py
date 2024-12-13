import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Prepare the data
data = {
    'Zon Taburan Hujan': ['Tinggi 1'] * 75,
    'Kelas Tanah': (
        ['Rata'] * 25 + 
        ['Beralun'] * 25 + 
        ['Berbukit'] * 25
    ),
    'Topografi': (
        ['Rata'] * 25 + 
        ['Beralun'] * 25 + 
        ['Berbukit'] * 25
    ),
    'Tahun Tuai': list(range(1, 26)) * 3,
    'Potensi Hasil': (
        [18, 23, 30, 32, 35, 35, 35, 35, 35, 35, 
         35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 
         35, 33, 32, 31, 31] +
        [16, 21, 28, 30, 30, 30, 30, 30, 30, 30, 
         30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 
         30, 29, 28, 25, 25] +
        [10, 15, 20, 23, 25, 25, 25, 25, 25, 25, 
         25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 
         25, 24, 23, 20, 20]
    )
}

df = pd.DataFrame(data)

def create_streamlit_app():
    st.set_page_config(page_title='Analisis Potensi Hasil Sawit', layout='wide')
    
    st.title('🌴 Analisis Potensi Hasil Sawit')
    
    # Sidebar for input selections
    st.sidebar.header('🔍 Pilih Kriteria')
    
    # Unique values for each attribute
    zon_options = df['Zon Taburan Hujan'].unique()
    kelas_options = df['Kelas Tanah'].unique()
    topografi_options = df['Topografi'].unique()
    tahun_options = sorted(df['Tahun Tuai'].unique())
    
    # Dropdown selections
    col1, col2 = st.sidebar.columns(2)
    with col1:
        selected_zon = st.selectbox('Zon Taburan Hujan', zon_options)
        selected_kelas = st.selectbox('Kelas Tanah', kelas_options)
    with col2:
        selected_topografi = st.selectbox('Topografi', topografi_options)
        selected_tahun = st.selectbox('Tahun Tuai', tahun_options)
    
    # Filter the dataframe based on selections
    filtered_df = df[
        (df['Zon Taburan Hujan'] == selected_zon) & 
        (df['Kelas Tanah'] == selected_kelas) & 
        (df['Topografi'] == selected_topografi) & 
        (df['Tahun Tuai'] == selected_tahun)
    ]
    
    # Main display area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header('📊 Hasil Analisis')
        
        if not filtered_df.empty:
            # Display Yield Potential
            st.metric('Potensi Hasil', f"{filtered_df['Potensi Hasil'].values[0]} Kg/Pokok")
            
            # Comparative Visualization
            st.subheader('Perbandingan Potensi Hasil')
            
            # Group by Topografi and calculate mean yield
            topografi_yield = df.groupby('Topografi')['Potensi Hasil'].mean()
            
            # Create bar chart
            fig = px.bar(
                x=topografi_yield.index, 
                y=topografi_yield.values, 
                labels={'x': 'Topografi', 'y': 'Rata-rata Potensi Hasil'},
                title='Potensi Hasil Berdasarkan Topografi'
            )
            st.plotly_chart(fig)
        else:
            st.warning('Tidak ada data yang sesuai dengan kriteria pilihan.')
    
    with col2:
        st.header('📝 Detail Informasi')
        if not filtered_df.empty:
            st.write(f"**Zon Taburan Hujan:** {selected_zon}")
            st.write(f"**Kelas Tanah:** {selected_kelas}")
            st.write(f"**Topografi:** {selected_topografi}")
            st.write(f"**Tahun Tuai:** {selected_tahun}")
        
        # Descriptive Statistics
        st.subheader('Statistik Deskriptif')
        st.write(df.describe())
    
    # Raw data display (optional)
    if st.checkbox('Tampilkan Data Mentah'):
        st.dataframe(df)

# Create a function to run the Streamlit app
def main():
    create_streamlit_app()

if __name__ == '__main__':
    main()

# Instructions for running the app
print("Petunjuk Menjalankan Aplikasi:")
print("1. Simpan skrip ini sebagai `app.py`")
print("2. Install library yang diperlukan: pip install streamlit pandas plotly")
print("3. Jalankan aplikasi: streamlit run app.py")
