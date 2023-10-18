import os
import grpc
import pyscreenshot as ImageGrab
import src.main.proto.minecraft_pb2_grpc
from src.main.proto.minecraft_pb2 import *
import server_code.load_player as player

def top_left_corner_screenshot(name: str, bbox):
    im = ImageGrab.grab(bbox)
    im.save(os.path.abspath(os.path.join(os.getcwd(), "../..", 'data', 'screenshots', f"{name}.png")))


def get_screenies(client, num_samples):
    SCREENSHOT_SIZE = (512, 512)
    BBOX_OFFSET = (0, 66)  # For 16" M1 MacBook Pro
    BBOX = (BBOX_OFFSET[0], BBOX_OFFSET[1], BBOX_OFFSET[0] + SCREENSHOT_SIZE[0], BBOX_OFFSET[1] + SCREENSHOT_SIZE[1])

    # Continue when user enters "y"
    input(
        "Put the Minecraft window in the top corner of the screen (do not scale it!). Enter the server (localhost) and " +
        " enter camera mode (F1). Press enter to continue...")
    print("Now change focus to the Minecraft window. (User, e.g. alt + tab. Do not move the window!)")
    print("Minecraft is active window now!")

    player_pos = player.get_list_of_command_by_interpolation(num_samples)
    i = 0
    for(x, y, z, rot, _) in player_pos:
        client.setLoc(Point(x=x, y=y, z=z))
        # -45 temp rotation, since y doesn't work well now
        client.setRot(Point(x=-45, y=int(rot), z=0))
        top_left_corner_screenshot(f"{i}", bbox=BBOX)
        print(f"Saved sreenshot {i}, location {x}, {y}, {z}")
        i += 1

def main(num_samples: int = 360):
    channel = grpc.insecure_channel('localhost:5001')
    client = src.main.proto.minecraft_pb2_grpc.MinecraftServiceStub(channel)
    get_screenies(client=client, num_samples=num_samples)


if __name__ == "__main__":
    main()
