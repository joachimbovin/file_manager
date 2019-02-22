# -*- coding: utf-8 -*-

from unittest import TestCase
#from bs4 import BeautifulSoup
import pandas as pd
from collections import Counter
import os
import re
import zipfile
from file_manager import file_manager
from pathlib import Path



class manager_test(TestCase):
    def setUp(self):
        self.file_manager = file_manager(path_to_students="../Resources/students_dict.json",
                                         path_to_gradebook="../gradebook",
                                         path_to_main="..")

    def test_get_dir(self):
        self.file_manager.get_dir()
        self.file_manager.go_to_gradebook()
        self.file_manager.get_all_txt_files()

    def test_get_dir_2(self):
        self.file_manager.get_dir()

    def test_create_dict(self):
        self.file_manager.get_all_txt_files()
        self.file_manager.read_students_dict()
        self.file_manager.create_metadata_dict()

    def test_create_students_dict(self):
        #self.file_manager.get_dir()
        self.file_manager.go_to_gradebook()
        self.file_manager.get_all_txt_files()
        self.file_manager.read_students_dict()
        #self.file_manager.get_dir()
        self.file_manager.create_metadata_dict()

    def test_create_csv(self):
        self.file_manager.go_to_gradebook()
        self.file_manager.get_all_txt_files()
        self.file_manager.read_students_dict()
        self.file_manager.create_metadata_dict()
        self.file_manager.create_csv_students()


    def test_unzip_files(self):
        self.file_manager.go_to_gradebook()
        self.file_manager.get_all_txt_files()
        self.file_manager.read_students_dict()
        self.file_manager.create_metadata_dict()
        self.file_manager.unzip_files()


    def test_rename_files(self):
        self.file_manager.go_to_gradebook()
        self.file_manager.get_all_txt_files()
        self.file_manager.read_students_dict()
        self.file_manager.create_metadata_dict()
        #self.file_manager.create_csv_students()
        self.file_manager.rename_folders()


    def test_unzip_rename_files(self):
        self.file_manager.go_to_gradebook()
        self.file_manager.get_all_txt_files()
        self.file_manager.read_students_dict()
        self.file_manager.create_metadata_dict()
        self.file_manager.unzip_files()
        #self.file_manager.rename_files()

    def test_rename_files_2(self):
        self.file_manager.go_to_gradebook()
        self.file_manager.get_all_txt_files()
        self.file_manager.read_students_dict()
        self.file_manager.create_metadata_dict()
        self.file_manager.rename_folders()



    def test_remove_test_files(self):
        self.file_manager.remove_txt_files()


    def test_rename_all_files(self):
        self.file_manager.rename_all_files()

    def test_get_file_extension(self):
        self.file_manager.get_file_extension()

    def test_key_value(self):
        self.file_manager.go_to_gradebook()
        self.file_manager.get_all_txt_files()
        self.file_manager.make_key_value_pair()


