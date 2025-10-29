"""App CLI untuk Student Performance Tracker."""

import os
from tracker import RekapKelas, build_markdown_report, save_text

DATA_DIR = "data"
OUT_DIR = "out"
ATTENDANCE_CSV = os.path.join(DATA_DIR, "attendance.csv")
GRADES_CSV = os.path.join(DATA_DIR, "grades.csv")
OUT_REPORT = os.path.join(OUT_DIR, "report.md")

def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(OUT_DIR, exist_ok=True)

def print_menu():
    print("\n=== Student Performance Tracker ===")
    print("1) Muat data dari CSV")
    print("2) Tambah mahasiswa")
    print("3) Ubah presensi")
    print("4) Ubah nilai")
    print("5) Lihat rekap")
    print("6) Simpan laporan Markdown")
    print("7) Keluar")

def input_non_empty(prompt):
    while True:
        v = input(prompt).strip()
        if v:
            return v

def main():
    ensure_dirs()
    rk = RekapKelas()

    while True:
        print_menu()
        pilih = input("Pilih menu: ").strip()

        if pilih == "1":
            print("Memuat data dari CSV...")
            if os.path.exists(ATTENDANCE_CSV):
                rk.load_attendance_csv(ATTENDANCE_CSV)
                print(" - attendance.csv dimuat.")
            if os.path.exists(GRADES_CSV):
                rk.load_grades_csv(GRADES_CSV)
                print(" - grades.csv dimuat.")
            if not os.path.exists(ATTENDANCE_CSV) and not os.path.exists(GRADES_CSV):
                print("Tidak ada file CSV di folder data/")

        elif pilih == "2":
            nim = input_non_empty("Masukkan NIM: ")
            nama = input_non_empty("Masukkan Nama: ")
            hadir = input("Persentase hadir (0-100): ").strip() or "0"
            try:
                rk.tambah_mahasiswa(nim, nama, hadir)
                print("Mahasiswa berhasil ditambahkan.")
            except Exception as e:
                print("Error:", e)

        elif pilih == "3":
            nim = input_non_empty("Masukkan NIM: ")
            hadir = input_non_empty("Persentase hadir baru: ")
            try:
                rk.set_hadir(nim, hadir)
                print("Presensi berhasil diperbarui.")
            except Exception as e:
                print("Error:", e)

        elif pilih == "4":
            nim = input_non_empty("Masukkan NIM: ")
            print("Kosongkan jika tidak ingin mengubah kolom tertentu.")
            quiz = input("Nilai quiz: ").strip() or None
            tugas = input("Nilai tugas: ").strip() or None
            uts = input("Nilai UTS: ").strip() or None
            uas = input("Nilai UAS: ").strip() or None
            try:
                rk.set_penilaian(nim, quiz=quiz, tugas=tugas, uts=uts, uas=uas)
                print("Nilai berhasil diperbarui.")
            except Exception as e:
                print("Error:", e)

        elif pilih == "5":
            records = rk.rekap()
            if not records:
                print("Belum ada data mahasiswa.")
            else:
                print("\n| NIM | Nama | Hadir (%) | Nilai Akhir | Predikat |")
                print("|---|---|---:|---:|:---:|")
                for r in records:
                    print(f"| {r['nim']} | {r['nama']} | {r['hadir']:.1f} | {r['nilai_akhir']:.2f} | {r['predikat']} |")

        elif pilih == "6":
            records = rk.rekap()
            content = build_markdown_report(records)
            save_text(OUT_REPORT, content)
            print(f"Laporan disimpan di {OUT_REPORT}")

        elif pilih == "7":
            print("Keluar dari aplikasi.")
            break

        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()
