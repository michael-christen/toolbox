import unittest

from apps.rubiks import rubiks


class TestRubiks(unittest.TestCase):
    def test_example(self):
        # print("og:")
        # for cube in rubiks.values():
        #     print(cube)

        # for result_i, operation_i in zip(result, operations):
        #     print(operation_i)
        #     for cube in result_i.values():
        #         print(cube)
        # print('COMPARISON')
        ...
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
