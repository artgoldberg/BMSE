"""
:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2020-03-04
"""


# layout note: import statements should be sorted
import filecmp
import numpy as np
import os   # os is a useful package of operating system interfaces
import pandas as pd
import shutil
import tempfile
import unittest


# layout note: two blank lines are recommended before a class definition
class TestPandasIO(unittest.TestCase):

    def setUp(self):
        # create a temporary directory for files
        self.tempdir = tempfile.mkdtemp()

        # create some simple dataframes to be used by multiple test methods
        d = {'col1': [1, 2], 'col2': [3, 4]}
        self.df_no_index = pd.DataFrame(data=d)
        dates = pd.date_range('20130101', periods=6)
        self.df_index = pd.DataFrame(np.random.random_integers(100, size=(6, 4)), index=dates,
                                     columns=list('ABCD'))

        # read a test file in a fixtures sub-directory of the current directory
        # __file__ is the filename of the current module (except for __main__ modules)
        my_dir = os.path.dirname(__file__)
        fixtures = os.path.join(my_dir, 'fixtures')
        self.json_fixtures = [os.path.join(fixtures, f) for f in ('df.json', 'df_w_index.json')]

    # tearDown is called immediately after the test method; it's called even when the test
    # method raises an exception
    # tearDown is typically used to deallocate resources, as in this commoon pattern
    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def compare_csv_write_read(self, test_df, has_index=False):
        """ round-trip test: csv write and read
        """
        # if test_df has an index, write and read it
        index_col = None
        if has_index:
            index_col = 0
        # make a new temp file in the temp directory
        _, path = tempfile.mkstemp(suffix='.csv', dir=self.tempdir)
        # write the df
        test_df.to_csv(path, index=has_index)   # to_csv writes csv file in path
        df_read = pd.read_csv(path, index_col=index_col)    # read_csv reads csv file in path
        # the initial data frame (test_df) should equal the one read from the file (df_read)
        self.assertTrue(pd.DataFrame.equals(df_read, test_df))

    def test_csv_write_read(self):
        # round-trip test: csv write and read
        # writes a couple of files in the temp dir
        self.compare_csv_write_read(self.df_no_index)
        self.compare_csv_write_read(self.df_index, has_index=True)

    def test_json(self):
        # round-trip test: JSON write and read
        for test_df in [self.df_no_index, self.df_index]:
            # convert df to a string
            json_string = test_df.to_json()
            # read the string into a df
            df_read = pd.read_json(json_string)
            self.assertTrue(pd.DataFrame.equals(df_read, test_df))
            try:
                pd.testing.assert_frame_equal(df_read, test_df)
            except AssertionError as e:
                self.fail(str(e))
                # an alternative: raise self.failureException(msg) from e

            # test round-trip read and write of JSON files
            for json_path in self.json_fixtures:
                # read the existing file
                df_read = pd.read_json(json_path)
                _, path = tempfile.mkstemp(suffix='.json', dir=self.tempdir)
                # write the file that was just read into another file
                df_read.to_json(path)
                # compare them
                # shallow=False means compare the file contents
                self.assertTrue(filecmp.cmp(json_path, path, shallow=False))
