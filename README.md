# Puding Kuy

Puding Kuy adalah aplikasi desktop berbasis Python yang digunakan untuk mencatat dan mengelola data pemesanan puding.  
Aplikasi ini membantu pemilik usaha dalam menyimpan data pesanan, melihat daftar pemesanan, serta menghitung total pendapatan secara otomatis.

## Fitur Aplikasi
- Input data pemesanan puding
- Pemilihan variasi puding dan jumlah pesanan
- Perhitungan harga dan total otomatis
- Menampilkan data pemesanan dalam tabel
- Menampilkan total pendapatan
- Terhubung dengan database Supabase

## Teknologi yang Digunakan
- Python
- PySide6 (Qt for Python)
- Supabase
- PyInstaller

## Cara Menjalankan Aplikasi

Setelah aplikasi Puding Kuy berhasil dibuka, pengguna dapat menjalankan dan menggunakan aplikasi dengan langkah-langkah berikut:

1. Pengguna mengisi data pemesanan pada form yang tersedia, meliputi:
   - Tanggal pemesanan
   - Nama pemesan
   - Variasi puding
   - Jumlah pesanan
   - Metode pengantaran
   - Status pembayaran

2. Harga puding akan tampil secara otomatis sesuai dengan variasi yang dipilih.

3. Setelah data diisi, pengguna dapat menekan tombol **Tambah** untuk menyimpan data pemesanan ke dalam database.

4. Data pemesanan yang telah disimpan akan ditampilkan pada tabel di sebelah kanan aplikasi.

5. Pengguna dapat memilih data pada tabel untuk:
   - Mengubah data dengan menekan tombol **Update**
   - Menghapus data dengan menekan tombol **Hapus**

6. Aplikasi akan menampilkan total pendapatan secara otomatis berdasarkan seluruh data pemesanan yang tersimpan.

Dengan adanya fitur tersebut, aplikasi ini memudahkan pengguna dalam mencatat, mengelola, dan memantau pemesanan puding secara sistematis.

## Tujuan Pembuatan
Saya membuat aplikasi pencatatan pemesanan puding ini dengan tujuan untuk membantu bibi saya dalam mengelola usaha puding yang beliau jalani. Sebelumnya, semua pesanan dicatat secara manual menggunakan buku, sehingga sering terjadi kesulitan saat mencari data pesanan, menghitung jumlah pesanan, maupun mengetahui total pendapatan secara keseluruhan.

Melalui aplikasi ini, saya ingin mempermudah proses pencatatan pemesanan agar menjadi lebih rapi, cepat, dan terstruktur. Setiap pesanan dapat langsung dimasukkan ke dalam aplikasi dengan informasi lengkap seperti tanggal pemesanan, nama pelanggan, variasi puding, jumlah pesanan, metode pemesanan (take away atau pesan antar), serta status pembayaran.
