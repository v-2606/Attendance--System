import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk
from tkinter import *

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get()
        if Subject == "":
            t = 'Please enter the subject name.'
            text_to_speech(t)
            return

        # Store the original working directory
        original_dir = os.getcwd()
        
        try:
            # Construct the directory path
            subject_dir = os.path.join("Attendance", Subject)
            
            # Check if the directory exists
            if not os.path.exists(subject_dir):
                t = f"The directory for subject '{Subject}' does not exist."
                text_to_speech(t)
                return
            
            # Get all CSV files for this subject
            file_pattern = os.path.join(subject_dir, f"{Subject}*.csv")
            filenames = glob(file_pattern)
            
            if not filenames:
                t = f"No attendance records found for {Subject}"
                text_to_speech(t)
                return
            
            # Read and process all CSV files
            df = [pd.read_csv(f) for f in filenames]
            newdf = df[0]
            
            for i in range(1, len(df)):
                newdf = newdf.merge(df[i], how="outer")
            
            newdf.fillna(0, inplace=True)
            newdf["Attendance"] = 0
            
            # Calculate attendance percentage
            for i in range(len(newdf)):
                attendance_cols = newdf.iloc[i, 2:-1]
                attendance_mean = attendance_cols.mean() * 100
                newdf.loc[i, "Attendance"] = f"{int(round(attendance_mean))}%"
            
            # Save the consolidated attendance
            output_file = os.path.join(subject_dir, "attendance.csv")
            newdf.to_csv(output_file, index=False)
            
            # Display the attendance in GUI
            root = tkinter.Tk()
            root.title("Attendance of " + Subject)
            root.configure(background="black")
            
            # Read and display the saved attendance file
            with open(output_file) as file:
                reader = csv.reader(file)
                for r, col in enumerate(reader):
                    for c, row in enumerate(col):
                        label = tkinter.Label(
                            root,
                            width=10,
                            height=1,
                            fg="yellow",
                            font=("times", 15, " bold "),
                            bg="black",
                            text=row,
                            relief=tkinter.RIDGE,
                        )
                        label.grid(row=r, column=c)
            
            # Print for debugging
            print("Attendance DataFrame:")
            print(newdf)
            
        except Exception as e:
            t = f"Error processing attendance: {str(e)}"
            text_to_speech(t)
            print(f"Error: {str(e)}")
        
        finally:
            # Return to original directory
            os.chdir(original_dir)

    subject = Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")
    titl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)
    titl = tk.Label(
        subject,
        text="Which Subject of Attendance?",
        bg="black",
        fg="green",
        font=("arial", 25),
    )
    titl.place(x=100, y=12)

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            os.startfile(os.path.join("Attendance", sub))

    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=10,
        relief=RIDGE,
    )
    attf.place(x=360, y=170)

    sub = tk.Label(
        subject,
        text="Enter Subject",
        width=10,
        height=2,
        bg="black",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("times new roman", 15),
    )
    sub.place(x=50, y=100)

    tx = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="black",
        fg="yellow",
        relief=RIDGE,
        font=("times", 30, "bold"),
    )
    tx.place(x=190, y=100)

    fill_a = tk.Button(
        subject,
        text="View Attendance",
        command=calculate_attendance,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=12,
        relief=RIDGE,
    )
    fill_a.place(x=195, y=170)
    subject.mainloop()
