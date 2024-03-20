from app import db
from sqlalchemy import Enum

class Dokumen_Model(db.Model):
    __tablename__ = "data_dokumen"

    id = db.Column(db.Integer, primary_key=True)
    nip = db.Column(db.String(30))
    type_dokumen = db.Column(Enum("file", "url"))
    nama_dokumen = db.Column(db.String(255))
    nama_file = db.Column(db.String(255))

    def __init__(self, id, nip, type_dokumen, nama_dokumen, nama_file):
        self.id = id
        self.nip = nip
        self.type_dokumen = type_dokumen
        self.nama_dokumen = nama_dokumen
        self.nama_file = nama_file
