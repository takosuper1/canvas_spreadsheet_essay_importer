import pandas as pd
import unittest


class TestDataFrameHeader(unittest.TestCase):
    def test_header_contains_essay(self):
        # Test for general  upload (not canvas related)
        df = pd.read_csv("./Sample_Data/generaluploadsample.csv")
        # Convert headers to lowercase to avoid case issues.
        lower_headers = df.columns.str.lower()

        target_word = "essay"

        self.assertIn(
            target_word,
            lower_headers,
            f"{target_word} not found in dataframe headers.",
        )

    def test_header_contains_ItemType(self):
        return

    def test_header_contains_Attempt(self):
        return


if __name__ == "__main__":
    unittest.main()
