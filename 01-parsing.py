import re

response = """
### [Tujuan Pembelajaran]

1. Mendefinisikan dan menjelaskan konsep dasar Reliability-Centered Maintenance (RCM) serta pentingnya dalam operasi PLN Persero.
2. Mengidentifikasi dan menggambarkan langkah-langkah dalam proses RCM, termasuk analisis fungsional dan analisis mode kegagalan dan efek (FMEA).
3. Menjelaskan bagaimana RCM dapat meningkatkan perencanaan pemeliharaan, termasuk manajemen persediaan suku cadang dan program pelatihan karyawan.
4. Menguraikan manfaat implementasi RCM, termasuk pengelolaan sumber daya yang lebih baik dan pemahaman yang lebih dalam tentang kinerja aset.
5. Menganalisis contoh dan studi kasus RCM dari industri lain untuk memahami aplikasi praktisnya dan hasil yang dapat dicapai.
6. Diskusikan tantangan dan arah masa depan adopsi RCM di PLN Persero, serta bagaimana teknologi terbaru dapat berperan dalam pengembangan strategi pemeliharaan.

### [Usulan Durasi Waktu]

**Metodologi Pengiriman**: Kombinasi antara pengajaran langsung (ceramah), diskusi kelompok kolaboratif, dan kegiatan berbasis inkuiri (analisis studi kasus).

**Durasi yang Disarankan**:

- **Pengantar dan Definisi RCM**: 15 menit
- **Langkah-langkah dalam Proses RCM**: 25 menit
- **Peningkatan Perencanaan Pemeliharaan**: 20 menit
- **Manfaat Implementasi RCM**: 20 menit
- **Contoh dan Studi Kasus**: 30 menit
- **Diskusi Tantangan dan Arah Masa Depan**: 20 menit
- **Sesi Tanya Jawab**: 10 menit

**Durasi Total**: 150 menit

### [Identifikasi Kriteria Penilaian]

1. **Pemahaman Konsep RCM**: Kemampuan siswa mendefinisikan RCM dan menjelaskan langkah-langkah dalam prosesnya dengan jelas.
2. **Aplikasi Langkah RCM**: Kemampuan siswa mengidentifikasi dan menjelaskan bagaimana RCM dapat diterapkan dalam konteks PLN Persero, termasuk analisis fungsional dan FMEA.
3. **Analisis Kasus Nyata**: Keterampilan siswa dalam menganalisis studi kasus terkait implementasi RCM dan hasilnya, serta kemampuan untuk merumuskan pelajaran yang dipetik.
4. **Diskusi Kritis**: Kemampuan siswa untuk mendiskusikan tantangan implementasi RCM dan memberikan solusi berdasarkan pemahaman yang diperoleh selama pembelajaran.
5. **Kemampuan Kolaboratif**: Keterlibatan siswa dalam diskusi kelompok dan kemampuan untuk bekerja sama dalam menjawab pertanyaan-pertanyaan yang muncul selama sesi.

Dengan modul ini, diharapkan para pengajar dapat mengajarkan pentingnya RCM secara efektif dan siswa dapat memahami, menerapkan, dan menganalisis konsep-konsep yang diajarkan dengan baik.
"""

# Correctly parse each section
learn_objective = re.search(r'\[Tujuan Pembelajaran\]\n\n(.*?)(?=\n###|\Z)', response, re.DOTALL)
if learn_objective:
    learn_objective_content = learn_objective.group(1).strip()
else:
    learn_objective_content = None

method = re.search(r'\[Usulan Durasi Waktu\]\n\n(.*?)(?=\*\*Durasi Total\*\*|\n###|\Z)', response, re.DOTALL)
if method:
    method_content = method.group(1).strip()
else:
    method_content = None

# Adjust assessment regex to capture only numbered items
assessment = re.search(r'\[Identifikasi Kriteria Penilaian\]\n\n((?:\d+\..*?)(?=\n\S|\Z))', response, re.DOTALL)
if assessment:
    assessment_content = assessment.group(1).strip()
else:
    assessment_content = None

duration_match = re.search(r'\*\*Durasi Total\*\*:\s*(\d+)\s*menit', response)
if duration_match:
    duration = int(duration_match.group(1))
else:
    duration = None

# Print the results
print("Learning Objectives:\n", learn_objective_content)
print("\nMethod:\n", method_content)
print("\nAssessment:\n", assessment_content)
print("\nDuration:\n", duration)