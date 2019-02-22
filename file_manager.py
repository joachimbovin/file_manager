# -*- coding: utf-8 -*-

import pandas as pd
import os
import re
from json import load
import zipfile


class file_manager(object):
    def __init__(self, path_to_students="../Resources/students_dict.json",
                 path_to_gradebook="./gradebook",
                 path_to_resources="./Resources",
                 path_to_main=".."):
        self.path_to_main = path_to_main
        self.text_files = None
        self.path_to_resources = path_to_resources
        self.path_to_students_dict = path_to_students
        self.path_to_gradebook = path_to_gradebook
        self.students_dict = None
        self.main_dir = None
        self.students = None
        self.studentname_filename = None

    def get_dir(self):
        """Get the location of the current directory"""
        self.main_dir = os.getcwd()
        #print (self.main_dir)
        #self.main_dir = Path.cwd()
        print (self.main_dir)


    def go_to_gradebook(self):
        """Go to location that contains the files (Resources)"""
        main = os.path.abspath(self.path_to_gradebook)
        print (main)
        os.chdir(main)

    def go_to_main(self):
        """Go to the main directory (file_manager)"""
        os.chdir(self.path_to_main)
        print (self.path_to_main)

    def get_all_txt_files(self):
        """Get all the text files in current directory and store them as a list"""
        filename= os.listdir (".")
        text_files = []
        for item in filename:
            if ".txt" in item:
                text_files.append(item)
        self.text_files = text_files

    def read_all_txt_files(self, i):
        """Function that iterates through the list with text files, reads each individual text file and returns
        the contents as a list
        :param i """
        my_list = []
        with open(self.text_files[i]) as file:
            text = file.readlines()
            for line in text:
                line_stripped = line.rstrip("\n")
                my_list.append(line_stripped)
        return my_list

    def read_students_dict(self):
        """Function that reads in the JSON file to store the information about the students"""
        #print (self.path_to_students_dict)
        with open(self.path_to_students_dict, "r", encoding="utf-8", buffering=1) as f:
            self.students_dict = load(f)


    def create_metadata_dict(self):
        """Create a dictionary with all the metadata about the students and stores this as a dataframe (class
        variable students"""
        problems_students = []
        for i in range(len(self.text_files)):
            my_list = self.read_all_txt_files(i)
            naam_student = my_list[0]
            q_nummer = re.findall(r'\(.+?\)', naam_student)
            if len(my_list) > 1:
                opdracht = my_list[1]
                bestands_naam = my_list[-2]
                extension = re.findall(r'.\w+$', bestands_naam)
                datum = my_list[2]
                hour = re.findall(r'[0-9][0-9]:[0-9][0-9]:[0-9][0-9]', datum)
                self.students_dict["naam_student"].append(naam_student[6:-11])
                try:
                    self.students_dict["extensie"].append(extension[0])
                except IndexError:
                    self.students_dict["extensie"].append("null")
                try:
                    self.students_dict["opdracht"].append(opdracht[10:])
                except IndexError:
                    self.students_dict["opdracht"].append("null")
                    problems_students.append(naam_student[6:-11])
                try:
                    self.students_dict["bestands_naam"].append(bestands_naam[15:-4])   #CHANGE!!
                except IndexError:
                    self.students_dict["bestands_naam"].append("null")
                    problems_students.append(naam_student[6:-11])
                try:
                    self.students_dict["bestands_naam_full"].append(bestands_naam[15:])
                except IndexError:
                    self.students_dict["bestands_naam_full"].append("null")
                self.students_dict["datum"].append(datum[14:-17])
                try:
                    self.students_dict["q_nummer"].append(q_nummer[0][1:-1])
                except IndexError:
                    self.students_dict["q_nummer"].append("null")
                    problems_students.append(naam_student[6:-11])
                if len(hour) != 0:
                    self.students_dict["hour"].append(hour[0])
                else:
                    self.students_dict["hour"].append("00:00:00")
                self.students_dict["punt"].append(0)
            else:
                pass
        self.students = pd.DataFrame(data=self.students_dict)
        print (self.students.head(n=20))


    def create_csv_students(self):
        """Creates a csv that contains the metadata about all the students as obtained from
        the .txt and stored in the dataframe self.students.
        Must be called after the function create_metadata_dict() """
        self.students.to_csv("portfolio_3_overzicht_zips.csv", sep=",", encoding="utf-8", index=False)


    def create_csv(self):
        """Combines previous methods to create a csv"""
        #self.get_dir()
        current_dir = os.getcwd()
        if current_dir == os.path.abspath(self.path_to_gradebook):
            pass
        else:
            self.go_to_gradebook()
        self.get_all_txt_files()
        self.read_students_dict()
        self.create_metadata_dict()
        self.create_csv_students()
        self.go_to_main()



    def unzip_files(self):
        """function to unzip all .zip files and store the unzipped files in a new folder"""
        #self.go_to_main()
        #self.go_to_gradebook()
        extension = ".zip"
        bad_zips = []
        for item in os.listdir("."):  #iterate over the files in the folder
            print (item)
            if item.endswith(extension):
                file_name = os.path.abspath(item)  # get full path of files
                real_name = item[:-4]
                print (file_name)
                print (real_name)
                cwd = os.getcwd()
                new_dir = os.mkdir(cwd + "/" + real_name)  # create new file to unpack zip
                with zipfile.ZipFile(file_name, 'r') as zip_ref:
                    try:
                        zip_ref.extractall(cwd + "/" + real_name)
                    except (zipfile.BadZipfile, zipfile.BadZipFile("File is not a zip file")):
                        bad_zips.append(file_name)
                        continue
                os.remove(file_name)  # delete zipped file


    def unzip_all_files(self):
        current_dir = os.getcwd()
        if current_dir == os.path.abspath(self.path_to_gradebook):
            pass
        else:
            self.go_to_gradebook()
        self.get_all_txt_files()
        self.read_students_dict()
        self.create_metadata_dict()
        self.unzip_files()
        self.go_to_main()


    def rename_folders(self):
        """Class method to rename all the files to the name of the student"""
        for index, row in self.students.iterrows():
            bestands_naam = row["bestands_naam"]
            naam_student = row["naam_student"]
            filename = os.listdir (".")
            for my_file in filename:
                #print (my_file)
                #print (bestands_naam)
                if my_file == bestands_naam:
                    #print (my_file)
                    current_dir = os.getcwd()
                    os.rename(my_file, current_dir + "/" + naam_student)
                else:
                    pass
                    #print ("file not found")

    def rename_all_folders(self):
        self.go_to_gradebook()
        self.get_all_txt_files()
        self.read_students_dict()
        self.create_metadata_dict()
        self.rename_folders()
        self.go_to_main()

    def remove_txt_files(self):
        current_dir = os.getcwd()
        if current_dir == os.path.abspath(self.path_to_gradebook):
            pass
        else:
            self.go_to_gradebook()
        self.get_all_txt_files()
        for file in self.text_files:
            os.remove(file)
        self.go_to_main()


    def make_key_value_pair(self):
        """read the name of the student (first line) and name of the corresponding assignment (last line) and
            store this in a dictionary (my_dict) as a key-value pair. """
        self.studentname_filename = {}
        for i in range(len(self.text_files)):
            with open(self.text_files[i]) as file:
                name_student = file.readline()  # read first line
                name_student_short = name_student[6:]  # remove Naam:
                name_student_strip = name_student_short.rstrip("\n")  # remove trailing white space
            with open(self.text_files[i]) as file:
                name_excel = file.readlines()[-2]  # read last line
                name_excel_short = name_excel[15:]  # remove Document name:
                name_excel_strip = name_excel_short.rstrip("\n")  # remove trailing white space
            self.studentname_filename[name_excel_strip] = name_student_strip  # make key-value pair
            print (self.studentname_filename)


    def rename_files(self):
        """rename all the files based on the extension provided
        :var provide the file extension for isntance .docx or .xlsx"""
        current_dir = os.getcwd()
        for index, row in self.students.iterrows():
            extension = row["extensie"]
            bestandsnaam_full = row["bestands_naam_full"]
            for item in self.studentname_filename:
                if bestandsnaam_full == item:
                     os.rename(item, current_dir + "/" + self.studentname_filename[item] + extension)


    def rename_all_files(self):
        self.go_to_gradebook()
        self.get_all_txt_files()
        self.read_students_dict()
        self.make_key_value_pair()
        self.create_metadata_dict()
        self.rename_files()
        self.go_to_main()


    def get_file_extension(self):
        self.go_to_gradebook()
        self.get_all_txt_files()
        self.read_students_dict()
        self.create_metadata_dict()
        extension = self.students["extensie"]
        print (extension)
        return extension




#if __name__ == "__main__":



#work with docx files?
#remove .txt files?
#...?

