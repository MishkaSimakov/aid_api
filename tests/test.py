import unittest

from unit.file_manager.FileManagerTests import FileManagerTests
from unit.generators.MazeGeneratorTests import MazeGeneratorTests
from unit.maze.MazePositionTests import MazePositionTests
from unit.maze.MazeTests import MazeTests
from unit.maze.ThickMazeTests import ThickMazeTests
from unit.solvers.MazeSolverTests import MazeSolverTests

if __name__ == '__main__':
    loader = unittest.TestLoader()

    test_suite = unittest.TestSuite()

    test_suite.addTests(loader.loadTestsFromTestCase(FileManagerTests))

    test_suite.addTests(loader.loadTestsFromTestCase(MazeGeneratorTests))

    test_suite.addTests(loader.loadTestsFromTestCase(MazePositionTests))
    test_suite.addTests(loader.loadTestsFromTestCase(MazeTests))
    test_suite.addTests(loader.loadTestsFromTestCase(ThickMazeTests))

    test_suite.addTests(loader.loadTestsFromTestCase(MazeSolverTests))

    testRunner = unittest.runner.TextTestRunner()
    testRunner.run(test_suite)
