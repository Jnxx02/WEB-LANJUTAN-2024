from app import app, db
from flask import request, jsonify
from app.models.DataProdi import DataProdi

@app.route("/data-prodi", methods=["POST", "GET"])
def data_prodis():
    if request.method == "POST":
        id = request.json["id"]
        kode_prodi = request.json["kode_prodi"]
        nama_prodi = request.json["nama_prodi"]

        new_dataprodi = DataProdi(id=id, kode_prodi=kode_prodi, nama_prodi=nama_prodi)
        db.session.add(new_dataprodi)
        db.session.commit()

        return jsonify({"message": "Data Prodi berhasil ditambahkan"})
    
    if request.method == "GET":
        dataprodi = DataProdi.query.all()
        print(dataprodi)
        dataprodi_list = []
        for prodi in dataprodi:
            dataprodi_list.append({
                "id": prodi.id,
                "kode_prodi": prodi.kode_prodi,
                "nama_prodi": prodi.nama_prodi
            })
        return jsonify(dataprodi_list)
    
@app.route("/data-prodi/<id>", methods=["GET", "PUT", "DELETE"])
def data_prodi(id):
    dataprodi = DataProdi.query.get_or_404(id)

    if request.method == "GET":
        return jsonify({
            "id": dataprodi.id,
            "kode_prodi": dataprodi.kode_prodi,
            "nama_prodi": dataprodi.nama_prodi
        })
    
    if request.method == "PUT":
        dataprodi.id = request.json["id"]
        dataprodi.kode_prodi = request.json["kode_prodi"]
        dataprodi.nama_prodi = request.json["nama_prodi"]
        db.session.commit()
        return jsonify({"message": "Data Prodi berhasil diperbarui"})
    
    if request.method == "DELETE":
        db.session.delete(dataprodi)
        db.session.commit()
        return jsonify({"message": "Data Prodi berhasil dihapus"})
