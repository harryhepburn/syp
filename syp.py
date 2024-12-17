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

# Data for the Kelas Tanah table
def get_soil_class_table():
    data = {
        "Kelas Tanah": ["Kelas 1 (Sangat sesuai)"] * 2 + ["Kelas 2 (Sesuai)"] * 28 + ["Kelas 3 (Kurang sesuai)"] * 30,
        "Jenis Tanah": ["SELANGOR", "KANGKONG", "BRIAH", "TELONG", "SEGAMAT", "KUANTAN", "BENTA", "SK. MAS", 
                        "KATONG", "SABAK", "YONG PENG", "TOM YONG", "KEMUNING", "JERANGAU", "JEMBANG", "JELAI", 
                        "CHAMP", "MUSANG", "SEMPAKA", "KAMPONG KOLAM", "MASSA", "LENGKAWI", "NENASI", "BATANG MERBAU", 
                        "LIMBAT", "TEBOK", "KALLA", "COLLUVIUM", "BUKIT", "ORGANIC ALLUVIUM", "LOCAL ALLUVIUM", 
                        "BUNGOR", "CHEROK", "SEMUPURNA/IMD", "BATANG", "BESAI", "RAU", "TAPAH", "RASAU", "BUNGOR", 
                        "ROMPIN", "RUDUA", "MUNCHONG/L", "BUNGOR/S", "DURIAN", "CHENIAN/S", "DUTALAN", "BATU LAPAN", 
                        "HARRADIL", "MERAPOH/L", "MT. HAIL", "MALACCA", "HARRADS", "GAJAH MATI", "MERAPOH", "HARAD/ACAD", 
                        "KEDAH", "TAY", "SEREMBAN", "KANTIS", "KALI BUKIT", "DURIAN ALAM", "SEMPORNA/S", "BATU/M", 
                        "PAGOH", "ORGANIC CLAY MUCK", "SANDY COLLUVIUM", "SRANTI", "KUALA BERANG", "BUKIT TUKU", 
                        "KAMP. KUBUR", "ULU TIRAM", "JABIL", "SEDIRANG", "MARANG", "TAPAH", "BINA", "KUALA BRANG", 
                        "PEAT/D"],
        "Kod": ["SLR", "KGR", "BRH", "TLG", "SGT", "KTN", "BNT", "SMS", "KTG", "SBK", "YPG", "TYN", "KMG", "JRN", "JMB", 
                "JLC", "CPG", "MUS", "SPA", "KKL", "MSI", "LKI", "NBI", "MRB", "LBT", "TBK", "KLL", "COL", "BKT", "ORA", 
                "LRA", "BGR", "CRK", "SPAMD", "BTG", "BSH", "RAU", "TGH", "RAS", "RGR", "RPN", "RDA", "MUNL", "BRS", 
                "DUR", "CHNS", "DTL", "BNL", "HRDL", "MRPL", "MTH", "MLC", "HRDS", "GMH", "MRP", "HRA", "KDH", "TAY", 
                "SRB", "KNT", "KBUK", "DAL", "SMP", "BTM", "PGH", "OCM", "SCL", "SRA", "KBG", "BKTK", "KPR", "ULT", 
                "JBL", "SDR", "MRG", "TGH", "BNA", "KLG/KBG", "PET/D"],
        "Kumpulan": [1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                     4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                     5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
    }
    return pd.DataFrame(data)

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
    soil_df = get_topography_table()
    st.dataframe(soil_df)

    st.markdown("### Developed by Rafizan Samian - FELDA Strategy & Transformation Department")

if __name__ == "__main__":
    main()
