# ============================================================
# IMPORT MODULE
# ============================================================

import os
import sys

# Widget utama PySide6
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QSpinBox,
    QTableWidget, QTableWidgetItem, QDateEdit,
    QMessageBox
)

# Khusus untuk konfigurasi SpinBox (+ -)
from PySide6.QtWidgets import QAbstractSpinBox

# GUI helpers
from PySide6.QtGui import QPixmap, QPalette, QBrush, QIcon, QColor
from PySide6.QtCore import Qt, QDate

# Supabase client
from supabase import create_client


# ============================================================
# HELPER FUNCTION
# ============================================================

def resource_path(relative_path):
    """
    Mengambil path resource (icon, gambar)
    Aman untuk mode development & PyInstaller
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ============================================================
# KONFIGURASI SUPABASE
# ============================================================

SUPABASE_URL = "https://yifnsmtzufupwjqkizoe.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlpZm5zbXR6dWZ1cHdqcWtpem9lIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjYwMDc4ODUsImV4cCI6MjA4MTU4Mzg4NX0.8VSWzHj6YHwxl8BHvVbCFcvdLbAJSw1r8iC2OliuA-Y"

# Inisialisasi client Supabase
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

    def __init__(self):
        super().__init__()

        # ---------------- WINDOW ----------------
        self.setWindowTitle("Puding Kuy")
        self.setWindowIcon(QIcon(resource_path("puding.ico")))
        self.resize(1100, 650)

        # Menyimpan baris tabel yang dipilih
        self.selected_row = None

        # ---------------- BACKGROUND ----------------
        palette = self.palette()
        pixmap = QPixmap(resource_path("wallpaper.jpg"))
        brush = QBrush(pixmap)
        brush.setStyle(Qt.TexturePattern)
        palette.setBrush(QPalette.Window, brush)
        self.setPalette(palette)

        # ---------------- LAYOUT UTAMA ----------------
        main_layout = QHBoxLayout(self)
        form_layout = QFormLayout()

        # ---------------- INPUT FORM ----------------
        self.input_tanggal = QDateEdit()
        self.input_tanggal.setCalendarPopup(True)
        self.input_tanggal.setDate(QDate.currentDate())

        self.input_nama = QLineEdit()

        self.input_variasi = QComboBox()
        self.input_variasi.addItems(VARIASI_HARGA.keys())
        self.input_variasi.currentTextChanged.connect(self.update_harga)

        # ===================== SPINBOX JUMLAH =====================
        self.input_jumlah = QSpinBox()
        self.input_jumlah.setMinimum(1)
        self.input_jumlah.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.input_jumlah.setFocusPolicy(Qt.StrongFocus)
        # ==========================================================

        self.input_harga = QLabel("Rp 0")

        self.input_metode = QComboBox()
        self.input_metode.addItems(["Take Away", "Pesan Antar"])

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

        # Style tombol (soft pink)
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

        # Event tombol
        btn_tambah.clicked.connect(self.tambah_data)
        btn_update.clicked.connect(self.update_data)
        btn_hapus.clicked.connect(self.hapus_data)

        btn_layout.addWidget(btn_tambah)
        btn_layout.addWidget(btn_update)
        btn_layout.addWidget(btn_hapus)

        # Layout kiri
        left_layout = QVBoxLayout()
        left_layout.addLayout(form_layout)
        left_layout.addLayout(btn_layout)

        # ----------------------------------------------------
        # TABEL DATA PEMESANAN
        # ----------------------------------------------------

        self.table = QTableWidget(0, 8)
        self.table.setShowGrid(True)
        self.table.setHorizontalHeaderLabels([
            "Tanggal", "Nama", "Variasi",
            "Metode", "Harga", "Jumlah", "Total", "Status"
        ])

        self.table.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.table.cellClicked.connect(self.pilih_data)

        # Label rekap
        self.label_rekap = QLabel("Total Pendapatan: Rp 0")

        # Layout kanan
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.table)
        right_layout.addWidget(self.label_rekap)

        main_layout.addLayout(left_layout, 3)
        main_layout.addLayout(right_layout, 7)

        # ----------------------------------------------------
        # INISIALISASI DATA & SCROLLBAR
        # ----------------------------------------------------

        self.load_data()
        self.update_harga()

        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.table.setColumnWidth(2, 220)

        # ----------------------------------------------------
        # STYLE GLOBAL APLIKASI 
        # ----------------------------------------------------

        self.setStyleSheet("""
        /* =========================================================
        GLOBAL WIDGET
        ========================================================= */
        QWidget {
            font-family: 'Comic Sans MS';
            font-size: 14px;
            color: #6b2d2d;
        }

        /* =========================================================
        TABEL (QTableWidget)
        ========================================================= */
        QTableWidget {
            background-color: #ffe4c4;
            alternate-background-color: #ffefd5;
            gridline-color: #f4a6b8;
            color: #5a2d0c;
        }

        QTableWidget::item {
            background-color: #ffe4c4;
            color: #5a2d0c;
            border-right: 1px solid #F4A6B8;
            border-bottom: 1px solid #F4A6B8;
            padding: 4px;
        }

        /* =========================================================
        HEADER TABEL (HORIZONTAL & VERTICAL)
        ========================================================= */
        QHeaderView {
            background-color: #ffe4c4;
        }

        QHeaderView::section:horizontal {
            background-color: #FFB6C1;
            color: #6b2d2d;
            font-weight: bold;
            border-right: 1px solid #F4A6B8;
            border-bottom: 1px solid #F4A6B8;
        }

        QHeaderView::section:vertical {
            background-color: #FFB6C1;
            color: #6b2d2d;
            font-weight: bold;
            border-right: 1px solid #F4A6B8;
            border-bottom: 1px solid #F4A6B8;
        }

        /* Hilangkan kotak abu-abu pojok kiri atas tabel */
        QTableCornerButton::section {
            background-color: #FFE4C4;
            border: none;
        }

        /* =========================================================
        BUTTON (QPushButton)
        ========================================================= */
        QPushButton {
            background-color: #FFE4E1;
            color: #6b2d2d;
            border: 2px solid #FF69B4;
            border-radius: 14px;
            padding: 8px 18px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #FFC0CB;
        }

        QPushButton:pressed {
            background-color: #FF69B4;
        }

        /* =========================================================
        INPUT TEXT (QLineEdit)
        ========================================================= */
        QLineEdit {
            background-color: #FFE4E1;
            border: 2px solid #FFB6C1;
            border-radius: 12px;
            padding: 6px;
            color: #6b2d2d;
        }

        /* =========================================================
        DATE EDIT (QDateEdit)
        ========================================================= */
        QDateEdit {
            background-color: #FFE4E1;
            border: 2px solid #FFB6C1;
            border-radius: 12px;
            padding: 6px;
            color: #6b2d2d;
        }

        QDateEdit::drop-down {
            background-color: #FFB6C1;
            border-left: 1px solid #FF69B4;
            border-top-right-radius: 12px;
            border-bottom-right-radius: 12px;
        }

        /* =========================================================
        LABEL
        ========================================================= */
        QLabel {
            background-color: #FFE4E1;
            border: 2px solid #FFB6C1;
            border-radius: 12px;
            padding: 6px;
            color: #6b2d2d;
        }

        /* =========================================================
        COMBOBOX (QComboBox)
        ========================================================= */
        QComboBox {
            background-color: #FFE4E1;
            border: 2px solid #FFB6C1;
            border-radius: 12px;
            padding: 6px;
            padding-right: 20px;
            color: #6b2d2d;
        }

        /* ---------- Popup dropdown ---------- */
        QComboBox QListView {
            background-color: #FFE4C4;
            border: 2px solid #FFB6C1;
            color: #6b2d2d;
            outline: 0;
        }

        QComboBox QListView::item {
            background-color: #FFE4C4;
            color: #6b2d2d;
            padding: 6px;
        }

        QComboBox QListView::item:hover {
            background-color: #FFC0CB;
        }

        QComboBox QListView::item:selected,
        QComboBox QListView::item:!active:selected {
            background-color: #FFB6C1;
            color: #6b2d2d;
        }

        QComboBox QListView::item:selected:pressed {
            background-color: #FF69B4;
            color: white;
        }

        /* =========================================================
        SPINBOX (QSpinBox)
        ========================================================= */
        QSpinBox {
            background-color: #FFE4E1;
            border: 2px solid #FFB6C1;
            border-radius: 12px;
            padding: 6px;
            color: #6b2d2d;
        }

        /* =========================================================
        MESSAGE BOX
        ========================================================= */
        QMessageBox {
            background-color: #FFE4C4;
            color: #6b2d2d;
            font-family: 'Comic Sans MS';
            font-size: 14px;
        }

        QMessageBox QLabel {
            color: #6b2d2d;
        }

        QMessageBox QPushButton {
            background-color: #FFB6C1;
            color: #6b2d2d;
            border: 2px solid #FF69B4;
            border-radius: 12px;
            padding: 6px 14px;
            font-weight: bold;
        }

        QMessageBox QPushButton:hover {
            background-color: #FFC0CB;
        }

        /* =========================================================
        CALENDAR (QCalendarWidget)
        ========================================================= */
        QCalendarWidget QWidget {
            background-color: #FFE4C4;
            color: #6b2d2d;
        }

        QCalendarWidget QToolButton {
            background-color: #FFB6C1;
            color: #6b2d2d;
            border-radius: 10px;
            padding: 6px;
            margin: 4px;
            font-weight: bold;
        }

        QCalendarWidget QToolButton:hover {
            background-color: #FFC0CB;
        }

        QCalendarWidget QToolButton#qt_calendar_prevmonth,
        QCalendarWidget QToolButton#qt_calendar_nextmonth {
            background-color: #FF69B4;
            color: white;
            border-radius: 8px;
        }

        QCalendarWidget QHeaderView::section {
            background-color: #FFB6C1;
            color: #6b2d2d;
            font-weight: bold;
        }

        QCalendarWidget QAbstractItemView {
            background-color: #FFE4C4;
            selection-background-color: #FFB6C1;
            selection-color: #6b2d2d;
            border: 2px solid #FFB6C1;
        }

        QCalendarWidget QAbstractItemView:item:selected {
            background-color: #FF69B4;
            color: white;
            border-radius: 6px;
        }

        /* =========================================================
        SCROLLBAR (VERTICAL & HORIZONTAL)
        ========================================================= */
        QScrollBar:vertical,
        QScrollBar:horizontal {
            background: #FFE4E1;
            width: 14px;
            margin: 2px;
            border-radius: 7px;
        }

        QScrollBar::handle:vertical,
        QScrollBar::handle:horizontal {
            background: #FFB6C1;
            min-height: 30px;
            border-radius: 7px;
        }

        QScrollBar::handle:vertical:hover,
        QScrollBar::handle:horizontal:hover {
            background: #FF69B4;
        }

        QScrollBar::add-line,
        QScrollBar::sub-line,
        QScrollBar::add-page,
        QScrollBar::sub-page {
            background: none;
        }
        """)

    # ========================================================
    # LOGIKA APLIKASI (CRUD & HELPER)
    # ========================================================

    def update_harga(self):
        """Update label harga sesuai variasi"""
        harga = VARIASI_HARGA[self.input_variasi.currentText()]
        self.input_harga.setText(f"Rp {harga:,}")

    def reset_form(self):
        """Reset form input"""
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
        """Ambil data saat baris diklik"""
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
        QMessageBox.information(self, "Informasi", "Data berhasil diperbarui.")

    def hapus_data(self):
        """Hapus data terpilih"""
        if self.selected_row is None:
            return

        reply = QMessageBox.question(
            self,
            "Konfirmasi Hapus",
            "Apakah Anda yakin ingin menghapus data ini?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            supabase.table("pemesanan_puding").delete().eq(
                "tanggal", self.table.item(self.selected_row, 0).text()
            ).eq(
                "nama", self.table.item(self.selected_row, 1).text()
            ).execute()
            self.load_data()
            self.reset_form()

    def load_data(self):
        """Load data Supabase ke tabel"""
        self.table.setRowCount(0)
        total = 0
        data = (
    supabase
    .table("pemesanan_puding")
    .select("*")
    .order("tanggal", desc=True)
    .execute()
    .data or []
)

        for row in reversed(data):
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
# Bagian ini adalah titik awal (start) aplikasi
# Kode di dalam blok ini hanya dijalankan jika file ini
# dieksekusi langsung (bukan di-import sebagai module)

if __name__ == "__main__":
    import ctypes

    # --------------------------------------------------------
    # Set App User Model ID (KHUSUS WINDOWS)
    # --------------------------------------------------------
    # Berguna agar:
    # - Icon aplikasi tampil benar di taskbar
    # - Tidak tergabung dengan aplikasi Python lain
    # - Nama aplikasi dikenali Windows sebagai aplikasi sendiri
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        "PudingKuy.App"
    )

    # --------------------------------------------------------
    # Inisialisasi QApplication
    # --------------------------------------------------------
    # QApplication WAJIB dibuat sebelum widget apa pun
    # sys.argv digunakan untuk membaca argumen dari command line
    app = QApplication(sys.argv)

    # Set icon global aplikasi (berpengaruh ke semua window)
    app.setWindowIcon(QIcon(resource_path("puding.ico")))

    # --------------------------------------------------------
    # Membuat & menampilkan window utama
    # --------------------------------------------------------
    window = AplikasiPuding()
    window.show()

    # Set icon window utama (cadangan jika OS tidak ambil icon global)
    window.setWindowIcon(QIcon(resource_path("puding.ico")))

    # --------------------------------------------------------
    # Menjalankan event loop Qt
    # --------------------------------------------------------
    # app.exec() akan:
    # - Menjaga aplikasi tetap berjalan
    # - Menangani klik, input, repaint UI, dsb
    # sys.exit memastikan aplikasi keluar dengan benar
    sys.exit(app.exec())
