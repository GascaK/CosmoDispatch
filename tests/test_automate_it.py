import unittest
import pyautogui as pyg

from automate_it import AutomateIt, UnableToLocateError


class TestAutomateIt(unittest.TestCase):
    def setUp(self):
        self.ait = AutomateIt()
        self.test_screen = 'tests/TestScreenshots/test_screen.png'

    def test_find_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.ait.find('File_Not_Here.png')

    def test_find_item_not_located_on_screen(self):
        with self.assertRaises(UnableToLocateError):
            self.ait.find(self.test_screen)

    def test_find_region_invalid_tuple(self):
        with self.assertRaises(UnableToLocateError):
            self.ait.find(self.test_screen, reg=('a', 'b', 'c', 'd'))

    def test_find_attempt_amount_invalid_int(self):
        with self.assertRaises(TypeError):
            self.ait.find(self.test_screen, attempt_amount='string')

    def test_mouse_click_invalid_x_and_y(self):
        with self.assertRaises(TypeError):
            self.ait.mouse_click(None, x='X', y='Y')


if __name__ == '__main__':
    unittest.main()
