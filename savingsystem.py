# Imports, sorted alphabetically.

# Python packages
import cPickle as pickle
import cStringIO as StringIO
import os
import struct
import zlib

# Third-party packages
# Nothing for now...

# Modules from this project
from blocks import BlockID
from debug import performance_info
import globals as G
from model import *
from player import *


structvec = struct.Struct("hhh")
structushort = struct.Struct("H")
structuchar2 = struct.Struct("BB")
structvecBB = struct.Struct("hhhBB")


@performance_info
def save_world(window, game_dir, world=None):
    if world is None: world = "world"
    if not os.path.exists(os.path.join(game_dir, world)):
        os.makedirs(os.path.join(game_dir, world))

    #Non block related data
    save = (3,window.player, window.time_of_day)
    pickle.dump(save, open(os.path.join(game_dir, world, "save.pkl"), "wb"))

    #blocks and sectors (window.model and window.model.sectors)
    if G.SAVE_MODE == G.FLATFILE_SAVE_MODE:
        blocks = window.model
        with open(os.path.join(game_dir, world, "blocks.dat"), "wb", 1024*1024) as f:
            f.write(struct.pack("Q",len(blocks)))
            for blockpos in blocks:
                id = blocks[blockpos].id
                f.write(structvec.pack(*blockpos) + structuchar2.pack(id.main, id.sub))
    elif G.SAVE_MODE == G.PICKLE_COMPRESSED_SAVE_MODE:
        worldsave = (window.model.items(), window.model.sectors)
        save_string = zlib.compress(pickle.dumps(worldsave), 9)
        file = open(os.path.join(game_dir, world, "blocks.pkl"), "wb")
        file.write(struct.pack("B", 1)) #Save Version
        file.write(save_string)
        file.close()
    elif G.SAVE_MODE == G.PICKLE_SAVE_MODE:
        worldsave = (window.model.items(), window.model.sectors)
        save_string = pickle.dumps(worldsave)
        file = open(os.path.join(game_dir, world, "blocks.pkl"), "wb")
        file.write(struct.pack("B", 0)) #Save Version
        file.write(save_string)
        file.close()


def world_exists(game_dir, world=None):
    if world is None: world = "world"
    return os.path.lexists(os.path.join(game_dir, world))


def remove_world(game_dir, world=None):
    if world is None: world = "world"
    if world_exists(game_dir, world):
        import shutil
        shutil.rmtree(os.path.join(game_dir, world))

@performance_info
def open_world(gamecontroller, game_dir, world=None):
    if world is None: world = "world"
    gamecontroller.model = Model(initialize=False)

    #Non block related data
    loaded_save = pickle.load(open(os.path.join(game_dir, world, "save.pkl"), "rb"))
    if loaded_save[0] == 3: #Version 3
        if isinstance(loaded_save[1], Player): gamecontroller.player = loaded_save[1]
        if isinstance(loaded_save[2], float): gamecontroller.time_of_day = loaded_save[2]
    #blocks and sectors (window.model and window.model.sectors)
    if G.SAVE_MODE == G.FLATFILE_SAVE_MODE:
        sectors = gamecontroller.model.sectors
        blocks = gamecontroller.model
        SECTOR_SIZE = G.SECTOR_SIZE
        BLOCKS_DIR = G.BLOCKS_DIR
        print bool(BlockID(0, 0))
        with open(os.path.join(game_dir, world, "blocks.dat"), "rb") as f:
            for i in xrange(struct.unpack("Q",f.read(8))[0]):
                bx, by, bz, blockid, dataid = structvecBB.unpack(f.read(8))
                position = bx,by,bz
                blocks[position] = BLOCKS_DIR[(blockid, dataid)]
                sectors[(bx/SECTOR_SIZE, 0, bz/SECTOR_SIZE)].append(position)
    else:
        file = open(os.path.join(game_dir, world, "blocks.pkl"), "rb")
        fileversion = struct.unpack("B",file.read(1))[0]
        if fileversion == G.PICKLE_COMPRESSED_SAVE_MODE:
            loaded_world = pickle.load(StringIO.StringIO(zlib.decompress(file.read())))
            for item in loaded_world[0]:
                gamecontroller.model[item[0]] = item[1]
            gamecontroller.model.sectors = loaded_world[1]
        elif fileversion == G.PICKLE_SAVE_MODE:
            loaded_world = pickle.load(file)
            for item in loaded_world[0]:
                gamecontroller.model[item[0]] = item[1]
            gamecontroller.model.sectors = loaded_world[1]

    gamecontroller.model.post_initialize()
