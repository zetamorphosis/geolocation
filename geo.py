import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium  # Untuk menampilkan peta di Streamlit

# Title aplikasi
st.title("Map Geolocation Viewer")

# Upload file CSV
uploaded_file = st.file_uploader("Upload CSV file with Geolocation", type="csv")

if uploaded_file is not None:
    # Baca CSV
    df = pd.read_csv(uploaded_file)
    
    # Hapus spasi ekstra pada semua nama kolom (termasuk 'Geolocation ')
    df.columns = df.columns.str.strip()
    
    # Tampilkan preview data
    st.write("Preview Data:")
    st.dataframe(df)

    # Periksa apakah kolom 'Geolocation' ada di CSV
    if 'Geolocation' in df.columns:
        # Extract locations
        locations = []

        # Loop untuk mendapatkan semua titik dari kolom 'Geolocation'
        for loc in df['Geolocation']:
            try:
                # Pisahkan geolocation menjadi latitude dan longitude
                lat, lon = map(float, loc.split(','))
                locations.append([lat, lon])
            except:
                pass  # Lewatkan baris jika ada error parsing geolocation

        # Menentukan titik tengah peta berdasarkan rata-rata latitude dan longitude
        if locations:
            avg_lat = sum([loc[0] for loc in locations]) / len(locations)
            avg_lon = sum([loc[1] for loc in locations]) / len(locations)
        else:
            avg_lat, avg_lon = -6.119496, 106.662934  # Titik default jika tidak ada lokasi valid

        # Buat peta dengan lokasi awal
        m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

        # Tambahkan semua titik geolokasi ke peta dengan marker simbol
        for loc in locations:
            folium.Marker(
                location=loc, 
                popup=f"Location: {loc[0]}, {loc[1]}", 
                icon=folium.Icon(icon="info-sign")  # Menambahkan simbol pada marker
            ).add_to(m)

        # Tampilkan peta di Streamlit
        st_folium(m, width=700, height=500)
    else:
        st.error("Kolom 'Geolocation' tidak ditemukan dalam file CSV.")
