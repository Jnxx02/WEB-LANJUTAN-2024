from fastapi import Depends, FastAPI, HTTPException, Path
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
import mysql.connector

# Inisialisasi koneksi ke database
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    database="db_repositori"
)
mycursor = mydb.cursor()

# Model Pydantic untuk entitas Data Prodi
class Prodi_Model(BaseModel):
    kode_prodi: str
    nama_prodi: str

# Model Pydantic untuk entitas Data Dosen
class Dosen_Model(BaseModel):
    nip: str
    nama_lengkap: str
    prodi_id: int

# Model Pydantic untuk entitas Data Dokumen
class Dokumen_Model(BaseModel):
    nip: str
    type_dokumen: str
    nama_dokumen: str
    nama_file: str

# Model Pydantic untuk login
class Login(BaseModel):
    username: str
    password: str

# Konfigurasi autentikasi JWT
SECRET_KEY = "12345"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Fungsi untuk pembuatan token JWT
def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Fungsi untuk memeriksa token JWT
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token sudah kedaluwarsa
    except jwt.InvalidTokenError:
        return None  # Token tidak valid

# Inisialisasi aplikasi FastAPI
app = FastAPI()

# Decorator untuk memeriksa token JWT
def authenticate_user(token: str = Depends(decode_token)):
    if token is None:
        raise HTTPException(status_code=401, detail="Token tidak valid")
    return token

#login dan pembuatan token JWT
@app.post("/login/")
async def login(login_data: Login):
    if login_data.username == "admin" and login_data.password == "123":
        access_token = create_access_token(data={"sub": login_data.username})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Username atau password salah")

# CRUD Data Prodi
@app.post("/data-prodi/")
async def create_prodi(data_prodi: Prodi_Model, token: dict = Depends(authenticate_user)):
    sql = "INSERT INTO data_prodi (kode_prodi, nama_prodi) VALUES (%s, %s)"
    val = (data_prodi.kode_prodi, data_prodi.nama_prodi)
    mycursor.execute(sql, val)
    mydb.commit()
    return {"message": "Data Prodi telah ditambahkan"}

@app.get("/data-prodi/{prodi_id}")
async def read_prodi(prodi_id: int):
    mycursor.execute("SELECT * FROM data_prodi WHERE id = %s", (prodi_id,))
    result = mycursor.fetchone()
    if result:
        return {"id": result[0], "kode_prodi": result[1], "nama_prodi": result[2]}
    else:
        raise HTTPException(status_code=404, detail="Prodi not found")

@app.put("/data-prodi/{prodi_id}")
async def update_prodi(prodi_id: int, data_prodi: Prodi_Model, token: dict = Depends(authenticate_user)):
    sql = "UPDATE data_prodi SET kode_prodi = %s, nama_prodi = %s WHERE id = %s"
    val = (data_prodi.kode_prodi, data_prodi.nama_prodi, prodi_id)
    mycursor.execute(sql, val)
    mydb.commit()
    return {"message": "Data Prodi telah diperbarui"}

@app.delete("/data-prodi/{prodi_id}")
async def delete_prodi(prodi_id: int, token: dict = Depends(authenticate_user)):
    mycursor.execute("DELETE FROM data_prodi WHERE id = %s", (prodi_id,))
    mydb.commit()
    return {"message": "Data Prodi telah dihapus"}

# CRUD Data Dosen
@app.post("/data-dosen/")
async def create_dosen(data_dosen: Dosen_Model, token: dict = Depends(authenticate_user)):
    sql = "INSERT INTO data_dosen (nip, nama_lengkap, prodi_id) VALUES (%s, %s, %s)"
    val = (data_dosen.nip, data_dosen.nama_lengkap, data_dosen.prodi_id)
    mycursor.execute(sql, val)
    mydb.commit()
    return {"message": "Data Dosen telah ditambahkan"}

@app.get("/data-dosen/{nip}")
async def read_dosen(nip: str):
    mycursor.execute("SELECT * FROM data_dosen WHERE nip = %s", (nip,))
    result = mycursor.fetchone()
    if result:
        return {"nip": result[0], "nama_lengkap": result[1], "prodi_id": result[2]}
    else:
        raise HTTPException(status_code=404, detail="Dosen not found")

@app.put("/data-dosen/{nip}")
async def update_dosen(nip: str, data_dosen: Dosen_Model, token: dict = Depends(authenticate_user)):
    sql = "UPDATE data_dosen SET nip = %s,nama_lengkap = %s, prodi_id = %s WHERE nip = %s"
    val = (data_dosen.nip,data_dosen.nama_lengkap, data_dosen.prodi_id, nip)
    mycursor.execute(sql, val)
    mydb.commit()
    return {"message": "Data Dosen telah diperbarui"}

@app.delete("/data-dosen/{nip}")
async def delete_dosen(nip: str, token: dict = Depends(authenticate_user)):
    mycursor.execute("DELETE FROM data_dosen WHERE nip = %s", (nip,))
    mydb.commit()
    return {"message": "Data Dosen telah dihapus"}

# CRUD Data Dokumen
@app.post("/data-dokumen/")
async def create_dokumen(data_dokumen: Dokumen_Model, token: dict = Depends(authenticate_user)):
    sql = "INSERT INTO data_dokumen (nip, type_dokumen, nama_dokumen, nama_file) VALUES (%s, %s, %s, %s)"
    val = (data_dokumen.nip, data_dokumen.type_dokumen, data_dokumen.nama_dokumen, data_dokumen.nama_file)
    mycursor.execute(sql, val)
    mydb.commit()
    return {"message": "Data Dokumen telah ditambahkan"}

@app.get("/data-dokumen/{dokumen_id}")
async def read_dokumen(dokumen_id: int):
    mycursor.execute("SELECT * FROM data_dokumen WHERE id = %s", (dokumen_id,))
    result = mycursor.fetchone()
    if result:
        return {
            "id": result[0],
            "nip": result[1],
            "type_dokumen": result[2],
            "nama_dokumen": result[3],
            "nama_file": result[4]
        }
    else:
        raise HTTPException(status_code=404, detail="Dokumen not found")

@app.put("/data-dokumen/{dokumen_id}")
async def update_dokumen(dokumen_id: int, data_dokumen: Dokumen_Model, token: dict = Depends(authenticate_user)):
    sql = "UPDATE data_dokumen SET nip = %s,type_dokumen = %s, nama_dokumen = %s, nama_file = %s WHERE id = %s"
    val = (data_dokumen.nip,data_dokumen.type_dokumen, data_dokumen.nama_dokumen, data_dokumen.nama_file, dokumen_id)
    mycursor.execute(sql, val)
    mydb.commit()
    return {"message": "Data Dokumen telah diperbarui"}

@app.delete("/data-dokumen/{dokumen_id}")
async def delete_dokumen(dokumen_id: int, token: dict = Depends(authenticate_user)):
    mycursor.execute("DELETE FROM data_dokumen WHERE id = %s", (dokumen_id,))
    mydb.commit()
    return {"message": "Data Dokumen telah dihapus"}