"""Kelas RekapKelas: menyimpan daftar mahasiswa dan nilai."""

from .mahasiswa import Mahasiswa
from .penilaian import Penilaian

class RekapKelas:
    """Mengelola daftar mahasiswa, kehadiran, dan nilai."""

    def __init__(self):
        self._data = {}

    def tambah_mahasiswa(self, nim, nama, hadir_persen=0):
        if nim in self._data:
            raise ValueError(f"Mahasiswa {nim} sudah terdaftar.")
        m = Mahasiswa(nim, nama, hadir_persen)
        p = Penilaian()
        self._data[nim] = {"mhs": m, "nilai": p}

    def set_hadir(self, nim, hadir_persen):
        if nim not in self._data:
            raise KeyError("NIM tidak ditemukan.")
        self._data[nim]["mhs"].hadir_persen = hadir_persen

    def set_penilaian(self, nim, quiz=None, tugas=None, uts=None, uas=None):
        if nim not in self._data:
            raise KeyError("NIM tidak ditemukan.")
        pen = self._data[nim]["nilai"]
        if quiz is not None: pen.quiz = quiz
        if tugas is not None: pen.tugas = tugas
        if uts is not None: pen.uts = uts
        if uas is not None: pen.uas = uas

    def rekap(self):
        records = []
        for nim, d in sorted(self._data.items()):
            m, p = d["mhs"], d["nilai"]
            nilai_akhir = round(p.nilai_akhir(), 2)
            records.append({
                "nim": nim,
                "nama": m.nama,
                "hadir": m.hadir_persen,
                "nilai_akhir": nilai_akhir,
                "predikat": self.predikat(nilai_akhir)
            })
        return records

    def predikat(self, n):
        n = float(n)
        if n >= 85: return "A"
        elif n >= 70: return "B"
        elif n >= 60: return "C"
        elif n >= 40: return "D"
        else: return "E"

    def load_attendance_csv(self, path):
        import csv
        with open(path, newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                nim = row.get("nim") or row.get("NIM")
                if not nim: continue
                nama = row.get("nama") or ""
                hadir = row.get("hadir_persen") or 0
                if nim not in self._data:
                    self.tambah_mahasiswa(nim, nama, hadir)
                else:
                    self.set_hadir(nim, hadir)

    def load_grades_csv(self, path):
        import csv
        with open(path, newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                nim = row.get("nim") or row.get("NIM")
                if not nim: continue
                if nim not in self._data:
                    self.tambah_mahasiswa(nim, "(unknown)", 0)
                self.set_penilaian(
                    nim,
                    quiz=row.get("quiz") or 0,
                    tugas=row.get("tugas") or 0,
                    uts=row.get("uts") or 0,
                    uas=row.get("uas") or 0,
                )
