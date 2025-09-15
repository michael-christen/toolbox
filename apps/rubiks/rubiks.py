"""Tools to simulate Rubik's cube and develop algorithms for solving.

Let's start with the 2x2 cube.

Within the 2x2 cube there are 8 individual cubes. We can pick one as the
origin-cube, around which everything else is rotated.

If we separate the top and bottom layers in order to describe each cube we
have:

               Top
               +----+----+
               | 4  | 5  |
               +----+----+
               | 6  | 7  |
               +----+----+

Bottom
+----+----+
| 0  | 1  |
+----+----+
| 2  | 3  |
+----+----+

If we think about this in terms of axes we can also number these inner cubes
differently:

"F: Front-Face Rotation"

               Top
               +----+----+
               |    |    |
               +----+----+
               | F1 | F2 |
               +----+----+

Bottom
+----+----+
| ∅  |    |
+----+----+
| F0 | F3 |
+----+----+


"U: Upper-Face Rotation"

               Top
               +----+----+
               | U0 | U1 |
               +----+----+
               | U3 | U2 |
               +----+----+

Bottom
+----+----+
| ∅  |    |
+----+----+
|    |    |
+----+----+


"R: Right-Face Rotation"

               Top
               +----+----+
               |    | R3 |
               +----+----+
               |    | R2 |
               +----+----+

Bottom
+----+----+
| ∅  | R0 |
+----+----+
|    | R1 |
+----+----+

You can make a table of all of these:

| #   | F   | U   | R   | Name |
| --- | --- | --- | --- | ---- |
| 0   | ∅   | ∅   | ∅   | ∅    |
| 1   |     |     | R0  | R0   |
| 2   | F0  |     |     | F0   |
| 3   | F3  |     | R1  | R1   |
| 4   |     | U0  |     | U0   |
| 5   |     | U1  | R3  | U1   |
| 6   | F1  | U3  |     | F1   |
| 7   | F2  | U2  | R2  | Ω    |

The "opposite posiion of ∅ we'll simply name Ω.

We have 3 operaitons: F,U,R that both change the position and orientation of a
cube.
"""
import copy
import dataclasses
import enum

import numpy as np


POSITION_TO_NAME = {
    0: "∅ ",
    1: "R0",
    2: "F0",
    3: "R1",
    4: "U0",
    5: "U1",
    6: "F1",
    7: "Ω ",
}


class RotationType(enum.Enum):
    F = 'F'
    U = 'U'
    R = 'R'

    def np_index(self) -> int:
        TYP_TO_INDEX = {
            RotationType.F: 0,
            RotationType.U: 1,
            RotationType.R: 2,
        }
        return TYP_TO_INDEX[self]


@dataclasses.dataclass
class PositionInfo:
    name: str
    f_index: int | None
    u_index: int | None
    r_index: int | None

    def get_index(self, rotation_type: RotationType) -> int | None:
        if rotation_type == RotationType.F:
            return self.f_index
        elif rotation_type == RotationType.U:
            return self.u_index
        elif rotation_type == RotationType.R:
            return self.r_index
        else:
            raise ValueError(f'Unhandled: {rotation_type}')


# XXX: We could likely simplify by using a coordinate frame (F, U, R) and
# defining each position as such. Orientation could use a similar scheme.
# It's a hollow-shell coordinate frame.
class Position(enum.Enum):
    POSITION_0 = 0
    POSITION_1 = 1
    POSITION_2 = 2
    POSITION_3 = 3
    POSITION_4 = 4
    POSITION_5 = 5
    POSITION_6 = 6
    POSITION_7 = 7

    def _get_info(self) -> PositionInfo:
        return POSITIONS[self]

    def get_name(self) -> str:
        return self._get_info().name

    def get_index(self, rotation_type: RotationType) -> int | None:
        return self._get_info().get_index(rotation_type)

    def get_f_index(self) -> int | None:
        return self._get_info().f_index

    def get_u_index(self) -> int | None:
        return self._get_info().u_index

    def get_r_index(self) -> int | None:
        return self._get_info().r_index


POSITIONS = {
    Position.POSITION_0: PositionInfo(name="∅ ", f_index=None, u_index=None, r_index=None),
    Position.POSITION_1: PositionInfo(name="R0", f_index=None, u_index=None, r_index=0),
    Position.POSITION_2: PositionInfo(name="F0", f_index=0, u_index=None, r_index=None),
    Position.POSITION_3: PositionInfo(name="R1", f_index=3, u_index=None, r_index=1),
    Position.POSITION_4: PositionInfo(name="U0", f_index=None, u_index=0, r_index=None),
    Position.POSITION_5: PositionInfo(name="U1", f_index=None, u_index=1, r_index=3),
    Position.POSITION_6: PositionInfo(name="F1", f_index=1, u_index=3, r_index=None),
    Position.POSITION_7: PositionInfo(name="Ω ", f_index=2, u_index=2, r_index=2),
}
POSITION_FOR_F_INDEX = {
    pos_info.f_index: pos for pos, pos_info in POSITIONS.items()
    if pos_info.f_index is not None
}
POSITION_FOR_U_INDEX = {
    pos_info.u_index: pos for pos, pos_info in POSITIONS.items()
    if pos_info.u_index is not None
}
POSITION_FOR_R_INDEX = {
    pos_info.r_index: pos for pos, pos_info in POSITIONS.items()
    if pos_info.r_index is not None
}
POSITION_FOR_INDEX_BY_TYPE = {
    RotationType.F: POSITION_FOR_F_INDEX,
    RotationType.U: POSITION_FOR_U_INDEX,
    RotationType.R: POSITION_FOR_R_INDEX,
}

NUM_ORIENTATIONS = 4


@dataclasses.dataclass
class Orientation:
    # 0 -> 0 deg, 1 -> 90 deg, 2 -> 180 deg, 3 -> 270 deg
    # %4 so that 0,1,2,3 are the only possible values
    f_rot: int
    u_rot: int
    r_rot: int
    # NOTE: The above description is a larger "space" than we actually have,
    # there are only 3 orienations each cube has for any given position,
    # not 4 x 4 x 4 (64), we're currently noting it this way because I can't
    # think of a better way to describe those 3 orientations yet and it's
    # convenient for performing operations
    # XXX: We need some way to validate what is "possible"

    def __str__(self) -> str:
        return f'(F:{self.f_rot}, U:{self.u_rot}, R:{self.r_rot})'

    def rotate(self, rotation_type: RotationType, num_rotations: int) -> None:
        if rotation_type == RotationType.F:
            self.f_rot = (self.f_rot + num_rotations) % NUM_ORIENTATIONS
        elif rotation_type == RotationType.U:
            self.u_rot = (self.u_rot + num_rotations) % NUM_ORIENTATIONS
        elif rotation_type == RotationType.R:
            self.r_rot = (self.r_rot + num_rotations) % NUM_ORIENTATIONS
        else:
            raise ValueError(f'Invalid rotation_type: {rotation_type}')


@dataclasses.dataclass
class InnerCube:
    position: Position
    orientation: Orientation
    # XXX: I probably need a definition for each unique cube, such as what its
    # "solved" position is
    # Or it could be the initial position
    identifier: Position



# XXX: How to best manage overall position tracking vs. cube's data?
# - we can worry about performance later
# XXX: Possibly make stateless?
@dataclasses.dataclass
class RubiksCube2x2:
    _cubes: list[InnerCube]

    def __init__(self, cubes: list[InnerCube]):
        # XXX: Validation that positions are correct
        self._cubes = cubes

    def __str__(self) -> str:
        positions = self.get_positions()
        lines = []
        for pos, cube in sorted(positions.items(), key=lambda kv: kv[1].identifier.value):
            lines.append(f'{cube.identifier.get_name()} -> {pos.get_name()}: {cube.orientation}')
        return "RubiksCube2x2:\n" + '\n'.join(lines + [""])

    def get_positions(self) -> dict[Position, InnerCube]:
        return {cube.position: cube for cube in self._cubes}

    def _rotate(self, rotation_type: RotationType, num_rotations: int) -> None:
        for cube in self._cubes:
            index = cube.position.get_index(rotation_type)
            if index is None:
                continue
            cube.position = POSITION_FOR_INDEX_BY_TYPE[rotation_type][
                (index + num_rotations) % NUM_ORIENTATIONS]
            cube.orientation.rotate(rotation_type=rotation_type, num_rotations=num_rotations)

    def _f(self, num_rotations: int) -> None:
        self._rotate(rotation_type=RotationType.F, num_rotations=num_rotations)

    def _u(self, num_rotations: int) -> None:
        self._rotate(rotation_type=RotationType.U, num_rotations=num_rotations)

    def _r(self, num_rotations: int) -> None:
        self._rotate(rotation_type=RotationType.R, num_rotations=num_rotations)

    def f(self) -> None:
        self._f(1)

    def fi(self) -> None:
        self._f(3)

    def u(self) -> None:
        self._u(1)

    def ui(self) -> None:
        self._u(3)

    def r(self) -> None:
        self._r(1)

    def ri(self) -> None:
        self._r(3)

def run_algorithm(rubiks: RubiksCube2x2, algorithm: str) -> list[RubiksCube2x2]:
    """Returns each state of a cube after applying steps of algorithm.

    algorithm is a string, such as "r,ri,u,f"
    """
    result = []
    for operation in algorithm.split(','):
        rubiks = copy.deepcopy(rubiks)
        operation = operation.lower()
        operation_to_fxn = {
            'f': rubiks.f,
            'fi': rubiks.fi,
            'u': rubiks.u,
            'ui': rubiks.ui,
            'r': rubiks.r,
            'ri': rubiks.ri,
        }
        fxn = operation_to_fxn.get(operation)
        if fxn is None:
            raise ValueError(f'Unsupported operation: "{operation}"')
        fxn()
        result.append(rubiks)
    return result

def run_and_display_algorithm(rubiks: RubiksCube2x2, algorithm: str) -> list[RubiksCube2x2]:
    result = run_algorithm(rubiks, algorithm)
    operations = algorithm.split(",")
    assert len(operations) == len(result)

    print("og", rubiks)
    for result_i, operation_i in zip(result, operations):
        print(operation_i, result_i)
    return result


def _smoke_test(rubiks: RubiksCube2x2) -> None:
    og = copy.deepcopy(rubiks)
    print('Og', rubiks)

    rubiks = copy.deepcopy(og)
    rubiks.f()
    print('F', rubiks)

    rubiks = copy.deepcopy(og)
    rubiks.fi()
    print('Fi', rubiks)

    rubiks = copy.deepcopy(og)
    rubiks.u()
    print('U', rubiks)

    rubiks = copy.deepcopy(og)
    rubiks.ui()
    print('Ui', rubiks)

    rubiks = copy.deepcopy(og)
    rubiks.r()
    print('R', rubiks)

    rubiks.ri()
    print('Ri', rubiks)

    # XXX: Unittests for the above, + show identity of certain operations
    # - could turn into benchmarks to measure performance if desired
    # - eyeballing it seems like it's fine

# Thought about rotations some more, then simplified to a 1x1 cube, in that
# case, it's equivalent to changing different coordinate frames which we can
# represent as a rotation matrix or as a quaternion. We can keep it simple as a
# rotation matrix

# https://en.wikipedia.org/wiki/Rotation_matrix
# Rotation matrices for F/U/R (X/Y/Z)
# R_x
R_f = np.array([[1, 0, 0],
                [0, 0, -1],
                [0, 1, 0]])
# R_y
R_u = np.array([[0, 0, 1],
                [0, 1, 0],
                [-1, 0, 0],
                ])
# R_z
R_r = np.array([[0, -1, 0],
                [1, 0, 0],
                [0, 0, 1]])
ROTATION_MATRIX_BY_TYPE = {
    RotationType.F: R_f,
    RotationType.U: R_u,
    RotationType.R: R_r,
}

IDENTITY_ROTATION = np.array([[1, 0, 0],
                              [0, 1, 0],
                              [0, 0, 1]])

@dataclasses.dataclass
class LinearInnerCube:
    # Technically all we need is the starting orientation. The
    # orientation/rotation matrix tells us how it changes over time.
    # ID the cube
    identifier: str
    # Vector3 of position of the cube
    position: np.ndarray
    # Orientation matrix
    orientation: np.ndarray

    def rotate(self, rotation_type: RotationType, num_rotations: int) -> None:
        np_index = rotation_type.np_index()
        if self.position[np_index] > 0:
            return

        rot_matrix = ROTATION_MATRIX_BY_TYPE[rotation_type]
        num_rotations %= NUM_ORIENTATIONS
        for _ in range(num_rotations):
            self.position = rot_matrix @ self.position
            # XXX; What's the correct ordering here?
            # - this seems right ...
            self.orientation = rot_matrix @ self.orientation


def run_linear_algorithm(rubiks: dict[int, LinearInnerCube], algorithm: str) -> list[dict[int, LinearInnerCube]]:
    """Returns each state of a cube after applying steps of algorithm.

    algorithm is a string, such as "r,ri,u,f"
    """
    result = []
    for operation in algorithm.split(','):
        rubiks = copy.deepcopy(rubiks)
        operation = operation.lower()
        operation_to_typ_and_num = {
            'f': (RotationType.F, 1),
            'fi': (RotationType.F, -1),
            'u': (RotationType.U, 1),
            'ui': (RotationType.U, -1),
            'r': (RotationType.R, 1),
            'ri': (RotationType.R, -1),
        }
        typ_num = operation_to_typ_and_num.get(operation)
        if typ_num is None:
            raise ValueError(f'Unsupported operation: "{operation}"')
        typ, num = typ_num
        for cube in rubiks.values():
            cube.rotate(typ, num)
        result.append(rubiks)
    return result

RAD_TO_DEG = 180 / np.pi

def run_and_display_linear_algorithm(rubiks: dict[int, LinearInnerCube], algorithm: str) -> list[dict[int, LinearInnerCube]]:
    result = run_linear_algorithm(rubiks, algorithm)
    operations = algorithm.split(",")
    assert len(operations) == len(result)

    print("og:")
    for cube in rubiks.values():
        # angle, axis = rotation_matrix_to_angle_axis(cube.orientation)
        euler = rot2eul(cube.orientation)
        deg = euler * RAD_TO_DEG
        f_deg = deg[RotationType.F.np_index()]
        u_deg = deg[RotationType.U.np_index()]
        r_deg = deg[RotationType.R.np_index()]
        print(f'{cube.identifier}: {cube.position} (F: {f_deg}°, U: {u_deg}°, R: {r_deg}°)')

    for result_i, operation_i in zip(result, operations):
        print(operation_i)
        for cube in result_i.values():
            # angle, axis = rotation_matrix_to_angle_axis(cube.orientation)
            # deg = angle * 180 / np.pi
            # print(f'{cube.identifier}: {cube.position} ({axis} @ {deg}°)')
            euler = rot2eul(cube.orientation)
            deg = euler * RAD_TO_DEG
            f_deg = deg[RotationType.F.np_index()]
            u_deg = deg[RotationType.U.np_index()]
            r_deg = deg[RotationType.R.np_index()]
            print(f'{cube.identifier}: {cube.position} (F: {f_deg}°, U: {u_deg}°, R: {r_deg}°)')
    return result


def linear_algebra_cube():
    rubiks = {
        0: LinearInnerCube('0', np.array([1, 1, 1]), IDENTITY_ROTATION.copy()),
        1: LinearInnerCube('1', np.array([1, 1, -1]), IDENTITY_ROTATION.copy()),
        2: LinearInnerCube('2', np.array([-1, 1, 1]), IDENTITY_ROTATION.copy()),
        3: LinearInnerCube('3', np.array([-1, 1, -1]), IDENTITY_ROTATION.copy()),
        4: LinearInnerCube('4', np.array([1, -1, 1]), IDENTITY_ROTATION.copy()),
        5: LinearInnerCube('5', np.array([1, -1, -1]), IDENTITY_ROTATION.copy()),
        6: LinearInnerCube('6', np.array([-1, -1, 1]), IDENTITY_ROTATION.copy()),
        7: LinearInnerCube('7', np.array([-1, -1, -1]), IDENTITY_ROTATION.copy()),
    }
    result = run_and_display_linear_algorithm(rubiks, "r,u,ri,u,r,u,u,ri")
    print("new")
    result = run_and_display_linear_algorithm(rubiks, "f,u,r,ui,ri,fi")
    # print('og:')
    # for cube in rubiks.values():
    #     angle, axis = rotation_matrix_to_angle_axis(cube.orientation)
    #     deg = angle * 180 / np.pi
    #     print(f'{cube.identifier}: {cube.position} ({axis} @ {deg}°)')

    # # Rotate F
    # print('f:')
    # for cube in rubiks.values():
    #     cube.rotate(RotationType.F, 2)
    # for cube in rubiks.values():
    #     angle, axis = rotation_matrix_to_angle_axis(cube.orientation)
    #     deg = angle * 180 / np.pi
    #     print(f'{cube.identifier}: {cube.position} ({axis} @ {deg}°)')
    # print('u:')
    # for cube in rubiks.values():
    #     cube.rotate(RotationType.U, 1)
    # for cube in rubiks.values():
    #     angle, axis = rotation_matrix_to_angle_axis(cube.orientation)
    #     deg = angle * 180 / np.pi
    #     print(f'{cube.identifier}: {cube.position} ({axis} @ {deg}°)')
    # print('r:')
    # for cube in rubiks.values():
    #     cube.rotate(RotationType.R, 1)
    # for cube in rubiks.values():
    #     angle, axis = rotation_matrix_to_angle_axis(cube.orientation)
    #     deg = angle * 180 / np.pi
    #     print(f'{cube.identifier}: {cube.position} ({axis} @ {deg}°)')


# XXX
# from quick search
import numpy as np

def rotation_matrix_to_angle_axis(R):
    trace = np.trace(R)
    angle = np.arccos((trace - 1) / 2.0)

    # Handle the case where angle is 0 (no rotation) or pi (180 degrees)
    if np.isclose(angle, 0):
        axis = np.array([0.0, 0.0, 1.0]) # Arbitrary axis for no rotation
    elif np.isclose(angle, np.pi):
        # For 180-degree rotation, the axis is not uniquely determined by the skew-symmetric part alone.
        # We can find the axis by looking at the largest diagonal element.
        # For example, if R[0,0] is the largest, the axis is along the x-axis.
        # A more robust method involves eigenvector decomposition.
        # Here, a simplified approach:
        if R[0,0] > R[1,1] and R[0,0] > R[2,2]:
            axis = np.array([np.sqrt((R[0,0] + 1) / 2), R[0,1] / (2 * np.sqrt((R[0,0] + 1) / 2)), R[0,2] / (2 * np.sqrt((R[0,0] + 1) / 2))])
        elif R[1,1] > R[2,2]:
            axis = np.array([R[1,0] / (2 * np.sqrt((R[1,1] + 1) / 2)), np.sqrt((R[1,1] + 1) / 2), R[1,2] / (2 * np.sqrt((R[1,1] + 1) / 2))])
        else:
            axis = np.array([R[2,0] / (2 * np.sqrt((R[2,2] + 1) / 2)), R[2,1] / (2 * np.sqrt((R[2,2] + 1) / 2)), np.sqrt((R[2,2] + 1) / 2)])
    else:
        axis = np.array([R[2,1] - R[1,2], R[0,2] - R[2,0], R[1,0] - R[0,1]])
        axis = axis / (2 * np.sin(angle)) # Normalize the axis

    return angle, axis

def rot2eul(R):
    """
    Converts a 3x3 rotation matrix to Euler angles (roll, pitch, yaw) in radians.
    Assumes ZYX extrinsic rotation (or XYZ intrinsic rotation).
    """
    sy = np.sqrt(R[0,0] * R[0,0] + R[1,0] * R[1,0])

    singular = sy < 1e-6 # Check for gimbal lock

    if not singular:
        x = np.arctan2(R[2,1], R[2,2]) # Roll
        y = np.arctan2(-R[2,0], sy)    # Pitch
        z = np.arctan2(R[1,0], R[0,0]) # Yaw
    else:
        x = np.arctan2(-R[1,2], R[1,1]) # Roll
        y = np.arctan2(-R[2,0], sy)    # Pitch
        z = 0                          # Yaw

    return np.array([x, y, z])


def main():
    linear_algebra_cube()

    # XXX
    return
    # TODO: Cool visualization
    rubiks = RubiksCube2x2([
        InnerCube(position=Position.POSITION_0,
                  orientation=Orientation(f_rot=0, u_rot=0, r_rot=0),
                  identifier=Position.POSITION_0,
                  ),
        InnerCube(position=Position.POSITION_1,
                  orientation=Orientation(f_rot=0, u_rot=0, r_rot=0),
                  identifier=Position.POSITION_1,
                  ),
        InnerCube(position=Position.POSITION_2,
                  orientation=Orientation(f_rot=0, u_rot=0, r_rot=0),
                  identifier=Position.POSITION_2,
                  ),
        InnerCube(position=Position.POSITION_3,
                  orientation=Orientation(f_rot=0, u_rot=0, r_rot=0),
                  identifier=Position.POSITION_3,
                  ),
        InnerCube(position=Position.POSITION_4,
                  orientation=Orientation(f_rot=0, u_rot=0, r_rot=0),
                  identifier=Position.POSITION_4,
                  ),
        InnerCube(position=Position.POSITION_5,
                  orientation=Orientation(f_rot=0, u_rot=0, r_rot=0),
                  identifier=Position.POSITION_5,
                  ),
        InnerCube(position=Position.POSITION_6,
                  orientation=Orientation(f_rot=0, u_rot=0, r_rot=0),
                  identifier=Position.POSITION_6,
                  ),
        InnerCube(position=Position.POSITION_7,
                  orientation=Orientation(f_rot=0, u_rot=0, r_rot=0),
                  identifier=Position.POSITION_7,
                  ),
    ])
    og = copy.deepcopy(rubiks)

    # _smoke_test(rubiks)

    rubiks = copy.deepcopy(og)
    result = run_and_display_algorithm(rubiks, "r,u,ri,u,r,u,u,ri")


if __name__ == "__main__":
    main()
