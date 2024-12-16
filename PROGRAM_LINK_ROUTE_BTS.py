import pandas as pd
import folium
from folium import plugins

# Fungsi untuk memuat file CSV
def load_routes_from_csv(file_path):
    data_routes = pd.read_csv(file_path)
    return data_routes['ROUTE'].tolist()  # Asumsi kolom "ROUTE" menyimpan data jalur

# Fungsi untuk memproses rute dan menambahkan panah pada peta
def process_route(route, bts_coords, map_bts):
    points = route.split('<NEC>')[::-1]  # Membaca dari kanan ke kiri
    route_coords = []
    
    for point in points:
        point = point.strip()
        
        # Periksa sufiks untuk menentukan warna ikon
        if '<ONT>' in point:
            point_id = point.split('<')[0]
            icon_color = "black"  # Warna untuk ONT
        elif '<ONT>' in point:
            point_id = point.split('<')[0]
            icon_color = "black"
        elif '<NEC>' in point:
            point_id = point.split('<')[0]
            icon_color = "red"
        elif '<L2SW>' in point:
            point_id = point.split('<')[0]
            icon_color = "black"  # Warna untuk L2SW
        elif 'OFDM' in point:
            point_id = point.split('<')[0]
            icon_color = "green"
        elif 'ROUTER' in point:
            point_id = point.split('<')[0]
            icon_color = "gray"
        else:
            point_id = point
            icon_color = "red"  # Warna default
        
        # Periksa apakah SITE ID ditemukan di koordinat BTS
        if point_id in bts_coords:
            site_info = bts_coords[point_id]
            coords = site_info['coords']
            route_coords.append(coords)
            
            # Siapkan konten untuk pop-up
            popup_content = f"""
                <div style="font-family: Arial; font-size: 14px;">
                    <b>{point_id}</b><br>
                    <i>{site_info['site_name']}</i><br>
                    {get_transmission_info(point_id)}
                </div>
            """
            
            # Tambahkan marker
            folium.Marker(
                location=coords,
                popup=popup_content,
                tooltip=f"SITE ID: {point_id}",
                icon=folium.Icon(color=icon_color)
            ).add_to(map_bts)

    # Jika ada lebih dari satu titik, tambahkan panah di sepanjang jalur
    if len(route_coords) > 1:
        line = folium.PolyLine(route_coords, color='transparent', weight=0).add_to(map_bts)  # Set garis tidak terlihat
        plugins.PolyLineTextPath(
            line,
            '→',  # Simbol panah
            repeat=True,
            offset=10,
            attributes={'fill': 'black', 'font-weight': 'bold', 'font-size': '11px'}
        ).add_to(map_bts)

# Fungsi untuk memuat koordinat BTS dari file Excel
def load_bts_coords(file_path):
    data_coords = pd.read_excel(file_path)
    bts_coords = {}
    
    for index, row in data_coords.iterrows():
        site_id = row['SITE ID']
        latitude = row['Latitude']
        longitude = row['Longitude']
        site_name = row['SITE NAME']
        if pd.notna(latitude) and pd.notna(longitude):
            bts_coords[site_id] = {
                'coords': (latitude, longitude),
                'site_name': site_name
            }
    return bts_coords

# Muat data transmisi dari Excel
def load_transmission_data(file_path):
    data = pd.read_excel(file_path)
    return data.set_index('SITE ID')  # Mengatur SITE ID sebagai index

# Mengambil informasi transmisi untuk SITE ID tertentu
import html

def get_transmission_info(site_id):
    if site_id in transmission_data.index:
        row = transmission_data.loc[site_id]

        # Fungsi untuk memproses nilai dan menghindari error
        def process_value(value):
            if pd.notna(value):  # Periksa apakah nilai tidak NaN
                return html.escape(str(value))  # Konversi ke string dan escape karakter HTML
            return "Tidak tersedia"
        longitude = process_value(row['Longitude'])
        latitude = process_value(row['Latitude'])
        band = process_value(row['BAND'])
        transport_2g = process_value(row['Remark Transport 2G'])
        transport_4g = process_value(row['Remark Transport 4G'])
        link_route_2g = process_value(row['LINK ROUTE 2G'])
        link_route_4g = process_value(row['LINK ROUTE 4G'])
        vlan_2g = process_value(row['VLAN 2G'])
        vlan_4g_up = process_value(row['VLAN 4G_UP'])
        vlan_4g_cp = process_value(row['VLAN 4G_CP'])
        vlan_oam = process_value(row['VLAN OAM'])
        ip_2g = process_value(row['IP 2G'])
        ip_4g_up = process_value(row['IP 4G_UP'])
        ip_4g_cp = process_value(row['IP 4G_CP'])
        ip_oam = process_value(row['IP OAM'])
        

        return (
            f"<b>BAND:</b> {band}<br>"
            f"<b>Longitude:</b> {longitude}<br>"
            f"<b>Latitude:</b> {latitude}<br>"
            f"<b>Transport 2G:</b> {transport_2g}<br>"
            f"<b>Transport 4G:</b> {transport_4g}<br>"
            f"<b>LinkRoute 2G:</b> {link_route_2g}<br>"
            f"<b>LinkRoute 4G:</b> {link_route_4g}<br>"
            f"<b>VLAN 2G:</b> {vlan_2g}<br>"
            f"<b>VLAN 4G UP:</b> {vlan_4g_up}<br>"
            f"<b>VLAN 4G CP:</b> {vlan_4g_cp}<br>"
            f"<b>VLAN OAM:</b> {vlan_oam}<br>"
            f"<b>IP 2G:</b> {ip_2g}<br>"
            f"<b>IP 4G UP:</b> {ip_4g_up}<br>"
            f"<b>IP 4G CP:</b> {ip_4g_cp}<br>"
            f"<b>IP OAM:</b> {ip_oam}<br>"
        )
    else:
        return "Data tidak ditemukan"



# Inisialisasi peta
map_bts = folium.Map(location=[-8.674722, 121.384444], zoom_start=12)

# Muat file koordinat BTS dari file Excel
bts_coords = load_bts_coords('D:/.xlsx')

# Muat rute dari file CSV
routes = load_routes_from_csv('D:/.CSV')

# Muat data transmisi
transmission_data = load_transmission_data('D:/.xlsx')

# Menambahkan marker untuk setiap BTS dari file koordinat
for site_id, info in bts_coords.items():
    coords = info['coords']
    site_name = info['site_name']
    
    # Siapkan konten untuk pop-up
    popup_content = f"""
        <div style="font-family: Arial; font-size: 14px;">
            <b>{site_id}</b><br>
            <i>{site_name}</i><br>
            {get_transmission_info(site_id)}
        </div>
    """
    
    folium.Marker(
        location=coords,
        popup=popup_content,
        tooltip=f"SITE ID: {site_id}",
        icon=folium.Icon(icon="star")
    ).add_to(map_bts)

    # Menambahkan SITE ID sebagai label (DivIcon) yang ditampilkan di sebelah marker
    folium.map.Marker(
        location=coords,
        icon=folium.DivIcon(
            html=f'<div style="font-size: 12px; color: black;"><b>{site_id}</b><br>{site_name}</div>')
    ).add_to(map_bts)

# Proses setiap rute dan tambahkan ke peta
for route in routes:
    process_route(route, bts_coords, map_bts)

# Menambahkan legenda
legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 150px; height: 130px; 
                background-color: white; z-index:9999; border:2px solid grey; 
                font-size:14px; padding: 10px;">
        <b>Legenda:</b><br>
        <i style="color: black;">&#9679;</i>ONT-L2SW<br>
        <i style="color: red;">&#9679;</i>Ipaso NEC<br>
        <i style="color: green;">&#9679;</i>OFDM<br>
        <i style="color: gray;">&#9679;</i>ROUTER<br>
    </div>
'''
map_bts.get_root().html.add_child(folium.Element(legend_html))

map_bts.get_root().html.add_child(folium.Element("""
    <script>
        // Meminta izin untuk mengakses lokasi pengguna
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                var lat = position.coords.latitude;
                var lon = position.coords.longitude;
                var userLocation = L.marker([lat, lon]).addTo(map);
                userLocation.bindPopup("<b>Lokasi Anda</b>").openPopup();
                map.setView([lat, lon], 13);
            });
        } else {
            alert("Geolocation tidak didukung oleh browser ini.");
        }
    </script>
"""))



import folium
from folium.plugins import LocateControl

# Inisialisasi peta

# Tambahkan tombol pelacakan lokasi pengguna
LocateControl(auto_start=True).add_to(map_bts)

# Tambahkan script JavaScript untuk menangani lokasi pengguna
map_bts.get_root().html.add_child(folium.Element("""
    <script>
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    var lat = position.coords.latitude;
                    var lon = position.coords.longitude;
                    
                    // Tambahkan marker di lokasi pengguna
                    var userLocation = L.marker([lat, lon]).addTo(map);
                    userLocation.bindPopup("<b>Lokasi Anda</b>").openPopup();
                    
                    // Pusatkan peta ke lokasi pengguna
                    map.setView([lat, lon], 13);
                },
                function(error) {
                    alert("Gagal mendapatkan lokasi: " + error.message);
                }
            );
        } else {
            alert("Browser tidak mendukung Geolocation.");
        }
    </script>
"""))

# Simpan peta sebagai file HTML


print("Peta dengan pelacakan lokasi pengguna telah dibuat.")



# Simpan peta sebagai file HTML
map_bts.save('D:/Link_Route_1.html')

print("Peta BTS dengan jalur berhasil dibuat.")


# Menambahkan JavaScript untuk lokasi pengguna secara otomatis


# Simpan peta sebagai file HTML


