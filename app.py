from flask import Flask, render_template, request, redirect, url_for
from models import BenhNhan, KhamBenh
from database import db_session, init_db
from sqlalchemy import func
from datetime import datetime

app = Flask(__name__)

# khởi tạo csdl
with app.app_context():
    init_db()

# dọn dẹp tài nguyên sau khi xử lý request.
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def index():
    patients = BenhNhan.query.all()
    return render_template('index.html', patients=patients)

@app.route('/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        patient = BenhNhan(
            ho_ten=request.form['ho_ten'],
            gioi_tinh=request.form['gioi_tinh'],
            nam_sinh=request.form['nam_sinh'],
            dia_chi=request.form['dia_chi'],
            dien_thoai=request.form['dien_thoai']
        )
        db_session.add(patient)
        db_session.commit()
        return redirect(url_for('index'))
    return render_template('add_patient.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    patient = BenhNhan.query.get(id)
    if request.method == 'POST':
        patient.ho_ten = request.form['ho_ten']
        patient.gioi_tinh = request.form['gioi_tinh']
        patient.nam_sinh = request.form['nam_sinh']
        patient.dia_chi = request.form['dia_chi']
        patient.dien_thoai = request.form['dien_thoai']
        db_session.commit()
        return redirect(url_for('index'))
    return render_template('edit_patient.html', patient=patient)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_patient(id):
    patient = BenhNhan.query.get(id)
    db_session.delete(patient)
    db_session.commit()
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search_patient():
    if request.method == 'POST':
        search_term = request.form['search_term']
        results = BenhNhan.query.filter(BenhNhan.ho_ten.like(f'%{search_term}%')).all()
        return render_template('search_patient.html', results=results)
    return render_template('search_patient.html', results=[])

@app.route('/patient/<int:id>')
def patient_detail(id):
    patient = BenhNhan.query.get(id)
    kham_benh = KhamBenh.query.filter_by(ma_benh_nhan=id).all()
    total_visits = db_session.query(func.count(KhamBenh.so_kham)).filter_by(ma_benh_nhan=id).scalar()
    total_amount = db_session.query(func.sum(KhamBenh.tong_tien)).filter_by(ma_benh_nhan=id).scalar()
    return render_template('patient_detail.html', patient=patient, kham_benh=kham_benh, total_visits=total_visits, total_amount=total_amount)

@app.route('/patient/<int:id>/add_visit', methods=['GET', 'POST'])
def add_visit(id):
    if request.method == 'POST':
        try:
            ngay_kham = datetime.strptime(request.form['ngay_kham'], '%Y-%m-%d').date()
            tong_tien = int(request.form['tong_tien'])
            
            visit = KhamBenh(
                ma_benh_nhan=id,
                ngay_kham=ngay_kham,
                tong_tien=tong_tien
            )
            db_session.add(visit)
            db_session.commit()
            return redirect(url_for('patient_detail', id=id))
        except ValueError:
            return "Lỗi: Ngày khám không hợp lệ. Vui lòng nhập lại."
    return render_template('add_visit.html', patient_id=id)

if __name__ == '__main__':
    app.run(debug=True)
