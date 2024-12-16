# Folium

# README

## Deskripsi Proyek

Selamat datang di proyek **Peta BTS dan Rute**! Aplikasi ini bertujuan untuk memvisualisasikan jaringan BTS (Base Transceiver Station) dan rute transmisi menggunakan peta interaktif. Dengan menggunakan data dari file Excel dan CSV, peta ini memberikan tampilan yang jelas tentang lokasi BTS serta rute yang dilalui.

### Fitur Utama

- **Visualisasi BTS**: Menampilkan marker BTS berdasarkan koordinat yang diambil dari file Excel.
- **Rute Transmisi**: Menambahkan jalur rute dari file CSV, lengkap dengan panah untuk menunjukkan arah.
- **Info Pop-up**: Setiap marker dilengkapi dengan pop-up yang berisi informasi detail mengenai BTS, termasuk data transmisi.
- **Pelacakan Lokasi Pengguna**: Memungkinkan pengguna untuk melihat posisi mereka sendiri di peta dengan menggunakan geolokasi.
- **Legenda**: Menyediakan legenda untuk membantu pengguna memahami ikon di peta.

### Teknologi yang Digunakan

- **Pandas**: Untuk mengelola data dari file Excel dan CSV.
- **Folium**: Untuk membuat peta interaktif berbasis JavaScript.
- **HTML dan JavaScript**: Untuk interaktivitas dan pengaturan tampilan peta.

### Cara Menggunakan

1. **Instalasi**: Pastikan Anda telah menginstal pustaka yang diperlukan:
   ```bash
   pip install pandas folium
   ```

2. **Persiapan Data**: Siapkan dua file:
   - **File Excel** yang berisi informasi BTS (kolom yang diperlukan: `SITE ID`, `Latitude`, `Longitude`, `SITE NAME`, dan detail lainnya).
   - **File CSV** yang berisi jalur rute dengan kolom `ROUTE`.

3. **Modifikasi Kode**: Sesuaikan jalur file input dalam kode:
   ```python
   bts_coords = load_bts_coords('D:/data_bts.xlsx')
   routes = load_routes_from_csv('D:/data_routes.csv')
   transmission_data = load_transmission_data('D:/data_transmission.xlsx')
   ```

4. **Menjalankan Kode**: Jalankan skrip Python untuk menghasilkan peta:
   ```bash
   python main.py
   ```

5. **Membuka Peta**: Setelah peta dibuat, Anda akan mendapatkan file HTML (`Link_Route_1.html`) yang dapat dibuka di browser.

### Contoh Keluaran

Setelah menjalankan skrip, sebuah file HTML akan dihasilkan yang berisi peta dengan marker untuk setiap BTS, jalur rute, dan lokasi pengguna:

- Marker BTS dengan informasi detail dalam pop-up.
- Panah pada rute untuk menunjukkan arah perjalanan.
- Kemampuan untuk melihat lokasi pengguna di peta.

### Kontribusi

Kami sangat terbuka untuk kontribusi! Jika Anda ingin menambahkan fitur baru atau memperbaiki bug, silakan ajukan pull request atau buka issue di repositori ini.

### Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).

---

Terima kasih telah menggunakan **Peta BTS dan Rute**! Nikmati pengelolaan data geospasial yang lebih baik! Jika Anda memiliki pertanyaan atau masukan, jangan ragu untuk menghubungi kami.
