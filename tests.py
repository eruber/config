#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
if __name__ == "__main__":

    import unittest

    loader = unittest.TestLoader()

    test_dir = "tests"

    suite = loader.discover(test_dir)

    runner = unittest.TextTestRunner()
    runner.run(suite)
