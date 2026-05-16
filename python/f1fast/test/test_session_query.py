import unittest
from unittest.mock import MagicMock
import pandas as pd
import python.f1fast.queries.session_query as sq
import python.f1fast.exceptions.analysis_exceptions as e
from python.f1fast.domain.driver_id import DriverId


class TestSessionQuery(unittest.TestCase):

    def setUp(self):
        self.mock_session = MagicMock()
        self.mock_session.name = "Race"

        data = {
            "DriverNumber": ["1", "11", "4", "81"],
            "LastName": ["Verstappen", "Perez", "Norris", "Piastri"],
            "FullName": ["Max VERSTAPPEN", "Sergio PEREZ", "Lando NORRIS", "Oscar PIASTRI"],
            "Abbreviation": ["VER", "PER", "NOR", "PIA"],
            "TeamName": ["Red Bull", "Red Bull", "McLaren", "McLaren"],
        }
        self.mock_session.results = pd.DataFrame(data)

        self.ver = DriverId("VER", "Max VERSTAPPEN")
        self.per = DriverId("PER", "Sergio PEREZ")
        self.nor = DriverId("NOR", "Lando NORRIS")

    def test_get_teammate_returns_correct_driver(self):
        teammate = sq.get_teammate_id(self.ver, self.mock_session)
        self.assertEqual(teammate, self.per)

    def test_get_teammate_driver_not_found_raises(self):
        ghost = DriverId("COL", "Franco COLAPINTO")
        with self.assertRaises(e.DriverNotFoundError):
            sq.get_teammate_id(ghost, self.mock_session)

    def test_get_driver_id_from_lastname_returns_driver_id(self):
        driver = sq.get_driver_id_from_lastname("Norris", self.mock_session)
        self.assertEqual(driver, self.nor)

    def test_get_driver_id_from_lastname_not_found_raises(self):
        with self.assertRaises(e.DriverNotFoundError):
            sq.get_driver_id_from_lastname("Colapinto", self.mock_session)

    def test_get_team_driver_ids_returns_both(self):
        d1, d2 = sq.get_team_driver_ids("Red Bull", self.mock_session)
        self.assertIn(d1, [self.ver, self.per])
        self.assertIn(d2, [self.ver, self.per])
        self.assertNotEqual(d1, d2)

    def test_get_team_driver_ids_team_not_found_raises(self):
        with self.assertRaises(e.TeamNotFoundError):
            sq.get_team_driver_ids("Alpine", self.mock_session)


if __name__ == "__main__":
    unittest.main()