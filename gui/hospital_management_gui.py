from datetime import datetime
import re
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Optional

from models import Patient, Room, Employee, Department, Ambulance
from services.hospital_management_system import HospitalManagementSystem

# Style Constants matching Java Swing
PRIMARY_COLOR = "#2980b9"
SECONDARY_COLOR = "#34495e"
ACCENT_COLOR = "#2ecc71"
ERROR_COLOR = "#e74c3c"
BACKGROUND_COLOR = "#ecf0f1"
PANEL_COLOR = "#ffffff"
TEXT_COLOR = "#2c3e50"
HEADER_COLOR = "#0063b1"

# Fonts
HEADER_FONT = ("Segoe UI", 18, "bold")
SUBHEADER_FONT = ("Segoe UI", 14, "bold")
LABEL_FONT = ("Segoe UI", 11, "bold")
BUTTON_FONT = ("Segoe UI", 11, "bold")
TABLE_FONT = ("Segoe UI", 10, "normal")

# Icon Symbols
ADD_PATIENT_ICON = "👤"
ROOM_ICON = "🏠"
DEPARTMENT_ICON = "🏥"
EMPLOYEE_ICON = "👨‍⚕️"
PATIENT_INFO_ICON = "📋"
DISCHARGE_ICON = "🚪"
SEARCH_ICON = "🔍"
UPDATE_ICON = "✏️"
AMBULANCE_ICON = "🚑"

class HospitalManagementGUI(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Hospital Management System")
        self.geometry("1024x768")
        self.configure(bg=BACKGROUND_COLOR)

        self.system = HospitalManagementSystem()
        
        # Patient ID generator counter
        existing_patients = self.system.get_all_patients()
        max_id = 0
        for p in existing_patients:
            digits = re.sub(r"[^0-9]", "", p.patient_id)
            if digits.isdigit():
                max_id = max(max_id, int(digits))
        self.next_patient_id = max_id + 1

        self.configure_styles()

        # Main Container (CardLayout equivalent)
        self.container = tk.Frame(self, bg=BACKGROUND_COLOR)
        self.container.pack(fill="both", expand=True)

        self.frames: Dict[str, tk.Frame] = {}

        self.initialize_gui()
        self.show_frame("LOGIN")

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Treeview styling
        style.configure("Treeview",
                        font=TABLE_FONT,
                        rowheight=30,
                        background="#ffffff",
                        fieldbackground="#ffffff",
                        foreground=TEXT_COLOR)
        style.configure("Treeview.Heading",
                        font=LABEL_FONT,
                        background=HEADER_COLOR,
                        foreground="#ffffff",
                        borderwidth=1,
                        relief="solid")
        style.map("Treeview.Heading",
                  background=[("active", PRIMARY_COLOR)],
                  foreground=[("active", "#ffffff")])

        # Combobox styling
        style.configure("TCombobox",
                        font=TABLE_FONT,
                        fieldbackground="#ffffff",
                        background="#ffffff")

    def show_frame(self, page_name: str):
        if page_name in self.frames:
            # Refresh dynamic frames when shown
            if page_name == "PATIENT_LIST":
                self.frames["PATIENT_LIST"] = self.create_patient_list_panel()
            elif page_name == "ROOMS":
                self.frames["ROOMS"] = self.create_room_panel()
            elif page_name == "DISCHARGE":
                self.frames["DISCHARGE"] = self.create_discharge_panel()
            elif page_name == "SEARCH_ROOM":
                self.frames["SEARCH_ROOM"] = self.create_search_room_panel()
            elif page_name == "UPDATE_PATIENT":
                self.frames["UPDATE_PATIENT"] = self.create_update_patient_panel()
            elif page_name == "AMBULANCE":
                self.frames["AMBULANCE"] = self.create_ambulance_panel()

            frame = self.frames[page_name]
            frame.tkraise()

    def initialize_gui(self):
        self.frames["LOGIN"] = self.create_login_panel()
        self.frames["MAIN_MENU"] = self.create_main_menu_panel()
        self.frames["ADD_PATIENT"] = self.create_add_patient_panel()
        self.frames["ROOMS"] = self.create_room_panel()
        self.frames["DEPARTMENTS"] = self.create_department_panel()
        self.frames["EMPLOYEES"] = self.create_employee_panel()
        self.frames["PATIENT_LIST"] = self.create_patient_list_panel()
        self.frames["DISCHARGE"] = self.create_discharge_panel()
        self.frames["SEARCH_ROOM"] = self.create_search_room_panel()
        self.frames["UPDATE_PATIENT"] = self.create_update_patient_panel()
        self.frames["AMBULANCE"] = self.create_ambulance_panel()

        for f in self.frames.values():
            f.grid(row=0, column=0, sticky="nsew")

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def create_styled_button(self, parent, text: str, command, width: int = 20, bg_color: str = PRIMARY_COLOR) -> tk.Button:
        btn = tk.Button(parent, text=text, command=command, font=BUTTON_FONT,
                        bg=bg_color, fg="#ffffff", activebackground=SECONDARY_COLOR,
                        activeforeground="#ffffff", relief="flat", bd=0, cursor="hand2",
                        padx=10, pady=8, width=width)
        return btn

    def create_header(self, parent, title: str, back_target: Optional[str] = "MAIN_MENU", extra_buttons=None) -> tk.Frame:
        header = tk.Frame(parent, bg=PRIMARY_COLOR, padx=20, pady=15)
        lbl = tk.Label(header, text=title, font=HEADER_FONT, bg=PRIMARY_COLOR, fg="#ffffff")
        lbl.pack(side="left")

        btn_frame = tk.Frame(header, bg=PRIMARY_COLOR)
        btn_frame.pack(side="right")

        if extra_buttons:
            for btn_text, btn_cmd in extra_buttons:
                b = self.create_styled_button(btn_frame, btn_text, btn_cmd, width=12)
                b.pack(side="left", padx=5)

        if back_target:
            back_btn = self.create_styled_button(btn_frame, "Back to Main Menu",
                                                  lambda: self.show_frame(back_target), width=16)
            back_btn.pack(side="left", padx=5)

        return header

    # 1. Login Panel
    def create_login_panel(self) -> tk.Frame:
        frame = tk.Frame(self.container, bg=BACKGROUND_COLOR)
        
        card = tk.Frame(frame, bg=PANEL_COLOR, highlightbackground=PRIMARY_COLOR, highlightthickness=1, padx=40, pady=40)
        card.place(relx=0.5, rely=0.5, anchor="center")

        title = tk.Label(card, text="Hospital Management System", font=HEADER_FONT, bg=PANEL_COLOR, fg=PRIMARY_COLOR)
        title.pack(pady=(0, 20))

        tk.Label(card, text="Username", font=LABEL_FONT, bg=PANEL_COLOR, fg=TEXT_COLOR).pack(anchor="w", pady=(10, 2))
        username_ent = tk.Entry(card, font=TABLE_FONT, width=30, bd=1, relief="solid")
        username_ent.pack(pady=(0, 15), ipady=6)

        tk.Label(card, text="Password", font=LABEL_FONT, bg=PANEL_COLOR, fg=TEXT_COLOR).pack(anchor="w", pady=(10, 2))
        password_ent = tk.Entry(card, font=TABLE_FONT, width=30, show="*", bd=1, relief="solid")
        password_ent.pack(pady=(0, 25), ipady=6)

        def handle_login():
            user = username_ent.get()
            pwd = password_ent.get()
            if self.system.login(user, pwd):
                username_ent.delete(0, tk.END)
                password_ent.delete(0, tk.END)
                self.show_frame("MAIN_MENU")
            else:
                messagebox.showerror("Login Error", "Invalid username or password")

        login_btn = self.create_styled_button(card, "Login", handle_login, width=28)
        login_btn.pack()

        password_ent.bind("<Return>", lambda event: handle_login())
        username_ent.bind("<Return>", lambda event: handle_login())

        return frame

    # 2. Main Menu Panel
    def create_main_menu_panel(self) -> tk.Frame:
        frame = tk.Frame(self.container, bg=BACKGROUND_COLOR)
        header = self.create_header(frame, "Hospital Management System", back_target=None)
        header.pack(fill="x")

        menu_grid = tk.Frame(frame, bg=BACKGROUND_COLOR, padx=30, pady=30)
        menu_grid.pack(fill="both", expand=True)

        items = [
            ("Add New Patient", ADD_PATIENT_ICON, "ADD_PATIENT"),
            ("Room Management", ROOM_ICON, "ROOMS"),
            ("Department Info", DEPARTMENT_ICON, "DEPARTMENTS"),
            ("Employee Info", EMPLOYEE_ICON, "EMPLOYEES"),
            ("Patient Info", PATIENT_INFO_ICON, "PATIENT_LIST"),
            ("Patient Discharge", DISCHARGE_ICON, "DISCHARGE"),
            ("Search Room", SEARCH_ICON, "SEARCH_ROOM"),
            ("Update Patient", UPDATE_ICON, "UPDATE_PATIENT"),
            ("Ambulance Service", AMBULANCE_ICON, "AMBULANCE")
        ]

        row = 0
        col = 0
        for title, icon, target in items:
            card = tk.Frame(menu_grid, bg=PANEL_COLOR, highlightbackground="#bdc3c7", highlightthickness=1, padx=20, pady=20, cursor="hand2")
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

            lbl_icon = tk.Label(card, text=icon, font=("Segoe UI Emoji", 32), bg=PANEL_COLOR)
            lbl_icon.pack(pady=(5, 5))
            lbl_title = tk.Label(card, text=title, font=LABEL_FONT, bg=PANEL_COLOR, fg=TEXT_COLOR)
            lbl_title.pack()

            def make_cmd(t=target):
                return lambda e: self.show_frame(t)

            card.bind("<Button-1>", make_cmd(target))
            lbl_icon.bind("<Button-1>", make_cmd(target))
            lbl_title.bind("<Button-1>", make_cmd(target))

            col += 1
            if col == 3:
                col = 0
                row += 1

        for r in range(3): menu_grid.grid_rowconfigure(r, weight=1)
        for c in range(3): menu_grid.grid_columnconfigure(c, weight=1)

        bottom = tk.Frame(frame, bg=BACKGROUND_COLOR, padx=20, pady=15)
        bottom.pack(fill="x", side="bottom")
        logout_btn = self.create_styled_button(bottom, "Logout", lambda: self.show_frame("LOGIN"), width=12)
        logout_btn.pack(side="right")

        return frame

    # 3. Add Patient Panel
    def create_add_patient_panel(self) -> tk.Frame:
        frame = tk.Frame(self.container, bg=BACKGROUND_COLOR)
        header = self.create_header(frame, "Add New Patient")
        header.pack(fill="x")

        form = tk.Frame(frame, bg=PANEL_COLOR, highlightbackground=PRIMARY_COLOR, highlightthickness=1, padx=30, pady=30)
        form.pack(pady=30, padx=50, fill="both", expand=True)

        fields = [
            ("Patient ID Type:", "combo", ["Aadhar Card", "Voter ID"]),
            ("Patient ID Number:", "entry", None),
            ("Name:", "entry", None),
            ("Gender:", "combo", ["Male", "Female"]),
            ("Disease:", "entry", None),
            ("Admission Time:", "entry", datetime.now().strftime("%Y-%m-%d %H:%M")),
            ("Deposit Amount:", "entry", None)
        ]

        widgets = {}
        for idx, (label_text, w_type, vals) in enumerate(fields):
            tk.Label(form, text=label_text, font=LABEL_FONT, bg=PANEL_COLOR, fg=TEXT_COLOR).grid(row=idx, column=0, sticky="w", pady=10, padx=10)
            if w_type == "combo":
                w = ttk.Combobox(form, values=vals, font=TABLE_FONT, state="readonly", width=28)
                w.current(0)
            else:
                w = tk.Entry(form, font=TABLE_FONT, width=30, bd=1, relief="solid")
                if vals:
                    w.insert(0, vals)
            w.grid(row=idx, column=1, sticky="w", pady=10, padx=10)
            widgets[label_text] = w

        def handle_submit():
            id_type = widgets["Patient ID Type:"].get()
            id_num = widgets["Patient ID Number:"].get().strip()
            name = widgets["Name:"].get().strip()
            gender = widgets["Gender:"].get()
            disease = widgets["Disease:"].get().strip()
            adm_str = widgets["Admission Time:"].get().strip()
            dep_str = widgets["Deposit Amount:"].get().strip()

            if not all([id_num, name, disease, adm_str, dep_str]):
                messagebox.showerror("Error", "Please fill in all fields")
                return

            try:
                dep_amt = float(dep_str)
                adm_time = datetime.strptime(adm_str, "%Y-%m-%d %H:%M")
                p_id = f"P{self.next_patient_id:02d}"

                patient = Patient(p_id, id_type, id_num, name, gender, disease, adm_time, dep_amt)
                if self.system.add_patient(patient):
                    self.next_patient_id += 1
                    messagebox.showinfo("Success", f"Patient {name} ({p_id}) added successfully!")
                    widgets["Patient ID Number:"].delete(0, tk.END)
                    widgets["Name:"].delete(0, tk.END)
                    widgets["Disease:"].delete(0, tk.END)
                    widgets["Deposit Amount:"].delete(0, tk.END)
                    self.show_frame("PATIENT_LIST")
                else:
                    messagebox.showerror("Error", "Failed to add patient to database")
            except ValueError:
                messagebox.showerror("Error", "Invalid Deposit Amount or Admission Time format (yyyy-MM-dd HH:mm)")

        sub_btn = self.create_styled_button(form, "Add Patient", handle_submit, width=20)
        sub_btn.grid(row=len(fields), column=0, columnspan=2, pady=20)

        return frame

    # 4. Room Management Panel
    def create_room_panel(self) -> tk.Frame:
        frame = tk.Frame(self.container, bg=BACKGROUND_COLOR)
        header = self.create_header(frame, "Room Management", extra_buttons=[("Refresh", lambda: self.show_frame("ROOMS"))])
        header.pack(fill="x")

        table_frame = tk.Frame(frame, bg=PANEL_COLOR, padx=20, pady=20)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        cols = ("Room Number", "Availability", "Price", "Bed Type")
        tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, anchor="center", width=200)

        tree.tag_configure("occupied", background="#ffc8c8")
        tree.tag_configure("available", background="#ffffff")

        rooms = self.system.get_all_rooms()
        for r in rooms:
            status = "Available" if r.available else "Occupied"
            tag = "available" if r.available else "occupied"
            tree.insert("", "end", values=(r.room_number, status, f"₹{r.price:.2f}", r.bed_type), tags=(tag,))

        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        return frame

    # 5. Department Panel
    def create_department_panel(self) -> tk.Frame:
        frame = tk.Frame(self.container, bg=BACKGROUND_COLOR)
        header = self.create_header(frame, "Department Information")
        header.pack(fill="x")

        table_frame = tk.Frame(frame, bg=PANEL_COLOR, padx=20, pady=20)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        cols = ("Department Name", "Phone Number")
        tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, anchor="center", width=400)

        for d in self.system.get_all_departments():
            tree.insert("", "end", values=(d.name, d.phone_number))

        tree.pack(fill="both", expand=True)
        return frame

    # 6. Employee Panel
    def create_employee_panel(self) -> tk.Frame:
        frame = tk.Frame(self.container, bg=BACKGROUND_COLOR)
        header = self.create_header(frame, "Employee Information")
        header.pack(fill="x")

        table_frame = tk.Frame(frame, bg=PANEL_COLOR, padx=20, pady=20)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        cols = ("ID", "Name", "Age", "Gender", "Role", "Salary", "Phone", "Email")
        tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, anchor="center", width=120)

        for e in self.system.get_all_employees():
            tree.insert("", "end", values=(e.employee_id, e.name, e.age, e.gender, e.role, f"₹{e.salary:.2f}", e.phone_number, e.email))

        tree.pack(fill="both", expand=True)
        return frame

    # 7. Patient List Panel
    def create_patient_list_panel(self) -> tk.Frame:
        frame = tk.Frame(self.container, bg=BACKGROUND_COLOR)
        header = self.create_header(frame, "Patient Information")
        header.pack(fill="x")

        table_frame = tk.Frame(frame, bg=PANEL_COLOR, padx=20, pady=20)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        cols = ("Patient ID", "ID Type", "ID Number", "Name", "Gender", "Disease", "Room", "Admission Time", "Deposit")
        tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, anchor="center", width=110)

        patients = sorted(self.system.get_all_patients(), key=lambda p: p.patient_id)
        for p in patients:
            tree.insert("", "end", values=(
                p.patient_id, p.id_type, p.id_number, p.name, p.gender, p.disease,
                p.room_number if p.room_number else "Not Assigned",
                p.admission_time.strftime("%Y-%m-%d %H:%M"),
                f"₹{p.deposit_amount:.2f}"
            ))

        tree.pack(fill="both", expand=True)
        return frame

    # 8. Patient Discharge Panel
    def create_discharge_panel(self) -> tk.Frame:
        frame = tk.Frame(self.container, bg=BACKGROUND_COLOR)
        header = self.create_header(frame, "Patient Discharge")
        header.pack(fill="x")

        content = tk.Frame(frame, bg=PANEL_COLOR, highlightbackground=PRIMARY_COLOR, highlightthickness=1, padx=30, pady=20)
        content.pack(fill="both", expand=True, padx=30, pady=20)

        all_patients = self.system.get_all_patients()
        options = [f"{p.patient_id} - {p.name} (Room: {p.room_number or 'Not Assigned'})" for p in all_patients]

        lbl_select = tk.Label(content, text="Select Patient:", font=LABEL_FONT, bg=PANEL_COLOR, fg=PRIMARY_COLOR)
        lbl_select.pack(anchor="w", pady=5)

        combo = ttk.Combobox(content, values=options, font=TABLE_FONT, state="readonly", width=50)
        combo.pack(anchor="w", pady=5)

        details_frame = tk.LabelFrame(content, text="Patient Details", font=LABEL_FONT, bg=PANEL_COLOR, fg=PRIMARY_COLOR, padx=20, pady=10)
        details_frame.pack(fill="x", pady=15)

        labels = ["Name:", "ID Type:", "ID Number:", "Room:", "Admission Date:", "Discharge Date:", "Deposit Amount:", "Amount Paid:", "Amount to Pay:"]
        value_vars = {lbl: tk.StringVar() for lbl in labels}

        for idx, lbl in enumerate(labels):
            tk.Label(details_frame, text=lbl, font=LABEL_FONT, bg=PANEL_COLOR).grid(row=idx, column=0, sticky="w", pady=2)
            tk.Label(details_frame, textvariable=value_vars[lbl], font=TABLE_FONT, bg=PANEL_COLOR).grid(row=idx, column=1, sticky="w", pady=2, padx=10)

        payment_frame = tk.LabelFrame(content, text="Payment Details", font=LABEL_FONT, bg=PANEL_COLOR, fg=PRIMARY_COLOR, padx=20, pady=10)
        payment_frame.pack(fill="x", pady=10)

        tk.Label(payment_frame, text="Amount Paid:", font=LABEL_FONT, bg=PANEL_COLOR).pack(side="left", padx=5)
        amt_ent = tk.Entry(payment_frame, font=TABLE_FONT, width=20, bd=1, relief="solid")
        amt_ent.pack(side="left", padx=10)

        def on_select(event):
            sel = combo.get()
            if sel:
                pid = sel.split(" - ")[0]
                p = self.system.find_patient_by_id(pid)
                if p:
                    value_vars["Name:"].set(p.name)
                    value_vars["ID Type:"].set(p.id_type)
                    value_vars["ID Number:"].set(p.id_number)
                    value_vars["Room:"].set(p.room_number or "Not Assigned")
                    value_vars["Admission Date:"].set(p.admission_time.strftime("%Y-%m-%d %H:%M"))
                    value_vars["Discharge Date:"].set(p.discharge_date.strftime("%Y-%m-%d %H:%M") if p.discharge_date else "Not Discharged")
                    value_vars["Deposit Amount:"].set(f"₹{p.deposit_amount:.2f}")
                    value_vars["Amount Paid:"].set(f"₹{p.amount_paid:.2f}")
                    value_vars["Amount to Pay:"].set(f"₹{p.pending_amount:.2f}")

        combo.bind("<<ComboboxSelected>>", on_select)

        def handle_discharge():
            sel = combo.get()
            if not sel:
                messagebox.showerror("Error", "Please select a patient")
                return
            pid = sel.split(" - ")[0]
            try:
                amt = float(amt_ent.get())
                if amt < 0:
                    messagebox.showerror("Error", "Amount paid cannot be negative")
                    return
                if self.system.discharge_patient(pid, amt):
                    p = self.system.find_patient_by_id(pid)
                    messagebox.showinfo("Success", f"Patient discharged successfully!\nPending Amount: ₹{p.pending_amount:.2f}")
                    amt_ent.delete(0, tk.END)
                    self.show_frame("DISCHARGE")
                else:
                    messagebox.showerror("Error", "Failed to discharge patient")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid numeric amount")

        dis_btn = self.create_styled_button(content, "Discharge Patient", handle_discharge, width=22)
        dis_btn.pack(pady=10)

        return frame

    # 9. Search Room Panel
    def create_search_room_panel(self) -> tk.Frame:
        frame = tk.Frame(self.container, bg=BACKGROUND_COLOR)
        header = self.create_header(frame, "Search and Book Rooms")
        header.pack(fill="x")

        content = tk.Frame(frame, bg=PANEL_COLOR, highlightbackground=PRIMARY_COLOR, highlightthickness=1, padx=20, pady=20)
        content.pack(fill="both", expand=True, padx=20, pady=20)

        search_box = tk.Frame(content, bg=PANEL_COLOR)
        search_box.pack(fill="x", pady=10)

        all_patients = self.system.get_all_patients()
        patient_opts = ["Select a patient..."] + [f"{p.patient_id} - {p.name}" for p in all_patients]

        tk.Label(search_box, text="Select Patient:", font=LABEL_FONT, bg=PANEL_COLOR).grid(row=0, column=0, sticky="w", padx=5)
        patient_combo = ttk.Combobox(search_box, values=patient_opts, font=TABLE_FONT, state="readonly", width=35)
        patient_combo.current(0)
        patient_combo.grid(row=0, column=1, sticky="w", padx=5)

        tk.Label(search_box, text="Bed Type:", font=LABEL_FONT, bg=PANEL_COLOR).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        bed_types = ["All", "Single", "Double", "General Ward", "ICU", "Maternity", "Pediatric", "Suite"]
        bed_combo = ttk.Combobox(search_box, values=bed_types, font=TABLE_FONT, state="readonly", width=15)
        bed_combo.current(0)
        bed_combo.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        cols = ("Room Number", "Bed Type", "Price", "Status")
        tree = ttk.Treeview(content, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, anchor="center", width=180)

        tree.pack(fill="both", expand=True, pady=10)

        def handle_search():
            b_type = bed_combo.get()
            all_r = self.system.get_all_rooms()
            if b_type != "All":
                all_r = [r for r in all_r if r.bed_type.lower() == b_type.lower()]

            for item in tree.get_children(): tree.delete(item)
            for r in all_r:
                st = "Available" if r.available else "Occupied"
                tree.insert("", "end", values=(r.room_number, r.bed_type, f"₹{r.price:.2f}", st))

        search_btn = self.create_styled_button(search_box, "Search Rooms", handle_search, width=15)
        search_btn.grid(row=1, column=2, padx=15)

        def handle_book():
            sel_item = tree.selection()
            p_sel = patient_combo.get()
            if not sel_item or p_sel == "Select a patient...":
                messagebox.showerror("Error", "Please select a patient and a room from the table")
                return

            pid = p_sel.split(" - ")[0]
            row_vals = tree.item(sel_item[0])['values']
            r_num, _, _, status = row_vals[0], row_vals[1], row_vals[2], row_vals[3]

            room = self.system.find_room_by_number(str(r_num))
            patient = self.system.find_patient_by_id(pid)

            if status == "Occupied" and (not patient or patient.room_number != str(r_num)):
                messagebox.showerror("Error", "This room is already occupied!")
                return

            if room and patient:
                if patient.room_number and patient.room_number != room.room_number:
                    old_room = self.system.find_room_by_number(patient.room_number)
                    if old_room:
                        old_room.available = True
                        self.system.update_room(old_room)
                room.available = False
                patient.room_number = room.room_number
                self.system.update_room(room)
                self.system.update_patient(patient)
                messagebox.showinfo("Success", f"Room {room.room_number} booked for patient {patient.name}!")
                self.show_frame("SEARCH_ROOM")

        book_btn = self.create_styled_button(content, "Book Selected Room", handle_book, width=22)
        book_btn.pack(pady=10)

        handle_search()
        return frame

    # 10. Update Patient Details Panel
    def create_update_patient_panel(self) -> tk.Frame:
        frame = tk.Frame(self.container, bg=BACKGROUND_COLOR)
        header = self.create_header(frame, "Update Patient Details")
        header.pack(fill="x")

        content = tk.Frame(frame, bg=PANEL_COLOR, highlightbackground=PRIMARY_COLOR, highlightthickness=1, padx=30, pady=30)
        content.pack(fill="both", expand=True, padx=30, pady=30)

        all_patients = self.system.get_all_patients()
        options = [f"{p.patient_id} - {p.name}" for p in all_patients]

        tk.Label(content, text="Select Patient:", font=LABEL_FONT, bg=PANEL_COLOR).pack(anchor="w", pady=5)
        combo = ttk.Combobox(content, values=options, font=TABLE_FONT, state="readonly", width=40)
        combo.pack(anchor="w", pady=5)

        form = tk.Frame(content, bg=PANEL_COLOR, pady=15)
        form.pack(fill="x")

        tk.Label(form, text="Pending Amount:", font=LABEL_FONT, bg=PANEL_COLOR).grid(row=0, column=0, sticky="w", pady=10)
        pend_ent = tk.Entry(form, font=TABLE_FONT, width=20, bd=1, relief="solid")
        pend_ent.grid(row=0, column=1, sticky="w", pady=10, padx=10)

        tk.Label(form, text="Amount Paid:", font=LABEL_FONT, bg=PANEL_COLOR).grid(row=1, column=0, sticky="w", pady=10)
        paid_ent = tk.Entry(form, font=TABLE_FONT, width=20, bd=1, relief="solid")
        paid_ent.grid(row=1, column=1, sticky="w", pady=10, padx=10)

        def on_select(event):
            sel = combo.get()
            if sel:
                pid = sel.split(" - ")[0]
                p = self.system.find_patient_by_id(pid)
                if p:
                    pend_ent.delete(0, tk.END)
                    pend_ent.insert(0, f"{p.pending_amount:.2f}")
                    paid_ent.delete(0, tk.END)
                    paid_ent.insert(0, f"{p.amount_paid:.2f}")

        combo.bind("<<ComboboxSelected>>", on_select)

        def handle_update():
            sel = combo.get()
            if not sel:
                messagebox.showerror("Error", "Please select a patient")
                return
            pid = sel.split(" - ")[0]
            try:
                pend = float(pend_ent.get())
                paid = float(paid_ent.get())
                if pend < 0 or paid < 0:
                    messagebox.showerror("Error", "Amounts cannot be negative")
                    return

                p = self.system.find_patient_by_id(pid)
                if p:
                    p.pending_amount = pend
                    p.amount_paid = paid
                    self.system.update_patient(p)
                    messagebox.showinfo("Success", "Patient details updated successfully!")
                    self.show_frame("UPDATE_PATIENT")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric amounts")

        upd_btn = self.create_styled_button(content, "Update Patient", handle_update, width=20)
        upd_btn.pack(pady=15)

        return frame

    # 11. Ambulance Service Panel
    def create_ambulance_panel(self) -> tk.Frame:
        frame = tk.Frame(self.container, bg=BACKGROUND_COLOR)
        header = self.create_header(frame, "Ambulance Service")
        header.pack(fill="x")

        table_frame = tk.Frame(frame, bg=PANEL_COLOR, padx=20, pady=20)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        cols = ("Ambulance ID", "Plate Number", "Driver Name", "Phone Number", "Status")
        tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, anchor="center", width=180)

        for a in self.system.get_all_ambulances():
            st = "Available" if a.is_available else "Ongoing"
            tree.insert("", "end", values=(a.ambulance_id, a.plate_number, a.driver_name, a.driver_phone, st))

        tree.pack(fill="both", expand=True)

        def handle_book_amb():
            sel = tree.selection()
            if not sel:
                messagebox.showerror("Error", "Please select an ambulance to book")
                return
            amb_id = tree.item(sel[0])['values'][0]
            if self.system.book_ambulance(str(amb_id)):
                messagebox.showinfo("Success", "Ambulance booked successfully!")
                self.show_frame("AMBULANCE")
            else:
                messagebox.showerror("Error", "Ambulance is not available!")

        book_btn = self.create_styled_button(table_frame, "Book Ambulance", handle_book_amb, width=20)
        book_btn.pack(pady=10)

        return frame
