from app import app, db
from flask import request, jsonify
from app.models.dosen_model import Dosen_Model
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


@app.route("/login", methods=["POST"])
def login():
    nama_lengkap = request.json["nama_lengkap"]
    nip = request.json["nip"]

    data_dosen = Dosen_Model.query.filter_by(nip=nip, nama_lengkap=nama_lengkap).first()

    if data_dosen is None:
        return jsonify({"message": "Data dosen tidak ditemukan"}), 401

    access_token = create_access_token(identity=nip)
    return jsonify({"message": "Login berhasil", "access_token": access_token}), 200


@app.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200