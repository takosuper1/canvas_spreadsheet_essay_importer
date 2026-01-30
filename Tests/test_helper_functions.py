import unittest
import pandas as pd
from Main.helper_functions import check_file_type


class TestDataFrameHeader(unittest.TestCase):
    def test_check_filetype(self):
        # setup paths to both types
        csvfilepath = "Tests/Sample_Data/generaluploadsample.csv"
        excelfilepath = "Tests/Sample_Data/Tutor Log Form 1.xlsx"
        isExcel = "XLSX"
        isCSV = "CSV"
        # Test if csv
        self.assertIn(
            isCSV,
            check_file_type(csvfilepath),
            "test_check_filetype is not processing CSV",
        )
        self.asserFalse()
