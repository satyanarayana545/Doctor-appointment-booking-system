import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk
import sqlite3
from datetime import datetime, timedelta

class Patient:
    def __init__(self, name, age, gender, diagnosis):
        self.name = name
        self.age = age
        self.gender = gender
        self.diagnosis = diagnosis

class Doctor:g
    def __init__(self, name):
        self.name = name

def book_appointment():
    def submit():
        try:
            age = int(patient_age_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid age.")
            return

        conn = sqlite3.connect('royal_hospital.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS appointments
                     (patient_name text, age integer, gender text, diagnosis text, doctor_name text, appointment_date text, appointment_time text)''')

        patient = Patient(patient_name_entry.get(), age, patient_gender_var.get(), patient_diagnosis_var.get())
        doctor = Doctor(doctor_var.get())

        c.execute("INSERT INTO appointments VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (patient.name, patient.age, patient.gender, patient.diagnosis, doctor.name,
                   appointment_date_var.get(), appointment_time_var.get()))

        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Appointment submitted successfully!")
        clear_fields()

    def cancel():
        conn = sqlite3.connect('royal_hospital.db')
        c = conn.cursor()
        c.execute("SELECT * FROM appointments")
        appointments = c.fetchall()
        appointment_str = "\n".join([f"Patient: {app[0]}, Date: {app[5]}, Time: {app[6]}" for app in appointments])

        selected_appointment = simpledialog.askstring("Cancel Appointment",
                                                      f"Available Appointments:\n{appointment_str}\n\nEnter the name of the patient to cancel appointment:")

        c.execute("SELECT * FROM appointments WHERE patient_name=?", (selected_appointment,))
        p = c.fetchall()

        if p:
            c.execute("DELETE FROM appointments WHERE patient_name=?", (selected_appointment,))
            messagebox.showinfo("Success", "Appointment cancelled successfully!")
        else:
            messagebox.showinfo("No record found", "Enter valid name")

        conn.commit()
        conn.close()

    def display_appointments():
        popup_window = tk.Toplevel(window)
        popup_window.title("Appointments")

        # Add a frame for filters and sorting
        filter_frame = ttk.Frame(popup_window)
        filter_frame.pack(padx=10, pady=10, fill=tk.X)

        ttk.Label(filter_frame, text="Filter by Doctor:").pack(side=tk.LEFT, padx=5)
        doctor_filter_var = tk.StringVar()
        doctor_filter_dropdown = ttk.Combobox(filter_frame, textvariable=doctor_filter_var, values=["All"] + doctor_list, state="readonly")
        doctor_filter_dropdown.pack(side=tk.LEFT, padx=5)
        doctor_filter_dropdown.current(0)

        # Add a button to apply the filter
        def apply_filter():
            selected_doctor = doctor_filter_var.get()
            conn = sqlite3.connect('royal_hospital.db')
            c = conn.cursor()
            
            if selected_doctor == "All":
                c.execute("SELECT * FROM appointments")
            else:
                c.execute("SELECT * FROM appointments WHERE doctor_name=?", (selected_doctor,))
            
            appointments = c.fetchall()
            appointments_text.delete(1.0, tk.END)
            
            for appointment in appointments:
                appointments_text.insert(tk.END, f"Patient: {appointment[0]}\n")
                appointments_text.insert(tk.END, f"Age: {appointment[1]}\n")
                appointments_text.insert(tk.END, f"Gender: {appointment[2]}\n")
                appointments_text.insert(tk.END, f"Diagnosis: {appointment[3]}\n")
                appointments_text.insert(tk.END, f"Doctor Name: {appointment[4]}\n")
                appointments_text.insert(tk.END, f"Appointment Date: {appointment[5]}\n")
                appointments_text.insert(tk.END, f"Appointment Time: {appointment[6]}\n\n")
            
            conn.close()

        apply_filter_button = tk.Button(filter_frame, text="Apply Filter", command=apply_filter)
        apply_filter_button.pack(side=tk.LEFT, padx=5)

        # Add a text widget to display appointments
        appointments_text = tk.Text(popup_window, width=80, height=20)
        appointments_text.pack(padx=10, pady=10)

        # Load all appointments initially
        apply_filter()

        # Add a close button
        close_button = tk.Button(popup_window, text="Close", command=popup_window.destroy)
        close_button.pack(pady=10)

    def clear_fields():
        patient_name_entry.delete(0, tk.END)
        patient_age_entry.delete(0, tk.END)
        patient_gender_var.set('')
        patient_diagnosis_var.set('')
        appointment_date_var.set('')

    def generate_dates():
        start_date = datetime.now()
        dates = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]
        return dates

    window = tk.Tk()
    window.title("Royal Hospital - Appointment Booking")
    window.geometry("500x500")
    window.configure(bg="#f0f4f7")

    # Define styles
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 10), padding=6)
    style.configure("TLabel", font=("Arial", 11), background="#f0f4f7")

    # Main heading
    header_label = ttk.Label(window, text="Welcome to Royal Hospital", font=("Arial", 16, "bold"), foreground="#4A90E2")
    header_label.pack(pady=10)

    # Subheading
    subheading_label = ttk.Label(window, text="Book and Cancel Appointment", font=("Arial", 14), foreground="#E94E77")
    subheading_label.pack(pady=5)

    # Form Frame
    form_frame = ttk.Frame(window)
    form_frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    ttk.Label(form_frame, text="Patient Name:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
    patient_name_entry = ttk.Entry(form_frame)
    patient_name_entry.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(form_frame, text="Age:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
    patient_age_entry = ttk.Entry(form_frame)
    patient_age_entry.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(form_frame, text="Gender:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
    patient_gender_var = tk.StringVar()
    patient_gender_entry = ttk.Combobox(form_frame, textvariable=patient_gender_var, values=["Male", "Female", "Other"])
    patient_gender_entry.grid(row=2, column=1, padx=10, pady=10)

    ttk.Label(form_frame, text="Diagnosis:").grid(row=3, column=0, padx=10, pady=10, sticky=tk.E)
    patient_diagnosis_var = tk.StringVar()
    diagnosis_list = ["Flu", "Cold", "Headache", "Stomach Ache", "Back Pain", "Fever", "Cough", "Sore Throat"]
    patient_diagnosis_entry = ttk.Combobox(form_frame, textvariable=patient_diagnosis_var, values=diagnosis_list, state="readonly")
    patient_diagnosis_entry.grid(row=3, column=1, padx=10, pady=10)
    patient_diagnosis_entry.current(0)

    ttk.Label(form_frame, text="Doctor:").grid(row=4, column=0, padx=10, pady=10, sticky=tk.E)
    doctor_list = ["Dr.Prasanth, General", "Dr.Anitha, Pediatrician", "Dr.Kishore, Neurologist", "Dr.Srinivas, Surgeon"]
    doctor_var = tk.StringVar()
    doctor_dropdown = ttk.Combobox(form_frame, textvariable=doctor_var, values=doctor_list, state="readonly")
    doctor_dropdown.grid(row=4, column=1, padx=10, pady=10)
    doctor_dropdown.current(0)

    ttk.Label(form_frame, text="Appointment Date:").grid(row=5, column=0, padx=10, pady=10, sticky=tk.E)
    appointment_date_var = tk.StringVar()
    date_dropdown = ttk.Combobox(form_frame, textvariable=appointment_date_var, values=generate_dates(), state="readonly")
    date_dropdown.grid(row=5, column=1, padx=10, pady=10)

    ttk.Label(form_frame, text="Appointment Time:").grid(row=6, column=0, padx=10, pady=10, sticky=tk.E)
    time_options = ["9:00 AM", "9:30 AM", "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM", "12:00 PM"]
    appointment_time_var = tk.StringVar()
    time_dropdown = ttk.Combobox(form_frame, textvariable=appointment_time_var, values=time_options, state="readonly")
    time_dropdown.grid(row=6, column=1, padx=10, pady=10)
    time_dropdown.current(0)

    # Buttons Frame
    button_frame = tk.Frame(window)
    button_frame.pack(side=tk.BOTTOM, pady=20)

    submit_button = tk.Button(button_frame, text="Book Appointment", command=submit, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
    submit_button.grid(row=0, column=0, padx=10)

    cancel_button = tk.Button(button_frame, text="Cancel Appointment", command=cancel, bg="#f44336", fg="white", font=("Arial", 10, "bold"))
    cancel_button.grid(row=0, column=1, padx=10)

    display_button = tk.Button(button_frame, text="Display Appointments", command=display_appointments, bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
    display_button.grid(row=0, column=2, padx=10)

    window.mainloop()

book_appointment()
