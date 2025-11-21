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


Changing to a matrix operation approach...

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

Axes
         (0)
          ^
          |
     +----+----+
     | 0  | 1  |
(2)<-+----+----+
     | 2  | 3  |
     +----+----+

(1) goes down from 4 -> 0, etc.

0: [+1, +1, +1]
1: [+1, +1, -1]
2: [-1, +1, +1]
3: [-1, +1, -1]
4: [+1, -1, +1]
5: [+1, -1, -1]
6: [-1, -1, +1]
7: [-1, -1, -1]
"""
import copy
import dataclasses
import enum

import numpy as np


RAD_TO_DEG = 180 / np.pi

NUM_ORIENTATIONS = 4

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

IDENTITY_ROTATION = np.array([[1, 0, 0],
                              [0, 1, 0],
                              [0, 0, 1]])


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

    def get_matrix(self) -> np.ndarray:
        ROTATION_MATRIX_BY_TYPE = {
            RotationType.F: R_f,
            RotationType.U: R_u,
            RotationType.R: R_r,
        }
        return ROTATION_MATRIX_BY_TYPE[self]


# XXX from quick search
# - typehinting too
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


# XXX: Better type-hinting for the ndarrays
def _get_degrees(orientation: np.ndarray) -> tuple[float, float, float]:
    euler = rot2eul(orientation)
    deg = euler * RAD_TO_DEG
    f_deg = deg[RotationType.F.np_index()]
    u_deg = deg[RotationType.U.np_index()]
    r_deg = deg[RotationType.R.np_index()]
    return [f_deg, u_deg, r_deg]


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

        rot_matrix = rotation_type.get_matrix()
        # Here is where negative gets converted into NUM_ORIENTATIONS -  1
        # - is there a more efficient way?
        num_rotations %= NUM_ORIENTATIONS
        for _ in range(num_rotations):
            self.position = rot_matrix @ self.position
            # XXX; What's the correct ordering here?
            # - this seems right ...
            self.orientation = rot_matrix @ self.orientation

    def __str__(self) -> str:
        f_deg, u_deg, r_deg = self.get_degrees()
        return f'{self.identifier}: {self.position} (F: {f_deg}°, U: {u_deg}°, R: {r_deg}°)'

    def get_degrees(self) -> tuple[float, float, float]:
        return _get_degrees(self.orientation)

    def compare_str(self, other: 'LinearInnerCube') -> str:
        assert self.identifier == other.identifier
        if self == other:
            return(f'{self.identifier} MATCH')
        else:
            pos_change = other.position - self.position
            # XXX: Can't change orientation, then get degrees from that
            sf_deg, su_deg, sr_deg = self.get_degrees()
            of_deg, ou_deg, or_deg = other.get_degrees()
            f_deg = of_deg - sf_deg
            u_deg = ou_deg - su_deg
            r_deg = or_deg - sr_deg
            return(f'{self.identifier} MISMATCH {pos_change} (F: {f_deg}°, U: {u_deg}°, R: {r_deg}°)')

    def __eq__(self, other) -> bool:
        if not isinstance(other, LinearInnerCube):
            raise ValueError('Must compare with LinearInnerCube')
        return (
            self.identifier == other.identifier and
            (self.position == other.position).all() and
            (self.orientation == other.orientation).all()
        )


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


def run_and_display_linear_algorithm(rubiks: dict[int, LinearInnerCube], algorithm: str) -> list[dict[int, LinearInnerCube]]:
    result = run_linear_algorithm(rubiks, algorithm)
    operations = algorithm.split(",")
    assert len(operations) == len(result)
    print(algorithm)
    # print("og:")
    # for cube in rubiks.values():
    #     print(cube)

    # for result_i, operation_i in zip(result, operations):
    #     print(operation_i)
    #     for cube in result_i.values():
    #         print(cube)
    # print('COMPARISON')
    for og_cube, result_cube in zip(rubiks.values(), result[-1].values()):
        print(og_cube.compare_str(result_cube))
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
    # 4/7 swap place; 4: F 90, R -90; 7: F -90, R 90
    # 5/6 swap place; 5: F -90, U -90; 6: F 180, R 180
    result = run_and_display_linear_algorithm(rubiks, "r,u,ri,u,r,u,u,ri")
    print("new")
    # 4/5 swap pos; 4 U 90°, 5: F -90°
    # 6/7 swap pos; 6 U -90°, 7: F -90°
    result = run_and_display_linear_algorithm(rubiks, "f,u,r,ui,ri,fi")
    # print('og:')
    # for cube in rubiks.values():
    #     angle, axis = rot2eul(cube.orientation)
    #     deg = angle * 180 / np.pi
    #     print(f'{cube.identifier}: {cube.position} ({axis} @ {deg}°)')

    # # Rotate F
    # print('f:')
    # for cube in rubiks.values():
    #     cube.rotate(RotationType.F, 2)
    # for cube in rubiks.values():
    #     angle, axis = rot2eul(cube.orientation)
    #     deg = angle * 180 / np.pi
    #     print(f'{cube.identifier}: {cube.position} ({axis} @ {deg}°)')
    # print('u:')
    # for cube in rubiks.values():
    #     cube.rotate(RotationType.U, 1)
    # for cube in rubiks.values():
    #     angle, axis = rot2eul(cube.orientation)
    #     deg = angle * 180 / np.pi
    #     print(f'{cube.identifier}: {cube.position} ({axis} @ {deg}°)')
    # print('r:')
    # for cube in rubiks.values():
    #     cube.rotate(RotationType.R, 1)
    # for cube in rubiks.values():
    #     angle, axis = rot2eul(cube.orientation)
    #     deg = angle * 180 / np.pi
    #     print(f'{cube.identifier}: {cube.position} ({axis} @ {deg}°)')

    # XXX: Unittests for the above, + show identity of certain operations
    # - could turn into benchmarks to measure performance if desired
    # - eyeballing it seems like it's fine


def main():
    linear_algebra_cube()
    # TODO: Cool visualization
    # TODO: unit testing
    # TODO: Add sanity check that rubiks cube makes sense
    # COULD: Extend to N-wide cube?
    # TODO: Establish a baseline for how long performing operations takes
    # TODO: Make a branch & bound optimal solver
    # - compare to open source / existing solutions


if __name__ == "__main__":
    main()
