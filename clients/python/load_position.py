import math

# parameter equation, given a specific degree, return the position and rotation player should be
def get_player_pos_and_rot_by_degree(degree):
    radius = math.pi / 180 * degree
    x = 50 * math.sqrt(2) * math.cos(radius) + 50
    y = 50
    z = 50 * math.sqrt(2) * math.sin(radius) + 50
    yRot = degree + 90
    xRot = 0
    result = f'teleport GIL_Bert {int(x)} {int(y)} {int(z)} {yRot} {xRot}'
    print(result)
    return int(x), int(y), int(z), yRot, xRot


# sample point: how many position you want to obtain
def get_list_of_command_by_interpolation(sample_point):
    results = list()
    for i in range(sample_point):
        degree = i * 360 / sample_point
        result = get_player_pos_and_rot_by_degree(degree)
        results.append(result)
    return results
