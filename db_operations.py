import json
from db_config import fetch_all, execute_query

def load_penyakit():
    rows = fetch_all("SELECT kode, nama, solusi FROM penyakit ORDER BY kode")
    return {r["kode"]: {"nama": r["nama"], "solusi": r["solusi"]} for r in rows}

def load_gejala():
    rows = fetch_all("SELECT kode, nama FROM gejala ORDER BY kode")
    return {r["kode"]: r["nama"] for r in rows}

def load_gejala_per_kategori():
    rows = fetch_all("SELECT kode, nama, kategori FROM gejala ORDER BY kategori, kode")
    result = {}
    for r in rows:
        kat = r["kategori"] or "Lainnya"
        if kat not in result:
            result[kat] = {}
        result[kat][r["kode"]] = r["nama"]
    return result

def load_rules():
    rows = fetch_all("SELECT kode_penyakit, kode_gejala, cf_pakar FROM rules")
    return [(r["kode_penyakit"], r["kode_gejala"], float(r["cf_pakar"])) for r in rows]

def load_pasien():
    return fetch_all("""
        SELECT p.*,
               (SELECT MAX(r.waktu_diagnosa) FROM riwayat_diagnosa r
                WHERE r.id_pasien = p.id) AS terakhir_diagnosa
        FROM pasien p
        ORDER BY terakhir_diagnosa DESC, p.id DESC
    """)

def load_riwayat(limit=20):
    return fetch_all(f"""
        SELECT r.id, r.waktu_diagnosa, r.cf_tertinggi,
               r.gejala_dipilih, r.hasil_diagnosa,
               p.nama AS nama_pasien,
               py.nama AS diagnosa_utama
        FROM riwayat_diagnosa r
        JOIN pasien p  ON r.id_pasien = p.id
        JOIN penyakit py ON r.diagnosa_utama = py.kode
        ORDER BY r.waktu_diagnosa DESC
        LIMIT {limit}
    """)

def simpan_pasien(nama, usia, jk, telp, alamat):
    return execute_query(
        "INSERT INTO pasien (nama, usia, jenis_kelamin, no_telp, alamat) VALUES (%s,%s,%s,%s,%s)",
        (nama, usia, jk, telp, alamat)
    )

def simpan_riwayat_db(id_pasien, gejala_list, hasil):
    if not hasil:
        return -1
    diagnosa_utama = list(hasil.keys())[0]
    cf_tertinggi   = list(hasil.values())[0]
    return execute_query(
        """INSERT INTO riwayat_diagnosa
           (id_pasien, gejala_dipilih, hasil_diagnosa, diagnosa_utama, cf_tertinggi)
           VALUES (%s, %s, %s, %s, %s)""",
        (
            id_pasien,
            json.dumps(gejala_list, ensure_ascii=False),
            json.dumps({k: round(v,4) for k,v in list(hasil.items())[:5]}, ensure_ascii=False),
            diagnosa_utama,
            round(cf_tertinggi, 4),
        )
    )

def get_statistik():
    rows_p  = fetch_all("SELECT COUNT(*) AS n FROM penyakit")
    rows_g  = fetch_all("SELECT COUNT(*) AS n FROM gejala")
    rows_r  = fetch_all("SELECT COUNT(*) AS n FROM rules")
    rows_ps = fetch_all("SELECT COUNT(*) AS n FROM pasien")
    rows_rv = fetch_all("SELECT COUNT(*) AS n FROM riwayat_diagnosa")
    return {
        "total_penyakit": rows_p[0]["n"]  if rows_p  else 0,
        "total_gejala":   rows_g[0]["n"]  if rows_g  else 0,
        "total_rules":    rows_r[0]["n"]  if rows_r  else 0,
        "total_pasien":   rows_ps[0]["n"] if rows_ps else 0,
        "total_riwayat":  rows_rv[0]["n"] if rows_rv else 0,
    }