import customtkinter as ctk
from tkinter import messagebox
import os
from datetime import datetime
from PIL import Image

# ─────────────────────────────────────────
#  IMPORT DATABASE
# ─────────────────────────────────────────
try:
    from db_config import test_connection
    from db_operations import (
        load_penyakit, load_gejala_per_kategori, load_rules,
        load_pasien, load_riwayat, simpan_pasien,
        simpan_riwayat_db, get_statistik
    )

    ok, _ = test_connection()
    DB_CONNECTED = ok
except Exception as e:
    print(f"[WARNING] Database tidak terhubung: {e}")
    DB_CONNECTED = False

# ─────────────────────────────────────────
#  FALLBACK DATA PENYAKIT (DIRAPIKAN)
# ─────────────────────────────────────────
FALLBACK_PENYAKIT = {
    "P01": {
        "nama": "TBC Paru Terkonfirmasi Bakteriologis (BTA Positif)",
        "solusi": (
            "Pengobatan intensif menggunakan Paket Obat Anti Tuberkulosis (OAT) Kategori 1 "
            "(Isoniazid, Rifampisin, Pirazinamid, Etambutol) selama minimal 6 bulan "
            "(2 bulan fase intensif, 4 bulan fase lanjutan). "
            "Segera lakukan isolasi mandiri di awal pengobatan, gunakan masker, "
            "jaga ventilasi udara rumah tetap baik, dan lakukan pemantauan kepatuhan "
            "minum obat melalui PMO (Pengawas Menelan Obat)."
        ),
    },
    "P02": {
        "nama": "TBC Paru Terkonfirmasi Klinis (BTA Negatif, rontgen mendukung)",
        "solusi": (
            "Meskipun hasil dahak negatif, pengobatan tetap menggunakan OAT Kategori 1 "
            "selama 6 bulan penuh karena gejala klinis dan rontgen dada menunjukkan infeksi aktif. "
            "Pasien disarankan menjaga daya tahan tubuh dengan nutrisi tinggi protein, "
            "kontrol berkala ke fasilitas kesehatan untuk evaluasi dahak/foto toraks ulang, "
            "serta memastikan anggota keluarga rumah diperiksa untuk pelacakan kontak erat."
        ),
    },
    "P03": {
        "nama": "TBC Laten (Terinfeksi tanpa gejala aktif)",
        "solusi": (
            "Kuman dalam kondisi 'tertidur' dan tidak menular, namun memerlukan "
            "Terapi Pencegahan Tuberkulosis (TPT). Solusinya meliputi pemberian obat pencegahan "
            "seperti Isoniazid (INH) selama 6 bulan atau kombinasi Rifampisin-Isoniazid lebih "
            "singkat sesuai resep dokter. Pasien wajib menerapkan pola hidup sehat guna "
            "mencegah kuman berkembang menjadi TBC aktif akibat penurunan imun."
        ),
    },
    "P04": {
        "nama": "TBC Kelenjar (Limfadenitis TB)",
        "solusi": (
            "Pengobatan utama menggunakan OAT Kategori 1, namun durasinya bisa diperpanjang "
            "hingga 9-12 bulan tergantung evaluasi klinis dokter. "
            "Disarankan untuk tidak memijat atau memanipulasi benjolan di leher/ketiak "
            "guna mencegah pecahnya benjolan menjadi luka terbuka (skrofuloderma). "
            "Pada kasus tertentu yang menyumbat saluran napas, tindakan drainase atau "
            "pembedahan minor dapat dipertimbangkan."
        ),
    },
    "P05": {
        "nama": "TBC Meningitis (Menyerang selaput otak)",
        "solusi": (
            "Merupakan kondisi darurat medis yang memerlukan rawat inap segera. "
            "Pengobatan menggunakan regimen OAT yang dimodifikasi dengan penambahan "
            "Kortikosteroid (seperti Deksametason) di awal terapi untuk mengurangi peradangan "
            "hebat pada otak. Durasi pengobatan total berkisar antara 9 hingga 12 bulan "
            "dengan pengawasan ketat dari dokter spesialis saraf."
        ),
    },
    "P06": {
        "nama": "TBC Peritoneal (Menyerang rongga perut/pencernaan)",
        "solusi": (
            "Terapi medis utama menggunakan OAT Kategori 1 dengan durasi 9-12 bulan. "
            "Pasien direkomendasikan mengonsumsi makanan yang mudah dicerna dalam porsi kecil "
            "tapi sering, serta pemantauan tanda-tanda komplikasi seperti penyumbatan usus "
            "atau penumpukan cairan perut (asites). "
            "Jika terjadi penumpukan cairan masif, tindakan parasintesis (penyedotan cairan) "
            "mungkin diperlukan."
        ),
    },
    "P07": {
        "nama": "TBC Urogenital / Ginjal (Menyerang saluran kemih)",
        "solusi": (
            "Pemberian terapi OAT jangka panjang minimal 9 bulan untuk mencegah kerusakan "
            "permanen pada struktur ginjal dan saluran kemih. "
            "Pasien disarankan memperbanyak konsumsi air putih, memantau fungsi ginjal "
            "secara berkala (cek Ureum & Kreatinin), serta waspada terhadap tanda obstruksi "
            "saluran kemih yang memerlukan konsultasi dengan dokter spesialis urologi."
        ),
    },
    "P08": {
        "nama": "TBC Kulit (Skrofuloderma)",
        "solusi": (
            "Pemberian regimen OAT Kategori 1 selama 6-9 bulan. "
            "Solusi lokal melibatkan perawatan luka (wound care) yang steril pada kulit "
            "yang pecah atau berulkus guna mencegah infeksi sekunder bakteri lain. "
            "Pasien harus menjaga higienitas area kulit yang terinfeksi dan menutup "
            "luka terbuka dengan kasa steril."
        ),
    },
    "P09": {
        "nama": "TBC Tulang dan Sendi (Spondilitis TB / Pott's Disease)",
        "solusi": (
            "Terapi OAT jangka panjang dengan durasi total 9 hingga 12 bulan karena "
            "penetrasi obat ke jaringan tulang membutuhkan waktu lebih lama. "
            "Pasien diwajibkan melakukan tirah baring (bed rest) dengan alat bantu imobilisasi "
            "(seperti korset khusus tulang belakang) untuk menjaga kestabilan postur tulang. "
            "Pada kasus deformitas berat atau penekanan saraf pusat, "
            "tindakan operasi ortopedi diperlukan."
        ),
    },
    "P10": {
        "nama": "TBC Laring (Menyerang pita suara/tenggorokan)",
        "solusi": (
            "Pengobatan menggunakan OAT Kategori 1 selama 6 bulan. "
            "Karena TBC Laring bersifat sangat menular melalui droplet udara saat berbicara "
            "atau batuk, isolasi ketat di awal pengobatan sangat krusial. "
            "Pasien disarankan mengistirahatkan pita suara (mengurangi berbicara), "
            "menghindari makanan/minuman yang memicu iritasi tenggorokan, "
            "serta selalu menggunakan masker medis."
        ),
    },
}

# ─────────────────────────────────────────
#  FALLBACK DATA GEJALA (DIRAPIKAN)
# ─────────────────────────────────────────
FALLBACK_KATEGORI_GEJALA = {
    "Gejala Utama": {
        "G01": "Batuk Kronis (>2 minggu)",
        "G02": "Batuk Berdarah (Hemoptisis)",
        "G03": "Batuk Berdahak",
    },
    "Gejala Sistemik / Umum": {
        "G04": "Demam Subfebris (37.5-38.5°C)",
        "G05": "Keringat Malam Berlebih",
        "G06": "Penurunan Berat Badan",
        "G07": "Lemas & Kelelahan",
        "G08": "Kehilangan Nafsu Makan (Anoreksia)",
        "G09": "Menggigil",
    },
    "Gejala Spesifik TB Ekstra Paru": {
        "G10": "Pembengkakan Kelenjar Getah Bening",
        "G11": "Sakit Kepala Hebat dan Kaku Kuduk",
        "G12": "Perut Membuncit dan Nyeri Tekan",
        "G13": "Urine Berwarna Keruh atau Kemerahan",
        "G14": "Kelainan Kulit (Skrofuloderma)",
        "G15": "Nyeri Sendi dan Tulang",
    },
    "Gejala Respiratorius (Pernapasan)": {
        "G16": "Nyeri Dada",
        "G17": "Sesak Napas (Dispnea)",
        "G18": "Suara Napas Tidak Normal",
        "G19": "Suara Serau (Disfonia)",
    },
    "Gejala Lain & Faktor": {
        "G20": "Kontak Erat Penderita TBC",
    },
}

DESKRIPSI_GEJALA = {
    "G01": "Batuk yang berlangsung lebih dari 2 minggu, bisa berdahak atau kering. Gejala utama dan paling umum pada TBC paru aktif.",
    "G02": "Batuk disertai darah (hemoptisis). Tanda serius adanya kerusakan jaringan paru akibat infeksi TB aktif yang tidak tertangani.",
    "G03": "Batuk yang menghasilkan sputum (dahak) kental, sering kali berwarna putih, kuning, atau hijau akibat infeksi saluran napas.",
    "G04": "Demam ringan atau meriang yang hilang timbul, biasanya terjadi pada sore atau malam hari. Khas pada infeksi TBC aktif.",
    "G05": "Mengeluarkan keringat berlebih pada malam hari meskipun tidak melakukan aktivitas fisik atau cuaca tidak panas.",
    "G06": "Berat badan turun secara drastis dalam waktu singkat tanpa menjalani program diet. Akibat metabolisme tubuh terganggu.",
    "G07": "Tubuh terasa sangat lelah, lemah, dan tidak bertenaga sepanjang hari meskipun istirahat cukup.",
    "G08": "Penurunan drastis terhadap keinginan untuk makan, yang memperburuk penurunan berat badan dan daya tahan tubuh.",
    "G09": "Rasa dingin yang tiba-tiba menyerang tubuh, sering kali menyertai gejala demam malam pada TBC aktif.",
    "G10": "Muncul benjolan tidak nyeri di area leher, ketiak, atau selangkangan. Khas pada TB Kelenjar (Limfadenitis TB).",
    "G11": "Gejala penurunan kesadaran atau kaku pada leher belakang jika kuman menyerang selaput otak. Khas pada Meningitis TB.",
    "G12": "Penumpukan cairan di rongga perut (asites) disertai nyeri tekan. Khas pada TB Peritoneal / TB Pencernaan.",
    "G13": "Gangguan berkemih atau nyeri pinggang jika infeksi menyerang sistem saluran kemih. Khas pada TB Ginjal / Urogenital.",
    "G14": "Munculnya benjolan kulit yang kemudian pecah dan membentuk luka/ulkus kronis tidak sembuh. Khas pada TB Kulit (Skrofuloderma).",
    "G15": "Rasa sakit parah pada tulang belakang atau sendi, sering disertai keterbatasan gerak. Khas pada TB Tulang (Pott's Disease).",
    "G16": "Rasa sakit atau sesak di area dada, terutama saat menarik napas dalam-dalam atau saat batuk keras.",
    "G17": "Kesulitan bernapas yang terjadi karena area parut atau kerusakan pada jaringan paru-paru semakin meluas dan mengganggu fungsi paru.",
    "G18": "Bunyi napas tidak normal (mengi/wheezing) saat diperiksa. Menandakan adanya penyempitan atau obstruksi pada saluran napas.",
    "G19": "Perubahan suara menjadi parau atau serak berlangsung lama. Terjadi jika kuman TBC menginfeksi area laring (TB Laring).",
    "G20": "Riwayat tinggal serumah atau kontak erat dengan penderita TBC aktif yang belum atau sedang menjalani pengobatan.",
}

# ─────────────────────────────────────────
#  FALLBACK RULES CF (DIPERBARUI MB/MD)
# ─────────────────────────────────────────
FALLBACK_RULES = [
    # P01 - TBC Paru BTA Positif
    ("P01", "G01", 0.80), ("P01", "G02", 0.90), ("P01", "G03", 0.70),
    ("P01", "G05", 0.60), ("P01", "G06", 0.60), ("P01", "G07", 0.50),
    ("P01", "G08", 0.50), ("P01", "G09", 0.40), ("P01", "G20", 0.50),

    # P02 - TBC Paru BTA Negatif (Klinis)
    ("P02", "G01", 0.80), ("P02", "G04", 0.50), ("P02", "G07", 0.40),
    ("P02", "G16", 0.60), ("P02", "G17", 0.80), ("P02", "G18", 0.70),

    # P03 - TBC Laten
    ("P03", "G20", 0.80),

    # P04 - TBC Kelenjar
    ("P04", "G10", 0.90), ("P04", "G04", 0.40),
    ("P04", "G06", 0.50), ("P04", "G07", 0.30),

    # P05 - TBC Meningitis
    ("P05", "G11", 0.90), ("P05", "G04", 0.50),
    ("P05", "G09", 0.40), ("P05", "G07", 0.40),

    # P06 - TBC Peritoneal
    ("P06", "G12", 0.90), ("P06", "G08", 0.60), ("P06", "G06", 0.60),

    # P07 - TBC Urogenital/Ginjal
    ("P07", "G13", 0.90), ("P07", "G04", 0.40), ("P07", "G07", 0.30),

    # P08 - TBC Kulit
    ("P08", "G14", 0.90), ("P08", "G10", 0.50),

    # P09 - TBC Tulang & Sendi
    ("P09", "G15", 0.90), ("P09", "G07", 0.40), ("P09", "G06", 0.50),

    # P10 - TBC Laring
    ("P10", "G19", 0.90), ("P10", "G01", 0.60),
    ("P10", "G03", 0.50), ("P10", "G04", 0.40),
]


# ─────────────────────────────────────────
#  CRUD DATABASE HELPERS
# ─────────────────────────────────────────
def db_exec(sql, params=()):
    if not DB_CONNECTED:
        return False
    try:
        import mysql.connector
        from db_config import DB_CONFIG
        conn = mysql.connector.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close();
        conn.close()
        return True
    except Exception as e:
        print(f"[DB ERROR] {e}")
        return False


def db_fetch(sql, params=()):
    if not DB_CONNECTED:
        return []
    try:
        import mysql.connector
        from db_config import DB_CONFIG
        conn = mysql.connector.connect(**DB_CONFIG)
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params)
        rows = cur.fetchall()
        cur.close();
        conn.close()
        return rows
    except Exception as e:
        print(f"[DB ERROR] {e}")
        return []


# ─────────────────────────────────────────
#  TABEL DETAIL GEJALA PER RIWAYAT (untuk Cetak Laporan Per Pasien)
#  Menyimpan rincian tiap gejala yang dipilih pada satu sesi diagnosa,
#  lengkap dengan nilai CF_pakar (dari Rules) dan CF_user (input pasien),
#  karena tabel riwayat_diagnosa bawaan hanya menyimpan CF gabungan akhir.
# ─────────────────────────────────────────
def pastikan_tabel_riwayat_detail():
    if not DB_CONNECTED:
        return
    db_exec(
        "CREATE TABLE IF NOT EXISTS riwayat_gejala_detail ("
        "id INT AUTO_INCREMENT PRIMARY KEY, "
        "id_riwayat INT NOT NULL, "
        "kode_gejala VARCHAR(10), "
        "nama_gejala VARCHAR(150), "
        "cf_pakar FLOAT, "
        "cf_user FLOAT, "
        "cf_gejala FLOAT)"
    )


pastikan_tabel_riwayat_detail()


# ─────────────────────────────────────────
#  LOAD DATA
# ─────────────────────────────────────────
def load_data():
    if DB_CONNECTED:
        penyakit = load_penyakit()
        kat_gejala = load_gejala_per_kategori()
        rules = load_rules()
        stat = get_statistik()
    else:
        penyakit = FALLBACK_PENYAKIT
        kat_gejala = FALLBACK_KATEGORI_GEJALA
        rules = FALLBACK_RULES
        stat = {
            "total_penyakit": len(FALLBACK_PENYAKIT),
            "total_gejala": sum(len(v) for v in FALLBACK_KATEGORI_GEJALA.values()),
            "total_rules": len(FALLBACK_RULES),
            "total_pasien": 0,
            "total_riwayat": 0,
        }
    # Poin 2: kategori gejala diurutkan berdasarkan kode gejala terkecil di
    # dalamnya, supaya "Gejala Utama" (berisi G01) selalu tampil paling atas,
    # dan urutan kategori mengikuti urutan kode G01 -> G20 secara alami.
    kat_gejala = dict(sorted(kat_gejala.items(),
                             key=lambda kv: min(kv[1].keys()) if kv[1] else "ZZ"))
    gejala = {k: v for cat in kat_gejala.values() for k, v in cat.items()}
    # Poin 1: rules diurutkan per penyakit lalu per gejala, supaya rule baru
    # yang ditambahkan langsung sejajar dengan rule penyakit yang sama,
    # bukan nyangkut di baris paling bawah.
    rules = sorted(rules, key=lambda r: (r[0], r[1]))
    return penyakit, kat_gejala, gejala, rules, stat


# ─────────────────────────────────────────
#  TEMA
# ─────────────────────────────────────────
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
NAVY = "#1B2A4A";
NAVY2 = "#243659";
GRAY_BG = "#F4F6F9";
GRAY_BD = "#DDE1E9"
BLUE = "#2563EB";
BLUE_LT = "#EFF4FF";
GREEN = "#16A34A";
AMBER = "#D97706"
RED = "#DC2626";
WHITE = "#FFFFFF";
TEXT1 = "#111827";
TEXT2 = "#6B7280"
TEXT3 = "#9CA3AF"

# ─────────────────────────────────────────
#  NAMA HARI & BULAN INDONESIA (tidak bergantung pada locale OS)
# ─────────────────────────────────────────
HARI_ID = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN_ID = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
            "Agustus", "September", "Oktober", "November", "Desember"]


def format_tanggal_id(dt=None):
    """Format tanggal gaya Indonesia untuk kop/tanda tangan laporan.
    Contoh hasil: 'Senin 10-Agustus 2026'.
    """
    if dt is None:
        dt = datetime.now()
    return f"{HARI_ID[dt.weekday()]} {dt.day:02d}-{BULAN_ID[dt.month]} {dt.year}"


# ─────────────────────────────────────────
#  KETENTUAN CF_USER (skala keyakinan pasien saat memilih gejala)
#  Catatan: sesuaikan nilai di sini jika berbeda dengan tabel di BAB penulisan.
# ─────────────────────────────────────────
CF_USER_SCALE = {
    "Rendah": 0.2,
    "Sedang": 0.4,
    "Tinggi": 0.6,
    "Sangat Tinggi": 0.8,
}


# ─────────────────────────────────────────
#  CF ENGINE
# ─────────────────────────────────────────
def hitung_cf(selected_gejala, penyakit, rules, cf_user_map=None):
    hasil = {}
    for p_kode in penyakit:
        cf_total = None
        for (pk, gk, cf_pakar) in rules:
            if pk == p_kode and gk in selected_gejala:
                cf_user = cf_user_map.get(gk, 1.0) if cf_user_map else 1.0
                cf_combine = cf_pakar * cf_user
                if cf_total is None:
                    cf_total = cf_combine
                elif cf_total >= 0 and cf_combine >= 0:
                    cf_total = cf_total + cf_combine * (1 - cf_total)
                elif cf_total < 0 and cf_combine < 0:
                    cf_total = cf_total + cf_combine * (1 + cf_total)
                else:
                    cf_total = (cf_total + cf_combine) / (1 - min(abs(cf_total), abs(cf_combine)))
        if cf_total is not None and cf_total > 0:
            hasil[p_kode] = round(cf_total, 4)
    return dict(sorted(hasil.items(), key=lambda x: x[1], reverse=True))


def interpretasi(cf):
    if cf >= 0.8:
        return "Keyakinan Sangat Tinggi", RED
    elif cf >= 0.6:
        return "Keyakinan Tinggi", AMBER
    elif cf >= 0.4:
        return "Keyakinan Sedang", BLUE
    else:
        return "Keyakinan Rendah", TEXT2


def hitung_cf_manual_steps(items):
    """
    Versi 'perhitungan manual' dari CF engine, dengan CF_user eksplisit
    (CF_gejala = CF_user x CF_pakar), lengkap dengan rincian tiap langkah.
    items: list of (kode_gejala, nama_gejala, cf_pakar, cf_user)
    return: (langkah1, langkah2, cf_akhir)
      langkah1 : list of dict {kode, nama, cf_pakar, cf_user, cf_gejala}
      langkah2 : list of dict {label, baris} - "baris" adalah list 3 baris
                 penjabaran (rumus simbolik, rumus tersubstitusi, hasil akhir)
      cf_akhir : nilai CF akhir (float) atau None jika items kosong
    """
    langkah1 = []
    for (kode, nama, cf_pakar, cf_user) in items:
        cf_gejala = cf_user * cf_pakar
        langkah1.append({"kode": kode, "nama": nama, "cf_pakar": cf_pakar,
                         "cf_user": cf_user, "cf_gejala": cf_gejala})

    langkah2 = []
    cf_total = None
    for i, row in enumerate(langkah1, 1):
        cf_g = row["cf_gejala"]
        if cf_total is None:
            cf_total = cf_g
            continue

        k = i - 1  # nomor CF_kombi yang dihasilkan pada langkah ini
        r, n = cf_total, cf_g
        sim_lama = "CF_1" if k == 1 else f"CF_kombi{k - 1}"
        sim_baru = f"CF_{i}"

        if r >= 0 and n >= 0:
            comp, prod = (1 - r), n * (1 - r)
            baru = r + prod
            baris = [
                f"CF_(kombi{k}) = {sim_lama} + {sim_baru} x (1 - {sim_lama})",
                f"CF_(kombi{k}) = {r:.4f} + {n:.4f} x (1 - {r:.4f})",
                f"CF_(kombi{k}) = {r:.4f} + {n:.4f} x {comp:.4f} = {r:.4f} + {prod:.4f} "
                f"= {baru:.4f} (CF_kombi{k}).",
            ]
        elif r < 0 and n < 0:
            comp, prod = (1 + r), n * (1 + r)
            baru = r + prod
            baris = [
                f"CF_(kombi{k}) = {sim_lama} + {sim_baru} x (1 + {sim_lama})",
                f"CF_(kombi{k}) = {r:.4f} + {n:.4f} x (1 + {r:.4f})",
                f"CF_(kombi{k}) = {r:.4f} + {n:.4f} x {comp:.4f} = {r:.4f} + {prod:.4f} "
                f"= {baru:.4f} (CF_kombi{k}).",
            ]
        else:
            m = min(abs(r), abs(n));
            numer = r + n;
            denom = 1 - m
            baru = numer / denom
            baris = [
                f"CF_(kombi{k}) = ({sim_lama} + {sim_baru}) / (1 - min(|{sim_lama}|,|{sim_baru}|))",
                f"CF_(kombi{k}) = ({r:.4f} + {n:.4f}) / (1 - {m:.4f})",
                f"CF_(kombi{k}) = {numer:.4f} / {denom:.4f} = {baru:.4f} (CF_kombi{k}).",
            ]

        label = ("Kombinasi CF_1 dan CF_2 (CF_kombi1):" if k == 1 else
                 f"Kombinasi CF_kombi{k - 1} dengan CF_{i} (CF_kombi{k}):")
        langkah2.append({"label": label, "baris": baris})
        cf_total = baru

    return langkah1, langkah2, cf_total


# ─────────────────────────────────────────
#  DIALOG HELPER
# ─────────────────────────────────────────
class CRUDDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, fields, values=None, callback=None):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, True)
        self.grab_set();
        self.lift();
        self.focus_force()
        self.configure(fg_color=GRAY_BG)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.callback = callback
        self.entries = {}

        W = 500
        h_body = 16
        for (key, label, wtype, opts) in fields:
            h_body += 22 + 14
            if wtype == "textbox":
                h_body += opts.get("height", 80)
            else:
                h_body += 38
            h_body += 10
        H = max(min(50 + h_body + 58, 700), 300)

        px = parent.winfo_x() + parent.winfo_width() // 2 - W // 2
        py = max(parent.winfo_y() + parent.winfo_height() // 2 - H // 2, 40)
        self.geometry(f"{W}x{H}+{px}+{py}")

        hdr = ctk.CTkFrame(self, fg_color=NAVY, height=50, corner_radius=0)
        hdr.pack(fill="x");
        hdr.pack_propagate(False)
        ctk.CTkLabel(hdr, text=f"  {title}",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="white").pack(side="left", padx=16, pady=12)

        foot = ctk.CTkFrame(self, fg_color=GRAY_BG, height=56, corner_radius=0)
        foot.pack(fill="x", side="bottom");
        foot.pack_propagate(False)
        ctk.CTkFrame(foot, fg_color=GRAY_BD, height=1).pack(fill="x", side="top")
        ctk.CTkButton(foot, text="Batal", width=90, height=34, corner_radius=7,
                      fg_color="transparent", text_color=TEXT2,
                      border_width=1, border_color=GRAY_BD,
                      command=self.destroy).pack(side="right", padx=(6, 18), pady=11)
        ctk.CTkButton(foot, text="✔  Simpan", width=110, height=34, corner_radius=7,
                      fg_color=NAVY, text_color="white", hover_color=NAVY2,
                      font=ctk.CTkFont(size=12, weight="bold"),
                      command=self._submit).pack(side="right", pady=11)

        body_outer = ctk.CTkScrollableFrame(self, fg_color="transparent")
        body_outer.pack(fill="both", expand=True)
        body = ctk.CTkFrame(body_outer, fg_color="transparent")
        body.pack(fill="x", padx=22, pady=(10, 10))

        for i, (key, label, widget_type, opts) in enumerate(fields):
            ctk.CTkLabel(body, text=label,
                         font=ctk.CTkFont(size=11, weight="bold"),
                         text_color=TEXT2).grid(row=i * 2, column=0, sticky="w", pady=(10, 2))
            val = (values or {}).get(key, "")
            if widget_type == "entry":
                e = ctk.CTkEntry(body, width=440, font=ctk.CTkFont(size=12),
                                 height=38, corner_radius=7)
                e.insert(0, str(val))
                e.grid(row=i * 2 + 1, column=0, sticky="ew", pady=(0, 4))
            elif widget_type == "textbox":
                e = ctk.CTkTextbox(body, width=440, height=opts.get("height", 90),
                                   font=ctk.CTkFont(size=12), corner_radius=7)
                e.insert("1.0", str(val))
                e.grid(row=i * 2 + 1, column=0, sticky="ew", pady=(0, 4))
            elif widget_type == "option":
                e = ctk.CTkOptionMenu(body, width=440, values=opts.get("values", []),
                                      font=ctk.CTkFont(size=12), height=38,
                                      fg_color=GRAY_BG, text_color=TEXT1,
                                      button_color=GRAY_BD, button_hover_color=NAVY,
                                      corner_radius=7)
                if val: e.set(str(val))
                e.grid(row=i * 2 + 1, column=0, sticky="ew", pady=(0, 4))
            self.entries[key] = e

        first = list(self.entries.values())
        if first and isinstance(first[0], ctk.CTkEntry):
            self.after(100, first[0].focus)

    def _submit(self):
        data = {}
        for key, widget in self.entries.items():
            if isinstance(widget, ctk.CTkTextbox):
                data[key] = widget.get("1.0", "end").strip()
            else:
                data[key] = widget.get().strip()
        if self.callback:
            self.callback(data)
        self.destroy()


class PerhitunganManualDialog(ctk.CTkToplevel):
    """
    Fitur 'Simulasi Perhitungan Manual CF' untuk Menu Rules CF.
    Menghitung CF_gejala = CF_user x CF_pakar per gejala, lalu mengombinasikannya
    secara bertahap - persis format perhitungan manual pada penulisan BAB 4.
    """

    def __init__(self, parent, penyakit, gejala, rules):
        super().__init__(parent)
        self.parent_app = parent
        self.PENYAKIT = penyakit
        self.GEJALA = gejala
        self.RULES = rules
        self.cf_user_widgets = {}  # kode_gejala -> CTkOptionMenu

        self.title("Simulasi Perhitungan Manual CF")
        self.resizable(False, True)
        self.grab_set();
        self.lift();
        self.focus_force()
        self.configure(fg_color=GRAY_BG)
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        W, H = 640, 660
        px = parent.winfo_x() + parent.winfo_width() // 2 - W // 2
        py = max(parent.winfo_y() + parent.winfo_height() // 2 - H // 2, 30)
        self.geometry(f"{W}x{H}+{px}+{py}")

        hdr = ctk.CTkFrame(self, fg_color=NAVY, height=50, corner_radius=0)
        hdr.pack(fill="x");
        hdr.pack_propagate(False)
        ctk.CTkLabel(hdr, text="  🧮 Simulasi Perhitungan Manual CF",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="white").pack(side="left", padx=16, pady=12)

        legend = ctk.CTkFrame(self, fg_color="#1A2840", corner_radius=0)
        legend.pack(fill="x")
        ctk.CTkLabel(legend, text="Ketentuan CF_User:", font=ctk.CTkFont(size=9, weight="bold"),
                     text_color="#8899BB").pack(side="left", padx=(12, 6), pady=6)
        for label, val in CF_USER_SCALE.items():
            ctk.CTkLabel(legend, text=f" {label}={val} ", font=ctk.CTkFont(size=9),
                         text_color="white").pack(side="left", pady=6)

        body = ctk.CTkScrollableFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=16, pady=(10, 4))
        self.parent_app._fix_scroll(body)

        ctk.CTkLabel(body, text="Pilih Hipotesis Penyakit",
                     font=ctk.CTkFont(size=11, weight="bold"), text_color=TEXT2
                     ).pack(anchor="w", pady=(2, 3))
        opsi_penyakit = [f"{k} - {v['nama']}" for k, v in self.PENYAKIT.items()]
        self.var_penyakit = ctk.StringVar(value=opsi_penyakit[0] if opsi_penyakit else "")
        ctk.CTkOptionMenu(body, values=opsi_penyakit, variable=self.var_penyakit,
                          width=580, height=34, command=lambda _=None: self._muat_gejala(),
                          fg_color=WHITE, text_color=TEXT1, button_color=GRAY_BD,
                          button_hover_color=NAVY, corner_radius=6
                          ).pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(body, text="Bobot Keyakinan Pasien (CF_User) per Gejala",
                     font=ctk.CTkFont(size=11, weight="bold"), text_color=TEXT2
                     ).pack(anchor="w", pady=(2, 3))
        self.gejala_box = ctk.CTkFrame(body, fg_color=WHITE, corner_radius=6)
        self.gejala_box.pack(fill="x", pady=(0, 10))

        ctk.CTkButton(body, text="Hitung", font=ctk.CTkFont(size=12, weight="bold"),
                      height=36, fg_color=NAVY, text_color="white", hover_color=NAVY2,
                      corner_radius=6, command=self._hitung).pack(fill="x", pady=(0, 10))

        self.hasil_box = ctk.CTkFrame(body, fg_color="transparent")
        self.hasil_box.pack(fill="both", expand=True)

        self._muat_gejala()

    def _muat_gejala(self):
        for w in self.gejala_box.winfo_children(): w.destroy()
        for w in self.hasil_box.winfo_children(): w.destroy()
        p_kode = self.var_penyakit.get().split(" - ")[0]
        self.cf_user_widgets = {}
        relevan = [(gk, cf) for (pk, gk, cf) in self.RULES if pk == p_kode]
        if not relevan:
            ctk.CTkLabel(self.gejala_box, text="Tidak ada rule untuk penyakit ini.",
                         font=ctk.CTkFont(size=10), text_color=TEXT2).pack(pady=10)
            return
        for gk, cf_pakar in relevan:
            row = ctk.CTkFrame(self.gejala_box, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=4)
            nama = self.GEJALA.get(gk, gk)
            ctk.CTkLabel(row, text=f"{gk} - {nama}  (CF_pakar={cf_pakar:.2f})",
                         font=ctk.CTkFont(size=10), text_color=TEXT1,
                         anchor="w").pack(side="left", fill="x", expand=True)
            var = ctk.StringVar(value="Sangat Tinggi")
            ctk.CTkOptionMenu(row, values=list(CF_USER_SCALE.keys()), variable=var,
                              width=140, height=28, font=ctk.CTkFont(size=10),
                              fg_color=GRAY_BG, text_color=TEXT1, button_color=GRAY_BD,
                              button_hover_color=NAVY, corner_radius=5
                              ).pack(side="right")
            self.cf_user_widgets[gk] = (var, nama, cf_pakar)

    def _hitung(self):
        for w in self.hasil_box.winfo_children(): w.destroy()
        p_kode = self.var_penyakit.get().split(" - ")[0]
        items = []
        for gk, (var, nama, cf_pakar) in self.cf_user_widgets.items():
            cf_user = CF_USER_SCALE[var.get()]
            items.append((gk, nama, cf_pakar, cf_user))
        if not items:
            return
        langkah1, langkah2, cf_akhir = hitung_cf_manual_steps(items)

        ctk.CTkLabel(self.hasil_box,
                     text=f"Langkah 1: Perhitungan (CF_gejala) = (CF_user) x (CF_pakar) — Hipotesis {p_kode}",
                     font=ctk.CTkFont(size=11, weight="bold"), text_color=TEXT1,
                     anchor="w", wraplength=580, justify="left").pack(anchor="w", pady=(6, 4))
        for i, row in enumerate(langkah1, 1):
            ctk.CTkLabel(self.hasil_box,
                         text=(f"CF_{i} ({row['kode']}) = CF_user({row['kode']}) x CF_pakar({p_kode},{row['kode']}) "
                               f"= {row['cf_user']:.1f} x {row['cf_pakar']:.2f} = {row['cf_gejala']:.4f}"),
                         font=ctk.CTkFont(size=10), text_color=TEXT2,
                         anchor="w", wraplength=580, justify="left").pack(anchor="w", padx=8)

        if langkah2:
            ctk.CTkLabel(self.hasil_box, text="Langkah 2: Kombinasi Nilai CF secara Bertahap",
                         font=ctk.CTkFont(size=11, weight="bold"), text_color=TEXT1,
                         anchor="w").pack(anchor="w", pady=(10, 4))
            for idx, step in enumerate(langkah2):
                huruf = chr(ord('a') + idx)
                ctk.CTkLabel(self.hasil_box, text=f"{huruf})  {step['label']}",
                             font=ctk.CTkFont(size=10, weight="bold"), text_color=TEXT2,
                             anchor="w", wraplength=580, justify="left").pack(anchor="w", padx=8, pady=(6, 1))
                for baris in step["baris"]:
                    ctk.CTkLabel(self.hasil_box, text=baris,
                                 font=ctk.CTkFont(size=10), text_color=TEXT2,
                                 anchor="w", wraplength=580, justify="left").pack(anchor="w", padx=20)

        persen = round(cf_akhir * 100, 2) if cf_akhir is not None else 0
        label, clr = interpretasi(cf_akhir if cf_akhir is not None else 0)
        final = ctk.CTkFrame(self.hasil_box, fg_color=BLUE_LT, corner_radius=6)
        final.pack(fill="x", pady=(12, 4))
        ctk.CTkLabel(final, text=f"Nilai CF Akhir = {persen}%  ({label})",
                     font=ctk.CTkFont(size=12, weight="bold"), text_color=clr
                     ).pack(padx=10, pady=8)


# ─────────────────────────────────────────
#  APLIKASI UTAMA
# ─────────────────────────────────────────
class SistemPakarApp(ctk.CTk):
    def __init__(self, user_info=None):
        super().__init__()
        self.user_info = user_info
        self.logout_flag = False
        self.title("Sistem Pakar Diagnosa TBC - Klinik Pratama EBHC")
        self.geometry("1100x660")
        self.minsize(860, 540)
        self.configure(fg_color=GRAY_BG)

        self.PENYAKIT, self.KAT_GEJALA, self.GEJALA, self.RULES, self.STAT = load_data()
        self.selected_gejala = {}
        self.chip_buttons = {}
        self.chip_rows = {}  # kode_gejala -> row frame (chip + dropdown CF_User)
        self.cfuser_gejala = {}  # kode_gejala -> StringVar (label bobot CF_User)
        self.cfuser_widgets = {}  # kode_gejala -> CTkOptionMenu
        self.pasien_aktif = None
        self.id_pasien_aktif = None
        self._pending_gejala = []

        self._build_sidebar()
        self._build_main()
        self.after(10, lambda: self._show_page("diagnosa"))

    # ════════ SIDEBAR ════════
    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, fg_color=NAVY, width=210, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        lf = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        lf.pack(fill="x", padx=14, pady=(18, 0))
        # Logo klinik di sidebar
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "LOGO_EBHC_noBG.png")
        if os.path.exists(logo_path):
            try:
                logo_img = ctk.CTkImage(light_image=Image.open(logo_path), size=(90, 100))
                ctk.CTkLabel(lf, image=logo_img, text="").pack(anchor="w")
            except:
                icon = ctk.CTkFrame(lf, fg_color=NAVY2, width=100, height=100, corner_radius=9)
                icon.pack(anchor="w");
                icon.pack_propagate(False)
                ctk.CTkLabel(icon, text="✚", font=ctk.CTkFont(size=18),
                             text_color="white").place(relx=.5, rely=.5, anchor="center")
        else:
            icon = ctk.CTkFrame(lf, fg_color=NAVY2, width=38, height=38, corner_radius=9)
            icon.pack(anchor="w");
            icon.pack_propagate(False)
            ctk.CTkLabel(icon, text="✚", font=ctk.CTkFont(size=18),
                         text_color="white").place(relx=.5, rely=.5, anchor="center")
        ctk.CTkLabel(lf, text="Sistem Pakar",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="white").pack(anchor="w", pady=(8, 0))
        ctk.CTkLabel(lf, text="Klinik Pratama EBHC - Diagnosa TBC",
                     font=ctk.CTkFont(size=9), text_color="#8899BB").pack(anchor="w")

        uname = self.user_info.get("username", "?") if self.user_info else "?"
        urole = self.user_info.get("role", "").upper() if self.user_info else ""
        ctk.CTkLabel(lf, text=f"● {uname}  [{urole}]",
                     font=ctk.CTkFont(size=9), text_color=GREEN).pack(anchor="w", pady=(4, 0))
        sc, st = (GREEN, "● DB Terhubung") if DB_CONNECTED else (RED, "● Mode Offline")
        ctk.CTkLabel(lf, text=st, font=ctk.CTkFont(size=9),
                     text_color=sc).pack(anchor="w", pady=(2, 0))

        ctk.CTkFrame(self.sidebar, fg_color="#2D3E60", height=1).pack(fill="x", padx=14, pady=10)

        self.nav_buttons = {}
        self.sidebar_scroll = ctk.CTkScrollableFrame(
            self.sidebar, fg_color="transparent",
            scrollbar_button_color=NAVY2, scrollbar_button_hover_color="#3D5070")
        self.sidebar_scroll.pack(fill="both", expand=True)
        self._fix_scroll(self.sidebar_scroll)

        self._sidebar_label("UTAMA")
        for key, ico, lbl in [("diagnosa", "⊞", "Diagnosa"), ("riwayat", "≡", "Riwayat")]:
            self._nav_btn(key, ico, lbl)
        ctk.CTkFrame(self.sidebar_scroll, fg_color="#2D3E60", height=1).pack(fill="x", padx=14, pady=(8, 6))

        self._sidebar_label("BASIS PENGETAHUAN")
        for key, ico, lbl in [("pasien", "👤", "Data Pasien"), ("rules", "∑", "Rules CF"),
                              ("penyakit", "◉", "Data Penyakit"), ("gejala", "◈", "Data Gejala")]:
            self._nav_btn(key, ico, lbl)
        ctk.CTkFrame(self.sidebar_scroll, fg_color="#2D3E60", height=1).pack(fill="x", padx=14, pady=(8, 6))

        self._sidebar_label("DATA & LAPORAN")
        for key, ico, lbl in [("laporan", "🖨", "Cetak Laporan"), ("tentang", "ℹ", "Tentang")]:
            self._nav_btn(key, ico, lbl)

        ctk.CTkFrame(self.sidebar_scroll, fg_color="#2D3E60", height=1).pack(fill="x", padx=14, pady=(10, 6))
        self.lbl_pasien_aktif = ctk.CTkLabel(
            self.sidebar_scroll, text="Belum ada pasien aktif",
            font=ctk.CTkFont(size=9), text_color="#5570A0", wraplength=175, justify="left")
        self.lbl_pasien_aktif.pack(anchor="w", padx=14, pady=(0, 6))
        self.after(50, self._refresh_status_pasien_aktif)

        ctk.CTkFrame(self.sidebar, fg_color="#2D3E60", height=1).pack(
            side="bottom", fill="x", padx=14, pady=(0, 2))
        ctk.CTkButton(
            self.sidebar, text="  ⏻  Logout", anchor="w",
            font=ctk.CTkFont(size=12), height=34, corner_radius=7,
            fg_color=RED, text_color="white", hover_color="#B91C1C",
            command=self._logout).pack(side="bottom", fill="x", padx=10, pady=(0, 6))
        ctk.CTkLabel(self.sidebar, text="v1.0 - Certainty Factor\nUniv. Indraprasta PGRI",
                     font=ctk.CTkFont(size=9), text_color="#5570A0",
                     justify="left").pack(side="bottom", anchor="w", padx=14, pady=(4, 2))

    def _sidebar_label(self, text):
        ctk.CTkLabel(self.sidebar_scroll, text=text,
                     font=ctk.CTkFont(size=9, weight="bold"),
                     text_color="#5570A0").pack(anchor="w", padx=16, pady=(0, 3))

    def _nav_btn(self, key, ico, label):
        btn = ctk.CTkButton(
            self.sidebar_scroll, text=f"  {ico}  {label}", anchor="w",
            font=ctk.CTkFont(size=12), height=36, corner_radius=7,
            fg_color="transparent", text_color="#8899BB", hover_color=NAVY2,
            command=lambda k=key: self._show_page(k))
        btn.pack(fill="x", padx=8, pady=2)
        self.nav_buttons[key] = btn

    def _set_nav_active(self, key):
        for k, btn in self.nav_buttons.items():
            btn.configure(fg_color=NAVY2 if k == key else "transparent",
                          text_color="white" if k == key else "#8899BB")

    def _refresh_status_pasien_aktif(self):
        # Menampilkan status pasien secara realtime:
        # - Jika sedang ada pasien aktif dalam sesi diagnosa -> tampilkan datanya
        # - Jika tidak, tampilkan jumlah pasien yang benar-benar ada di database saat ini
        if not hasattr(self, "lbl_pasien_aktif"):
            return
        if self.pasien_aktif:
            self.lbl_pasien_aktif.configure(
                text=f"Pasien:\n{self.pasien_aktif['nama']}\n"
                     f"{self.pasien_aktif['usia']} th - {self.pasien_aktif['jk']}")
            return
        total = len(load_pasien()) if DB_CONNECTED else 0
        if total == 0:
            self.lbl_pasien_aktif.configure(text="Belum ada pasien aktif")
        else:
            self.lbl_pasien_aktif.configure(text=f"Ada {total} pasien aktif")

    def _logout(self):
        if messagebox.askyesno("Logout", "Yakin ingin keluar dari sistem?"):
            self.logout_flag = True
            # Batalkan semua pending after() sebelum destroy
            try:
                for after_id in self.tk.call('after', 'info'):
                    try:
                        self.after_cancel(after_id)
                    except:
                        pass
            except:
                pass
            self.destroy()

    # ════════ MAIN ════════
    def _build_main(self):
        self.main_frame = ctk.CTkFrame(self, fg_color=GRAY_BG, corner_radius=0)
        self.main_frame.pack(side="left", fill="both", expand=True)

        self.topbar = ctk.CTkFrame(self.main_frame, fg_color=WHITE, height=56, corner_radius=0)
        self.topbar.pack(fill="x");
        self.topbar.pack_propagate(False)
        self.lbl_title = ctk.CTkLabel(self.topbar, text="Diagnosa",
                                      font=ctk.CTkFont(size=15, weight="bold"), text_color=TEXT1)
        self.lbl_title.pack(side="left", padx=18)
        self.lbl_sub = ctk.CTkLabel(self.topbar, text="",
                                    font=ctk.CTkFont(size=11), text_color=TEXT2)
        self.lbl_sub.pack(side="left", padx=2)
        bc = BLUE_LT if DB_CONNECTED else "#FEF3C7"
        bt = BLUE if DB_CONNECTED else AMBER
        bs = " MySQL OK " if DB_CONNECTED else " Offline "
        ctk.CTkLabel(self.topbar, text=bs, font=ctk.CTkFont(size=10),
                     fg_color=bc, text_color=bt, corner_radius=20).pack(side="right", padx=16)

        self.lbl_clock = ctk.CTkLabel(self.topbar, text="", font=ctk.CTkFont(size=10),
                                      text_color=TEXT2)
        self.lbl_clock.pack(side="right", padx=(0, 4))
        self._update_clock()

        self.content = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=12, pady=10)

        self.pages = {}
        self._build_page_diagnosa()
        self._build_page_form_pasien()
        self._build_page_riwayat()
        self._build_page_rules()
        self._build_page_penyakit()
        self._build_page_gejala()
        self._build_page_pasien()
        self._build_page_tentang()
        self._build_page_laporan()

    def _update_clock(self):
        if not self.winfo_exists():
            return
        now = datetime.now()
        teks = (f"{HARI_ID[now.weekday()]}, {now.day:02d} {BULAN_ID[now.month]} "
                f"{now.year}  {now.strftime('%H:%M:%S')}")
        try:
            self.lbl_clock.configure(text=teks)
        except Exception:
            return
        self.after(1000, self._update_clock)

    def _show_page(self, key):
        self._set_nav_active(key)
        for p in self.pages.values(): p.pack_forget()
        self.pages[key].pack(fill="both", expand=True)
        titles = {
            "diagnosa": ("Diagnosa Penyakit TBC", "Pilih gejala yang dirasakan pasien"),
            "form_pasien": ("Data Pasien", "Isi data pasien sebelum diagnosa"),
            "riwayat": ("Riwayat Diagnosa", "Histori diagnosa dari database"),
            "rules": ("Rules Certainty Factor", "Tabel nilai CF basis pengetahuan TBC"),
            "penyakit": ("Data Penyakit", "Basis pengetahuan penyakit TBC"),
            "gejala": ("Data Gejala", "Daftar gejala dalam basis pengetahuan"),
            "pasien": ("Data Pasien", "Daftar pasien terdaftar"),
            "laporan": ("Cetak Laporan", "Ekspor laporan data sistem pakar TBC"),
            "tentang": ("Tentang Sistem", "Informasi aplikasi dan pengembang"),
        }
        t, s = titles.get(key, ("", ""))
        self.lbl_title.configure(text=t);
        self.lbl_sub.configure(text=s)
        if key == "riwayat": self.after(20, self._refresh_riwayat)
        if key == "pasien":  self.after(20, self._refresh_pasien)
        if key == "laporan": self.after(20, self._refresh_laporan)
        if key == "penyakit": self.after(20, self._refresh_penyakit)
        if key == "gejala":  self.after(20, self._refresh_gejala)
        if key == "rules":   self.after(20, self._refresh_rules)

    # ════════ DIAGNOSA ════════
    def _build_page_diagnosa(self):
        page = ctk.CTkFrame(self.content, fg_color="transparent")
        self.pages["diagnosa"] = page
        sf = ctk.CTkFrame(page, fg_color="transparent")
        sf.pack(fill="x", pady=(0, 10))
        self.lbl_stat_dipilih = None
        for i, (val, lbl) in enumerate([
            (str(self.STAT["total_penyakit"]), "Total Penyakit"),
            (str(self.STAT["total_gejala"]), "Total Gejala"),
            ("0", "Dipilih"),
            (str(self.STAT["total_riwayat"]), "Riwayat"),
        ]):
            card = ctk.CTkFrame(sf, fg_color=WHITE, corner_radius=8)
            card.pack(side="left", fill="x", expand=True, padx=(0 if i == 0 else 6, 0))
            v = ctk.CTkLabel(card, text=val,
                             font=ctk.CTkFont(size=20, weight="bold"), text_color=TEXT1)
            v.pack(anchor="w", padx=12, pady=(8, 0))
            ctk.CTkLabel(card, text=lbl,
                         font=ctk.CTkFont(size=10), text_color=TEXT2).pack(anchor="w", padx=12, pady=(0, 8))
            if lbl == "Dipilih": self.lbl_stat_dipilih = v
        body = ctk.CTkFrame(page, fg_color="transparent")
        body.pack(fill="both", expand=True)
        left = ctk.CTkFrame(body, fg_color=WHITE, corner_radius=8)
        left.pack(side="left", fill="both", expand=True)
        right = ctk.CTkFrame(body, fg_color=WHITE, corner_radius=8)
        right.pack(side="left", fill="both", expand=True, padx=(8, 0))
        self._build_gejala_panel(left)
        self._build_hasil_panel(right)

    def _build_gejala_panel(self, parent):
        ctk.CTkLabel(parent, text="PILIH GEJALA PASIEN",
                     font=ctk.CTkFont(size=9, weight="bold"),
                     text_color=TEXT3).pack(anchor="w", padx=12, pady=(10, 3))
        sf = ctk.CTkFrame(parent, fg_color=GRAY_BG, corner_radius=7)
        sf.pack(fill="x", padx=12, pady=(0, 4))
        ctk.CTkLabel(sf, text="🔍", font=ctk.CTkFont(size=11)).pack(side="left", padx=(6, 2))
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self._filter_chips)
        ctk.CTkEntry(sf, textvariable=self.search_var, placeholder_text="Cari gejala...",
                     border_width=0, fg_color="transparent",
                     font=ctk.CTkFont(size=11)).pack(side="left", fill="x", expand=True, pady=5)
        legend = " · ".join(f"{k}={v}" for k, v in CF_USER_SCALE.items())
        ctk.CTkLabel(parent, text=f"Centang gejala, lalu atur keyakinan pasien (CF_User: {legend})",
                     font=ctk.CTkFont(size=9), text_color=TEXT3,
                     wraplength=380, justify="left").pack(anchor="w", padx=12, pady=(0, 4))
        self.chip_scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        self.chip_scroll.pack(fill="both", expand=True, padx=8, pady=(0, 6))
        self._fix_scroll(self.chip_scroll)
        for kat, gejala_dict in self.KAT_GEJALA.items():
            ctk.CTkLabel(self.chip_scroll, text=kat.upper(),
                         font=ctk.CTkFont(size=8, weight="bold"),
                         text_color=TEXT3).pack(anchor="w", padx=3, pady=(6, 3))
            for kode, nama in gejala_dict.items():
                row = ctk.CTkFrame(self.chip_scroll, fg_color="transparent")
                row.pack(fill="x", pady=1)
                self.chip_rows[kode] = row

                var = ctk.BooleanVar(value=False)
                self.selected_gejala[kode] = var
                btn = ctk.CTkButton(
                    row, text=nama, font=ctk.CTkFont(size=10), height=28,
                    corner_radius=5, anchor="w", fg_color=GRAY_BG, text_color=TEXT2,
                    hover_color="#E8EDF5", border_width=1, border_color=GRAY_BD,
                    command=lambda k=kode: self._toggle_chip(k))
                btn.pack(side="left", fill="x", expand=True)
                self.chip_buttons[kode] = btn

                cfu_var = ctk.StringVar(value="Sangat Tinggi")
                self.cfuser_gejala[kode] = cfu_var
                cfu_menu = ctk.CTkOptionMenu(
                    row, values=list(CF_USER_SCALE.keys()), variable=cfu_var,
                    width=118, height=28, font=ctk.CTkFont(size=9),
                    fg_color=GRAY_BG, text_color=TEXT2, button_color=GRAY_BD,
                    button_hover_color=NAVY, corner_radius=5, state="disabled")
                cfu_menu.pack(side="left", padx=(4, 0))
                self.cfuser_widgets[kode] = cfu_menu
        foot = ctk.CTkFrame(parent, fg_color=GRAY_BG, corner_radius=0)
        foot.pack(fill="x", side="bottom")
        ctk.CTkFrame(foot, fg_color=GRAY_BD, height=1).pack(fill="x")
        inner = ctk.CTkFrame(foot, fg_color="transparent")
        inner.pack(fill="x", padx=12, pady=8)
        self.lbl_count = ctk.CTkLabel(inner, text="0 gejala dipilih",
                                      font=ctk.CTkFont(size=10), text_color=TEXT2)
        self.lbl_count.pack(side="left")
        ctk.CTkButton(inner, text="Reset", font=ctk.CTkFont(size=10), height=28, width=55,
                      fg_color="transparent", text_color=TEXT2, border_width=1, border_color=GRAY_BD,
                      hover_color=GRAY_BG, corner_radius=5,
                      command=self._reset_gejala).pack(side="right", padx=(4, 0))
        ctk.CTkButton(inner, text=" Diagnosa ",
                      font=ctk.CTkFont(size=11, weight="bold"), height=28,
                      fg_color=NAVY, text_color="white", hover_color=NAVY2,
                      corner_radius=5, command=self._jalankan_diagnosa).pack(side="right")

    def _toggle_chip(self, kode):
        aktif = not self.selected_gejala[kode].get()
        self.selected_gejala[kode].set(aktif)
        self._update_chip_style(kode);
        self._update_count()
        if kode in self.cfuser_widgets:
            self.cfuser_widgets[kode].configure(state="normal" if aktif else "disabled")

    def _update_chip_style(self, kode):
        btn = self.chip_buttons[kode]
        if self.selected_gejala[kode].get():
            btn.configure(fg_color=BLUE_LT, text_color=BLUE, border_color=BLUE)
        else:
            btn.configure(fg_color=GRAY_BG, text_color=TEXT2, border_color=GRAY_BD)

    def _update_count(self):
        n = sum(1 for v in self.selected_gejala.values() if v.get())
        self.lbl_count.configure(text=f"{n} gejala dipilih")
        if self.lbl_stat_dipilih: self.lbl_stat_dipilih.configure(text=str(n))

    def _reset_gejala(self):
        for kode in self.selected_gejala:
            self.selected_gejala[kode].set(False);
            self._update_chip_style(kode)
            if kode in self.cfuser_widgets:
                self.cfuser_gejala[kode].set("Sangat Tinggi")
                self.cfuser_widgets[kode].configure(state="disabled")
        self._update_count();
        self._clear_hasil()
        self.pasien_aktif = None;
        self.id_pasien_aktif = None;
        self._pending_gejala = []
        self._refresh_status_pasien_aktif()

    def _filter_chips(self, *args):
        q = self.search_var.get().lower()
        for kode, row in self.chip_rows.items():
            nama = self.GEJALA.get(kode, "").lower()
            row.pack() if q in nama else row.pack_forget()

    def _build_hasil_panel(self, parent):
        ctk.CTkLabel(parent, text="HASIL DIAGNOSA",
                     font=ctk.CTkFont(size=9, weight="bold"),
                     text_color=TEXT3).pack(anchor="w", padx=12, pady=(10, 6))
        self.hasil_scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        self.hasil_scroll.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self._fix_scroll(self.hasil_scroll);
        self._clear_hasil()

    def _clear_hasil(self):
        for w in self.hasil_scroll.winfo_children(): w.destroy()
        ph = ctk.CTkFrame(self.hasil_scroll, fg_color=GRAY_BG, corner_radius=8)
        ph.pack(fill="both", expand=True, pady=30, padx=8)
        ctk.CTkLabel(ph, text="⊙", font=ctk.CTkFont(size=26), text_color=TEXT3).pack(pady=(24, 6))
        ctk.CTkLabel(ph, text="Pilih gejala lalu tekan Diagnosa",
                     font=ctk.CTkFont(size=11), text_color=TEXT3).pack(pady=(0, 24))

    # ════════ FORM PASIEN ════════
    def _build_page_form_pasien(self):
        page = ctk.CTkFrame(self.content, fg_color=WHITE, corner_radius=10)
        self.pages["form_pasien"] = page
        hdr = ctk.CTkFrame(page, fg_color=NAVY, height=50, corner_radius=0)
        hdr.pack(fill="x");
        hdr.pack_propagate(False)
        ctk.CTkLabel(hdr, text="  Data Pasien",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="white").pack(side="left", padx=18, pady=12)
        ctk.CTkLabel(hdr, text="Isi data pasien sebelum diagnosa",
                     font=ctk.CTkFont(size=10), text_color="#8899BB").pack(side="left")
        btn_frame = ctk.CTkFrame(page, fg_color=GRAY_BG, height=58, corner_radius=0)
        btn_frame.pack(fill="x", side="bottom");
        btn_frame.pack_propagate(False)
        ctk.CTkFrame(btn_frame, fg_color=GRAY_BD, height=1).pack(fill="x", side="top")
        ctk.CTkButton(btn_frame, text="Batal", width=90, height=34,
                      fg_color="transparent", text_color=TEXT2,
                      border_width=1, border_color=GRAY_BD,
                      font=ctk.CTkFont(size=11), corner_radius=7,
                      command=self._batal_form_pasien).pack(side="right", padx=(6, 18), pady=12)
        ctk.CTkButton(btn_frame, text="Simpan & Lanjut Diagnosa ->",
                      height=34, fg_color=NAVY, text_color="white", hover_color=NAVY2,
                      font=ctk.CTkFont(size=11, weight="bold"), corner_radius=7,
                      command=self._submit_form_pasien).pack(side="right", pady=12)
        center = ctk.CTkFrame(page, fg_color="transparent")
        center.pack(fill="both", expand=True)
        form = ctk.CTkFrame(center, fg_color="transparent", width=460)
        form.place(relx=0.5, rely=0.5, anchor="center")
        form.columnconfigure(0, weight=1)

        def lbl(text, r):
            ctk.CTkLabel(form, text=text,
                         font=ctk.CTkFont(size=11, weight="bold"),
                         text_color=TEXT2).grid(row=r, column=0, sticky="w", pady=(10, 2))

        lbl("Nama Lengkap *", 0)
        self.fp_nama = ctk.CTkEntry(form, width=460,
                                    placeholder_text="Masukkan nama lengkap pasien",
                                    font=ctk.CTkFont(size=12), height=38, corner_radius=7)
        self.fp_nama.grid(row=1, column=0, sticky="ew")
        lbl("Usia (tahun) *", 2)
        self.fp_usia = ctk.CTkEntry(form, width=460, placeholder_text="Contoh: 25",
                                    font=ctk.CTkFont(size=12), height=38, corner_radius=7)
        self.fp_usia.grid(row=3, column=0, sticky="ew")
        lbl("Jenis Kelamin *", 4)
        self.fp_jk = ctk.CTkOptionMenu(form, width=460, values=["Laki-laki", "Perempuan"],
                                       font=ctk.CTkFont(size=12), height=38,
                                       fg_color=GRAY_BG, text_color=TEXT1,
                                       button_color=GRAY_BD, button_hover_color=NAVY,
                                       corner_radius=7)
        self.fp_jk.grid(row=5, column=0, sticky="ew")
        lbl("No. Telepon", 6)
        self.fp_telp = ctk.CTkEntry(form, width=460, placeholder_text="08xxxxxxxxxx",
                                    font=ctk.CTkFont(size=12), height=38, corner_radius=7)
        self.fp_telp.grid(row=7, column=0, sticky="ew")
        lbl("Alamat Lengkap", 8)
        self.fp_alamat = ctk.CTkEntry(form, width=460,
                                      placeholder_text="Jl. Contoh No.1, Jakarta",
                                      font=ctk.CTkFont(size=12), height=38, corner_radius=7)
        self.fp_alamat.grid(row=9, column=0, sticky="ew")

    def _tampilkan_form_pasien(self, gejala_terpilih):
        self._pending_gejala = gejala_terpilih
        self.fp_nama.delete(0, "end");
        self.fp_usia.delete(0, "end")
        self.fp_telp.delete(0, "end");
        self.fp_alamat.delete(0, "end")
        self.fp_jk.set("Laki-laki")
        self._show_page("form_pasien");
        self.after(80, lambda: self.fp_nama.focus())

    def _batal_form_pasien(self):
        self._pending_gejala = [];
        self._show_page("diagnosa")

    def _submit_form_pasien(self):
        nama = self.fp_nama.get().strip();
        usia_str = self.fp_usia.get().strip()
        if not nama:
            messagebox.showwarning("Peringatan", "Nama pasien wajib diisi!");
            return
        if not usia_str.isdigit():
            messagebox.showwarning("Peringatan", "Usia harus berupa angka!");
            return
        self.pasien_aktif = {
            "nama": nama, "usia": int(usia_str), "jk": self.fp_jk.get(),
            "telp": self.fp_telp.get().strip(), "alamat": self.fp_alamat.get().strip()
        }
        if DB_CONNECTED:
            self.id_pasien_aktif = simpan_pasien(
                self.pasien_aktif["nama"], self.pasien_aktif["usia"],
                self.pasien_aktif["jk"], self.pasien_aktif["telp"],
                self.pasien_aktif["alamat"])
        self._refresh_status_pasien_aktif()
        self._show_page("diagnosa");
        self.after(100, self._proses_diagnosa)

    def _jalankan_diagnosa(self):
        pilih = [k for k, v in self.selected_gejala.items() if v.get()]
        if not pilih:
            messagebox.showwarning("Peringatan", "Pilih minimal 1 gejala terlebih dahulu!");
            return
        if not self.pasien_aktif:
            self._tampilkan_form_pasien(pilih);
            return
        self._proses_diagnosa()

    def _proses_diagnosa(self):
        pilih = self._pending_gejala if self._pending_gejala else \
            [k for k, v in self.selected_gejala.items() if v.get()]
        self._pending_gejala = []
        cf_user_map = {k: CF_USER_SCALE[self.cfuser_gejala[k].get()]
                       for k in pilih if k in self.cfuser_gejala}
        hasil = hitung_cf(pilih, self.PENYAKIT, self.RULES, cf_user_map)

        for w in self.hasil_scroll.winfo_children(): w.destroy()

        # Gejala TBC bervariasi menurut jenisnya (TBC Paru butuh batuk, tapi
        # TBC Extra Paru - kelenjar, tulang, urogenital, meningitis, dll -
        # tidak selalu disertai batuk). Sistem tidak lagi mensyaratkan gejala
        # batuk secara khusus; selama kombinasi gejala cocok dengan rules CF
        # penyakit manapun (hasil tidak kosong), diagnosa tetap ditampilkan.
        # "Tidak ditemukan" hanya muncul jika benar-benar tidak ada rule yang
        # cocok dengan kombinasi gejala yang dipilih.
        if not hasil:
            self._tampilkan_tidak_cocok()
            return

        if DB_CONNECTED and hasil and self.id_pasien_aktif:
            simpan_riwayat_db(self.id_pasien_aktif, pilih, hasil)
            self._simpan_detail_gejala_riwayat(pilih, hasil, cf_user_map)
        if self.pasien_aktif:
            pc = ctk.CTkFrame(self.hasil_scroll, fg_color="#F0FDF4", corner_radius=7,
                              border_width=1, border_color="#BBF7D0")
            pc.pack(fill="x", pady=(0, 8))
            ctk.CTkLabel(pc, text=(
                f"Pasien: {self.pasien_aktif['nama']}  |  "
                f"{self.pasien_aktif['usia']} tahun  |  {self.pasien_aktif['jk']}"),
                         font=ctk.CTkFont(size=10, weight="bold"),
                         text_color=GREEN).pack(anchor="w", padx=10, pady=6)
        for i, (p_kode, cf_val) in enumerate(list(hasil.items())[:5]):
            nama = self.PENYAKIT[p_kode]["nama"]
            solusi = self.PENYAKIT[p_kode]["solusi"]
            persen = round(cf_val * 100, 2)
            lbl_cf, _ = interpretasi(cf_val)
            is_top = (i == 0)
            pct_clr = BLUE if cf_val >= 0.6 else (AMBER if cf_val >= 0.4 else TEXT3)
            card = ctk.CTkFrame(self.hasil_scroll,
                                fg_color=BLUE_LT if is_top else WHITE,
                                corner_radius=8, border_width=1,
                                border_color=BLUE if is_top else GRAY_BD)
            card.pack(fill="x", pady=(0, 6))
            head = ctk.CTkFrame(card, fg_color="transparent")
            head.pack(fill="x", padx=10, pady=(8, 3))
            lh = ctk.CTkFrame(head, fg_color="transparent");
            lh.pack(side="left")
            if is_top:
                ctk.CTkLabel(lh, text=" Diagnosa Utama ",
                             font=ctk.CTkFont(size=9),
                             fg_color=BLUE, text_color="white",
                             corner_radius=8).pack(anchor="w", pady=(0, 2))
            ctk.CTkLabel(lh, text=nama,
                         font=ctk.CTkFont(size=13, weight="bold"),
                         text_color=TEXT1, wraplength=300,
                         justify="left").pack(anchor="w")
            ctk.CTkLabel(lh, text=lbl_cf,
                         font=ctk.CTkFont(size=9),
                         text_color=pct_clr).pack(anchor="w")
            ctk.CTkLabel(head, text=f"{persen}%",
                         font=ctk.CTkFont(size=18, weight="bold"),
                         text_color=pct_clr).pack(side="right")
            bar_bg = ctk.CTkFrame(card,
                                  fg_color="#D6E8FF" if is_top else GRAY_BG,
                                  height=5, corner_radius=2)
            bar_bg.pack(fill="x", padx=10, pady=(0, 3));
            bar_bg.pack_propagate(False)
            ctk.CTkFrame(bar_bg,
                         fg_color=pct_clr if cf_val >= 0.4 else TEXT3,
                         corner_radius=2).place(relwidth=cf_val, relheight=1.0)
            ctk.CTkLabel(card, text=f"Nilai CF: {cf_val:.4f}",
                         font=ctk.CTkFont(size=9),
                         text_color=TEXT3).pack(anchor="w", padx=10, pady=(0, 3))
            if is_top:
                ctk.CTkFrame(card, fg_color=GRAY_BD, height=1).pack(fill="x", padx=10)
                sf2 = ctk.CTkFrame(card, fg_color="transparent")
                sf2.pack(fill="x", padx=10, pady=(4, 8))
                ctk.CTkLabel(sf2, text="Saran:",
                             font=ctk.CTkFont(size=9, weight="bold"),
                             text_color=TEXT2).pack(anchor="w")
                ctk.CTkLabel(sf2, text=solusi,
                             font=ctk.CTkFont(size=10), text_color=TEXT2,
                             wraplength=320, justify="left").pack(anchor="w", pady=(1, 0))
        ctk.CTkLabel(self.hasil_scroll,
                     text=f"Menampilkan {min(len(hasil), 5)} dari {len(hasil)} penyakit",
                     font=ctk.CTkFont(size=9), text_color=TEXT3).pack(pady=3)

    def _simpan_detail_gejala_riwayat(self, pilih, hasil, cf_user_map):
        """Menyimpan rincian tiap gejala (kode, nama, CF_pakar, CF_user, CF_gejala)
        dari diagnosa utama (CF tertinggi) ke tabel riwayat_gejala_detail, supaya
        bisa ditampilkan lagi pada Laporan Cetak Per Pasien di menu Data Pasien.
        """
        try:
            row = db_fetch(
                "SELECT id FROM riwayat_diagnosa WHERE id_pasien=%s "
                "ORDER BY id DESC LIMIT 1", (self.id_pasien_aktif,))
            if not row:
                return
            id_riwayat = row[0]["id"]
            p_kode_utama = next(iter(hasil))
            rule_map = {(pk, gk): cf for (pk, gk, cf) in self.RULES}
            for gk in pilih:
                cf_pakar = rule_map.get((p_kode_utama, gk))
                if cf_pakar is None:
                    continue  # gejala ini tidak punya rule utk diagnosa utama
                cf_user = cf_user_map.get(gk)
                cf_gejala = (cf_pakar * cf_user) if cf_user is not None else None
                db_exec(
                    "INSERT INTO riwayat_gejala_detail "
                    "(id_riwayat, kode_gejala, nama_gejala, cf_pakar, cf_user, cf_gejala) "
                    "VALUES (%s,%s,%s,%s,%s,%s)",
                    (id_riwayat, gk, self.GEJALA.get(gk, gk), cf_pakar, cf_user, cf_gejala))
        except Exception as e:
            print(f"[WARNING] Gagal menyimpan detail gejala riwayat: {e}")

    def _tampilkan_tidak_cocok(self):
        ph = ctk.CTkFrame(self.hasil_scroll, fg_color="#FFF7ED", corner_radius=8,
                          border_width=1, border_color="#FED7AA")
        ph.pack(fill="both", expand=True, pady=8, padx=8)
        ctk.CTkLabel(ph, text="⚠", font=ctk.CTkFont(size=26),
                     text_color=AMBER).pack(pady=(24, 4))
        ctk.CTkLabel(ph, text="Penyakit Tidak Bisa Ditemukan",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=TEXT1).pack(pady=(0, 6))
        pesan = ("Kombinasi gejala yang dipilih tidak cocok dengan pola penyakit "
                 "manapun pada basis pengetahuan sistem (Rules CF).")
        ctk.CTkLabel(ph, text=pesan, font=ctk.CTkFont(size=11), text_color=TEXT2,
                     wraplength=380, justify="center").pack(padx=24, pady=(0, 8))
        ctk.CTkLabel(ph,
                     text="Silakan tinjau kembali gejala yang dipilih, atau konsultasikan "
                          "langsung ke tenaga medis / fasilitas kesehatan terdekat.",
                     font=ctk.CTkFont(size=10), text_color=TEXT3,
                     wraplength=380, justify="center").pack(padx=24, pady=(0, 26))

    # ════════ RIWAYAT ════════
    def _build_page_riwayat(self):
        page = ctk.CTkFrame(self.content, fg_color=WHITE, corner_radius=8)
        self.pages["riwayat"] = page
        tb = ctk.CTkFrame(page, fg_color=GRAY_BG, height=46, corner_radius=0)
        tb.pack(fill="x");
        tb.pack_propagate(False)
        ctk.CTkLabel(tb, text="  Histori Diagnosa Pasien",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=TEXT1).pack(side="left", padx=12, pady=10)
        ctk.CTkButton(tb, text="🗑 Hapus Semua Riwayat", width=170, height=30,
                      font=ctk.CTkFont(size=10), fg_color=RED, text_color="white",
                      hover_color="#B91C1C", corner_radius=6,
                      command=self._hapus_semua_riwayat).pack(side="right", padx=12, pady=8)
        self.riwayat_scroll = ctk.CTkScrollableFrame(page, fg_color="transparent")
        self.riwayat_scroll.pack(fill="both", expand=True, padx=12, pady=8)
        self._fix_scroll(self.riwayat_scroll)

    def _refresh_riwayat(self):
        for w in self.riwayat_scroll.winfo_children(): w.destroy()
        if not DB_CONNECTED:
            ctk.CTkLabel(self.riwayat_scroll,
                         text="Database tidak terhubung.\nRiwayat tidak tersedia.",
                         font=ctk.CTkFont(size=12), text_color=TEXT3).pack(pady=50);
            return
        data = load_riwayat(50)
        if not data:
            ctk.CTkLabel(self.riwayat_scroll, text="Belum ada riwayat diagnosa.",
                         font=ctk.CTkFont(size=12), text_color=TEXT3).pack(pady=50);
            return
        hdr = ctk.CTkFrame(self.riwayat_scroll, fg_color=NAVY, corner_radius=5)
        hdr.pack(fill="x", pady=(0, 4))
        for txt, w in [("Waktu", 130), ("Pasien", 145), ("Diagnosa Utama", 145), ("CF", 52), ("Aksi", 80)]:
            ctk.CTkLabel(hdr, text=txt, font=ctk.CTkFont(size=10, weight="bold"),
                         text_color="white", width=w, anchor="w").pack(side="left", padx=8, pady=7)
        for entry in data:
            row = ctk.CTkFrame(self.riwayat_scroll, fg_color=GRAY_BG, corner_radius=5)
            row.pack(fill="x", pady=(0, 3))
            waktu = str(entry.get("waktu_diagnosa", ""))[:16]
            cf_v = entry.get("cf_tertinggi", 0)
            cf_s = f"{float(cf_v) * 100:.1f}%" if cf_v else "-"
            ctk.CTkLabel(row, text=waktu, width=130, font=ctk.CTkFont(size=10),
                         text_color=TEXT3, anchor="w").pack(side="left", padx=8, pady=7)
            ctk.CTkLabel(row, text=entry.get("nama_pasien", "-"), width=145,
                         font=ctk.CTkFont(size=10, weight="bold"),
                         text_color=TEXT1, anchor="w").pack(side="left", padx=3)
            ctk.CTkLabel(row, text=entry.get("diagnosa_utama", "-"), width=145,
                         font=ctk.CTkFont(size=10), text_color=BLUE,
                         anchor="w").pack(side="left", padx=3)
            ctk.CTkLabel(row, text=cf_s, width=52,
                         font=ctk.CTkFont(size=10, weight="bold"),
                         text_color=GREEN, anchor="w").pack(side="left", padx=3)
            rid = entry.get("id", None)
            ctk.CTkButton(row, text="Hapus", width=70, height=26,
                          font=ctk.CTkFont(size=9), fg_color=RED, text_color="white",
                          hover_color="#B91C1C", corner_radius=5,
                          command=lambda i=rid: self._hapus_riwayat(i)).pack(
                side="left", padx=6, pady=5)

    def _hapus_riwayat(self, rid):
        if rid is None:
            messagebox.showerror("Error", "ID riwayat tidak ditemukan.");
            return
        if messagebox.askyesno("Hapus", "Yakin hapus riwayat diagnosa ini?"):
            ok = db_exec("DELETE FROM riwayat_diagnosa WHERE id=%s", (rid,))
            if ok:
                self._refresh_riwayat()
            else:
                messagebox.showerror("Error", "Gagal hapus. Cek koneksi database.")

    def _hapus_semua_riwayat(self):
        if messagebox.askyesno("Hapus Semua",
                               "Yakin hapus SEMUA riwayat diagnosa?\nTindakan ini tidak bisa dibatalkan!"):
            ok = db_exec("DELETE FROM riwayat_diagnosa")
            if ok:
                self._refresh_riwayat()
            else:
                messagebox.showerror("Error", "Gagal hapus. Cek koneksi database.")

    # ════════ RULES CF ════════
    def _build_page_rules(self):
        page = ctk.CTkFrame(self.content, fg_color=WHITE, corner_radius=8)
        self.pages["rules"] = page
        # Panel rumus
        rumus_frame = ctk.CTkFrame(page, fg_color=NAVY, corner_radius=0)
        rumus_frame.pack(fill="x")
        jr = ctk.CTkFrame(rumus_frame, fg_color="transparent")
        jr.pack(fill="x", padx=16, pady=(10, 4))
        ctk.CTkLabel(jr, text="Rumus CF - Shortliffe & Buchanan (1975)",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color="white").pack(side="left")
        rr = ctk.CTkFrame(rumus_frame, fg_color="transparent")
        rr.pack(fill="x", padx=16, pady=(0, 6))
        for judul, formula, bg, fg in [
            ("CF(H,E)", "CF_pakar x CF_user", BLUE_LT, BLUE),
            ("(+,+)", "CF1+CF2x(1-CF1)", "#F0FDF4", GREEN),
            ("(-,-)", "CF1+CF2x(1+CF1)", "#FFF1F2", RED),
            ("(+,-)", "(CF1+CF2)/(1-min(|CF1|, |CF2|))", "#FFFBEB", AMBER),
        ]:
            box = ctk.CTkFrame(rr, fg_color=bg, corner_radius=6)
            box.pack(side="left", padx=(0, 5), pady=2, ipadx=5, ipady=3)
            ctk.CTkLabel(box, text=judul, font=ctk.CTkFont(size=8, weight="bold"),
                         text_color=fg).pack(anchor="w", padx=5, pady=(2, 0))
            ctk.CTkLabel(box, text=formula, font=ctk.CTkFont(size=9),
                         text_color=TEXT1).pack(anchor="w", padx=5, pady=(0, 2))
        skala = ctk.CTkFrame(rumus_frame, fg_color="#1A2840")
        skala.pack(fill="x", padx=16, pady=(0, 8))
        ctk.CTkLabel(skala, text="Skala:", font=ctk.CTkFont(size=9, weight="bold"),
                     text_color="#8899BB").pack(side="left", padx=8, pady=4)
        for t, c in [("0.8-1.0=Sangat Tinggi", RED), ("0.6-0.79=Tinggi", AMBER),
                     ("0.4-0.59=Sedang", BLUE), ("<0.4=Rendah", TEXT3)]:
            ctk.CTkLabel(skala, text=f" {t}", font=ctk.CTkFont(size=9),
                         text_color=c).pack(side="left", pady=4)
        # Toolbar
        tb = ctk.CTkFrame(page, fg_color=GRAY_BG, height=44, corner_radius=0)
        tb.pack(fill="x");
        tb.pack_propagate(False)
        ctk.CTkButton(tb, text="+ Tambah Rule", width=120, height=30,
                      font=ctk.CTkFont(size=10, weight="bold"), fg_color=GREEN,
                      text_color="white", hover_color="#15803D", corner_radius=6,
                      command=self._tambah_rule).pack(side="left", padx=12, pady=7)
        ctk.CTkButton(tb, text="🧮 Hitung Manual", width=140, height=30,
                      font=ctk.CTkFont(size=10, weight="bold"), fg_color=BLUE,
                      text_color="white", hover_color="#1D4ED8", corner_radius=6,
                      command=self._buka_perhitungan_manual).pack(side="left", padx=(0, 12), pady=7)
        self.lbl_total_rules = ctk.CTkLabel(tb, text="",
                                            font=ctk.CTkFont(size=10), text_color=TEXT2)
        self.lbl_total_rules.pack(side="right", padx=14)
        # Tabel — pakai CTkScrollableFrame + fix_scroll agar mouse scroll bekerja
        self.rules_scroll = ctk.CTkScrollableFrame(page, fg_color="transparent")
        self.rules_scroll.pack(fill="both", expand=True, padx=10, pady=6)
        self._fix_scroll(self.rules_scroll)

    def _refresh_rules(self):
        for w in self.rules_scroll.winfo_children(): w.destroy()
        self.lbl_total_rules.configure(text=f"Total: {len(self.RULES)} rules")

        hdr = ctk.CTkFrame(self.rules_scroll, fg_color=NAVY2, corner_radius=5)
        hdr.pack(fill="x", pady=(0, 4))
        for txt, w in [("No", 32), ("P", 52), ("Nama Penyakit", 172), ("G", 52),
                       ("Nama Gejala", 162), ("CF", 60), ("Interp.", 100), ("Aksi", 80)]:
            ctk.CTkLabel(hdr, text=txt, font=ctk.CTkFont(size=10, weight="bold"),
                         text_color="white", width=w, anchor="w").pack(side="left", padx=5, pady=7)

        self._rules_loading_lbl = ctk.CTkLabel(
            self.rules_scroll, text="⏳  Memuat data rules...",
            font=ctk.CTkFont(size=11), text_color=TEXT2)
        self._rules_loading_lbl.pack(pady=20)

        warna_map = {
            "P01": "#FFF7ED", "P02": "#F0FDF4", "P03": "#EFF4FF", "P04": "#F0FDF4", "P05": "#FFF1F2",
            "P06": "#F0FDFA", "P07": "#FFF7ED", "P08": "#FFF1F2", "P09": "#F5F3FF", "P10": "#FEFCE8",
        }
        rules_data = []
        for i, rule in enumerate(self.RULES, 1):
            pk, gk, cf = rule[0], rule[1], rule[2]
            nama_p = self.PENYAKIT.get(pk, {}).get("nama", pk)
            nama_g = self.GEJALA.get(gk, gk)
            persen = round(cf * 100)
            bg = warna_map.get(pk, GRAY_BG)
            if cf >= 0.8:
                interp, clr = "Sangat Tinggi", RED
            elif cf >= 0.6:
                interp, clr = "Tinggi", AMBER
            elif cf >= 0.4:
                interp, clr = "Sedang", BLUE
            else:
                interp, clr = "Rendah", TEXT3
            rules_data.append((i, pk, gk, cf, nama_p, nama_g, persen, bg, interp, clr))

        self.after(30, lambda: self._render_rules_batch(rules_data, 0, 15))

    def _render_rules_batch(self, rules_data, start, batch_size):
        if start == 0 and hasattr(self, "_rules_loading_lbl"):
            try:
                self._rules_loading_lbl.destroy()
            except:
                pass
        end = min(start + batch_size, len(rules_data))
        chunk = rules_data[start:end]
        for (i, pk, gk, cf, nama_p, nama_g, persen, bg, interp, clr) in chunk:
            row = ctk.CTkFrame(self.rules_scroll, fg_color=bg,
                               corner_radius=5, border_width=1, border_color=GRAY_BD)
            row.pack(fill="x", pady=(0, 2))
            ctk.CTkLabel(row, text=str(i), width=32,
                         font=ctk.CTkFont(size=9), text_color=TEXT3,
                         anchor="w").pack(side="left", padx=5, pady=5)
            ctk.CTkLabel(row, text=pk, width=52,
                         font=ctk.CTkFont(size=10, weight="bold"), text_color=NAVY,
                         anchor="w").pack(side="left", padx=2)
            ctk.CTkLabel(row, text=nama_p, width=172,
                         font=ctk.CTkFont(size=10), text_color=TEXT1,
                         anchor="w").pack(side="left", padx=2)
            ctk.CTkLabel(row, text=gk, width=52,
                         font=ctk.CTkFont(size=10, weight="bold"), text_color=BLUE,
                         anchor="w").pack(side="left", padx=2)
            ctk.CTkLabel(row, text=nama_g, width=162,
                         font=ctk.CTkFont(size=10), text_color=TEXT1,
                         anchor="w").pack(side="left", padx=2)
            ctk.CTkLabel(row, text=f"{cf:.2f}({persen}%)", width=60,
                         font=ctk.CTkFont(size=10, weight="bold"), text_color=clr,
                         anchor="w").pack(side="left", padx=2)
            badge = ctk.CTkFrame(row, fg_color=clr, corner_radius=5, height=20, width=92)
            badge.pack(side="left", padx=3, pady=4);
            badge.pack_propagate(False)
            ctk.CTkLabel(badge, text=interp, font=ctk.CTkFont(size=9),
                         text_color="white").place(relx=.5, rely=.5, anchor="center")
            ctk.CTkButton(row, text="Hapus", width=68, height=24,
                          font=ctk.CTkFont(size=9), fg_color=RED, text_color="white",
                          hover_color="#B91C1C", corner_radius=4,
                          command=lambda p=pk, g=gk: self._hapus_rule(p, g)).pack(
                side="left", padx=4, pady=4)
            # Bind scroll mouse ke setiap baris yang baru dibuat
            self._fix_scroll_row(row)
        if end < len(rules_data):
            self.after(20, lambda: self._render_rules_batch(rules_data, end, batch_size))

    def _fix_scroll_row(self, widget):
        """Bind scroll mouse ke setiap baris rules agar rules_scroll bisa di-scroll via mouse."""
        sf = self.rules_scroll

        def up(e):
            try:
                sf._parent_canvas.yview_scroll(-1, "units")
            except:
                pass

        def dn(e):
            try:
                sf._parent_canvas.yview_scroll(1, "units")
            except:
                pass

        def rec(w):
            w.bind("<Button-4>", up, add="+")
            w.bind("<Button-5>", dn, add="+")
            for c in w.winfo_children():
                rec(c)

        # Bind ke widget baris dan semua child-nya
        rec(widget)
        # Pastikan canvas juga ter-bind
        try:
            sf._parent_canvas.bind("<Button-4>", up, add="+")
            sf._parent_canvas.bind("<Button-5>", dn, add="+")
        except:
            pass

    def _buka_perhitungan_manual(self):
        if not self.PENYAKIT or not self.RULES:
            messagebox.showinfo("Info", "Belum ada data penyakit/rules untuk disimulasikan.")
            return
        PerhitunganManualDialog(self, self.PENYAKIT, self.GEJALA, self.RULES)

    def _tambah_rule(self):
        p_list = list(self.PENYAKIT.keys())
        g_list = list(self.GEJALA.keys())
        fields = [
            ("kode_penyakit", "Kode Penyakit", "option", {"values": p_list}),
            ("kode_gejala", "Kode Gejala", "option", {"values": g_list}),
            ("cf_pakar", "Nilai CF (0.1 - 1.0)", "entry", {}),
        ]

        def cb(data):
            try:
                cf = float(data["cf_pakar"])
                if not (0 < cf <= 1): raise ValueError
            except:
                messagebox.showerror("Error", "Nilai CF harus angka antara 0.1 - 1.0");
                return
            ok = db_exec(
                "INSERT INTO rules (kode_penyakit, kode_gejala, cf_pakar) VALUES (%s,%s,%s)",
                (data["kode_penyakit"], data["kode_gejala"], cf))
            if ok:
                self.RULES.append((data["kode_penyakit"], data["kode_gejala"], cf))
                self.RULES.sort(key=lambda r: (r[0], r[1]))
                self._refresh_rules()
                messagebox.showinfo("Sukses", "Rule CF berhasil ditambahkan!")
            else:
                messagebox.showerror("Error", "Gagal simpan. Cek koneksi database atau data duplikat.")

        CRUDDialog(self, "Tambah Rule CF", fields, callback=cb)

    def _hapus_rule(self, pk, gk):
        if messagebox.askyesno("Hapus Rule", f"Hapus rule {pk} -> {gk}?"):
            ok = db_exec(
                "DELETE FROM rules WHERE kode_penyakit=%s AND kode_gejala=%s", (pk, gk))
            if ok:
                self.RULES = [r for r in self.RULES if not (r[0] == pk and r[1] == gk)]
                self._refresh_rules()
            else:
                messagebox.showerror("Error", "Gagal hapus. Cek koneksi database.")

    # ════════ DATA PENYAKIT ════════
    def _build_page_penyakit(self):
        page = ctk.CTkFrame(self.content, fg_color=WHITE, corner_radius=8)
        self.pages["penyakit"] = page
        tb = ctk.CTkFrame(page, fg_color=GRAY_BG, height=46, corner_radius=0)
        tb.pack(fill="x");
        tb.pack_propagate(False)
        ctk.CTkLabel(tb, text="  Daftar Penyakit TBC",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=TEXT1).pack(side="left", padx=12, pady=10)
        ctk.CTkButton(tb, text="+ Tambah Penyakit", width=140, height=30,
                      font=ctk.CTkFont(size=10, weight="bold"), fg_color=GREEN,
                      text_color="white", hover_color="#15803D", corner_radius=6,
                      command=self._tambah_penyakit).pack(side="right", padx=12, pady=8)
        self.penyakit_scroll = ctk.CTkScrollableFrame(page, fg_color="transparent")
        self.penyakit_scroll.pack(fill="both", expand=True, padx=12, pady=8)
        self._fix_scroll(self.penyakit_scroll)

    def _refresh_penyakit(self):
        for w in self.penyakit_scroll.winfo_children(): w.destroy()
        hdr = ctk.CTkFrame(self.penyakit_scroll, fg_color=NAVY, corner_radius=5)
        hdr.pack(fill="x", pady=(0, 4))
        for txt, w in [("Kode", 55), ("Nama Penyakit", 200), ("Solusi / Penanganan", 380), ("Aksi", 110)]:
            ctk.CTkLabel(hdr, text=txt, font=ctk.CTkFont(size=10, weight="bold"),
                         text_color="white", width=w, anchor="w").pack(side="left", padx=8, pady=7)
        for kode, info in self.PENYAKIT.items():
            row = ctk.CTkFrame(self.penyakit_scroll, fg_color=GRAY_BG, corner_radius=5)
            row.pack(fill="x", pady=(0, 4))
            # Kode
            ctk.CTkLabel(row, text=kode, width=55,
                         font=ctk.CTkFont(size=10), text_color=BLUE,
                         anchor="w").pack(side="left", padx=8, pady=8)
            # Nama Penyakit — wraplength agar tidak terpotong
            ctk.CTkLabel(row, text=info["nama"], width=200,
                         font=ctk.CTkFont(size=11, weight="bold"), text_color=TEXT1,
                         anchor="w", wraplength=195,
                         justify="left").pack(side="left", padx=3, pady=6)
            # Solusi — wraplength lebih besar, teks panjang tampil rapi
            ctk.CTkLabel(row, text=info["solusi"],
                         font=ctk.CTkFont(size=10), text_color=TEXT2,
                         anchor="nw", wraplength=375,
                         justify="left").pack(side="left", padx=3, pady=6, fill="y")
            # Tombol Aksi
            btn_frame = ctk.CTkFrame(row, fg_color="transparent")
            btn_frame.pack(side="right", padx=6, pady=6)
            ctk.CTkButton(btn_frame, text="Edit", width=46, height=26,
                          font=ctk.CTkFont(size=9), fg_color=AMBER, text_color="white",
                          hover_color="#B45309", corner_radius=4,
                          command=lambda k=kode, i=info: self._edit_penyakit(k, i)).pack(
                side="left", padx=(0, 3))
            ctk.CTkButton(btn_frame, text="Hapus", width=52, height=26,
                          font=ctk.CTkFont(size=9), fg_color=RED, text_color="white",
                          hover_color="#B91C1C", corner_radius=4,
                          command=lambda k=kode: self._hapus_penyakit(k)).pack(side="left")

    def _tambah_penyakit(self):
        fields = [
            ("kode", "Kode Penyakit (contoh: P11)", "entry", {}),
            ("nama", "Nama Penyakit", "entry", {}),
            ("deskripsi", "Deskripsi", "entry", {}),
            ("solusi", "Solusi / Penanganan", "textbox", {"height": 100}),
        ]

        def cb(data):
            if not data["kode"] or not data["nama"]:
                messagebox.showerror("Error", "Kode dan Nama wajib diisi!");
                return
            ok = db_exec(
                "INSERT INTO penyakit (kode,nama,deskripsi,solusi) VALUES (%s,%s,%s,%s)",
                (data["kode"], data["nama"], data["deskripsi"], data["solusi"]))
            if ok:
                self.PENYAKIT[data["kode"]] = {"nama": data["nama"], "solusi": data["solusi"]}
                self._refresh_penyakit()
                messagebox.showinfo("Sukses", "Penyakit berhasil ditambahkan!")
            else:
                messagebox.showerror("Error", "Gagal simpan. Kode mungkin sudah ada.")

        CRUDDialog(self, "Tambah Data Penyakit", fields, callback=cb)

    def _edit_penyakit(self, kode, info):
        fields = [
            ("nama", "Nama Penyakit", "entry", {}),
            ("solusi", "Solusi / Penanganan", "textbox", {"height": 100}),
        ]
        vals = {"nama": info["nama"], "solusi": info["solusi"]}

        def cb(data):
            if not data["nama"]:
                messagebox.showerror("Error", "Nama wajib diisi!");
                return
            ok = db_exec(
                "UPDATE penyakit SET nama=%s, solusi=%s WHERE kode=%s",
                (data["nama"], data["solusi"], kode))
            if ok:
                self.PENYAKIT[kode]["nama"] = data["nama"]
                self.PENYAKIT[kode]["solusi"] = data["solusi"]
                self._refresh_penyakit()
                messagebox.showinfo("Sukses", "Data penyakit berhasil diperbarui!")
            else:
                messagebox.showerror("Error", "Gagal update. Cek koneksi database.")

        CRUDDialog(self, f"Edit Penyakit [{kode}]", fields, values=vals, callback=cb)

    def _hapus_penyakit(self, kode):
        if messagebox.askyesno("Hapus",
                               f"Hapus penyakit {kode}?\nRules terkait juga akan terhapus!"):
            db_exec("DELETE FROM rules WHERE kode_penyakit=%s", (kode,))
            ok = db_exec("DELETE FROM penyakit WHERE kode=%s", (kode,))
            if ok:
                self.PENYAKIT.pop(kode, None)
                self.RULES = [r for r in self.RULES if r[0] != kode]
                self._refresh_penyakit()
            else:
                messagebox.showerror("Error", "Gagal hapus. Cek koneksi database.")

    # ════════ DATA GEJALA ════════
    def _build_page_gejala(self):
        page = ctk.CTkFrame(self.content, fg_color=WHITE, corner_radius=8)
        self.pages["gejala"] = page
        tb = ctk.CTkFrame(page, fg_color=GRAY_BG, height=46, corner_radius=0)
        tb.pack(fill="x");
        tb.pack_propagate(False)
        ctk.CTkLabel(tb, text="  Daftar Gejala TBC",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=TEXT1).pack(side="left", padx=12, pady=10)
        ctk.CTkButton(tb, text="+ Tambah Gejala", width=135, height=30,
                      font=ctk.CTkFont(size=10, weight="bold"), fg_color=GREEN,
                      text_color="white", hover_color="#15803D", corner_radius=6,
                      command=self._tambah_gejala).pack(side="right", padx=12, pady=8)
        self.gejala_scroll = ctk.CTkScrollableFrame(page, fg_color="transparent")
        self.gejala_scroll.pack(fill="both", expand=True, padx=12, pady=8)
        self._fix_scroll(self.gejala_scroll)

    def _refresh_gejala(self):
        for w in self.gejala_scroll.winfo_children(): w.destroy()
        hdr = ctk.CTkFrame(self.gejala_scroll, fg_color=NAVY, corner_radius=5)
        hdr.pack(fill="x", pady=(0, 5))
        for txt, w in [("Kode", 55), ("Kategori", 158), ("Nama Gejala", 175), ("Deskripsi", 290), ("Aksi", 110)]:
            ctk.CTkLabel(hdr, text=txt, font=ctk.CTkFont(size=10, weight="bold"),
                         text_color="white", width=w, anchor="w").pack(side="left", padx=7, pady=7)

        kat_warna = {
            "Gejala Utama": ("#EFF4FF", BLUE),
            "Gejala Sistemik / Umum": ("#FEF3C7", AMBER),
            "Gejala Spesifik TB Ekstra Paru": ("#F0FDF4", GREEN),
            "Gejala Respiratorius (Pernapasan)": ("#FFF1F2", RED),
            "Gejala Lain & Faktor": ("#F5F3FF", "#7C3AED"),
        }
        for kat, gejala_dict in self.KAT_GEJALA.items():
            bg, fg_color = kat_warna.get(kat, (GRAY_BG, TEXT2))
            for kode, nama in gejala_dict.items():
                row = ctk.CTkFrame(self.gejala_scroll, fg_color=WHITE,
                                   corner_radius=5, border_width=1, border_color=GRAY_BD)
                row.pack(fill="x", pady=(0, 3))
                ctk.CTkLabel(row, text=kode, width=55,
                             font=ctk.CTkFont(size=10, weight="bold"), text_color=BLUE,
                             anchor="w").pack(side="left", padx=7, pady=7)
                ctk.CTkLabel(row, text=kat, width=158,
                             font=ctk.CTkFont(size=9), fg_color=bg, text_color=fg_color,
                             corner_radius=5, anchor="w",
                             wraplength=150).pack(side="left", padx=3, pady=7, ipady=2)
                ctk.CTkLabel(row, text=nama, width=175,
                             font=ctk.CTkFont(size=11, weight="bold"), text_color=TEXT1,
                             anchor="w", wraplength=170,
                             justify="left").pack(side="left", padx=3, pady=5)
                ctk.CTkLabel(row, text=DESKRIPSI_GEJALA.get(kode, "-"),
                             font=ctk.CTkFont(size=9), text_color=TEXT2,
                             anchor="nw", wraplength=282,
                             justify="left").pack(side="left", padx=3, pady=6, fill="y")
                bf = ctk.CTkFrame(row, fg_color="transparent")
                bf.pack(side="right", padx=5, pady=5)
                ctk.CTkButton(bf, text="Edit", width=46, height=26,
                              font=ctk.CTkFont(size=9), fg_color=AMBER, text_color="white",
                              hover_color="#B45309", corner_radius=4,
                              command=lambda k=kode, n=nama, kt=kat: self._edit_gejala(k, n, kt)).pack(
                    side="left", padx=(0, 3))
                ctk.CTkButton(bf, text="Hapus", width=52, height=26,
                              font=ctk.CTkFont(size=9), fg_color=RED, text_color="white",
                              hover_color="#B91C1C", corner_radius=4,
                              command=lambda k=kode: self._hapus_gejala(k)).pack(side="left")

    def _tambah_gejala(self):
        kat_list = list(self.KAT_GEJALA.keys())
        fields = [
            ("kode", "Kode Gejala (contoh: G21)", "entry", {}),
            ("nama", "Nama Gejala", "entry", {}),
            ("kategori", "Kategori", "option", {"values": kat_list}),
        ]

        def cb(data):
            if not data["kode"] or not data["nama"]:
                messagebox.showerror("Error", "Kode dan Nama wajib diisi!");
                return
            ok = db_exec(
                "INSERT INTO gejala (kode,nama,kategori) VALUES (%s,%s,%s)",
                (data["kode"], data["nama"], data["kategori"]))
            if ok:
                self.GEJALA[data["kode"]] = data["nama"]
                if data["kategori"] in self.KAT_GEJALA:
                    self.KAT_GEJALA[data["kategori"]][data["kode"]] = data["nama"]
                self._refresh_gejala()
                messagebox.showinfo("Sukses", "Gejala berhasil ditambahkan!")
            else:
                messagebox.showerror("Error", "Gagal simpan. Kode mungkin sudah ada.")

        CRUDDialog(self, "Tambah Data Gejala", fields, callback=cb)

    def _edit_gejala(self, kode, nama, kat):
        kat_list = list(self.KAT_GEJALA.keys())
        fields = [
            ("nama", "Nama Gejala", "entry", {}),
            ("kategori", "Kategori", "option", {"values": kat_list}),
        ]
        vals = {"nama": nama, "kategori": kat}

        def cb(data):
            if not data["nama"]:
                messagebox.showerror("Error", "Nama wajib diisi!");
                return
            ok = db_exec(
                "UPDATE gejala SET nama=%s, kategori=%s WHERE kode=%s",
                (data["nama"], data["kategori"], kode))
            if ok:
                self.GEJALA[kode] = data["nama"]
                self._refresh_gejala()
                messagebox.showinfo("Sukses", "Data gejala berhasil diperbarui!")
            else:
                messagebox.showerror("Error", "Gagal update. Cek koneksi database.")

        CRUDDialog(self, f"Edit Gejala [{kode}]", fields, values=vals, callback=cb)

    def _hapus_gejala(self, kode):
        if messagebox.askyesno("Hapus",
                               f"Hapus gejala {kode}?\nRules terkait juga akan terhapus!"):
            db_exec("DELETE FROM rules WHERE kode_gejala=%s", (kode,))
            ok = db_exec("DELETE FROM gejala WHERE kode=%s", (kode,))
            if ok:
                self.GEJALA.pop(kode, None)
                for kt in self.KAT_GEJALA.values(): kt.pop(kode, None)
                self.RULES = [r for r in self.RULES if r[1] != kode]
                self._refresh_gejala()
            else:
                messagebox.showerror("Error", "Gagal hapus. Cek koneksi database.")

    # ════════ DATA PASIEN ════════
    def _build_page_pasien(self):
        page = ctk.CTkFrame(self.content, fg_color=WHITE, corner_radius=8)
        self.pages["pasien"] = page
        tb = ctk.CTkFrame(page, fg_color=GRAY_BG, height=46, corner_radius=0)
        tb.pack(fill="x");
        tb.pack_propagate(False)
        ctk.CTkLabel(tb, text="  Daftar Pasien TBC",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=TEXT1).pack(side="left", padx=12, pady=10)
        ctk.CTkButton(tb, text="+ Tambah Pasien", width=135, height=30,
                      font=ctk.CTkFont(size=10, weight="bold"), fg_color=GREEN,
                      text_color="white", hover_color="#15803D", corner_radius=6,
                      command=lambda: self._tampilkan_form_pasien([])).pack(side="right", padx=12, pady=8)
        self.pasien_scroll = ctk.CTkScrollableFrame(page, fg_color="transparent")
        self.pasien_scroll.pack(fill="both", expand=True, padx=12, pady=8)
        self._fix_scroll(self.pasien_scroll)

    def _refresh_pasien(self):
        self._refresh_status_pasien_aktif()
        for w in self.pasien_scroll.winfo_children(): w.destroy()
        if not DB_CONNECTED:
            ctk.CTkLabel(self.pasien_scroll, text="Database tidak terhubung.",
                         font=ctk.CTkFont(size=12), text_color=TEXT3).pack(pady=50);
            return
        data = load_pasien()
        if not data:
            ctk.CTkLabel(self.pasien_scroll, text="Belum ada data pasien.",
                         font=ctk.CTkFont(size=12), text_color=TEXT3).pack(pady=50);
            return
        hdr = ctk.CTkFrame(self.pasien_scroll, fg_color=NAVY, corner_radius=5)
        hdr.pack(fill="x", pady=(0, 4))
        for txt, w in [("ID", 36), ("Nama", 155), ("Usia", 50), ("J/K", 85), ("No.Telp", 110), ("Alamat", 160),
                       ("Aksi", 160)]:
            ctk.CTkLabel(hdr, text=txt, font=ctk.CTkFont(size=10, weight="bold"),
                         text_color="white", width=w, anchor="w").pack(side="left", padx=7, pady=7)
        for p in data:
            row = ctk.CTkFrame(self.pasien_scroll, fg_color=GRAY_BG, corner_radius=5)
            row.pack(fill="x", pady=(0, 3))
            ctk.CTkLabel(row, text=str(p["id"]), width=36,
                         font=ctk.CTkFont(size=10), text_color=TEXT3,
                         anchor="w").pack(side="left", padx=7, pady=7)
            ctk.CTkLabel(row, text=p["nama"], width=155,
                         font=ctk.CTkFont(size=11, weight="bold"), text_color=TEXT1,
                         anchor="w").pack(side="left", padx=3)
            ctk.CTkLabel(row, text=f"{p['usia']} th", width=50,
                         font=ctk.CTkFont(size=10), text_color=TEXT2,
                         anchor="w").pack(side="left", padx=3)
            ctk.CTkLabel(row, text=p["jenis_kelamin"], width=85,
                         font=ctk.CTkFont(size=10), text_color=TEXT2,
                         anchor="w").pack(side="left", padx=3)
            ctk.CTkLabel(row, text=p.get("no_telp", "-"), width=110,
                         font=ctk.CTkFont(size=10), text_color=TEXT2,
                         anchor="w").pack(side="left", padx=3)
            ctk.CTkLabel(row, text=p.get("alamat", "-"), width=160,
                         font=ctk.CTkFont(size=10), text_color=TEXT2,
                         anchor="w", wraplength=155).pack(side="left", padx=3, pady=3)
            bf = ctk.CTkFrame(row, fg_color="transparent");
            bf.pack(side="right", padx=5, pady=4)
            ctk.CTkButton(bf, text="Cetak", width=50, height=26,
                          font=ctk.CTkFont(size=9), fg_color=BLUE, text_color="white",
                          hover_color=NAVY2, corner_radius=4,
                          command=lambda px=p: self._cetak_laporan_pasien(px)).pack(side="left", padx=(0, 3))
            ctk.CTkButton(bf, text="Edit", width=46, height=26,
                          font=ctk.CTkFont(size=9), fg_color=AMBER, text_color="white",
                          hover_color="#B45309", corner_radius=4,
                          command=lambda px=p: self._edit_pasien(px)).pack(side="left", padx=(0, 3))
            ctk.CTkButton(bf, text="Hapus", width=52, height=26,
                          font=ctk.CTkFont(size=9), fg_color=RED, text_color="white",
                          hover_color="#B91C1C", corner_radius=4,
                          command=lambda pid=p["id"]: self._hapus_pasien(pid)).pack(side="left")

    def _edit_pasien(self, p):
        fields = [
            ("nama", "Nama Lengkap", "entry", {}),
            ("usia", "Usia (tahun)", "entry", {}),
            ("jenis_kelamin", "Jenis Kelamin", "option", {"values": ["Laki-laki", "Perempuan"]}),
            ("no_telp", "No. Telepon", "entry", {}),
            ("alamat", "Alamat", "entry", {}),
        ]
        vals = {"nama": p["nama"], "usia": str(p["usia"]), "jenis_kelamin": p["jenis_kelamin"],
                "no_telp": p.get("no_telp", ""), "alamat": p.get("alamat", "")}

        def cb(data):
            if not data["nama"] or not data["usia"]:
                messagebox.showerror("Error", "Nama dan Usia wajib diisi!");
                return
            if not data["usia"].isdigit():
                messagebox.showerror("Error", "Usia harus angka!");
                return
            ok = db_exec(
                "UPDATE pasien SET nama=%s,usia=%s,jenis_kelamin=%s,no_telp=%s,alamat=%s WHERE id=%s",
                (data["nama"], int(data["usia"]), data["jenis_kelamin"],
                 data["no_telp"], data["alamat"], p["id"]))
            if ok:
                self._refresh_pasien()
                messagebox.showinfo("Sukses", "Data pasien berhasil diperbarui!")
            else:
                messagebox.showerror("Error", "Gagal update. Cek koneksi database.")

        CRUDDialog(self, f"Edit Pasien [ID:{p['id']}]", fields, values=vals, callback=cb)

    def _hapus_pasien(self, pid):
        if messagebox.askyesno("Hapus",
                               f"Hapus pasien ID:{pid}?\nRiwayat diagnosa pasien ini juga terhapus!"):
            db_exec("DELETE FROM riwayat_diagnosa WHERE id_pasien=%s", (pid,))
            ok = db_exec("DELETE FROM pasien WHERE id=%s", (pid,))
            if ok:
                self._refresh_pasien()
            else:
                messagebox.showerror("Error", "Gagal hapus. Cek koneksi database.")

    def _cetak_laporan_pasien(self, p):
        """Laporan cetak untuk SATU pasien: data diri + seluruh riwayat
        diagnosanya, lengkap dengan rincian gejala beserta nilai CF_user
        dan CF_pakar (jika tersedia). Tombol ini khusus ada di menu
        Data Pasien, terpisah dari menu Cetak Laporan di sisi kiri.
        """
        import json as _json
        lines = ["=" * 70,
                 "         LAPORAN DIAGNOSA PASIEN",
                 "         Sistem Pakar Diagnosa TBC - Klinik Pratama EBHC",
                 f"         Dicetak: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
                 "=" * 70, "",
                 "DATA PASIEN",
                 "-" * 70,
                 f"  ID Pasien      : {p['id']}",
                 f"  Nama           : {p['nama']}",
                 f"  Usia           : {p['usia']} tahun",
                 f"  Jenis Kelamin  : {p['jenis_kelamin']}",
                 f"  No. Telepon    : {p.get('no_telp') or '-'}",
                 f"  Alamat         : {p.get('alamat') or '-'}",
                 ""]

        if not DB_CONNECTED:
            lines += ["Database tidak terhubung. Riwayat diagnosa tidak tersedia.", "=" * 70]
            self._simpan_dan_buka(lines, f"laporan_pasien_{p['nama'].replace(' ', '_')}.txt")
            return

        riwayat = db_fetch(
            "SELECT * FROM riwayat_diagnosa WHERE id_pasien=%s "
            "ORDER BY waktu_diagnosa DESC, id DESC", (p["id"],))
        if not riwayat:
            lines += ["Pasien ini belum memiliki riwayat diagnosa.", "=" * 70]
            self._simpan_dan_buka(lines, f"laporan_pasien_{p['nama'].replace(' ', '_')}.txt")
            return

        lines += ["RIWAYAT DIAGNOSA", "-" * 70, ""]
        for i, entry in enumerate(riwayat, 1):
            cf_v = entry.get("cf_tertinggi", 0)
            cf_s = f"{float(cf_v) * 100:.1f}%" if cf_v else "-"
            waktu = str(entry.get("waktu_diagnosa", ""))[:16]
            lines += [f"[{i}] Diagnosa Penyakit : {entry.get('diagnosa_utama', '-')}",
                      f"    Waktu Diagnosa    : {waktu}",
                      f"    Nilai CF Gabungan : {cf_s}"]
            detail = db_fetch(
                "SELECT * FROM riwayat_gejala_detail WHERE id_riwayat=%s ORDER BY id",
                (entry.get("id"),))
            if detail:
                lines.append(f"    {'Gejala':<32}{'CF Pakar':>10}{'CF User':>10}{'CF Gejala':>11}")
                lines.append("    " + "-" * 62)
                for d in detail:
                    nama_g = str(d.get("nama_gejala") or "-")[:30]
                    cfp = d.get("cf_pakar")
                    cfu = d.get("cf_user")
                    cfg = d.get("cf_gejala")
                    s_cfp = f"{float(cfp):.2f}" if cfp is not None else "-"
                    s_cfu = f"{float(cfu):.2f}" if cfu is not None else "-"
                    s_cfg = f"{float(cfg):.2f}" if cfg is not None else "-"
                    lines.append(f"    {nama_g:<32}{s_cfp:>10}{s_cfu:>10}{s_cfg:>11}")
            else:
                try:
                    gl = _json.loads(entry.get("gejala_dipilih", "[]"))
                except Exception:
                    gl = []
                lines.append(f"    Gejala Dipilih    : {', '.join(gl) if gl else '-'}")
            lines.append("")
        lines += ["=" * 70, f"Total Riwayat Diagnosa: {len(riwayat)}", "=" * 70]
        self._simpan_dan_buka(lines, f"laporan_pasien_{p['nama'].replace(' ', '_')}.txt")

    # ════════ TENTANG ════════
    def _build_page_tentang(self):
        page = ctk.CTkFrame(self.content, fg_color=WHITE, corner_radius=8)
        self.pages["tentang"] = page
        scroll = ctk.CTkScrollableFrame(page, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=18, pady=18)
        self._fix_scroll(scroll)
        uname = self.user_info.get("username", "?") if self.user_info else "?"
        urole = self.user_info.get("role", "?") if self.user_info else "?"
        for label, val in [
            ("Judul Penelitian",
             "Pengembangan Sistem Pakar Diagnosa Penyakit Tuberkulosis\n"
             "Menggunakan Metode Certainty Factor\nStudi Kasus Klinik Pratama EBHC"),
            ("Metode", "Certainty Factor (CF) - Shortliffe & Buchanan (1975)"),
            ("Studi Kasus", "Klinik Pratama EBHC, Jakarta Selatan"),
            ("Program Studi", "Teknik Informatika S1"),
            ("Universitas", "Universitas Indraprasta PGRI"),
            ("Database", "MySQL via XAMPP (MariaDB 10.4)"),
            ("Status DB", "Terhubung  OK" if DB_CONNECTED else "Tidak Terhubung  X"),
            ("Versi Aplikasi", "1.0.0 (2026)"),
            ("Bahasa", "Python 3.x + CustomTkinter + MySQL Connector"),
            ("User Aktif", f"{uname}  [{urole}]"),
        ]:
            row = ctk.CTkFrame(scroll, fg_color=GRAY_BG, corner_radius=7)
            row.pack(fill="x", pady=3)
            ctk.CTkLabel(row, text=label,
                         font=ctk.CTkFont(size=10, weight="bold"), text_color=TEXT2,
                         width=170, anchor="w").pack(side="left", padx=12, pady=8)
            clr = GREEN if ("OK" in val or "[" in val) else (RED if " X" in val else TEXT1)
            ctk.CTkLabel(row, text=val, font=ctk.CTkFont(size=11),
                         text_color=clr, anchor="w", justify="left").pack(side="left", padx=3)

    # ════════ FIX SCROLL (Linux) ════════
    def _fix_scroll(self, sf):
        """Fix scroll mouse Linux (Button-4/5) untuk semua CTkScrollableFrame."""

        def up(e):
            try:
                sf._parent_canvas.yview_scroll(-1, "units")
            except:
                pass

        def dn(e):
            try:
                sf._parent_canvas.yview_scroll(1, "units")
            except:
                pass

        def rec(w):
            w.bind("<Button-4>", up, add="+")
            w.bind("<Button-5>", dn, add="+")
            for c in w.winfo_children():
                rec(c)

        # Bind ke frame utama
        sf.bind("<Button-4>", up, add="+")
        sf.bind("<Button-5>", dn, add="+")

        # Bind ke canvas internal CTkScrollableFrame
        try:
            sf._parent_canvas.bind("<Button-4>", up, add="+")
            sf._parent_canvas.bind("<Button-5>", dn, add="+")
        except:
            pass

        # Bind ke semua child yang sudah ada
        rec(sf)

        # Bind ke child baru yang ditambahkan nanti (batch render dll)
        def on_new_widget(event):
            try:
                w = event.widget
                w.bind("<Button-4>", up, add="+")
                w.bind("<Button-5>", dn, add="+")
            except:
                pass

        sf.bind("<Map>", on_new_widget, add="+")
        try:
            sf._parent_canvas.bind("<Map>", on_new_widget, add="+")
        except:
            pass

    # ════════ LAPORAN ════════
    def _build_page_laporan(self):
        page = ctk.CTkFrame(self.content, fg_color=WHITE, corner_radius=8)
        self.pages["laporan"] = page
        hdr_info = ctk.CTkFrame(page, fg_color=NAVY, height=50, corner_radius=0)
        hdr_info.pack(fill="x");
        hdr_info.pack_propagate(False)
        ctk.CTkLabel(hdr_info, text=" Daftar Laporan",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="white").pack(side="left", padx=18, pady=12)
        ctk.CTkLabel(hdr_info, text="",
                     font=ctk.CTkFont(size=10), text_color="#8899BB").pack(side="left")
        self.laporan_scroll = ctk.CTkScrollableFrame(page, fg_color=GRAY_BG)
        self.laporan_scroll.pack(fill="both", expand=True)
        self._fix_scroll(self.laporan_scroll)

    def _refresh_laporan(self):
        for w in self.laporan_scroll.winfo_children(): w.destroy()
        laporan_items = [
            {"judul": "Laporan Data Penyakit TBC",
             "sub": "Daftar penyakit TBC beserta kode dan solusi penanganan",
             "icon": "◉", "warna": BLUE, "warna_lt": BLUE_LT, "action": self._cetak_laporan_penyakit},
            {"judul": "Laporan Data Gejala TBC",
             "sub": "Daftar gejala TBC per kategori beserta deskripsi medis",
             "icon": "◈", "warna": GREEN, "warna_lt": "#F0FDF4", "action": self._cetak_laporan_gejala},
            {"judul": "Laporan Nilai CF (Basis Pengetahuan)",
             "sub": "Tabel lengkap nilai Certainty Factor seluruh rule penyakit TBC",
             "icon": "∑", "warna": AMBER, "warna_lt": "#FFFBEB", "action": self._cetak_laporan_cf},
            {"judul": "Laporan Riwayat Diagnosa Pasien",
             "sub": "Rekap seluruh hasil diagnosa yang tersimpan di database",
             "icon": "≡", "warna": RED, "warna_lt": "#FFF1F2", "action": self._cetak_laporan_riwayat},
        ]
        ctk.CTkLabel(self.laporan_scroll,
                     text="Pilih jenis laporan di bawah ini untuk dicetak atau disimpan:",
                     font=ctk.CTkFont(size=11), text_color=TEXT2).pack(
            anchor="w", padx=18, pady=(14, 6))
        for item in laporan_items:
            card = ctk.CTkFrame(self.laporan_scroll, fg_color=WHITE,
                                corner_radius=10, border_width=1, border_color=GRAY_BD)
            card.pack(fill="x", padx=14, pady=(0, 10))
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=14, pady=12)
            badge = ctk.CTkFrame(inner, fg_color=item["warna_lt"],
                                 width=46, height=46, corner_radius=9)
            badge.pack(side="left");
            badge.pack_propagate(False)
            ctk.CTkLabel(badge, text=item["icon"], font=ctk.CTkFont(size=20),
                         text_color=item["warna"]).place(relx=.5, rely=.5, anchor="center")
            txt = ctk.CTkFrame(inner, fg_color="transparent")
            txt.pack(side="left", fill="x", expand=True, padx=12)
            ctk.CTkLabel(txt, text=item["judul"],
                         font=ctk.CTkFont(size=12, weight="bold"),
                         text_color=TEXT1, anchor="w").pack(anchor="w")
            ctk.CTkLabel(txt, text=item["sub"],
                         font=ctk.CTkFont(size=10), text_color=TEXT2,
                         anchor="w").pack(anchor="w", pady=(2, 0))
            ctk.CTkButton(inner, text="Cetak", width=95, height=34,
                          font=ctk.CTkFont(size=11, weight="bold"),
                          fg_color=item["warna"], text_color="white",
                          hover_color=NAVY2, corner_radius=7,
                          command=item["action"]).pack(side="right")
        info = ctk.CTkFrame(self.laporan_scroll, fg_color=BLUE_LT, corner_radius=7,
                            border_width=1, border_color="#93C5FD")
        info.pack(fill="x", padx=14, pady=(2, 14))
        ctk.CTkLabel(info,
                     text="Laporan disimpan ke Desktop sebagai file .txt dan dibuka otomatis.",
                     font=ctk.CTkFont(size=10), text_color=BLUE,
                     wraplength=680, justify="left").pack(anchor="w", padx=12, pady=8)

    def _cetak_laporan_penyakit(self):
        from datetime import datetime
        lines = ["=" * 70, "         LAPORAN DATA PENYAKIT TBC",
                 "         Sistem Pakar Diagnosa TBC - Klinik Pratama EBHC",
                 f"         Dicetak: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", "=" * 70, ""]
        for kode, info in self.PENYAKIT.items():
            lines += [f"[{kode}] {info['nama']}", f"      Solusi : {info['solusi']}", ""]
        lines += ["=" * 70, f"Total Penyakit: {len(self.PENYAKIT)}", "=" * 70]
        self._simpan_dan_buka(lines, "laporan_penyakit_tbc.txt")

    def _cetak_laporan_gejala(self):
        from datetime import datetime
        lines = ["=" * 70, "         LAPORAN DATA GEJALA TBC",
                 "         Sistem Pakar Diagnosa TBC - Klinik Pratama EBHC",
                 f"         Dicetak: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", "=" * 70, ""]
        for kat, gejala_dict in self.KAT_GEJALA.items():
            lines += [f"[ {kat.upper()} ]", "-" * 50]
            for kode, nama in gejala_dict.items():
                lines += [f"  [{kode}] {nama}", f"         {DESKRIPSI_GEJALA.get(kode, '-')}", ""]
        total = sum(len(v) for v in self.KAT_GEJALA.values())
        lines += ["=" * 70, f"Total Gejala: {total}", "=" * 70]
        self._simpan_dan_buka(lines, "laporan_gejala_tbc.txt")

    def _cetak_laporan_cf(self):
        from datetime import datetime
        lines = ["=" * 70, "         LAPORAN NILAI CF (BASIS PENGETAHUAN TBC)",
                 "         Sistem Pakar Diagnosa TBC - Klinik Pratama EBHC",
                 f"         Dicetak: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", "=" * 70, "",
                 "Rumus: CF(H,E) = CF_pakar x CF_user",
                 "Kombinasi: CF1+CF2*(1-CF1) jika keduanya positif",
                 "Kombinasi: CF1+CF2*(1+CF1) jika keduanya negatif",
                 "Kombinasi: CF1+CF2/(1-min(|CF1|, |CF2|)) jika satu positif dan satu negatif",
                 f"{'KodeP':<7}{'Nama Penyakit':<30}{'KodeG':<7}{'Nama Gejala':<28}{'CF':>5}  {'Interp.':<14}",
                 "-" * 91]
        for (pk, gk, cf) in self.RULES:
            nama_p = self.PENYAKIT.get(pk, {}).get("nama", pk)[:28]
            nama_g = self.GEJALA.get(gk, gk)[:26]
            interp = ("Sangat Tinggi" if cf >= 0.8 else
                      "Tinggi" if cf >= 0.6 else
                      "Sedang" if cf >= 0.4 else "Rendah")
            lines.append(f"{pk:<7}{nama_p:<30}{gk:<7}{nama_g:<28}{cf:>5.2f}  {interp:<14}")
        lines += ["=" * 70, f"Total Rules: {len(self.RULES)}", "=" * 70]
        self._simpan_dan_buka(lines, "laporan_nilai_cf_tbc.txt")

    def _cetak_laporan_riwayat(self):
        from datetime import datetime;
        import json as _json
        lines = ["=" * 70, "         LAPORAN RIWAYAT DIAGNOSA PASIEN TBC",
                 "         Sistem Pakar Diagnosa TBC - Klinik Pratama EBHC",
                 f"         Dicetak: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", "=" * 70, ""]
        if not DB_CONNECTED:
            lines.append("Database tidak terhubung. Riwayat tidak tersedia.")
        else:
            data = load_riwayat(100)
            if not data:
                lines.append("Belum ada riwayat diagnosa.")
            else:
                for i, entry in enumerate(data, 1):
                    cf_v = entry.get("cf_tertinggi", 0)
                    lines += [f"No.{i}",
                              f"  Pasien   : {entry.get('nama_pasien', '-')}",
                              f"  Waktu    : {str(entry.get('waktu_diagnosa', ''))[:16]}",
                              f"  Diagnosa : {entry.get('diagnosa_utama', '-')}",
                              f"  Nilai CF : {f'{float(cf_v) * 100:.1f}%' if cf_v else '-'}"]
                    try:
                        gl = _json.loads(entry.get("gejala_dipilih", "[]"))
                        lines.append(f"  Gejala   : {', '.join(gl[:4])}")
                    except:
                        pass
                    lines.append("")
                lines += ["-" * 70, f"Total Riwayat: {len(data)}"]
        lines += ["=" * 70]
        self._simpan_dan_buka(lines, "laporan_riwayat_diagnosa.txt")

    def _simpan_dan_buka(self, lines, filename):
        title_doc = filename.replace("laporan_", "").replace(".txt", "").replace("_", " ").title()
        LaporanPreviewWindow(self, title_doc, lines, filename)


# ─────────────────────────────────────────
#  JASPERVIEWER-STYLE PREVIEW WINDOW
# ─────────────────────────────────────────
class LaporanPreviewWindow(ctk.CTkToplevel):
    def __init__(self, parent, title_doc, lines, default_filename):
        super().__init__(parent)
        self.title(f"JasperViewer - Preview [{title_doc}]")
        self.geometry("760x780")
        self.minsize(650, 550)
        self.grab_set()
        self.lift()
        self.focus_force()
        self.configure(fg_color="#D1D5DB")

        self.lines = lines
        self.default_filename = default_filename
        self.saved_path = None

        self._build_toolbar(title_doc)
        self._build_paper_view()

    def _build_toolbar(self, title_doc):
        tb = ctk.CTkFrame(self, fg_color=NAVY, height=48, corner_radius=0)
        tb.pack(fill="x", side="top")
        tb.pack_propagate(False)

        ctk.CTkLabel(tb, text=f"  📄 Preview Laporan: {title_doc}",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color="white").pack(side="left", padx=14)

        ctk.CTkButton(tb, text="✖  Tutup", width=80, height=30,
                      font=ctk.CTkFont(size=10, weight="bold"),
                      fg_color=RED, text_color="white", hover_color="#B91C1C",
                      corner_radius=6, command=self.destroy).pack(side="right", padx=12, pady=9)

        ctk.CTkButton(tb, text="💾  Simpan / Export Laporan", width=160, height=30,
                      font=ctk.CTkFont(size=10, weight="bold"),
                      fg_color=GREEN, text_color="white", hover_color="#15803D",
                      corner_radius=6, command=self._simpan_file).pack(side="right", padx=4, pady=9)

    def _build_paper_view(self):
        # Scrollable Outer Container
        outer_scroll = ctk.CTkScrollableFrame(self, fg_color="#D1D5DB")
        outer_scroll.pack(fill="both", expand=True, padx=16, pady=12)

        # Lembaran Kertas A4 (Warna Putih Bersih)
        paper = ctk.CTkFrame(outer_scroll, fg_color="white", corner_radius=4,
                             border_width=1, border_color="#9CA3AF")
        paper.pack(fill="both", expand=True, padx=10, pady=8, ipady=15)

        # KOP SURAT KLINIK
        kop_frame = ctk.CTkFrame(paper, fg_color="transparent")
        kop_frame.pack(fill="x", padx=25, pady=(20, 5))

        # Logo Klinik di Kop Surat
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "LOGO_EBHC_noBG.png")
        if os.path.exists(logo_path):
            try:
                logo_img = ctk.CTkImage(light_image=Image.open(logo_path), size=(65, 65))
                ctk.CTkLabel(kop_frame, image=logo_img, text="").pack(side="left", padx=(0, 15))
            except:
                pass

        kop_text = ctk.CTkFrame(kop_frame, fg_color="transparent")
        kop_text.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(kop_text, text="KLINIK PRATAMA EBHC INDONESIA",
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color=NAVY, anchor="w").pack(anchor="w")
        ctk.CTkLabel(kop_text,
                     text="Melayani Pemeriksaan Kesehatan Dasar, Vaksinasi anak dan Lansia, Dan Menerbitkan Sertifikat Vaksin Internasional - Aman, Nyaman, Prima",
                     font=ctk.CTkFont(size=10, weight="bold"),
                     text_color="#16A34A", anchor="w").pack(anchor="w", pady=(1, 0))
        ctk.CTkLabel(kop_text,
                     text="Jl. Rawajati Timur No.9 Blok K RT.07/RW.06,Rawajati, Pancoran, Jakarta Selatan, Daerah Khusus Ibukota Jakarta,12750| Telp: 0812-9007-0644",
                     font=ctk.CTkFont(size=9), text_color=TEXT2, anchor="w").pack(anchor="w")

        # Garis Pembatas KOP Surat Double Line
        ctk.CTkFrame(paper, fg_color=NAVY, height=3).pack(fill="x", padx=25, pady=(10, 2))
        ctk.CTkFrame(paper, fg_color=NAVY, height=1).pack(fill="x", padx=25, pady=(1, 15))

        # DOKUMEN BODY (Teks Laporan)
        body_frame = ctk.CTkFrame(paper, fg_color="transparent")
        body_frame.pack(fill="both", expand=True, padx=25)

        font_doc = ctk.CTkFont(family="Consolas", size=10) if os.name == "nt" else ctk.CTkFont(family="Courier",
                                                                                               size=10)

        tb_view = ctk.CTkTextbox(body_frame, font=font_doc, fg_color="#F9FAFB",
                                 text_color="#1F2937", border_width=1, border_color="#E5E7EB",
                                 height=360, corner_radius=6)
        tb_view.pack(fill="both", expand=True)
        tb_view.insert("1.0", "\n".join(self.lines))
        tb_view.configure(state="disabled")

        # AREA TANDA TANGAN (Khas JasperReports)
        from datetime import datetime
        ttd_frame = ctk.CTkFrame(paper, fg_color="transparent")
        ttd_frame.pack(fill="x", padx=25, pady=(20, 10))

        right_ttd = ctk.CTkFrame(ttd_frame, fg_color="transparent")
        right_ttd.pack(side="right")

        tgl_str = format_tanggal_id()
        ctk.CTkLabel(right_ttd, text=f"Jakarta, {tgl_str}",
                     font=ctk.CTkFont(size=10), text_color=TEXT1).pack(anchor="c")
        ctk.CTkLabel(right_ttd, text="Dokter Penanggung Jawab,",
                     font=ctk.CTkFont(size=10, weight="bold"), text_color=TEXT1).pack(anchor="c", pady=(2, 45))
        ctk.CTkLabel(right_ttd, text="( ________________________ )",
                     font=ctk.CTkFont(size=10, weight="bold"), text_color=TEXT1).pack(anchor="c")
        ctk.CTkLabel(right_ttd, text="dr. Ika Fajarwati, MARS",
                     font=ctk.CTkFont(size=9), text_color=TEXT2).pack(anchor="c")

    def _simpan_file(self):
        import sys
        from tkinter import filedialog
        content = "\n".join(self.lines)

        home = os.path.expanduser("~")
        candidates = [
            os.path.join(home, "Desktop"),
            os.path.join(home, "OneDrive", "Desktop"),
            os.path.join(home, "OneDrive - Personal", "Desktop"),
        ]
        desktop = next((p for p in candidates if os.path.isdir(p)), home)

        path = filedialog.asksaveasfilename(
            title="Simpan Laporan",
            initialdir=desktop,
            initialfile=self.default_filename,
            defaultextension=".txt",
            filetypes=[("Text File", "*.txt"), ("Semua File", "*.*")]
        )
        if not path:
            return

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            self.saved_path = path
            if messagebox.askyesno("Berhasil Disimpan",
                                   f"Laporan berhasil disimpan di:\n{path}\n\nIngin membuka file sekarang?"):
                if sys.platform == "win32":
                    os.startfile(path)
                elif sys.platform == "darwin":
                    import subprocess;
                    subprocess.Popen(["open", path])
                else:
                    import subprocess;
                    subprocess.Popen(["xdg-open", path])
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan laporan:\n{e}")


# ─────────────────────────────────────────
#  USERS & LOGIN
# ─────────────────────────────────────────
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "dokter": {"password": "dokter123", "role": "dokter"},
}


class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login - Sistem Pakar TBC Klinik Pratama EBHC")
        self.geometry("420x560")
        self.resizable(False, False)
        self.configure(fg_color=GRAY_BG)
        self.logged_in_user = None
        self._build_ui()

    def _build_ui(self):
        card = ctk.CTkFrame(self, fg_color=WHITE, corner_radius=14,
                            border_width=1, border_color=GRAY_BD, width=370, height=500)
        card.pack_propagate(False);
        card.place(relx=0.5, rely=0.5, anchor="center")
        hdr = ctk.CTkFrame(card, fg_color=NAVY, height=130, corner_radius=14)
        hdr.pack(fill="x");
        hdr.pack_propagate(False)
        ctk.CTkFrame(card, fg_color=NAVY, height=14, corner_radius=0).pack(fill="x")
        # Logo klinik di header login
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "LOGO_EBHC_noBG.png")
        if os.path.exists(logo_path):
            try:
                login_logo = ctk.CTkImage(light_image=Image.open(logo_path), size=(80, 90))
                ctk.CTkLabel(hdr, image=login_logo, text="").place(
                    relx=0.5, rely=0.32, anchor="center")
            except:
                icon = ctk.CTkFrame(hdr, fg_color=NAVY2, width=46, height=46, corner_radius=10)
                icon.place(relx=0.5, rely=0.32, anchor="center")
                ctk.CTkLabel(icon, text="✚", font=ctk.CTkFont(size=22),
                             text_color="white").place(relx=.5, rely=.5, anchor="center")
        else:
            icon = ctk.CTkFrame(hdr, fg_color=NAVY2, width=46, height=46, corner_radius=10)
            icon.place(relx=0.5, rely=0.32, anchor="center")
            ctk.CTkLabel(icon, text="✚", font=ctk.CTkFont(size=22),
                         text_color="white").place(relx=.5, rely=.5, anchor="center")
        ctk.CTkLabel(hdr, text="Sistem Pakar TBC",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="white").place(relx=0.5, rely=0.72, anchor="center")
        ctk.CTkLabel(hdr, text="Klinik Pratama EBHC Indonesia",
                     font=ctk.CTkFont(size=10),
                     text_color="#8899BB").place(relx=0.5, rely=0.88, anchor="center")
        body = ctk.CTkFrame(card, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=26, pady=14)
        ctk.CTkLabel(body, text="Username",
                     font=ctk.CTkFont(size=10, weight="bold"), text_color=TEXT2).pack(anchor="w")
        self.entry_user = ctk.CTkEntry(body, placeholder_text="Masukkan username",
                                       font=ctk.CTkFont(size=12), height=38, corner_radius=7)
        self.entry_user.pack(fill="x", pady=(3, 10))
        ctk.CTkLabel(body, text="Password",
                     font=ctk.CTkFont(size=10, weight="bold"), text_color=TEXT2).pack(anchor="w")
        self.entry_pass = ctk.CTkEntry(body, placeholder_text="Masukkan password",
                                       font=ctk.CTkFont(size=12), height=38,
                                       corner_radius=7, show="*")
        self.entry_pass.pack(fill="x", pady=(3, 4))
        # Show Password checkbox
        self.show_pass_var = ctk.BooleanVar(value=False)
        self.chk_show_pass = ctk.CTkCheckBox(
            body, text="Show Password",
            variable=self.show_pass_var,
            command=self._toggle_show_password,
            font=ctk.CTkFont(size=10), text_color=TEXT2,
            fg_color=NAVY, hover_color=NAVY2,
            checkbox_width=18, checkbox_height=18, corner_radius=4)
        self.chk_show_pass.pack(anchor="w", pady=(2, 10))
        self.lbl_error = ctk.CTkLabel(body, text="",
                                      font=ctk.CTkFont(size=10), text_color=RED)
        self.lbl_error.pack()
        ctk.CTkButton(body, text="Masuk", height=40,
                      font=ctk.CTkFont(size=12, weight="bold"),
                      fg_color=NAVY, text_color="white", hover_color=NAVY2,
                      corner_radius=9, command=self._login).pack(fill="x", pady=(6, 0))
        ctk.CTkLabel(body, text="Default: dokter / dokter123",
                     font=ctk.CTkFont(size=9), text_color=TEXT3).pack(pady=(8, 0))
        self.entry_user.bind("<Return>", lambda e: self.entry_pass.focus())
        self.entry_pass.bind("<Return>", lambda e: self._login())
        self.after(80, lambda: self.entry_user.focus())

    def _toggle_show_password(self):
        """Toggle visibility password field."""
        if self.show_pass_var.get():
            self.entry_pass.configure(show="")
        else:
            self.entry_pass.configure(show="*")

    def _login(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()
        if username in USERS and USERS[username]["password"] == password:
            self.logged_in_user = {"username": username, "role": USERS[username]["role"]}
            self.after(10, self.destroy)
        else:
            self.lbl_error.configure(text="Username atau password salah!")
            self.entry_pass.delete(0, "end")
            self.after(80, lambda: self.entry_pass.focus())


# ─────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────
if __name__ == "__main__":
    while True:
        # Buat instance LoginWindow baru setiap siklus
        login = LoginWindow()
        login.mainloop()

        user_info = login.logged_in_user
        # Pastikan window login benar-benar sudah dihancurkan
        try:
            login.destroy()
        except:
            pass

        if not user_info:
            break  # User tutup window tanpa login → keluar

        # Buka aplikasi utama
        app = SistemPakarApp(user_info=user_info)
        app.mainloop()

        # Pastikan window app benar-benar sudah dihancurkan
        try:
            app.destroy()
        except:
            pass

        if not getattr(app, "logout_flag", False):
            break  # Window ditutup bukan via tombol Logout → keluar total
        # Jika logout_flag=True → lanjut loop → buka LoginWindow baru