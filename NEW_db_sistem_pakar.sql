-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Waktu pembuatan: 13 Jul 2026 pada 11.59
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_sistem_pakar`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `gejala`
--

CREATE TABLE `gejala` (
  `id` int(11) NOT NULL,
  `kode` varchar(5) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `kategori` varchar(50) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data untuk tabel `gejala`
--

INSERT INTO `gejala` (`id`, `kode`, `nama`, `kategori`, `created_at`) VALUES
(1, 'G01', 'Batuk Kronis (>2 minggu)', 'Gejala Utama', '2026-05-22 06:24:47'),
(2, 'G02', 'Batuk Berdarah (Hemoptisis)', 'Gejala Utama', '2026-05-22 06:24:47'),
(3, 'G03', 'Batuk Berdahak', 'Gejala Utama', '2026-05-22 06:24:47'),
(4, 'G04', 'Demam Subfebris (37.5-38.5°C)', 'Gejala Sistemik / Umum', '2026-05-22 06:24:47'),
(5, 'G05', 'Keringat Malam Berlebih', 'Gejala Sistemik / Umum', '2026-05-22 06:24:47'),
(6, 'G06', 'Penurunan Berat Badan', 'Gejala Sistemik / Umum', '2026-05-22 06:24:47'),
(7, 'G07', 'Lemas & Kelelahan', 'Gejala Sistemik / Umum', '2026-05-22 06:24:47'),
(8, 'G08', 'Kehilangan Nafsu Makan (Anoreksia)', 'Gejala Sistemik / Umum', '2026-05-22 06:24:47'),
(9, 'G09', 'Menggigil', 'Gejala Sistemik / Umum', '2026-05-22 06:24:47'),
(10, 'G10', 'Pembengkakan Kelenjar Getah Bening', 'Gejala Spesifik TB Ekstra Paru (Luar Paru)', '2026-05-22 06:24:47'),
(11, 'G11', 'Sakit Kepala Hebat dan Kaku Kuduk', 'Gejala Spesifik TB Ekstra Paru (Luar Paru)', '2026-05-22 06:24:47'),
(12, 'G12', 'Perut Membuncit dan Nyeri Tekan', 'Gejala Spesifik TB Ekstra Paru (Luar Paru)', '2026-05-22 06:24:47'),
(13, 'G13', 'Urine Berwarna Keruh atau Kemerahan', 'Gejala Spesifik TB Ekstra Paru (Luar Paru)', '2026-05-22 06:24:47'),
(14, 'G14', 'Kelainan Kulit (Skrofuloderma)', 'Gejala Spesifik TB Ekstra Paru (Luar Paru)', '2026-05-22 06:24:47'),
(15, 'G15', 'Nyeri Sendi dan Tulang', 'Gejala Spesifik TB Ekstra Paru (Luar Paru)', '2026-05-22 06:24:47'),
(16, 'G16', 'Nyeri Dada', 'Gejala Respiratorius (Sistem Pernapasan)', '2026-05-22 06:24:47'),
(17, 'G17', 'Sesak Napas (Dispnea)', 'Gejala Respiratorius (Sistem Pernapasan)', '2026-05-22 06:24:47'),
(18, 'G18', 'Suara Napas Tidak Normal', 'Gejala Respiratorius (Sistem Pernapasan)', '2026-05-22 06:24:47'),
(19, 'G19', 'Suara Serau (Disfonia)', 'Gejala Respiratorius (Sistem Pernapasan)', '2026-07-03 06:30:06'),
(20, 'G20', 'Kontak Erat Penderita TBC', 'Gejala Lainnya', '2026-05-22 06:24:47');

-- --------------------------------------------------------

--
-- Struktur dari tabel `pasien`
--

CREATE TABLE `pasien` (
  `id` int(11) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `usia` int(11) NOT NULL,
  `jenis_kelamin` enum('Laki-laki','Perempuan') NOT NULL,
  `no_telp` varchar(20) DEFAULT NULL,
  `alamat` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data untuk tabel `pasien`
--

INSERT INTO `pasien` (`id`, `nama`, `usia`, `jenis_kelamin`, `no_telp`, `alamat`, `created_at`) VALUES
(1, 'Ahmad Fauzi', 35, 'Laki-laki', '081234567890', 'Jl. Merdeka No.1, Jakarta', '2026-04-24 12:37:22'),
(2, 'Siti Maimunah', 28, 'Perempuan', '082345678901', 'Jl. Sudirman No.5, Jakarta', '2026-04-24 12:37:22'),
(3, 'Budi Sulis', 45, 'Laki-laki', '083456789012', 'Jl. Gatot Subroto No.10, Jakarta', '2026-04-24 12:37:22'),
(5, 'Ramadhan', 16, 'Laki-laki', '08123456789', 'Jakarta Selatan, 12750', '2026-05-04 14:23:29'),
(6, 'Shafa', 15, 'Perempuan', '08987654321', 'Jakarta Timur, 12890', '2026-05-04 15:29:31'),
(7, 'JEJE', 20, 'Perempuan', '08987456321', 'Jakarta barat, 13456', '2026-05-05 15:01:10'),
(8, 'owowi', 40, 'Laki-laki', '021345678', 'Istana solo merdeka, 31245', '2026-05-06 11:48:09'),
(9, 'gilang', 29, 'Laki-laki', '08789456123', 'jakarta', '2026-05-09 18:06:08'),
(10, 'RAJALON', 23, 'Laki-laki', '02136456987', 'jakbar, 12345', '2026-05-22 06:28:55'),
(11, 'samar', 44, 'Perempuan', '0123456789', 'indonesia, jakarta', '2026-05-22 08:52:56'),
(12, 'jono', 30, 'Laki-laki', '12345678', 'disini dibatas kota ini, INDONESIA', '2026-05-23 05:47:32'),
(13, 'tayo', 35, 'Laki-laki', '08798456123', 'rajawali selatan 2', '2026-06-24 05:24:32'),
(14, 'Listyo', 55, 'Laki-laki', '08789456123', 'Jakbar, Tomang', '2026-07-09 06:24:24');

-- --------------------------------------------------------

--
-- Struktur dari tabel `penyakit`
--

CREATE TABLE `penyakit` (
  `id` int(11) NOT NULL,
  `kode` varchar(5) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `deskripsi` text DEFAULT NULL,
  `solusi` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data untuk tabel `penyakit`
--

INSERT INTO `penyakit` (`id`, `kode`, `nama`, `deskripsi`, `solusi`, `created_at`) VALUES
(1, 'P01', 'TBC Paru Terkonfirmasi Bakteriologis (BTA Positif)', 'Infeksi bakteri TBC yang menyerang jaringan parenkim paru-paru dan hasil pemeriksaan laboratorium (seperti tes dahak mikroskopis atau Tes Cepat Molekuler/TCM) menyatakan positif ditemukan keberadaan bakteri. Jenis ini memiliki tingkat penularan yang sangat tinggi melalui droplet udara.', 'Pengobatan intensif menggunakan Paket Obat Anti Tuberkulosis (OAT) Kategori 1 (Isoniazid, Rifampisin, Pirazinamid, Etambutol) selama minimal 6 bulan (2 bulan fase intensif, 4 bulan fase lanjutan). Segera lakukan isolasi mandiri di awal pengobatan, gunakan masker, jagalah ventilasi udara rumah tetap baik, dan lakukan pemantauan kepatuhan minum obat melalui PMO (Pengawas Menelan Obat).', '2026-05-22 06:24:47'),
(2, 'P02', 'TBC Paru Terkonfirmasi Klinis (BTA Negatif, rontgen mendukung)', 'Infeksi TBC yang menyerang paru-paru, namun hasil pemeriksaan bakteriologis (dahak) menunjukkan hasil negatif atau belum keluar. Meskipun begitu, dokter tetap mendiagnosisnya sebagai TBC aktif karena pasien menunjukkan gejala klinis yang khas serta didukung oleh hasil foto rontgen dada (toraks) yang abnormal.', 'Meskipun hasil dahak negatif, pengobatan tetap menggunakan OAT Kategori 1 selama 6 bulan penuh karena gejala klinis dan rontgen dada menunjukkan infeksi aktif. Pasien disarankan menjaga daya tahan tubuh dengan nutrisi tinggi protein, kontrol berkala ke fasilitas kesehatan untuk evaluasi dahak/foto toraks ulang, serta memastikan anggota keluarga rumah diperiksa untuk pelacakan kontak erat.', '2026-05-22 06:24:47'),
(3, 'P03', 'TBC Laten (Terinfeksi tanpa gejala aktif)', 'Kondisi di mana bakteri TBC sudah masuk dan hidup di dalam tubuh seseorang (biasanya karena riwayat kontak erat), namun sistem kekebalan tubuh mampu menahan bakteri tersebut tetap tidak aktif (tertidur). Pasien dalam kondisi ini tidak menunjukkan gejala klinis, tidak merasa sakit, dan tidak menular, namun berisiko menjadi TBC aktif jika imun tubuh drop.\r\n', 'Kuman dalam kondisi \'tertidur\' dan tidak menular, namun memerlukan Terapi Pencegahan Tuberkulosis (TPT). Solusinya meliputi pemberian obat pencegahan seperti Isoniazid (INH) selama 6 bulan atau kombinasi Rifampisin-Isoniazid lebih singkat sesuai resep dokter. Pasien wajib menerapkan pola hidup sehat guna mencegah kuman berkembang menjadi TBC aktif akibat penurunan imun.', '2026-05-22 06:24:47'),
(4, 'P04', 'TBC Kelenjar (Limfadenitis TB)', 'Salah satu bentuk TBC luar paru (ekstra paru) yang paling sering terjadi. Kuman TBC menyerang sistem limfatik, menyebabkan peradangan dan pembengkakan pada kelenjar getah bening. Area yang paling sering diserang adalah kelenjar di daerah leher (servikal), ketiak, atau selangkingan.', 'Pengobatan utama menggunakan OAT Kategori 1, namun durasinya bisa diperpanjang hingga 9-12 bulan tergantung evaluasi klinis dokter. Disarankan untuk tidak memijat atau memanipulasi benjolan di leher/ketiak guna mencegah pecahnya benjolan menjadi luka terbuka (skrofuloderma). Pada kasus tertentu yang menyumbat saluran napas, tindakan drainase atau pembedahan minor dapat dipertimbangkan.', '2026-05-22 06:24:47'),
(5, 'P05', 'TBC Meningitis (Menyerang selaput otak)', 'Kondisi komplikasi yang sangat serius di mana bakteri TBC menyebar melalui aliran darah dan menginfeksi selaput yang menutupi otak dan sumsum tulang belakang (meningen). Penyakit ini memicu peradangan hebat di kepala dan dapat menyebabkan kerusakan saraf permanen hingga penurunan kesadaran jika terlambat ditangani.', 'Merupakan kondisi darurat medis yang memerlukan rawat inap segera. Pengobatan menggunakan regimen OAT yang dimodifikasi dengan penambahan Kortikosteroid (seperti Deksametason) di awal terapi untuk mengurangi peradangan hebat pada otak. Durasi pengobatan total berkisar antara 9 hingga 12 bulan dengan pengawasan ketat dari dokter spesialis saraf.', '2026-05-22 06:24:47'),
(6, 'P06', 'TBC Peritoneal (Menyerang rongga perut/pencernaan)', 'Bentuk TBC ekstra paru di mana kuman menginfeksi lapisan membran tipis yang melapisi rongga perut dan organ dalam perut (peritoneum). Infeksi ini sering kali menyebabkan akumulasi penumpukan cairan abnormal di dalam rongga perut (kondisi perut membusung/asites) disertai rasa nyeri kronis.', 'Terapi medis utama menggunakan OAT Kategori 1 dengan durasi 9-12 bulan. Pasien direkomendasikan mengonsumsi makanan yang mudah dicerna dalam porsi kecil tapi sering, serta pemantauan tanda-tanda komplikasi seperti penyumbatan usus atau penumpukan cairan perut (asites). Jika terjadi penumpukan cairan masif, tindakan parasintesis (penyedotan cairan) mungkin diperlukan.', '2026-05-22 06:24:47'),
(7, 'P07', 'TBC Urogenital / Ginjal (Menyerang saluran kemih)', 'Infeksi bakteri TBC yang menyerang organ sistem reproduksi dan saluran kemih, utamanya organ ginjal. Bakteri yang merusak jaringan ginjal ini secara perlahan dapat menyebar ke saluran kandung kemih, menyebabkan nyeri pinggang, gangguan berkemih, hingga memicu urine bercampur darah.', 'Pemberian terapi OAT jangka panjang minimal 9 bulan untuk mencegah kerusakan permanen pada struktur ginjal dan saluran kemih. Pasien disarankan memperbanyak konsumsi air putih, memantau fungsi ginjal secara berkala (cek Ureum & Kreatinin), serta waspada terhadap tanda obstruksi saluran kemih yang memerlukan konsultasi dengan dokter spesialis urologi.', '2026-05-22 06:24:47'),
(8, 'P08', 'TBC Kulit (Skrofuloderma)', 'Infeksi TBC pada jaringan kulit yang umumnya terjadi akibat perluasan langsung dari infeksi kelenjar getah bening di bawahnya yang pecah. Kondisi ini ditandai dengan munculnya benjolan padat di kulit yang lambat laun melunak, pecah, dan membentuk luka terbuka/ulkus kronis yang sulit sembuh.', 'Pemberian regimen OAT Kategori 1 selama 6-9 bulan. Solusi lokal melibatkan perawatan luka (wound care) yang steril pada kulit yang pecah atau berulkus guna mencegah infeksi sekunder bakteri lain. Pasien harus menjaga higienitas area kulit yang terinfeksi dan menutup luka terbuka dengan kasa steril.', '2026-05-22 06:24:47'),
(9, 'P09', 'TBC Tulang dan Sendi (Spondilitis TB / Pott\'s Disease)', 'Kondisi di mana bakteri TBC menyebar dari paru-paru menuju ke sistem rangka tubuh. Area yang paling sering diserang adalah bagian tulang belakang (Pott\'s disease) atau sendi-sendi besar. Infeksi ini merusak struktur tulang, memicu nyeri hebat, dan bisa menyebabkan deformitas (kelainan bentuk punggung bungkuk) hingga kelumpuhan.', 'Terapi OAT jangka panjang dengan durasi total 9 hingga 12 bulan karena penetrasi obat ke jaringan tulang membutuhkan waktu lebih lama. Pasien diwajibkan melakukan tirah baring (bed rest) dengan alat bantu imobilisasi (seperti korset khusus tulang belakang) untuk menjaga kestabilan postur tulang. Pada kasus deformitas berat atau penekanan saraf saraf pusat, tindakan operasi ortopedi diperlukan.', '2026-05-22 06:24:47'),
(10, 'P10', 'TBC Laring (Menyerang pita suara/tenggorokan)', 'Bentuk TBC ekstra paru yang menyerang organ laring atau pita suara di tenggorokan. Penyakit ini biasanya terjadi akibat komplikasi dari TBC paru aktif akibat dahak yang mengandung kuman terus-menerus melewati pita suara. Ciri khasnya adalah suara pasien yang mendadak serak/parau dalam jangka waktu lama dan bersifat sangat menular.', 'Pengobatan menggunakan OAT Kategori 1 selama 6 bulan. Karena TBC Laring bersifat sangat menular melalui droplet udara saat berbicara atau batuk, isolasi ketat di awal pengobatan sangat krusial. Pasien disarankan mengistirahatkan pita suara (mengurangi berbicara), menghindari makanan/minuman yang memicu iritasi tenggorokan, serta selalu menggunakan masker medis.', '2026-05-22 06:24:47');

-- --------------------------------------------------------

--
-- Struktur dari tabel `riwayat_diagnosa`
--

CREATE TABLE `riwayat_diagnosa` (
  `id` int(11) NOT NULL,
  `id_pasien` int(11) NOT NULL,
  `gejala_dipilih` text NOT NULL COMMENT 'JSON array kode gejala',
  `hasil_diagnosa` text NOT NULL COMMENT 'JSON object {kode_penyakit: cf_value}',
  `diagnosa_utama` varchar(5) DEFAULT NULL,
  `cf_tertinggi` decimal(5,4) DEFAULT NULL,
  `waktu_diagnosa` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data untuk tabel `riwayat_diagnosa`
--

INSERT INTO `riwayat_diagnosa` (`id`, `id_pasien`, `gejala_dipilih`, `hasil_diagnosa`, `diagnosa_utama`, `cf_tertinggi`, `waktu_diagnosa`) VALUES
(2, 5, '[\"G16\", \"G07\", \"G11\"]', '{\"P11\": 0.9, \"P03\": 0.7, \"P08\": 0.7, \"P09\": 0.7, \"P13\": 0.7}', 'P11', 0.9000, '2026-05-04 14:23:29'),
(3, 6, '[\"G07\", \"G08\", \"G11\", \"G15\"]', '{\"P09\": 0.85, \"P04\": 0.8, \"P03\": 0.7, \"P08\": 0.7, \"P10\": 0.7}', 'P09', 0.8500, '2026-05-04 15:29:31'),
(4, 7, '[\"G20\", \"G18\", \"G10\"]', '{\"P12\": 0.9, \"P09\": 0.8, \"P04\": 0.7, \"P14\": 0.7, \"P10\": 0.6}', 'P12', 0.9000, '2026-05-05 15:01:11'),
(5, 8, '[\"G16\", \"G02\", \"G13\", \"G15\"]', '{\"P15\": 0.96, \"P01\": 0.9, \"P11\": 0.9, \"P07\": 0.8, \"P02\": 0.7}', 'P15', 0.9600, '2026-05-06 11:48:09'),
(6, 9, '[\"G05\", \"G16\", \"G15\"]', '{\"P11\": 0.95, \"P14\": 0.9, \"P04\": 0.5, \"P09\": 0.5, \"P06\": 0.4}', 'P11', 0.9500, '2026-05-09 18:06:08'),
(7, 10, '[\"G10\", \"G11\", \"G01\"]', '{\"P01\": 0.9, \"P04\": 0.9, \"P07\": 0.9, \"P03\": 0.8, \"P11\": 0.8}', 'P01', 0.9000, '2026-05-22 06:28:56'),
(8, 11, '[\"G09\", \"G10\", \"G19\"]', '{\"P04\": 0.99, \"P02\": 0.9, \"P14\": 0.7, \"P12\": 0.6, \"P15\": 0.5}', 'P04', 0.9900, '2026-05-22 08:52:56'),
(9, 12, '[\"G14\", \"G15\", \"G16\"]', '{\"P08\": 0.98, \"P07\": 0.8}', 'P08', 0.9800, '2026-05-23 05:47:33'),
(10, 13, '[\"G18\", \"G06\", \"G08\"]', '{\"P01\": 0.988, \"P03\": 0.96, \"P11\": 0.96, \"P12\": 0.952, \"P07\": 0.94}', 'P01', 0.9880, '2026-06-24 05:24:32'),
(11, 14, '[\"G20\", \"G07\", \"G08\", \"G14\"]', '{\"P07\": 0.982, \"P03\": 0.96, \"P01\": 0.91, \"P08\": 0.84, \"P04\": 0.75}', 'P07', 0.9820, '2026-07-09 06:24:24');

-- --------------------------------------------------------

--
-- Struktur dari tabel `rules`
--

CREATE TABLE `rules` (
  `id` int(11) NOT NULL,
  `kode_penyakit` varchar(5) NOT NULL,
  `kode_gejala` varchar(5) NOT NULL,
  `cf_pakar` decimal(4,2) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data untuk tabel `rules`
--

INSERT INTO `rules` (`id`, `kode_penyakit`, `kode_gejala`, `cf_pakar`, `created_at`) VALUES
(1, 'P01', 'G01', 0.90, '2026-05-22 06:24:47'),
(2, 'P01', 'G02', 0.80, '2026-05-22 06:24:47'),
(3, 'P01', 'G05', 0.80, '2026-05-22 06:24:47'),
(4, 'P01', 'G06', 0.90, '2026-05-22 06:24:47'),
(5, 'P01', 'G07', 0.70, '2026-05-22 06:24:47'),
(6, 'P01', 'G08', 0.70, '2026-05-22 06:24:47'),
(7, 'P01', 'G18', 0.60, '2026-05-22 06:24:47'),
(8, 'P02', 'G05', 0.50, '2026-05-22 06:24:47'),
(9, 'P02', 'G08', 0.40, '2026-05-22 06:24:47'),
(10, 'P02', 'G18', 0.70, '2026-05-22 06:24:47'),
(12, 'P03', 'G01', 0.80, '2026-05-22 06:24:47'),
(13, 'P03', 'G03', 0.70, '2026-05-22 06:24:47'),
(14, 'P03', 'G05', 0.80, '2026-05-22 06:24:47'),
(15, 'P03', 'G06', 0.80, '2026-05-22 06:24:47'),
(16, 'P03', 'G07', 0.80, '2026-05-22 06:24:47'),
(17, 'P03', 'G08', 0.80, '2026-05-22 06:24:47'),
(18, 'P04', 'G05', 0.60, '2026-05-22 06:24:47'),
(19, 'P04', 'G07', 0.50, '2026-05-22 06:24:47'),
(20, 'P04', 'G08', 0.50, '2026-05-22 06:24:47'),
(21, 'P04', 'G09', 0.90, '2026-05-22 06:24:47'),
(22, 'P04', 'G10', 0.90, '2026-05-22 06:24:47'),
(23, 'P05', 'G03', 0.90, '2026-05-22 06:24:47'),
(24, 'P05', 'G04', 0.80, '2026-05-22 06:24:47'),
(25, 'P05', 'G05', 0.70, '2026-05-22 06:24:47'),
(26, 'P05', 'G06', 0.60, '2026-05-22 06:24:47'),
(27, 'P05', 'G07', 0.60, '2026-05-22 06:24:47'),
(28, 'P06', 'G04', 0.60, '2026-05-22 06:24:47'),
(29, 'P06', 'G07', 0.50, '2026-05-22 06:24:47'),
(30, 'P06', 'G08', 0.50, '2026-05-22 06:24:47'),
(31, 'P07', 'G05', 0.70, '2026-05-22 06:24:47'),
(32, 'P07', 'G06', 0.80, '2026-05-22 06:24:47'),
(33, 'P07', 'G07', 0.70, '2026-05-22 06:24:47'),
(34, 'P07', 'G08', 0.70, '2026-05-22 06:24:47'),
(35, 'P07', 'G11', 0.90, '2026-05-22 06:24:47'),
(36, 'P07', 'G12', 0.90, '2026-05-22 06:24:47'),
(37, 'P07', 'G13', 0.80, '2026-05-22 06:24:47'),
(38, 'P07', 'G14', 0.80, '2026-05-22 06:24:47'),
(39, 'P08', 'G07', 0.60, '2026-05-22 06:24:47'),
(40, 'P08', 'G08', 0.60, '2026-05-22 06:24:47'),
(41, 'P08', 'G15', 0.90, '2026-05-22 06:24:47'),
(42, 'P08', 'G16', 0.80, '2026-05-22 06:24:47'),
(43, 'P08', 'G17', 0.70, '2026-05-22 06:24:47'),
(44, 'P09', 'G05', 0.50, '2026-05-22 06:24:47'),
(45, 'P09', 'G07', 0.50, '2026-05-22 06:24:47'),
(46, 'P09', 'G08', 0.50, '2026-05-22 06:24:47'),
(47, 'P10', 'G03', 0.70, '2026-05-22 06:24:47'),
(48, 'P10', 'G04', 0.80, '2026-05-22 06:24:47'),
(49, 'P10', 'G05', 0.70, '2026-05-22 06:24:47'),
(50, 'P10', 'G06', 0.70, '2026-05-22 06:24:47'),
(51, 'P10', 'G07', 0.60, '2026-05-22 06:24:47'),
(52, 'P11', 'G01', 0.80, '2026-05-22 06:24:47'),
(53, 'P11', 'G02', 0.70, '2026-05-22 06:24:47'),
(54, 'P11', 'G05', 0.70, '2026-05-22 06:24:47'),
(55, 'P11', 'G06', 0.80, '2026-05-22 06:24:47'),
(56, 'P11', 'G07', 0.70, '2026-05-22 06:24:47'),
(57, 'P11', 'G08', 0.80, '2026-05-22 06:24:47'),
(58, 'P11', 'G20', 0.90, '2026-05-22 06:24:47'),
(59, 'P12', 'G01', 0.70, '2026-05-22 06:24:47'),
(60, 'P12', 'G05', 0.70, '2026-05-22 06:24:47'),
(61, 'P12', 'G06', 0.70, '2026-05-22 06:24:47'),
(62, 'P12', 'G07', 0.60, '2026-05-22 06:24:47'),
(63, 'P12', 'G08', 0.60, '2026-05-22 06:24:47'),
(64, 'P12', 'G09', 0.60, '2026-05-22 06:24:47'),
(65, 'P12', 'G18', 0.60, '2026-05-22 06:24:47'),
(66, 'P13', 'G01', 0.60, '2026-05-22 06:24:47'),
(67, 'P13', 'G03', 0.60, '2026-05-22 06:24:47'),
(68, 'P13', 'G05', 0.70, '2026-05-22 06:24:47'),
(69, 'P13', 'G07', 0.70, '2026-05-22 06:24:47'),
(70, 'P13', 'G08', 0.70, '2026-05-22 06:24:47'),
(71, 'P13', 'G18', 0.50, '2026-05-22 06:24:47'),
(72, 'P14', 'G01', 0.80, '2026-05-22 06:24:47'),
(73, 'P14', 'G03', 0.70, '2026-05-22 06:24:47'),
(74, 'P14', 'G05', 0.80, '2026-05-22 06:24:47'),
(75, 'P14', 'G07', 0.80, '2026-05-22 06:24:47'),
(76, 'P14', 'G08', 0.80, '2026-05-22 06:24:47'),
(77, 'P14', 'G09', 0.70, '2026-05-22 06:24:47'),
(78, 'P14', 'G18', 0.70, '2026-05-22 06:24:47'),
(79, 'P15', 'G05', 0.60, '2026-05-22 06:24:47'),
(80, 'P15', 'G07', 0.50, '2026-05-22 06:24:47'),
(81, 'P15', 'G08', 0.60, '2026-05-22 06:24:47'),
(82, 'P15', 'G09', 0.50, '2026-05-22 06:24:47'),
(83, 'P15', 'G18', 0.60, '2026-05-22 06:24:47');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `gejala`
--
ALTER TABLE `gejala`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `kode` (`kode`);

--
-- Indeks untuk tabel `pasien`
--
ALTER TABLE `pasien`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `penyakit`
--
ALTER TABLE `penyakit`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `kode` (`kode`);

--
-- Indeks untuk tabel `riwayat_diagnosa`
--
ALTER TABLE `riwayat_diagnosa`
  ADD PRIMARY KEY (`id`),
  ADD KEY `diagnosa_utama` (`diagnosa_utama`),
  ADD KEY `fk_riwayat_pasien` (`id_pasien`);

--
-- Indeks untuk tabel `rules`
--
ALTER TABLE `rules`
  ADD PRIMARY KEY (`id`),
  ADD KEY `kode_penyakit` (`kode_penyakit`),
  ADD KEY `kode_gejala` (`kode_gejala`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `gejala`
--
ALTER TABLE `gejala`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT untuk tabel `pasien`
--
ALTER TABLE `pasien`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT untuk tabel `penyakit`
--
ALTER TABLE `penyakit`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT untuk tabel `riwayat_diagnosa`
--
ALTER TABLE `riwayat_diagnosa`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT untuk tabel `rules`
--
ALTER TABLE `rules`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=84;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `riwayat_diagnosa`
--
ALTER TABLE `riwayat_diagnosa`
  ADD CONSTRAINT `fk_riwayat_pasien` FOREIGN KEY (`id_pasien`) REFERENCES `pasien` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `riwayat_diagnosa_ibfk_2` FOREIGN KEY (`diagnosa_utama`) REFERENCES `penyakit` (`kode`) ON DELETE SET NULL;

--
-- Ketidakleluasaan untuk tabel `rules`
--
ALTER TABLE `rules`
  ADD CONSTRAINT `rules_ibfk_1` FOREIGN KEY (`kode_penyakit`) REFERENCES `penyakit` (`kode`),
  ADD CONSTRAINT `rules_ibfk_2` FOREIGN KEY (`kode_gejala`) REFERENCES `gejala` (`kode`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
