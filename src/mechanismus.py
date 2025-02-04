class Joint:
    def __init__(self, x: float, y: float, fixed: bool = False):
        self.x = x
        self.y = y
        self.fixed = fixed

class Link:
    def __init__(self, joint1: Joint, joint2: Joint):
        self.joint1 = joint1
        self.joint2 = joint2
        self.length = ((joint1.x - joint2.x) ** 2 + (joint1.y - joint2.y) ** 2) ** 0.5

class Mechanism:
    def __init__(self):
        self.joints = []
        self.links = []

    def add_joint(self, x: float, y: float, fixed: bool = False):
        joint = Joint(x, y, fixed)
        self.joints.append(joint)
        return joint

    def add_link(self, joint1: Joint, joint2: Joint):
        link = Link(joint1, joint2)
        self.links.append(link)

    def get_joint_positions(self):
        return [(joint.x, joint.y) for joint in self.joints]