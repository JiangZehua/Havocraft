import math
SCREENSHOT_SIZE = (512, 512)
BBOX_OFFSET = (0, 0)  # For 16" M1 MacBook Pro
BBOX = (BBOX_OFFSET[0], BBOX_OFFSET[1], BBOX_OFFSET[0] + SCREENSHOT_SIZE[0], BBOX_OFFSET[1] + SCREENSHOT_SIZE[1])


# parameter equation, given a specific degree, return the position and rotation player should be
def get_player_pos_and_rot_by_degree(degree):
    radius = math.pi / 180 * degree
    x = 50 * math.sqrt(2) * math.cos(radius) + 50
    y = 150
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


# def top_left_corner_screenshot(name: str, bbox: tuple, save_dir: str):
#     im = ImageGrab.grab(bbox)
#     im.save(os.path.join(save_dir, f"{name}.png"))
#
#
# def player_screenshot():
#     channel = grpc.insecure_channel('localhost:5001')
#     client = MinecraftServiceStub(channel)
#     results = get_list_of_command_by_interpolation(360)
#     picture_name = 0
#     for (x, y, z, yRot, xRot) in results:
#         picture_name += 1
#         client.setLoc(Point(x=x, y=y, z=z))
#         client.setRot(Point(x=xRot, y=yRot, z=0))
#         top_left_corner_screenshot(str(picture_name), BBOX, "../screenshot")


