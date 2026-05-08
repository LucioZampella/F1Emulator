import unittest
from unittest.mock import MagicMock
import pandas as pd
from python.f1fast.main.querys.SessionQuery import SessionQuerys
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

        self.queries = SessionQuerys(self.mock_session)

    def test_get_driver_teammate_success(self):
        teammate = self.queries.get_driver_teammate("1")
        self.assertEqual(teammate.DriverNumber, "11")

    def test_get_driver_teammate_not_found(self):
        with self.assertRaises(e.DriverNotFoundError):
            self.queries.get_driver_teammate("99")

    def test_get_driver_number_from_lastname_success(self):
        number = self.queries.get_driver_number_from_lastname("Norris")
        self.assertEqual(number, "4")

    def test_get_driver_number_lastname_error(self):
        with self.assertRaises(e.DriverNotFoundError):
            self.queries.get_driver_number_from_lastname("Colapinto")

    def test_get_team_drivers_success(self):
        drivers = self.queries.get_team_drivers("Red Bull")
        self.assertEqual(drivers, ["1", "11"])


if __name__ == "__main__":
    unittest.main()