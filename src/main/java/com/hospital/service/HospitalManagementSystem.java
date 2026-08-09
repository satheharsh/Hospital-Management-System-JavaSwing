package com.hospital.service;

import com.hospital.model.*;
import com.hospital.dao.*;
import com.hospital.util.DatabaseInitializer;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class HospitalManagementSystem {
    private List<Patient> patients;
    private List<Room> rooms;
    private List<Department> departments;
    private List<Employee> employees;
    private List<Ambulance> ambulances;
    
    private static final String DEFAULT_USERNAME = "shrikar";
    private static final String DEFAULT_PASSWORD = "431001";
    
    private RoomDAO roomDAO;
    private PatientDAO patientDAO;
    private EmployeeDAO employeeDAO;
    private DepartmentDAO departmentDAO;
    private AmbulanceDAO ambulanceDAO;

    public HospitalManagementSystem() {
        // Initialize database schema
        DatabaseInitializer.initializeDatabase();
        
        // Initialize DAOs
        roomDAO = new RoomDAO();
        patientDAO = new PatientDAO();
        employeeDAO = new EmployeeDAO();
        departmentDAO = new DepartmentDAO();
        ambulanceDAO = new AmbulanceDAO();
        
        // Load data from database
        rooms = roomDAO.getAllRooms();
        patients = patientDAO.getAllPatients();
        departments = departmentDAO.getAllDepartments();
        employees = employeeDAO.getAllEmployees();
        ambulances = ambulanceDAO.getAllAmbulances();
        
        // Initialize default data if tables are empty
        if (rooms.isEmpty()) {
            initializeDefaultRooms();
        }
        if (departments.isEmpty()) {
            initializeDefaultDepartments();
        }
        if (employees.isEmpty()) {
            initializeDefaultEmployees();
        }
        if (ambulances.isEmpty()) {
            initializeDefaultAmbulances();
        }
    }

    private void initializeDefaultDepartments() {
        departments = new ArrayList<>();
        departments.add(new Department("OPD", "1234567890"));
        departments.add(new Department("OT", "1234567891"));
        departments.add(new Department("Nursing Department", "1234567892"));
        departments.add(new Department("Surgical Department", "1234567893"));

        for (Department dept : departments) {
            departmentDAO.addDepartment(dept);
        }
    }

    private void initializeDefaultEmployees() {
        employees = new ArrayList<>();
        employees.add(new Employee("D001", "Dr. Rajesh Kumar", 45, "Male", 150000.0, "9876543210", "rajesh.kumar@hospital.com", "Cardiologist"));
        employees.add(new Employee("D002", "Dr. Priya Sharma", 38, "Female", 140000.0, "9876543211", "priya.sharma@hospital.com", "Neurologist"));
        employees.add(new Employee("D003", "Dr. Amit Patel", 42, "Male", 145000.0, "9876543212", "amit.patel@hospital.com", "Orthopedic"));
        employees.add(new Employee("D004", "Dr. Sneha Gupta", 35, "Female", 135000.0, "9876543213", "sneha.gupta@hospital.com", "Pediatrician"));
        employees.add(new Employee("D005", "Dr. Vikram Singh", 50, "Male", 130000.0, "9876543214", "vikram.singh@hospital.com", "General Physician"));

        employees.add(new Employee("N001", "Sarah Wilson", 32, "Female", 80000.0, "9876543215", "sarah.wilson@hospital.com", "Head Nurse"));
        employees.add(new Employee("N002", "John Smith", 35, "Male", 75000.0, "9876543216", "john.smith@hospital.com", "Emergency Nurse"));
        employees.add(new Employee("N003", "Maria Garcia", 28, "Female", 70000.0, "9876543217", "maria.garcia@hospital.com", "ICU Nurse"));
        employees.add(new Employee("N004", "David Chen", 30, "Male", 72000.0, "9876543218", "david.chen@hospital.com", "Surgical Nurse"));
        employees.add(new Employee("N005", "Lisa Anderson", 33, "Female", 68000.0, "9876543219", "lisa.anderson@hospital.com", "Pediatric Nurse"));

        for (Employee emp : employees) {
            employeeDAO.addEmployee(emp);
        }
    }

    private void initializeDefaultAmbulances() {
        ambulances = new ArrayList<>();
        ambulances.add(new Ambulance("AMB001", "Harsh Sathe", "9876543210", "MH12AB1234"));
        ambulances.add(new Ambulance("AMB002", "Shardul Walunj", "9876543211", "MH12CD5678"));
        ambulances.add(new Ambulance("AMB003", "Savit Pandita", "9876543212", "MH12EF9012"));
        ambulances.add(new Ambulance("AMB004", "Shrikar Bende", "9876543213", "MH12GH3456"));
        ambulances.add(new Ambulance("AMB005", "Rajshekhar Shinde", "9876543214", "MH12IJ7890"));
        
        ambulances.get(2).setAvailable(false);

        for (Ambulance amb : ambulances) {
            ambulanceDAO.addAmbulance(amb);
        }
    }

    private void initializeDefaultRooms() {
        rooms = new ArrayList<>();
        
        for (int i = 1; i <= 10; i++) { Room room = new Room("S" + i, "Single", 1500.0, true); rooms.add(room); roomDAO.addRoom(room); }
        for (int i = 1; i <= 10; i++) { Room room = new Room("D" + i, "Double", 2500.0, true); rooms.add(room); roomDAO.addRoom(room); }
        for (int i = 1; i <= 5; i++) { Room room = new Room("SU" + i, "Suite", 5000.0, true); rooms.add(room); roomDAO.addRoom(room); }
        for (int i = 1; i <= 5; i++) { Room room = new Room("ICU" + i, "ICU", 8000.0, true); rooms.add(room); roomDAO.addRoom(room); }
        for (int i = 1; i <= 3; i++) { Room room = new Room("DL" + i, "Deluxe", 3500.0, true); rooms.add(room); roomDAO.addRoom(room); }
        for (int i = 1; i <= 15; i++) { Room room = new Room("GW" + i, "General Ward", 800.0, true); rooms.add(room); roomDAO.addRoom(room); }
        for (int i = 1; i <= 8; i++) { Room room = new Room("P" + i, "Pediatric", 2000.0, true); rooms.add(room); roomDAO.addRoom(room); }
        for (int i = 1; i <= 6; i++) { Room room = new Room("M" + i, "Maternity", 3000.0, true); rooms.add(room); roomDAO.addRoom(room); }
    }

    public boolean login(String username, String password) {
        return username != null && password != null &&
               username.trim().equals(DEFAULT_USERNAME) &&
               password.trim().equals(DEFAULT_PASSWORD);
    }

    // Patient Management
    public void addPatient(Patient patient) {
        if (!validatePatient(patient)) {
            System.err.println("Patient validation failed!");
            return;
        }
        boolean added = patientDAO.addPatient(patient);
        if (added) {
            patients.add(patient);
        } else {
            System.err.println("Patient NOT added to the database!");
        }
    }

    public List<Patient> getAllPatients() {
        patients = patientDAO.getAllPatients();
        return new ArrayList<>(patients);
    }

    public Patient findPatientById(String patientId) {
        return patientDAO.getPatientById(patientId);
    }

    public void updatePatient(Patient patient) {
        boolean updated = patientDAO.updatePatient(patient);
        if (updated) {
            for (int i = 0; i < patients.size(); i++) {
                if (patients.get(i).getPatientId().equals(patient.getPatientId())) {
                    patients.set(i, patient);
                    break;
                }
            }
        }
    }

    /**
     * Discharge a patient: update billing, discharge timestamp, and free up occupied room.
     */
    public boolean dischargePatient(String patientId, double amountPaid) {
        Patient patient = findPatientById(patientId);
        if (patient == null) {
            return false;
        }

        patient.setAmountPaid(patient.getAmountPaid() + amountPaid);
        patient.setPendingAmount(Math.max(0, patient.getDepositAmount() - patient.getAmountPaid()));
        patient.setDischargeDate(LocalDateTime.now());

        // Free up patient's room if assigned
        String roomNumber = patient.getRoomNumber();
        if (roomNumber != null && !roomNumber.trim().isEmpty()) {
            Room room = roomDAO.getRoomByNumber(roomNumber);
            if (room != null) {
                room.setAvailable(true);
                roomDAO.updateRoom(room);
            }
        }

        return patientDAO.updatePatient(patient);
    }

    // Room Management
    public List<Room> getAllRooms() {
        return roomDAO.getAllRooms();
    }

    public List<Room> getAvailableRooms() {
        return getAllRooms().stream()
                .filter(Room::isAvailable)
                .collect(Collectors.toList());
    }

    public List<Room> getRoomsByBedType(String bedType) {
        return getAllRooms().stream()
                .filter(r -> r.getBedType().equalsIgnoreCase(bedType))
                .collect(Collectors.toList());
    }

    public Room findRoomByNumber(String roomNumber) {
        return roomDAO.getRoomByNumber(roomNumber);
    }

    public boolean updateRoom(Room updatedRoom) {
        boolean success = roomDAO.updateRoom(updatedRoom);
        if (success) {
            for (int i = 0; i < rooms.size(); i++) {
                if (rooms.get(i).getRoomNumber().equalsIgnoreCase(updatedRoom.getRoomNumber())) {
                    rooms.set(i, updatedRoom);
                    break;
                }
            }
        }
        return success;
    }

    public boolean addRoom(Room room) {
        boolean success = roomDAO.addRoom(room);
        if (success) {
            rooms.add(room);
        }
        return success;
    }

    public boolean deleteRoom(String roomNumber) {
        boolean success = roomDAO.deleteRoom(roomNumber);
        if (success) {
            rooms.removeIf(room -> room.getRoomNumber().equalsIgnoreCase(roomNumber));
        }
        return success;
    }

    // Department Management
    public List<Department> getAllDepartments() {
        departments = departmentDAO.getAllDepartments();
        return new ArrayList<>(departments);
    }

    public boolean addDepartment(Department department) {
        boolean added = departmentDAO.addDepartment(department);
        if (added) {
            departments.add(department);
        }
        return added;
    }

    // Employee Management
    public List<Employee> getAllEmployees() {
        employees = employeeDAO.getAllEmployees();
        return new ArrayList<>(employees);
    }

    public boolean addEmployee(Employee employee) {
        boolean added = employeeDAO.addEmployee(employee);
        if (added) {
            employees.add(employee);
        }
        return added;
    }

    // Ambulance Management
    public List<Ambulance> getAllAmbulances() {
        ambulances = ambulanceDAO.getAllAmbulances();
        return new ArrayList<>(ambulances);
    }

    public List<Ambulance> getAvailableAmbulances() {
        return getAllAmbulances().stream()
                .filter(Ambulance::isAvailable)
                .collect(Collectors.toList());
    }

    public boolean bookAmbulance(String ambulanceId) {
        List<Ambulance> currentList = getAllAmbulances();
        for (Ambulance a : currentList) {
            if (a.getAmbulanceId().equalsIgnoreCase(ambulanceId) && a.isAvailable()) {
                a.setAvailable(false);
                return ambulanceDAO.updateAvailability(ambulanceId, false);
            }
        }
        return false;
    }

    public boolean releaseAmbulance(String ambulanceId) {
        return ambulanceDAO.updateAvailability(ambulanceId, true);
    }

    public void exportPatientsToCSV(String filePath) {
        try (FileWriter writer = new FileWriter(filePath)) {
            writer.write("ID,Name,Gender,Disease,Admission Date,Room Number\n");
            List<Patient> patientsList = patientDAO.getAllPatients();
            for (Patient patient : patientsList) {
                writer.write(String.format("%s,%s,%s,%s,%s,%s\n",
                    patient.getPatientId(),
                    patient.getName(),
                    patient.getGender(),
                    patient.getDisease(),
                    patient.getAdmissionTime().toString(),
                    patient.getRoomNumber() != null ? patient.getRoomNumber() : "N/A"));
            }
            System.out.println("Patient data exported to " + filePath);
        } catch (IOException e) {
            System.err.println("Error exporting patient data: " + e.getMessage());
        }
    }

    public void backupDatabase(String backupPath) {
        try {
            File backupDir = new File(backupPath);
            if (!backupDir.exists()) {
                backupDir.mkdirs();
            }
            
            String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
            String backupFile = backupPath + "/hospital_db_backup_" + timestamp + ".sql";
            
            // Detect mysqldump command dynamically
            String mysqldumpCmd = "mysqldump";
            File winDump = new File("C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysqldump.exe");
            if (winDump.exists()) {
                mysqldumpCmd = winDump.getAbsolutePath();
            }

            ProcessBuilder pb = new ProcessBuilder(
                mysqldumpCmd,
                "-u", "root",
                "-p431001",
                "hospital_db"
            );
            pb.redirectOutput(new File(backupFile));
            Process p = pb.start();
            int exitCode = p.waitFor();
            
            if (exitCode == 0) {
                System.out.println("Database backup created successfully at: " + backupFile);
            } else {
                System.err.println("mysqldump exited with code: " + exitCode);
            }
        } catch (Exception e) {
            System.err.println("Error creating database backup: " + e.getMessage());
        }
    }

    public boolean validatePatient(Patient patient) {
        if (patient == null) {
            System.err.println("Patient cannot be null");
            return false;
        }

        if (patient.getPatientId() == null || patient.getPatientId().trim().isEmpty()) {
            System.err.println("Patient ID cannot be empty");
            return false;
        }
        
        if (patient.getName() == null || patient.getName().trim().isEmpty()) {
            System.err.println("Patient name cannot be empty");
            return false;
        }
        
        if (patient.getDepositAmount() < 0) {
            System.err.println("Deposit amount cannot be negative");
            return false;
        }
        
        if (patient.getRoomNumber() != null && !patient.getRoomNumber().trim().isEmpty()) {
            Room room = roomDAO.getRoomByNumber(patient.getRoomNumber());
            if (room == null) {
                System.err.println("Invalid room number: " + patient.getRoomNumber());
                return false;
            }
            // Room availability check: pass if room is available OR if current patient already owns this room
            Patient existingOwner = patientDAO.getPatientById(patient.getPatientId());
            boolean isSelfOwned = existingOwner != null && patient.getRoomNumber().equalsIgnoreCase(existingOwner.getRoomNumber());
            if (!room.isAvailable() && !isSelfOwned) {
                System.err.println("Room is not available: " + patient.getRoomNumber());
                return false;
            }
        }
        
        return true;
    }
}