from datetime import datetime
import os
import re
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS

from models import Patient, Room, Employee, Department, Ambulance
from services.hospital_management_system import HospitalManagementSystem

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

hms = HospitalManagementSystem()

# Helper for patient ID generation
def get_next_patient_id():
    patients = hms.get_all_patients()
    max_id = 0
    for p in patients:
        digits = re.sub(r"[^0-9]", "", p.patient_id)
        if digits.isdigit():
            max_id = max(max_id, int(digits))
    return f"P{max_id + 1:02d}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json or {}
    username = data.get("username", "")
    password = data.get("password", "")
    if hms.login(username, password):
        return jsonify({"success": True, "message": "Login successful"})
    return jsonify({"success": False, "message": "Invalid username or password"}), 401

@app.route("/api/dashboard", methods=["GET"])
def get_dashboard():
    patients = hms.get_all_patients()
    rooms = hms.get_all_rooms()
    employees = hms.get_all_employees()
    ambulances = hms.get_all_ambulances()

    active_patients = [p for p in patients if p.discharge_date is None]
    available_rooms = [r for r in rooms if r.available]
    available_ambulances = [a for a in ambulances if a.is_available]

    return jsonify({
        "total_patients": len(patients),
        "active_patients": len(active_patients),
        "total_rooms": len(rooms),
        "available_rooms": len(available_rooms),
        "total_employees": len(employees),
        "available_ambulances": len(available_ambulances),
        "total_ambulances": len(ambulances)
    })

@app.route("/api/patients", methods=["GET"])
def get_patients():
    patients = hms.get_all_patients()
    result = []
    for p in patients:
        result.append({
            "patient_id": p.patient_id,
            "id_type": p.id_type,
            "id_number": p.id_number,
            "name": p.name,
            "gender": p.gender,
            "disease": p.disease,
            "admission_time": p.admission_time.strftime("%Y-%m-%d %H:%M"),
            "deposit_amount": p.deposit_amount,
            "room_number": p.room_number or "Not Assigned",
            "pending_amount": p.pending_amount,
            "amount_paid": p.amount_paid,
            "discharge_date": p.discharge_date.strftime("%Y-%m-%d %H:%M") if p.discharge_date else None,
            "is_discharged": p.discharge_date is not None
        })
    return jsonify(result)

@app.route("/api/patients", methods=["POST"])
def add_patient():
    data = request.json or {}
    id_type = data.get("id_type", "Aadhar Card")
    id_number = data.get("id_number", "").strip()
    name = data.get("name", "").strip()
    gender = data.get("gender", "Male")
    disease = data.get("disease", "").strip()
    deposit_amount = data.get("deposit_amount", 0.0)

    if not id_number or not name or not disease:
        return jsonify({"success": False, "message": "All required fields must be filled"}), 400

    try:
        deposit_amount = float(deposit_amount)
        patient_id = get_next_patient_id()
        patient = Patient(patient_id, id_type, id_number, name, gender, disease, datetime.now(), deposit_amount)
        if hms.add_patient(patient):
            return jsonify({"success": True, "message": f"Patient {name} ({patient_id}) admitted successfully!", "patient_id": patient_id})
        return jsonify({"success": False, "message": "Failed to save patient to database"}), 500
    except ValueError:
        return jsonify({"success": False, "message": "Invalid deposit amount"}), 400

@app.route("/api/patients/update", methods=["POST"])
def update_patient():
    data = request.json or {}
    patient_id = data.get("patient_id")
    try:
        pending_amount = float(data.get("pending_amount", 0.0))
        amount_paid = float(data.get("amount_paid", 0.0))
        patient = hms.find_patient_by_id(patient_id)
        if not patient:
            return jsonify({"success": False, "message": "Patient not found"}), 404
        
        patient.pending_amount = max(0.0, pending_amount)
        patient.amount_paid = max(0.0, amount_paid)
        if hms.update_patient(patient):
            return jsonify({"success": True, "message": "Patient details updated successfully"})
        return jsonify({"success": False, "message": "Failed to update patient"}), 500
    except ValueError:
        return jsonify({"success": False, "message": "Invalid numeric amounts"}), 400

@app.route("/api/patients/discharge", methods=["POST"])
def discharge_patient():
    data = request.json or {}
    patient_id = data.get("patient_id")
    try:
        amount_paid = float(data.get("amount_paid", 0.0))
        if amount_paid < 0:
            return jsonify({"success": False, "message": "Amount paid cannot be negative"}), 400
        
        if hms.discharge_patient(patient_id, amount_paid):
            p = hms.find_patient_by_id(patient_id)
            return jsonify({
                "success": True,
                "message": f"Patient discharged successfully! Pending amount: ₹{p.pending_amount:.2f}",
                "pending_amount": p.pending_amount
            })
        return jsonify({"success": False, "message": "Failed to discharge patient"}), 500
    except ValueError:
        return jsonify({"success": False, "message": "Invalid amount"}), 400

@app.route("/api/rooms", methods=["GET"])
def get_rooms():
    bed_type = request.args.get("bed_type", "All")
    price_range = request.args.get("price_range", "All")

    rooms = hms.get_all_rooms()
    if bed_type != "All":
        rooms = [r for r in rooms if r.bed_type.lower() == bed_type.lower()]
    
    if price_range == "Under 1500":
        rooms = [r for r in rooms if r.price < 1500]
    elif price_range == "1500-2500":
        rooms = [r for r in rooms if 1500 <= r.price <= 2500]
    elif price_range == "Above 2500":
        rooms = [r for r in rooms if r.price > 2500]

    result = []
    for r in rooms:
        result.append({
            "room_number": r.room_number,
            "bed_type": r.bed_type,
            "price": r.price,
            "available": r.available,
            "status": "Available" if r.available else "Occupied"
        })
    return jsonify(result)

@app.route("/api/rooms/book", methods=["POST"])
def book_room():
    data = request.json or {}
    patient_id = data.get("patient_id")
    room_number = data.get("room_number")

    room = hms.find_room_by_number(room_number)
    patient = hms.find_patient_by_id(patient_id)

    if not room or not patient:
        return jsonify({"success": False, "message": "Invalid room or patient selection"}), 400

    if not room.available:
        return jsonify({"success": False, "message": "This room is already occupied"}), 400

    room.available = False
    patient.room_number = room.room_number
    if hms.update_room(room) and hms.update_patient(patient):
        return jsonify({"success": True, "message": f"Room {room_number} booked successfully for {patient.name}!"})
    return jsonify({"success": False, "message": "Failed to book room"}), 500

@app.route("/api/employees", methods=["GET"])
def get_employees():
    employees = hms.get_all_employees()
    result = []
    for e in employees:
        result.append({
            "employee_id": e.employee_id,
            "name": e.name,
            "age": e.age,
            "gender": e.gender,
            "salary": e.salary,
            "phone_number": e.phone_number,
            "email": e.email,
            "role": e.role
        })
    return jsonify(result)

@app.route("/api/departments", methods=["GET"])
def get_departments():
    departments = hms.get_all_departments()
    result = []
    for d in departments:
        result.append({
            "name": d.name,
            "phone_number": d.phone_number
        })
    return jsonify(result)

@app.route("/api/ambulances", methods=["GET"])
def get_ambulances():
    ambulances = hms.get_all_ambulances()
    result = []
    for a in ambulances:
        result.append({
            "ambulance_id": a.ambulance_id,
            "driver_name": a.driver_name,
            "driver_phone": a.driver_phone,
            "plate_number": a.plate_number,
            "is_available": a.is_available,
            "status": "Available" if a.is_available else "Ongoing"
        })
    return jsonify(result)

@app.route("/api/ambulances/book", methods=["POST"])
def book_ambulance():
    data = request.json or {}
    ambulance_id = data.get("ambulance_id")
    if hms.book_ambulance(ambulance_id):
        return jsonify({"success": True, "message": f"Ambulance {ambulance_id} booked successfully!"})
    return jsonify({"success": False, "message": "Ambulance is currently unavailable"}), 400

@app.route("/api/export/csv", methods=["GET"])
def export_csv():
    csv_file = "patients_export.csv"
    hms.export_patients_to_csv(csv_file)
    if os.path.exists(csv_file):
        return send_file(csv_file, as_attachment=True, download_name="hospital_patients.csv")
    return jsonify({"success": False, "message": "Export failed"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
