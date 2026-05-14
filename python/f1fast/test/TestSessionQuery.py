import unittest
from unittest.mock import MagicMock
import pandas as pd
import python.f1fast.main.querys.SessionQuery as sq
import python.f1fast.main.errors.Errors as e


class TestSessionQuerys(unittest.TestCase):

    def setUp(self):

        self.mock_session = MagicMock()

        data = {
            "DriverNumber": ["1", "11", "4", "81"],
            "LastName": ["Verstappen", "Perez", "Norris", "Piastri"],
            "TeamName": ["Red Bull", "Red Bull", "McLaren", "McLaren"]
        }

        self.mock_session.results = pd.DataFrame(data)

    def test_get_driver_teammate_success(self):
        teammate = sq.get_driver_teammate("1", self.mock_session)
        self.assertEqual(teammate.DriverNumber, "11")

    def test_get_driver_teammate_not_found(self):
        with self.assertRaises(e.DriverNotFoundError):
            sq.get_driver_teammate("99", self.mock_session)

    def test_get_driver_number_from_lastname_success(self):
        number = sq.get_driver_number_from_lastname("Norris", self.mock_session)
        self.assertEqual(number, "4")

    def test_get_driver_number_lastname_error(self):
        with self.assertRaises(e.DriverNotFoundError):
            sq.get_driver_number_from_lastname("Colapinto, self.mock_session)

    def test_get_team_drivers_success(self):
        drivers = sq.get_team_drivers("Red Bull", self.mock_session)
        self.assertEqual(drivers, ["1", "11"])


if __name__ == "__main__":
    unittest.main()