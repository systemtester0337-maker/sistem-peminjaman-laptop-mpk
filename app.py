import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify

# Muat turun pembolehubah persekitaran daripada fail .env sekiranya wujud
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import database

app = Flask(__name__)

# Konfigurasi Keselamatan Pengeluaran (Production Security)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sppl-mpk-secret-key-production-2026')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1')

# Mulakan pangkalan data semasa aplikasi dimulakan
database.init_db()

@app.route('/')
def index():
    """Halaman utama sistem peminjaman laptop MPK."""
    return render_template('index.html')

@app.route('/health')
def health():
    """Endpoint pemeriksaan kesihatan (health check) untuk platform hosting."""
    return jsonify({"status": "healthy", "service": "Sistem Pengurusan Peminjaman Laptop MPK"}), 200

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Mendapatkan statistik ringkasan untuk paparan papan pemuka."""
    try:
        stats = database.get_dashboard_stats()
        return jsonify({"success": True, "data": stats})
    except Exception as e:
        return jsonify({"success": False, "message": f"Ralat mendapatkan statistik: {str(e)}"}), 500

@app.route('/api/records', methods=['GET'])
def list_records():
    """Mendapatkan senarai rekod peminjaman dengan sokongan carian dan tapisan tarikh."""
    search = request.args.get('search', '').strip()
    date_filter = request.args.get('date', '').strip()
    try:
        records = database.get_all_records(search=search, date_filter=date_filter)
        return jsonify({
            "success": True,
            "count": len(records),
            "records": records
        })
    except Exception as e:
        return jsonify({"success": False, "message": f"Ralat memuatkan rekod: {str(e)}"}), 500

@app.route('/api/records/<int:record_id>', methods=['GET'])
def get_record(record_id):
    """Mendapatkan butiran satu rekod peminjaman."""
    try:
        record = database.get_record_by_id(record_id)
        if not record:
            return jsonify({"success": False, "message": "Rekod tidak dijumpai."}), 404
        return jsonify({"success": True, "record": record})
    except Exception as e:
        return jsonify({"success": False, "message": f"Ralat mendapatkan rekod: {str(e)}"}), 500

@app.route('/api/records', methods=['POST'])
def add_record():
    """Mendaftar permohonan peminjaman laptop baharu."""
    data = request.get_json() or {}
    nama_laptop = data.get('nama_laptop', '').strip()
    nama_jabatan = data.get('nama_jabatan', '').strip()
    tarikh_peminjaman = data.get('tarikh_peminjaman', '').strip()
    tujuan = data.get('tujuan', '').strip()

    # Pengesahan medan wajib (Validation)
    if not nama_laptop:
        return jsonify({"success": False, "message": "Sila masukkan Nama Laptop."}), 400
    if not nama_jabatan:
        return jsonify({"success": False, "message": "Sila masukkan Nama Jabatan."}), 400
    if not tarikh_peminjaman:
        return jsonify({"success": False, "message": "Sila pilih Tarikh Peminjaman."}), 400
    if not tujuan:
        return jsonify({"success": False, "message": "Sila nyatakan Tujuan peminjaman."}), 400

    # Sahkan format tarikh (YYYY-MM-DD)
    try:
        datetime.strptime(tarikh_peminjaman, "%Y-%m-%d")
    except ValueError:
        return jsonify({"success": False, "message": "Format tarikh tidak sah. Sila gunakan format YYYY-MM-DD."}), 400

    try:
        record = database.create_record(nama_laptop, nama_jabatan, tarikh_peminjaman, tujuan)
        return jsonify({
            "success": True,
            "message": "Rekod peminjaman berjaya ditambah.",
            "record": record
        }), 201
    except Exception as e:
        return jsonify({"success": False, "message": f"Ralat menyimpan rekod: {str(e)}"}), 500

@app.route('/api/records/<int:record_id>', methods=['PUT'])
def update_record(record_id):
    """Mengemaskini rekod peminjaman sedia ada."""
    existing = database.get_record_by_id(record_id)
    if not existing:
        return jsonify({"success": False, "message": "Rekod tidak dijumpai."}), 404

    data = request.get_json() or {}
    nama_laptop = data.get('nama_laptop', '').strip()
    nama_jabatan = data.get('nama_jabatan', '').strip()
    tarikh_peminjaman = data.get('tarikh_peminjaman', '').strip()
    tujuan = data.get('tujuan', '').strip()

    # Pengesahan medan wajib
    if not nama_laptop:
        return jsonify({"success": False, "message": "Sila masukkan Nama Laptop."}), 400
    if not nama_jabatan:
        return jsonify({"success": False, "message": "Sila masukkan Nama Jabatan."}), 400
    if not tarikh_peminjaman:
        return jsonify({"success": False, "message": "Sila pilih Tarikh Peminjaman."}), 400
    if not tujuan:
        return jsonify({"success": False, "message": "Sila nyatakan Tujuan peminjaman."}), 400

    try:
        datetime.strptime(tarikh_peminjaman, "%Y-%m-%d")
    except ValueError:
        return jsonify({"success": False, "message": "Format tarikh tidak sah. Sila gunakan format YYYY-MM-DD."}), 400

    try:
        updated = database.update_record(record_id, nama_laptop, nama_jabatan, tarikh_peminjaman, tujuan)
        return jsonify({
            "success": True,
            "message": "Rekod peminjaman berjaya dikemaskini.",
            "record": updated
        })
    except Exception as e:
        return jsonify({"success": False, "message": f"Ralat mengemaskini rekod: {str(e)}"}), 500

@app.route('/api/records/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    """Memadam rekod peminjaman mengikut ID."""
    existing = database.get_record_by_id(record_id)
    if not existing:
        return jsonify({"success": False, "message": "Rekod tidak dijumpai."}), 404

    try:
        success = database.delete_record(record_id)
        if success:
            return jsonify({
                "success": True,
                "message": f"Rekod peminjaman ID #{record_id} berjaya dipadam."
            })
        return jsonify({"success": False, "message": "Gagal memadam rekod."}), 500
    except Exception as e:
        return jsonify({"success": False, "message": f"Ralat memadam rekod: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = app.config['DEBUG']
    app.run(host='0.0.0.0', port=port, debug=debug)
