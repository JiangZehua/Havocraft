import numpy as np
import torch
from src.main.proto.minecraft_pb2 import *
from src.main.proto.minecraft_pb2_grpc import *

# name of the blocks map to Minecraft block index
textures_to_ec = {
    "stone": STONE,
    "dirt": DIRT,
    "brick": BRICK_BLOCK,
    "cactus": CACTUS,
    "clay": CLAY,
    "coal_ore": COAL_ORE,
    "log_oak": LOG,
    "snow": SNOW,
    "glazed_terracotta_light_blue": LIGHT_BLUE_GLAZED_TERRACOTTA,
    "glazed_terracotta_yellow": YELLOW_GLAZED_TERRACOTTA,
    "redstone_block": REDSTONE_BLOCK,
    "gold_block": GOLD_BLOCK,
    "iron_block": IRON_BLOCK,
    "diamond_block": DIAMOND_BLOCK,
    "emerald_block": EMERALD_BLOCK,
    "cobblestone": COBBLESTONE,
    "slime": SLIME,
    "water_still": WATER,
    "sand": SAND,
    "sandstone": SANDSTONE,
    "iron_ore": IRON_ORE,
    "gold_ore": GOLD_ORE,
    "gravel": GRAVEL,
    "deadbush": DEADBUSH,
    "mushroom_block_skin_brown": BROWN_MUSHROOM_BLOCK,
    "glass": GLASS,
    "air": AIR,
}


# read the .npz file and map the block array to the mc indexes
def load_data(data_path):
    data = torch.load(data_path, map_location=torch.device('cpu'))
    block_names_to_idxs = data['block_names_to_idxs']
    block_arr = data['block_arr'].float()
    density_arr_hard = data['density_arr_hard'].float()

    idxs_to_textures = {v: k for k, v in block_names_to_idxs.items()}
    idxs_to_ec = {k: textures_to_ec[v] for k, v in idxs_to_textures.items()}
    block_arr = block_arr.round().int().cpu().numpy().argmax(axis=0)
    density_arr_hard = density_arr_hard.round().int().cpu().numpy()
    block_arr = np.vectorize(idxs_to_ec.get)(block_arr)
    # Place air wherever the density is 0
    block_arr = np.where(density_arr_hard == 0, AIR, block_arr)
    return block_arr


# orig: block spawn original position
def spawn_block(client, orig, blocks):
    # Only operate on a handful of blocks or less at once
    x0, y0, z0 = orig
    block_lst = []
    for k in range(len(blocks)):
        for j in range(len(blocks[k])):
            for i in range(len(blocks[k][j])):
                block = int((blocks[k][j][i]))
                block_lst.append(Block(position=Point(x=x0 + i, y=y0 + j, z=z0 + k),
                                       type=block, orientation=NORTH))
    # the matrix's size is 10000
    n_blocks = 10000
    for i in range(0, len(block_lst), n_blocks):
        client.spawnBlocks(Blocks(blocks=block_lst[i:i + n_blocks]))


# 300 represents the height of the spawn block
def render_blocks(block_arr):
    channel = grpc.insecure_channel('localhost:5001')
    client = MinecraftServiceStub(channel)
    spawn_block(client, (0, 150, 0), block_arr)


def load_block_in_Minecraft(path):
    block_arr = load_data(path)
    render_blocks(block_arr)


# eg:
load_block_in_Minecraft('../../data/ec_block_arr_w-100.npz')
