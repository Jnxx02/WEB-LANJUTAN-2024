from app import db

class Dosen_Model(db.Model):
    __tablename__ = "data_dosen"

    nip = db.Column(db.String(30), primary_key=True)
    nama_lengkap = db.Column(db.String(100))
    prodi_id = db.Column(db.String(5))

    def __init__(self, nip, nama_lengkap, prodi_id):
        self.nip = nip
        self.nama_lengkap = nama_lengkap
        self.prodi_id = prodi_id
