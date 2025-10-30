"""Jalankan langsung paket dengan `python -m tracker`."""
from tracker import RekapKelas, build_markdown_report, save_text
import os

def main():
    print("=== Menjalankan student_performance_tracker ===")
    rk = RekapKelas()
    rk.tambah_mahasiswa("230101001", "Ana", 95)
    rk.set_penilaian("230101001", quiz=90, tugas=85, uts=88, uas=92)
    records = rk.rekap()
    os.makedirs("out", exist_ok=True)
    save_text("out/report.md", build_markdown_report(records))
    print("File out/report.md berhasil dibuat otomatis.")

if __name__ == "__main__":
    main()
