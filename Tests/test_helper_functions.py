import unittest
import os
import tempfile
from Main.helper_functions import check_file_type, UnsupportedFileTypeError, FileNotFoundError


class TestCheckFileType(unittest.TestCase):

    def test_check_filetype_csv(self):
        """Test CSV file detection"""
        csvfilepath = "Tests/Sample_Data/generaluploadsample.csv"
        result = check_file_type(csvfilepath)
        self.assertEqual(result, "CSV", "CSV file not correctly identified")

    def test_check_filetype_xlsx(self):
        """Test XLSX file detection"""
        excelfilepath = "Tests/Sample_Data/Tutor Log Form 1.xlsx"
        result = check_file_type(excelfilepath)
        self.assertEqual(result, "XLSX", "XLSX file not correctly identified")

    def test_check_filetype_ods(self):
        """Test ODS file detection (if you have sample ODS files)"""
        ods_path = "Tests/Sample_Data/sample.ods"
        if os.path.exists(ods_path):
            result = check_file_type(ods_path)
            self.assertEqual(result, "ODS", "ODS file not correctly identified")
        else:
            self.skipTest("ODS sample file not available")

    def test_check_filetype_nonexistent_file(self):
        """Test that FileNotFoundError is raised for non-existent files"""
        nonexistent_path = "Tests/Sample_Data/nonexistent_file.csv"
        with self.assertRaises(FileNotFoundError) as context:
            check_file_type(nonexistent_path)
        self.assertIn("does not exist", str(context.exception))

    def test_check_filetype_directory(self):
        """Test that FileNotFoundError is raised when path is a directory"""
        # Use a directory that should exist
        directory_path = "Tests/Sample_Data"
        if os.path.exists(directory_path):
            with self.assertRaises(FileNotFoundError) as context:
                check_file_type(directory_path)
            self.assertIn("not a file", str(context.exception))
        else:
            self.skipTest("Test directory not available")

    def test_check_filetype_unsupported_pdf(self):
        """Test that UnsupportedFileTypeError is raised for PDF files"""
        # Create a temporary file with PDF-like content
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.pdf', delete=False) as f:
            pdf_path = f.name
            # Write PDF header
            f.write(b'%PDF-1.4\n')
            f.write(b'Some PDF content here')

        try:
            with self.assertRaises(UnsupportedFileTypeError) as context:
                check_file_type(pdf_path)
            self.assertIn("Unsupported file type", str(context.exception))
            self.assertIn("MIME type", str(context.exception))
        finally:
            os.unlink(pdf_path)

    def test_check_filetype_unsupported_image(self):
        """Test that UnsupportedFileTypeError is raised for image files"""
        # Create a minimal PNG file
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.png', delete=False) as f:
            png_path = f.name
            # PNG signature
            f.write(b'\x89PNG\r\n\x1a\n')

        try:
            with self.assertRaises(UnsupportedFileTypeError) as context:
                check_file_type(png_path)
            self.assertIn("Unsupported file type", str(context.exception))
        finally:
            os.unlink(png_path)

    def test_check_filetype_empty_file(self):
        """Test that UnsupportedFileTypeError is raised for empty files"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            empty_path = f.name
            # Write nothing - file is empty

        try:
            with self.assertRaises(UnsupportedFileTypeError) as context:
                check_file_type(empty_path)
            self.assertIn("empty", str(context.exception))
        finally:
            os.unlink(empty_path)

    def test_check_filetype_csv_with_commas(self):
        """Test CSV file with comma delimiters"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            csv_path = f.name
            f.write("Column1,Column2,Column3\n")
            f.write("Value1,Value2,Value3\n")

        try:
            result = check_file_type(csv_path)
            self.assertEqual(result, "CSV", "CSV file with commas not correctly identified")
        finally:
            os.unlink(csv_path)

    def test_check_filetype_text_without_commas(self):
        """Test that plain text files without commas raise UnsupportedFileTypeError"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            txt_path = f.name
            f.write("This is just plain text without any delimiters\n")
            f.write("Another line of text\n")

        try:
            with self.assertRaises(UnsupportedFileTypeError) as context:
                check_file_type(txt_path)
            self.assertIn("does not appear to be a valid CSV", str(context.exception))
        finally:
            os.unlink(txt_path)

    def test_check_filetype_invalid_encoding(self):
        """Test that IOError is raised for files with invalid UTF-8 encoding"""
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False) as f:
            invalid_path = f.name
            # Write invalid UTF-8 bytes
            f.write(b'\xff\xfe Invalid UTF-8')

        try:
            with self.assertRaises(IOError) as context:
                check_file_type(invalid_path)
            self.assertIn("UTF-8 encoding", str(context.exception))
        finally:
            os.unlink(invalid_path)

    def test_check_filetype_csv_mime_type(self):
        """Test CSV file that's explicitly detected as text/csv MIME type"""
        # This test depends on having a file that magic detects as text/csv
        # You may need to adjust based on your actual sample files
        csvfilepath = "Tests/Sample_Data/generaluploadsample.csv"
        if os.path.exists(csvfilepath):
            result = check_file_type(csvfilepath)
            self.assertEqual(result, "CSV")

    def test_check_filetype_returns_correct_types(self):
        """Test that return values are strings and one of the expected types"""
        csvfilepath = "Tests/Sample_Data/generaluploadsample.csv"
        if os.path.exists(csvfilepath):
            result = check_file_type(csvfilepath)
            self.assertIsInstance(result, str)
            self.assertIn(result, ["CSV", "XLSX", "ODS"])


class TestCheckFileTypeEdgeCases(unittest.TestCase):
    """Additional edge case tests"""

    def test_check_filetype_csv_single_column(self):
        """Test CSV file with single column (no commas)"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            csv_path = f.name
            f.write("SingleColumn\n")
            f.write("Value1\n")
            f.write("Value2\n")

        try:
            # This might raise UnsupportedFileTypeError based on your logic
            # Adjust the assertion based on your desired behavior
            with self.assertRaises(UnsupportedFileTypeError):
                check_file_type(csv_path)
        finally:
            os.unlink(csv_path)

    def test_check_filetype_csv_with_header_only(self):
        """Test CSV file with only header row"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            csv_path = f.name
            f.write("Column1,Column2,Column3\n")

        try:
            result = check_file_type(csv_path)
            self.assertEqual(result, "CSV")
        finally:
            os.unlink(csv_path)


if __name__ == '__main__':
    unittest.main()