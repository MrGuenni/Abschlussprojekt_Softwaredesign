import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import matplotlib.pyplot as plt
from src.mechanismus import Mechanism
from src.kinematik import Kinematics

def create_default_mechanism():
    mech = Mechanism()
    j1 = mech.add_joint(0, 0, fixed=True)
    j2 = mech.add_joint(2, 0)
    j3 = mech.add_joint(2, 2)
    j4 = mech.add_joint(0, 2, fixed=True)

    mech.add_link(j1, j2)
    mech.add_link(j2, j3)
    mech.add_link(j3, j4)
    mech.add_link(j4, j1)

    return mech

st.title("Mechanismus-Simulation")

mech = create_default_mechanism()
kin = Kinematics(mech, mech.joints[1])  

angle = st.slider("Antriebswinkel", 0, 360, 0)

updated_joints = kin.calculate_positions(angle)

fig, ax = plt.subplots()
for link in mech.links:
    x1, y1 = link.joint1.x, link.joint1.y
    x2, y2 = link.joint2.x, link.joint2.y
    ax.plot([x1, x2], [y1, y2], 'bo-')

for joint in mech.joints:
    ax.plot(joint.x, joint.y, 'ro', markersize=6)

ax.set_xlim(-5, 7)
ax.set_ylim(-5, 7)
ax.set_aspect('equal')
ax.set_title("Mechanismus-Simulation")


if st.button("Bahnkurve speichern"):
    kin.save_positions_to_csv()
    st.success("Bahnkurve gespeichert als 'bahnkurve.csv'")

st.pyplot(fig)
