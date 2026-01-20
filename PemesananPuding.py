# ============================================================
# IMPORT MODULE
# ============================================================

import os                      # Untuk pengelolaan path file
import sys                     # Untuk akses sistem & PyInstaller (_MEIPASS)

# Komponen GUI PySide6
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QSpinBox,
    QTableWidget, QTableWidgetItem, QDateEdit
)

# Komponen grafis & styling
from PySide6.QtGui import QPixmap, QPalette, QBrush, QIcon
from PySide6.QtCore import Qt, QDate

# Client Supabase (database online)
from supabase import create_client


# ============================================================
# HELPER FUNCTION
# ============================================================

def resource_path(relative_path):
    """
    Mengambil path resource yang kompatibel dengan:
    - Mode development (python biasa)
    - Mode PyInstaller one-file
    """
    try:
        base_path = sys._MEIPASS  # Folder temporary PyInstaller
    except Exception:
        base_path = os.path.abspath(".")  # Folder project biasa

    return os.path.join(base_path, relative_path)


# ============================================================
# KONFIGURASI SUPABASE
# ============================================================

# URL project Supabase
SUPABASE_URL = "https://yifnsmtzufupwjqkizoe.supabase.co"

# API key Supabase (anon key)
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlpZm5zbXR6dWZ1cHdqcWtpem9lIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjYwMDc4ODUsImV4cCI6MjA4MTU4Mzg4NX0.8VSWzHj6YHwxl8BHvVbCFcvdLbAJSw1r8iC2OliuA-Y"

# Inisialisasi koneksi Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ============================================================
# DATA VARIASI PUDING & HARGA
# ============================================================

VARIASI_HARGA = {
    "Puding Buah Variasi Besar": 150000,
    "Puding Gula Merah Besar": 100000,
    "Puding Nutella Oreo": 175000,
    "Puding Regal Besar": 130000,
    "Puding Regal Keju Besar": 140000,
    "Puding Buah Besar": 130000,
    "Puding Lapis Buah Besar": 160000,
    "Puding Regal Kecil": 75000,
    "Puding Lapis Besar": 150000,
    "Puding Tiramisu Besar": 130000,
    "Puding Tiramisu Kecil": 75000
}


# ============================================================
# KELAS UTAMA APLIKASI
# ============================================================

class AplikasiPuding(QWidget):
    """
    Kelas utama aplikasi Puding Kuy
    Berfungsi untuk:
    - Menampilkan UI
    - Mengelola input
    - CRUD data ke Supabase
    """

    def __init__(self):
        super().__init__()

        # ----------------------------------------------------
        # SETUP WINDOW UTAMA
        # ----------------------------------------------------

        self.setWindowTitle("Puding Kuy")  # Judul aplikasi
        self.setWindowIcon(QIcon(resource_path("puding.ico")))  # Icon window
        self.resize(1100, 650)  # Ukuran window

        self.selected_row = None  # Menyimpan baris tabel yang dipilih

        # ----------------------------------------------------
        # SETUP BACKGROUND WALLPAPER
        # ----------------------------------------------------

        palette = self.palette()
        pixmap = QPixmap(resource_path("wallpaper.jpg"))  # Load wallpaper
        brush = QBrush(pixmap)
        brush.setStyle(Qt.TexturePattern)
        palette.setBrush(QPalette.Window, brush)
        self.setPalette(palette)

        # ----------------------------------------------------
        # SETUP LAYOUT & FORM INPUT
        # ----------------------------------------------------

        main_layout = QHBoxLayout(self)
        form_layout = QFormLayout()

        # Input tanggal pemesanan
        self.input_tanggal = QDateEdit()
        self.input_tanggal.setCalendarPopup(True)
        self.input_tanggal.setDate(QDate.currentDate())

        # Input nama pelanggan
        self.input_nama = QLineEdit()

        # Dropdown variasi puding
        self.input_variasi = QComboBox()
        self.input_variasi.addItems(VARIASI_HARGA.keys())
        self.input_variasi.currentTextChanged.connect(self.update_harga)

        # Input jumlah pesanan
        self.input_jumlah = QSpinBox()
        self.input_jumlah.setMinimum(1)

        # Label harga
        self.input_harga = QLabel("Rp 0")

        # Metode pengantaran
        self.input_metode = QComboBox()
        self.input_metode.addItems(["Take Away", "Pesan Antar"])

        # Status pembayaran
        self.input_status = QComboBox()
        self.input_status.addItems(["Belum Lunas", "Lunas"])

        # Menambahkan field ke form
        form_layout.addRow("Tanggal", self.input_tanggal)
        form_layout.addRow("Nama", self.input_nama)
        form_layout.addRow("Variasi", self.input_variasi)
        form_layout.addRow("Jumlah", self.input_jumlah)
        form_layout.addRow("Harga", self.input_harga)
        form_layout.addRow("Metode", self.input_metode)
        form_layout.addRow("Status", self.input_status)

        # ----------------------------------------------------
        # BUTTON AKSI
        # ----------------------------------------------------

        btn_layout = QHBoxLayout()
        btn_tambah = QPushButton("Tambah")
        btn_update = QPushButton("Update")
        btn_hapus = QPushButton("Hapus")

        # Styling tombol
        btn_style = """
        QPushButton {
            background-color: #FFB6C1;
            color: #6b2d2d;
            border: 2px solid #FF69B4;
            border-radius: 14px;
            padding: 8px 18px;
            font-weight: bold;
        }
        QPushButton:hover { background-color: #FFC0CB; }
        QPushButton:pressed { background-color: #FF69B4; }
        """

        btn_tambah.setStyleSheet(btn_style)
        btn_update.setStyleSheet(btn_style)
        btn_hapus.setStyleSheet(btn_style)

        # Event handler tombol
        btn_tambah.clicked.connect(self.tambah_data)
        btn_update.clicked.connect(self.update_data)
        btn_hapus.clicked.connect(self.hapus_data)

        btn_layout.addWidget(btn_tambah)
        btn_layout.addWidget(btn_update)
        btn_layout.addWidget(btn_hapus)

        left_layout = QVBoxLayout()
        left_layout.addLayout(form_layout)
        left_layout.addLayout(btn_layout)

        # ----------------------------------------------------
        # TABEL DATA PEMESANAN
        # ----------------------------------------------------

        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels([
            "Tanggal", "Nama", "Variasi",
            "Metode", "Harga", "Jumlah", "Total", "Status"
        ])
        self.table.cellClicked.connect(self.pilih_data)

        # Label rekap pendapatan
        self.label_rekap = QLabel("Total Pendapatan: Rp 0")

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.table)
        right_layout.addWidget(self.label_rekap)

        main_layout.addLayout(left_layout, 3)
        main_layout.addLayout(right_layout, 7)

        # ----------------------------------------------------
        # STYLE GLOBAL APLIKASI
        # ----------------------------------------------------

        self.setStyleSheet("""
        QWidget {
            font-family: 'Comic Sans MS';
            font-size: 14px;
            color: #6b2d2d;
        }
        ...
        """)

        # Load data awal
        self.load_data()
        self.update_harga()

    # ========================================================
    # LOGIKA APLIKASI (CRUD & HELPER)
    # ========================================================

    def update_harga(self):
        """Update label harga sesuai variasi"""
        harga = VARIASI_HARGA[self.input_variasi.currentText()]
        self.input_harga.setText(f"Rp {harga:,}")

    def reset_form(self):
        """Reset input form"""
        self.selected_row = None
        self.input_tanggal.setDate(QDate.currentDate())
        self.input_nama.clear()
        self.input_variasi.setCurrentIndex(0)
        self.input_jumlah.setValue(1)
        self.input_metode.setCurrentIndex(0)
        self.input_status.setCurrentIndex(0)
        self.update_harga()

    def tambah_data(self):
        """Tambah data ke Supabase"""
        supabase.table("pemesanan_puding").insert({
            "tanggal": self.input_tanggal.date().toString("yyyy-MM-dd"),
            "nama": self.input_nama.text(),
            "variasi": self.input_variasi.currentText(),
            "metode_pengantaran": self.input_metode.currentText(),
            "harga": VARIASI_HARGA[self.input_variasi.currentText()],
            "jumlah": self.input_jumlah.value(),
            "status_bayar": self.input_status.currentText()
        }).execute()
        self.load_data()
        self.reset_form()

    def pilih_data(self, row, _):
        """Ambil data saat baris tabel diklik"""
        self.selected_row = row
        self.input_tanggal.setDate(QDate.fromString(self.table.item(row, 0).text(), "yyyy-MM-dd"))
        self.input_nama.setText(self.table.item(row, 1).text())
        self.input_variasi.setCurrentText(self.table.item(row, 2).text())
        self.input_metode.setCurrentText(self.table.item(row, 3).text())
        self.input_jumlah.setValue(int(self.table.item(row, 5).text()))
        self.input_status.setCurrentText(self.table.item(row, 7).text())

    def update_data(self):
        """Update data Supabase"""
        if self.selected_row is None:
            return
        supabase.table("pemesanan_puding").update({
            "tanggal": self.input_tanggal.date().toString("yyyy-MM-dd"),
            "nama": self.input_nama.text(),
            "variasi": self.input_variasi.currentText(),
            "metode_pengantaran": self.input_metode.currentText(),
            "harga": VARIASI_HARGA[self.input_variasi.currentText()],
            "jumlah": self.input_jumlah.value(),
            "status_bayar": self.input_status.currentText()
        }).eq(
            "tanggal", self.table.item(self.selected_row, 0).text()
        ).eq(
            "nama", self.table.item(self.selected_row, 1).text()
        ).execute()
        self.load_data()
        self.reset_form()

    def hapus_data(self):
        """Hapus data Supabase"""
        if self.selected_row is None:
            return
        supabase.table("pemesanan_puding").delete().eq(
            "tanggal", self.table.item(self.selected_row, 0).text()
        ).eq(
            "nama", self.table.item(self.selected_row, 1).text()
        ).execute()
        self.load_data()
        self.reset_form()

    def load_data(self):
        """Load data dari Supabase ke tabel"""
        self.table.setRowCount(0)
        total = 0
        data = supabase.table("pemesanan_puding").select("*").execute().data or []
        for row in data:
            r = self.table.rowCount()
            self.table.insertRow(r)
            t = row["harga"] * row["jumlah"]
            total += t
            self.table.setItem(r, 0, QTableWidgetItem(row["tanggal"]))
            self.table.setItem(r, 1, QTableWidgetItem(row["nama"]))
            self.table.setItem(r, 2, QTableWidgetItem(row["variasi"]))
            self.table.setItem(r, 3, QTableWidgetItem(row["metode_pengantaran"]))
            self.table.setItem(r, 4, QTableWidgetItem(f"Rp {row['harga']:,}"))
            self.table.setItem(r, 5, QTableWidgetItem(str(row["jumlah"])))
            self.table.setItem(r, 6, QTableWidgetItem(f"Rp {t:,}"))
            self.table.setItem(r, 7, QTableWidgetItem(row["status_bayar"]))
        self.label_rekap.setText(f"Total Pendapatan: Rp {total:,}")


# ============================================================
# ENTRY POINT PROGRAM
# ============================================================

if __name__ == "__main__":
    import ctypes

    # Set AppUserModelID agar icon taskbar Windows muncul
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("PudingKuy.App")

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path("puding.ico")))

    window = AplikasiPuding()
    window.show()
    window.setWindowIcon(QIcon(resource_path("puding.ico")))

    sys.exit(app.exec())