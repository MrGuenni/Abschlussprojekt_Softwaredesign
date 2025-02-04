import sys
import os
import csv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from scipy.optimize import least_squares
from src.mechanismus import Mechanism, Joint, Link
import pandas as pd 

class Kinematics:
    def __init__(self, mechanism: Mechanism, driving_joint: Joint):
        self.mechanism = mechanism
        self.driving_joint = driving_joint

    def apply_rotation(self, theta):
        fixed_joint = next((j for j in self.mechanism.joints if j.fixed), None)
        if fixed_joint is None:
            raise ValueError("Kein festes Gelenk gefunden!")

        r = np.sqrt((self.driving_joint.x - fixed_joint.x) ** 2 + (self.driving_joint.y - fixed_joint.y) ** 2)
        angle_rad = np.radians(theta)

        self.driving_joint.x = fixed_joint.x + r * np.cos(angle_rad)
        self.driving_joint.y = fixed_joint.y + r * np.sin(angle_rad)

    def calculate_positions(self, theta):
        self.apply_rotation(theta)

        known_positions = {joint: (joint.x, joint.y) for joint in self.mechanism.joints if joint.fixed}
        variable_joints = [j for j in self.mechanism.joints if not j.fixed and j != self.driving_joint]
        initial_guesses = [coord for joint in variable_joints for coord in (joint.x, joint.y)]

        if not initial_guesses:
            return self.mechanism.joints

        def equations(vars):
            joint_map = {variable_joints[i]: (vars[2 * i], vars[2 * i + 1]) for i in range(len(variable_joints))}
            eqs = []
            for link in self.mechanism.links:
                x1, y1 = known_positions.get(link.joint1, joint_map.get(link.joint1, (None, None)))
                x2, y2 = known_positions.get(link.joint2, joint_map.get(link.joint2, (None, None)))

                if None in (x1, y1, x2, y2):
                    continue

                eqs.append((x2 - x1) ** 2 + (y2 - y1) ** 2 - link.length ** 2)
            return eqs

        result = least_squares(equations, initial_guesses, xtol=1e-6)

        for i, joint in enumerate(variable_joints):
            joint.x, joint.y = result.x[2 * i], result.x[2 * i + 1]

        return self.mechanism.joints

    def save_positions_to_csv(self, filename="bahnkurve.csv"):
        data = {"Joint": [], "X": [], "Y": []}
        for i, joint in enumerate(self.mechanism.joints):
            data["Joint"].append(f"Joint {i}")
            data["X"].append(joint.x)
            data["Y"].append(joint.y)
        
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Speicherung abgeschlossen: {filename}")
