"""Kelas Mahasiswa: menyimpan identitas dan kehadiran."""

class Mahasiswa:
    """Representasi mahasiswa dengan data NIM, nama, dan persentase hadir."""

    def __init__(self, nim, nama, hadir_persen=0):
        self.nim = nim
        self.nama = nama
        self._hadir_persen = 0
        self.hadir_persen = hadir_persen

    @property
    def hadir_persen(self):
        return self._hadir_persen

    @hadir_persen.setter
    def hadir_persen(self, value):
        try:
            v = float(value)
        except ValueError:
            raise ValueError("Nilai hadir harus berupa angka.")
        if not 0 <= v <= 100:
            raise ValueError("Persentase hadir harus antara 0-100.")
        self._hadir_persen = v

    def info(self):
        return f"{self.nim} - {self.nama} (Hadir: {self.hadir_persen}%)"
