import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from src.mechanismus import Mechanism
from src.kinematik import Kinematics

class TestKinematics(unittest.TestCase):

    def setUp(self):
        self.mech = Mechanism()
        self.j1 = self.mech.add_joint(0, 0, fixed=True)
        self.j2 = self.mech.add_joint(2, 0)
        self.j3 = self.mech.add_joint(2, 2)
        self.j4 = self.mech.add_joint(0, 2, fixed=True)

        self.mech.add_link(self.j1, self.j2)
        self.mech.add_link(self.j2, self.j3)
        self.mech.add_link(self.j3, self.j4)
        self.mech.add_link(self.j4, self.j1)

        self.kin = Kinematics(self.mech, self.j2)

    def test_initial_positions(self):
        positions = self.mech.get_joint_positions()
        expected_positions = [(0, 0), (2, 0), (2, 2), (0, 2)]
        self.assertEqual(positions, expected_positions)

    def test_rotation_updates_positions(self):
        self.kin.calculate_positions(90)
        self.assertAlmostEqual(self.j2.x, 0, places=5)
        self.assertAlmostEqual(self.j2.y, 2, places=5)

if __name__ == '__main__':
    unittest.main()
