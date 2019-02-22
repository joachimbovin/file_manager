import os
import tkinter
import tkinter.messagebox as messagebox
from file_manager import file_manager

file_manager = file_manager()

top = tkinter.Tk()

photo = tkinter.PhotoImage(file="title_3.png")
w = tkinter.Label(top, image=photo)
w.pack()


def show_directory():
    file_manager.get_dir()
    messagebox.showinfo( "This is the current directory", file_manager.main_dir)

def close_window():
    top.destroy()

def about_file_manager():
    messagebox.showinfo( "About", """File Manager is an application written in the Python programming language that helps you manage files exported from the Blackboard learning management system. 
    
    File Manager allows you to create a CSV with an overview of relevant metadata, unzip all the files in a specific directory and rename the files using student names.
    
    Created by Joachim Bovin"""
                                  )


def instructions_button():
    messagebox.showinfo("Instructions", """In order for File Manager to work correctly it is important that you follow these instructions
    
    1. Rename the folder containing your files to "gradebook" and place it in the folder file_manager. This folder should also
     contain file_manager.py and GUI.py
    2. That's it :)"""
                        )

instructions = tkinter.Button(top, text ="Instructions", command = instructions_button)

about = tkinter.Button(top, text ="About", command = about_file_manager)

B = tkinter.Button(top, text ="Create CSV", command = file_manager.create_csv)

C = tkinter.Button(top, text="Show current directory", command = show_directory)

A = tkinter.Button(top, text ="Unzip all files", command = file_manager.unzip_all_files)

D = tkinter.Button(top, text ="Rename all files", command = file_manager.rename_all_files)

remove_txt = tkinter.Button(top, text ="Remove all .txt files", command = file_manager.remove_txt_files)

E = tkinter.Button(top, text ="Close File Manager", command = close_window)



top.geometry("500x250")
top.configure(background="white")

#C.pack()
instructions.pack()
B.pack()
A.pack()
D.pack()
remove_txt.pack()
about.pack()
E.pack()

# Code to add widgets will go here...
top.mainloop()