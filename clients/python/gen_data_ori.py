import os
import grpc
import numpy as np
import pandas as pd
import pyscreenshot as ImageGrab
from fire import Fire
import src.main.proto.minecraft_pb2_grpc
from src.main.proto.minecraft_pb2 import *
from utils import get_vox_xz_from_view
from utils import idx_to_x_z_rot


# import sys
# sys.path.append('../..')
# from clients.python.utils import square_spiral


def top_left_corner_screenshot(name: str, bbox):
    im = ImageGrab.grab(bbox)

    # Save image to file
    im.save(os.path.abspath(os.path.join(os.getcwd(), "../..", 'data', 'screenshots', f"{name}.png")))


def cube_to_voxels(cube: Cube, shape: tuple, min_xyz: tuple):
    voxels = np.zeros(shape)
    for block in cube.blocks:
        if block.type != AIR:
            voxels[block.position.x - min_xyz[0], block.position.y - min_xyz[1], block.position.z - min_xyz[2]] = 1
    return voxels


def read_cube(client, min_xyz: tuple, max_xyz: tuple):
    print(min_xyz, max_xyz)
    return client.readCube(Cube(min=Point(x=min_xyz[0], y=min_xyz[1], z=min_xyz[2]),
                                max=Point(x=max_xyz[0], y=max_xyz[1], z=max_xyz[2])))


def get_screenies(client, num_samples, load: bool = False):
    """Boopchie does a tourism."""
    SCREENSHOT_SIZE = (512, 512)
    BBOX_OFFSET = (0, 66)  # For 16" M1 MacBook Pro
    BBOX = (BBOX_OFFSET[0], BBOX_OFFSET[1], BBOX_OFFSET[0] + SCREENSHOT_SIZE[0], BBOX_OFFSET[1] + SCREENSHOT_SIZE[1])
    # Continue when user enters "y"
    input(
        "Put the Minecraft window in the top corner of the screen (do not scale it!). Enter the server (localhost) and " +
        " enter camera mode (F1). Press enter to continue...")
    print("Now change focus to the Minecraft window. (User, e.g. alt + tab. Do not move the window!)")

    i = 0
    scrn_coords = pd.DataFrame(columns=["x", "y", "z", "rot"])
    vox_coords = pd.DataFrame(columns=["x", "y", "z", "rot"])

    print("Minecraft is active window now!")
    # User pyautogui to take a screenshot of the Minecraft window

    y = 0  # dummy height variable
    while i < num_samples:
        if load and os.path.exists(os.path.join("data", "screenshots", f"{i}.png")):
            i += 1
            continue
        if i % 100 == 0:
            # FIXME: hack to keep weather clear and daylight on, since this function does not seem to have a lasting effect.
            client.initDataGen(Point(x=0, y=0, z=0))  # dummy point variable
        x, z, rot = idx_to_x_z_rot(i)
        x *= 20
        z *= 20
        loc = client.setLoc(Point(x=x, y=y, z=z))
        client.setRot(Point(x=0, y=rot, z=0))
        assert loc.x == x and loc.z == z
        y = loc.y
        scrn_coords.loc[i] = [x, y, z, rot]
        foothold_cube = read_cube(client, (x, y - 1, z), (x, y - 1, z))
        # Don't overwrite existing screenshots if loading (in case we need to fix a select few that were duds, in which
        # case we'll delete these manually and reset the index in proj.json to an earlier value).
        if foothold_cube.blocks[0].type == WATER:
            print("Water detected at", x, y, z)
            i += 1
            continue
        vox_x, vox_z = get_vox_xz_from_view(x, z, rot)
        vox_coords.loc[i] = [vox_x, y, vox_z, rot]
        if (i + 1) % 100 == 0:
            # Save dataframe to file
            # TODO: Append to the file instead of overwriting
            scrn_coords.to_csv(os.path.join("data", "screenshot_coords.csv"))
            vox_coords.to_csv(os.path.join("data", "vox_coords.csv"))
            print(f"Saved {i + 1} samples")
        top_left_corner_screenshot(f"{i}", bbox=BBOX)
        print(f"Saved sreenshot {i}, location {x}, {y}, {z}")
        i += 1


def main(mode: str = "screenies", num_samples: int = 1000, load: bool = False):
    channel = grpc.insecure_channel('localhost:5001')
    client = src.main.proto.minecraft_pb2_grpc.MinecraftServiceStub(channel)
    # NOTE: num_samples is an upper bound on number of screenshots (since we don't take screenshots from on top of water).
    #  We do take all voxel samples, though.
    if mode == "screenies":
        get_screenies(client=client, num_samples=num_samples, load=load)
        # elif mode == "voxels":
        #     get_voxel_chunks(client, num_samples, load)
        # else:
        raise ValueError("Invalid mode")


if __name__ == "__main__":
    Fire(main)
