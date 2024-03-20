from app import db

class Prodi_Model(db.Model):
    __tablename__ = "data_prodi"

    id = db.Column(db.Integer, primary_key=True)
    kode_prodi = db.Column(db.String(5))
    nama_prodi = db.Column(db.String(100))

    def __init__(self, id, kode_prodi, nama_prodi):
        self.id = id
        self.kode_prodi = kode_prodi
        self.nama_prodi = nama_prodi
