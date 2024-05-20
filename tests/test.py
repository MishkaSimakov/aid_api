import unittest

from unit.ticker.BasicTests import TickerBasicTests
from unit.ticker.IndicatorsTests import TickerIndicatorsTests

if __name__ == '__main__':
    loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()

    test_suite.addTests(loader.loadTestsFromTestCase(TickerBasicTests))
    test_suite.addTests(loader.loadTestsFromTestCase(TickerIndicatorsTests))

    testRunner = unittest.runner.TextTestRunner()
    testRunner.run(test_suite)
