from app import app, db
from flask import request, jsonify
from app.models.dokumen_model import DataDokumen

@app.route("/data-dokumen", methods=["POST", "GET"])
def data_dokumens():
    if request.method == "POST":
        id = request.json["id"]
        nip = request.json["nip"]
        type_dokumen = request.json["type_dokumen"]
        nama_dokumen = request.json["nama_dokumen"]
        nama_file = request.json["nama_file"]

        if type_dokumen != "file" and type_dokumen != "url":
            return jsonify({"message": "Tipe dokumen harus file atau url"})

        new_datadokumen = DataDokumen(id=id, nip=nip, type_dokumen=type_dokumen, nama_dokumen=nama_dokumen, nama_file=nama_file)
        db.session.add(new_datadokumen)
        db.session.commit()

        return jsonify({"message": "Data Dokumen berhasil ditambahkan"})
    
    if request.method == "GET":
        datadokumen = DataDokumen.query.all()
        print(datadokumen)
        datadokumen_list = []
        for dokumen in datadokumen:
            datadokumen_list.append({
                "id": dokumen.id,
                "nip": dokumen.nip,
                "type_dokumen": dokumen.type_dokumen,
                "nama_dokumen": dokumen.nama_dokumen,
                "nama_file": dokumen.nama_file,
            })
        return jsonify(datadokumen_list)
    
@app.route("/data-dokumen/<id>", methods=["GET", "PUT", "DELETE"])
def data_dokumen(id):
    datadokumen = DataDokumen.query.get_or_404(id)

    if request.method == "GET":
        return jsonify({
                "id": datadokumen.id,
                "nip": datadokumen.nip,
                "type_dokumen": datadokumen.type_dokumen,
                "nama_dokumen": datadokumen.nama_dokumen,
                "nama_file": datadokumen.nama_file,
        })
    
    if request.method == "PUT":
        datadokumen.id = request.json["id"]
        datadokumen.nip = request.json["nip"]
        datadokumen.type_dokumen = request.json["type_dokumen"]
        datadokumen.nama_dokumen = request.json["nama_dokumen"]
        datadokumen.nama_file = request.json["nama_file"]

        if datadokumen.type_dokumen != "file" and datadokumen.type_dokumen != "url":
            return jsonify({"message": "Tipe dokumen harus file atau url"})

        db.session.commit()
        return jsonify({"message": "Data Dokumen berhasil diperbarui"})
    
    if request.method == "DELETE":
        db.session.delete(datadokumen)
        db.session.commit()
        return jsonify({"message": "Data Dokumen berhasil dihapus"})
