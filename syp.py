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
    
def main():
    st.title('Palm Oil Site Yield Potential (SYP) Calculator')
    
    # Load data
    df = load_data()
    
    # Create columns for input
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Rainfall Zone Selection
        rainfall_zones = df['Zon Taburan Hujan'].unique()
        rainfall_zone = st.selectbox('Rainfall Zone', rainfall_zones)
    
    with col2:
        # Soil Class Selection
        soil_classes = df['Kelas Tanah'].unique()
        soil_class = st.selectbox('Soil Class', soil_classes)
    
    with col3:
        # Topography Selection
        topographies = df['Topografi'].unique()
        topography = st.selectbox('Topography', topographies)
    
    # Year Selection
    max_year = df['Tahun Tuai'].max()
    min_year = df['Tahun Tuai'].min()
    year = st.slider('Planting Year', min_value=min_year, max_value=max_year, value=min_year)
    
    # Calculate Button
    if st.button('Calculate Site Yield Potential'):
        syp = predict_syp(df, rainfall_zone, soil_class, topography, year)
        
        if syp is not None:
            st.success(f'Estimated Site Yield Potential: {syp:.2f} metric tons per hectare')
            
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
    


# Data for the table
data = {
    "Kelas Tanah": ["Kelas 1 (Sangat sesuai)"] * 2 + ["Kelas 2 (Sesuai)"] * 28 + ["Kelas 3 (Kurang sesuai)"] * 30,
    "Jenis Tanah": [
        "SELANGOR", "KANGKONG", "BRIAH", "TELONG", "SEGAMAT", "KUANTAN", "BENTA", "SK. MAS", "KATONG", "SABAK",
        "YONG PENG", "TOM YONG", "KEMUNING", "JERANGAU", "JEMBANG", "JELAI", "CHAMP", "MUSANG", "SEMPAKA",
        "KAMPONG KOLAM", "MASSA", "LENGKAWI", "NENASI", "BATANG MERBAU", "LIMBAT", "TEBOK", "KALLA", "COLLUVIUM",
        "BUKIT", "ORGANIC ALLUVIUM", "LOCAL ALLUVIUM", "BUNGOR", "CHEROK", "SEMUPURNA/IMD", "BATANG", "BESAI",
        "RAU", "TAPAH", "RASAU", "BUNGOR", "ROMPIN",
        "RUDUA", "MUNCHONG/L", "BUNGOR/S", "DURIAN", "CHENIAN/S", "DUTALAN", "BATU LAPAN", "HARRADIL", "MERAPOH/L",
        "MT. HAIL", "MALACCA", "HARRADS", "GAJAH MATI", "MERAPOH", "HARAD/ACAD", "KEDAH", "TAY", "SEREMBAN", "KANTIS",
        "KALI BUKIT", "DURIAN ALAM", "SEMPORNA/S", "BATU/M", "PAGOH", "ORGANIC CLAY MUCK", "SANDY COLLUVIUM", 
        "SRANTI", "KUALA BERANG", "BUKIT TUKU", "KAMP. KUBUR", "ULU TIRAM", "JABIL", "SEDIRANG", "MARANG", 
        "TAPAH", "BINA", "KUALA BRANG", "PEAT/D"
    ],
    "Kod": [
        "SLR", "KGR", "BRH", "TLG", "SGT", "KTN", "BNT", "SMS", "KTG", "SBK",
        "YPG", "TYN", "KMG", "JRN", "JMB", "JLC", "CPG", "MUS", "SPA", "KKL",
        "MSI", "LKI", "NBI", "MRB", "LBT", "TBK", "KLL", "COL", "BKT", "ORA",
        "LRA", "BGR", "CRK", "SPAMD", "BTG", "BSH", "RAU", "TGH", "RAS", "RGR", "RPN",
        "RDA", "MUNL", "BRS", "DUR", "CHNS", "DTL", "BNL", "HRDL", "MRPL", "MTH",
        "MLC", "HRDS", "GMH", "MRP", "HRA", "KDH", "TAY", "SRB", "KNT", "KBUK",
        "DAL", "SMP", "BTM", "PGH", "OCM", "SCL", "SRA", "KBG", "BKTK", "KPR",
        "ULT", "JBL", "SDR", "MRG", "TGH", "BNA", "KLG/KBG", "PET/D"
    ],
    "Kumpulan": [
        1, 1, 2, 2, 2, 3, 3, 3, 3, 3,
        3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
        3, 3, 4, 4, 4, 4, 4, 4, 4, 4,
        4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
        4, 4, 5, 5, 5, 5, 5, 5, 5, 5,
        5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
        5, 5, 5, 5, 5, 5, 5, 6, 6, 6,
        6, 6, 6, 6, 6, 6, 6
    ]
}

# Create the DataFrame
df = pd.DataFrame(data)

# Streamlit App
st.title("Kelas Tanah Table")


# Display the table
st.dataframe(df)

    # Footer
    st.markdown('### Developed by Rafizan Samian - FELDA Strategy & Transformation Department')

if __name__ == '__main__':
    main()
