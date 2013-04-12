import os
import cPickle as pickle
import zlib
import cStringIO as StringIO
import struct
import math

# Modules from this project
from model import *
from player import *
import globals


structvec = struct.Struct("hhh")
structushort = struct.Struct("H")
structuchar2 = struct.Struct("BB")
structvecBB = struct.Struct("hhhBB")

def save_world(window, game_dir, world=None):
    if world is None: world = "world"
    if not os.path.exists(os.path.join(game_dir, world)):
        os.makedirs(os.path.join(game_dir, world))

    #Non block related data
    save = (3,window.player, window.time_of_day)
    pickle.dump(save, open(os.path.join(game_dir, world, "save.pkl"), "wb"))

    #blocks and sectors (window.model and window.model.sectors)
    if globals.LAUNCH_OPTIONS.save_mode == globals.FLATFILE_SAVE_MODE:
        blocks = window.model
        with open(os.path.join(game_dir, world, "blocks.dat"), "wb", 1024*1024) as f:
            f.write(struct.pack("Q",len(blocks)))
            for blockpos in blocks:
                f.write(structvec.pack(*blockpos) + structuchar2.pack(blocks[blockpos].id_main, blocks[blockpos].id_sub))
        sectors = window.model.sectors
        with open(os.path.join(game_dir, world, "sectors.dat"), "wb", 1024*1024) as f:
            f.write(struct.pack("Q",len(sectors)))
            for secpos in sectors:
                f.write(structvec.pack(*secpos) + structushort.pack(len(sectors[secpos])))
                for blockpos in sectors[secpos]:
                    f.write(structvec.pack(*blockpos))
    elif globals.LAUNCH_OPTIONS.save_mode == globals.PICKLE_COMPRESSED_SAVE_MODE:
        worldsave = (window.model.items(), window.model.sectors)
        save_string = zlib.compress(pickle.dumps(worldsave), 9)
        file = open(os.path.join(game_dir, world, "blocks.pkl"), "wb")
        file.write(struct.pack("B", 1)) #Save Version
        file.write(save_string)
        file.close()
    elif globals.LAUNCH_OPTIONS.save_mode == globals.PICKLE_SAVE_MODE:
        worldsave = (window.model.items(), window.model.sectors)
        save_string = pickle.dumps(worldsave)
        file = open(os.path.join(game_dir, world, "blocks.pkl"), "wb")
        file.write(struct.pack("B", 0)) #Save Version
        file.write(save_string)
        file.close()

def world_exists(game_dir, world=None):
    if world is None: world = "world"
    return os.path.lexists(os.path.join(game_dir, world))

def open_world(gamecontroller, game_dir, world=None):
    if world is None: world = "world"
    gamecontroller.model = Model(initialize=False)

    #Non block related data
    loaded_save = pickle.load(open(os.path.join(game_dir, world, "save.pkl"), "rb"))
    if loaded_save[0] == 3: #Version 3
        if isinstance(loaded_save[1], Player): gamecontroller.player = loaded_save[1]
        if isinstance(loaded_save[2], float): gamecontroller.time_of_day = loaded_save[2]
    #blocks and sectors (window.model and window.model.sectors)
    if globals.LAUNCH_OPTIONS.save_mode == globals.FLATFILE_SAVE_MODE:
        sectors = gamecontroller.model.sectors
        with open(os.path.join(game_dir, world, "sectors.dat"), "rb") as f:
            for i in xrange(struct.unpack("Q",f.read(8))[0]):
                sector = sectors[structvec.unpack(f.read(6))]
                for i2 in xrange(structushort.unpack(f.read(2))[0]):
                    sector.append(structvec.unpack(f.read(6)))
        blocks = gamecontroller.model
        with open(os.path.join(game_dir, world, "blocks.dat"), "rb") as f:
            for i in xrange(struct.unpack("Q",f.read(8))[0]):
                bx, by, bz, blockid, dataid = structvecBB.unpack(f.read(8))
                if dataid is not 0: blockid += (float(dataid) / 10)
                blocks[(bx,by,bz)] = globals.BLOCKS_DIR[blockid]
    else:
        file = open(os.path.join(game_dir, world, "blocks.pkl"), "rb")
        fileversion = struct.unpack("B",file.read(1))[0]
        if fileversion == globals.PICKLE_COMPRESSED_SAVE_MODE:
            loaded_world = pickle.load(StringIO.StringIO(zlib.decompress(file.read())))
            for item in loaded_world[0]:
                gamecontroller.model[item[0]] = item[1]
            gamecontroller.model.sectors = loaded_world[1]
        elif fileversion == globals.PICKLE_SAVE_MODE:
            loaded_world = pickle.load(file)
            for item in loaded_world[0]:
                gamecontroller.model[item[0]] = item[1]
            gamecontroller.model.sectors = loaded_world[1]
