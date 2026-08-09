// Hospital Management System Single-Page Web App Controller

document.addEventListener("DOMContentLoaded", () => {
    initNavigation();
    loadDashboardStats();
    loadPatients();
    loadRooms();
    loadEmployees();
    loadDepartments();
    loadAmbulances();
    bindFormEvents();
});

// Toast Notifications
function showToast(message, type = "info") {
    const toast = document.getElementById("toast");
    toast.textContent = message;
    toast.className = `toast show ${type}`;
    setTimeout(() => {
        toast.className = "toast";
    }, 3500);
}

// Navigation Switcher
function initNavigation() {
    const navItems = document.querySelectorAll(".nav-item");
    const sections = document.querySelectorAll(".view-section");

    navItems.forEach(item => {
        item.addEventListener("click", () => {
            const target = item.getAttribute("data-target");

            navItems.forEach(i => i.classList.remove("active"));
            item.classList.add("active");

            sections.forEach(sec => {
                if (sec.id === target) {
                    sec.classList.add("active");
                } else {
                    sec.classList.remove("active");
                }
            });

            // Trigger refresh on view change
            if (target === "dashboard") loadDashboardStats();
            else if (target === "patients") loadPatients();
            else if (target === "rooms") loadRooms();
            else if (target === "discharge") populateDischargePatients();
            else if (target === "search-room") populateSearchRoomPatients();
            else if (target === "employees") loadEmployees();
            else if (target === "departments") loadDepartments();
            else if (target === "ambulances") loadAmbulances();
        });
    });
}

// 1. Dashboard Stats
async function loadDashboardStats() {
    try {
        const res = await fetch("/api/dashboard");
        const data = await res.json();
        document.getElementById("stat-total-patients").textContent = data.total_patients || 0;
        document.getElementById("stat-available-rooms").textContent = data.available_rooms || 0;
        document.getElementById("stat-total-employees").textContent = data.total_employees || 0;
        document.getElementById("stat-available-ambulances").textContent = data.available_ambulances || 0;
    } catch (err) {
        console.error("Error loading dashboard stats:", err);
    }
}

// 2. Load Patients
async function loadPatients() {
    try {
        const res = await fetch("/api/patients");
        const patients = await res.json();
        const tbody = document.getElementById("patients-tbody");
        tbody.innerHTML = "";

        patients.forEach(p => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td><strong>${p.patient_id}</strong></td>
                <td>${p.name}</td>
                <td>${p.id_type} (${p.id_number})</td>
                <td>${p.gender}</td>
                <td>${p.disease}</td>
                <td><span class="badge ${p.room_number !== 'Not Assigned' ? 'badge-available' : 'badge-discharged'}">${p.room_number}</span></td>
                <td>${p.admission_time}</td>
                <td>₹${p.deposit_amount.toFixed(2)}</td>
                <td><span class="badge ${p.is_discharged ? 'badge-discharged' : 'badge-available'}">${p.is_discharged ? 'Discharged' : 'Admitted'}</span></td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error("Error loading patients:", err);
    }
}

// 3. Load Rooms
async function loadRooms() {
    const bedType = document.getElementById("filter-bed-type") ? document.getElementById("filter-bed-type").value : "All";
    const priceRange = document.getElementById("filter-price-range") ? document.getElementById("filter-price-range").value : "All";

    try {
        const res = await fetch(`/api/rooms?bed_type=${encodeURIComponent(bedType)}&price_range=${encodeURIComponent(priceRange)}`);
        const rooms = await res.json();
        const tbody = document.getElementById("rooms-tbody");
        tbody.innerHTML = "";

        rooms.forEach(r => {
            const tr = document.createElement("tr");
            const badgeClass = r.available ? "badge-available" : "badge-occupied";
            tr.innerHTML = `
                <td><strong>${r.room_number}</strong></td>
                <td>${r.bed_type}</td>
                <td>₹${r.price.toFixed(2)}</td>
                <td><span class="badge ${badgeClass}">${r.status}</span></td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error("Error loading rooms:", err);
    }
}

// 4. Load Employees
async function loadEmployees() {
    try {
        const res = await fetch("/api/employees");
        const employees = await res.json();
        const tbody = document.getElementById("employees-tbody");
        tbody.innerHTML = "";

        employees.forEach(e => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td><strong>${e.employee_id}</strong></td>
                <td>${e.name}</td>
                <td>${e.role}</td>
                <td>${e.gender} / ${e.age} yrs</td>
                <td>₹${e.salary.toFixed(2)}</td>
                <td>${e.phone_number}</td>
                <td>${e.email}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error("Error loading employees:", err);
    }
}

// 5. Load Departments
async function loadDepartments() {
    try {
        const res = await fetch("/api/departments");
        const departments = await res.json();
        const tbody = document.getElementById("departments-tbody");
        tbody.innerHTML = "";

        departments.forEach(d => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td><strong>${d.name}</strong></td>
                <td>${d.phone_number}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error("Error loading departments:", err);
    }
}

// 6. Load Ambulances
async function loadAmbulances() {
    try {
        const res = await fetch("/api/ambulances");
        const ambulances = await res.json();
        const tbody = document.getElementById("ambulances-tbody");
        tbody.innerHTML = "";

        ambulances.forEach(a => {
            const tr = document.createElement("tr");
            const badgeClass = a.is_available ? "badge-available" : "badge-occupied";
            const bookBtn = a.is_available ?
                `<button class="btn btn-primary" style="padding: 4px 12px; font-size:12px;" onclick="bookAmbulance('${a.ambulance_id}')">Book</button>` :
                `<span style="color: var(--text-muted); font-size:12px;">Booked</span>`;

            tr.innerHTML = `
                <td><strong>${a.ambulance_id}</strong></td>
                <td>${a.plate_number}</td>
                <td>${a.driver_name}</td>
                <td>${a.driver_phone}</td>
                <td><span class="badge ${badgeClass}">${a.status}</span></td>
                <td>${bookBtn}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error("Error loading ambulances:", err);
    }
}

async function bookAmbulance(ambulanceId) {
    try {
        const res = await fetch("/api/ambulances/book", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ambulance_id: ambulanceId })
        });
        const data = await res.json();
        if (data.success) {
            showToast(data.message, "success");
            loadAmbulances();
        } else {
            showToast(data.message, "error");
        }
    } catch (err) {
        showToast("Error booking ambulance", "error");
    }
}

// Populate Dropdowns
async function populateDischargePatients() {
    const select = document.getElementById("discharge-patient-select");
    select.innerHTML = '<option value="">-- Select Patient --</option>';

    const res = await fetch("/api/patients");
    const patients = await res.json();
    patients.filter(p => !p.is_discharged).forEach(p => {
        const opt = document.createElement("option");
        opt.value = p.patient_id;
        opt.textContent = `${p.patient_id} - ${p.name} (Room: ${p.room_number})`;
        select.appendChild(opt);
    });
}

async function populateSearchRoomPatients() {
    const select = document.getElementById("search-room-patient-select");
    select.innerHTML = '<option value="">-- Select Patient --</option>';

    const res = await fetch("/api/patients");
    const patients = await res.json();
    patients.filter(p => !p.is_discharged).forEach(p => {
        const opt = document.createElement("option");
        opt.value = p.patient_id;
        opt.textContent = `${p.patient_id} - ${p.name} (${p.disease})`;
        select.appendChild(opt);
    });
}

// Bind Form Submissions
function bindFormEvents() {
    // Add Patient Form
    document.getElementById("add-patient-form").addEventListener("submit", async (e) => {
        e.preventDefault();
        const payload = {
            id_type: document.getElementById("add-id-type").value,
            id_number: document.getElementById("add-id-number").value,
            name: document.getElementById("add-name").value,
            gender: document.getElementById("add-gender").value,
            disease: document.getElementById("add-disease").value,
            deposit_amount: parseFloat(document.getElementById("add-deposit").value || 0)
        };

        const res = await fetch("/api/patients", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.success) {
            showToast(data.message, "success");
            e.target.reset();
            loadPatients();
        } else {
            showToast(data.message, "error");
        }
    });

    // Discharge Patient Dropdown Select
    const disSelect = document.getElementById("discharge-patient-select");
    if (disSelect) {
        disSelect.addEventListener("change", async () => {
            const pid = disSelect.value;
            if (!pid) return;
            const res = await fetch("/api/patients");
            const patients = await res.json();
            const p = patients.find(x => x.patient_id === pid);
            if (p) {
                document.getElementById("dis-name").textContent = p.name;
                document.getElementById("dis-room").textContent = p.room_number;
                document.getElementById("dis-adm").textContent = p.admission_time;
                document.getElementById("dis-deposit").textContent = `₹${p.deposit_amount.toFixed(2)}`;
                document.getElementById("dis-paid").textContent = `₹${p.amount_paid.toFixed(2)}`;
                document.getElementById("dis-pending").textContent = `₹${p.pending_amount.toFixed(2)}`;
            }
        });
    }

    // Discharge Form Submit
    document.getElementById("discharge-form").addEventListener("submit", async (e) => {
        e.preventDefault();
        const pid = document.getElementById("discharge-patient-select").value;
        const amt = parseFloat(document.getElementById("discharge-amount-paid").value || 0);

        if (!pid) {
            showToast("Please select a patient to discharge", "error");
            return;
        }

        const res = await fetch("/api/patients/discharge", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ patient_id: pid, amount_paid: amt })
        });
        const data = await res.json();
        if (data.success) {
            showToast(data.message, "success");
            e.target.reset();
            populateDischargePatients();
            loadRooms();
        } else {
            showToast(data.message, "error");
        }
    });

    // Search Room Filters
    document.getElementById("btn-search-rooms").addEventListener("click", () => {
        loadRooms();
    });

    // Book Room Click Listener
    document.getElementById("btn-book-room").addEventListener("click", async () => {
        const pid = document.getElementById("search-room-patient-select").value;
        const roomNum = document.getElementById("book-room-number-input").value.trim();

        if (!pid || !roomNum) {
            showToast("Please select a patient and enter a valid room number to book", "error");
            return;
        }

        const res = await fetch("/api/rooms/book", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ patient_id: pid, room_number: roomNum })
        });
        const data = await res.json();
        if (data.success) {
            showToast(data.message, "success");
            loadRooms();
        } else {
            showToast(data.message, "error");
        }
    });
}
