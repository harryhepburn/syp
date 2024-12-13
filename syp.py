import streamlit as st
import pandas as pd
import numpy as np

# Create the DataFrame
data = {
    'Zon Taburan Hujan': ['Tinggi 1'] * 75,
    'Kelas Tanah': ['1'] * 75,
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
    st.title('Analisis Potensi Hasil Sawit')
    
    # Sidebar for input selections
    st.sidebar.header('Pilih Kriteria')
    
    # Unique values for each attribute
    zon_options = df['Zon Taburan Hujan'].unique()
    kelas_options = df['Kelas Tanah'].unique()
    topografi_options = df['Topografi'].unique()
    tahun_options = df['Tahun Tuai'].unique()
    
    # Dropdown selections
    selected_zon = st.sidebar.selectbox('Pilih Zon Taburan Hujan', zon_options)
    selected_kelas = st.sidebar.selectbox('Pilih Kelas Tanah', kelas_options)
    selected_topografi = st.sidebar.selectbox('Pilih Topografi', topografi_options)
    selected_tahun = st.sidebar.selectbox('Pilih Tahun Tuai', tahun_options)
    
    # Filter the dataframe based on selections
    filtered_df = df[
        (df['Zon Taburan Hujan'] == selected_zon) & 
        (df['Kelas Tanah'] == selected_kelas) & 
        (df['Topografi'] == selected_topografi) & 
        (df['Tahun Tuai'] == selected_tahun)
    ]
    
    # Display results
    st.header('Hasil Analisis')
    
    if not filtered_df.empty:
        st.write('### Potensi Hasil:', filtered_df['Potensi Hasil'].values[0])
        
        # Visualization
        st.subheader('Grafik Potensi Hasil Berdasarkan Topografi')
        chart_data = df.groupby('Topografi')['Potensi Hasil'].mean().reset_index()
        st.bar_chart(chart_data.set_index('Topografi'))
        
        # Additional information
        st.subheader('Informasi Tambahan')
        col1, col2 = st.columns(2)
        with col1:
            st.metric('Zon Taburan Hujan', selected_zon)
            st.metric('Kelas Tanah', selected_kelas)
        with col2:
            st.metric('Topografi', selected_topografi)
            st.metric('Tahun Tuai', selected_tahun)
    else:
        st.warning('Tidak ada data yang sesuai dengan kriteria pilihan.')
    
    # Raw data display (optional)
    if st.checkbox('Tampilkan Data Mentah'):
        st.dataframe(df)

# Save the Streamlit app script
if __name__ == '__main__':
    import streamlit as st
    create_streamlit_app()

# Instructions for running the app
print("To run this Streamlit app:")
print("1. Save this script as `app.py`")
print("2. Install required libraries: pip install streamlit pandas")
print("3. Run the app: streamlit run app.py")
