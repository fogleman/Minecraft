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

null2 = struct.pack("xx") #Two \0's
null1024 = null2*512      #1024 \0's
air = G.BLOCKS_DIR[(0,0)]

def sector_to_filename(secpos):
    x,y,z = secpos
    return "%i.%i.%i.pyr" % (x/4, y/4, z/4)
def region_to_filename(region):
    return "%i.%i.%i.pyr" % region
def sector_to_region(secpos):
    x,y,z = secpos
    return (x/4, y/4, z/4)
def sector_to_offset(secpos):
    x,y,z = secpos
    return ((x % 4)*16 + (y % 4)*4 + (z % 4)) * 1024
def sector_to_blockpos(secpos):
    x,y,z = secpos
    return x*8, y*8, z*8

@performance_info
def save_world(window, game_dir, world=None):
    if world is None: world = "world"
    if not os.path.exists(os.path.join(game_dir, world)):
        os.makedirs(os.path.join(game_dir, world))

    #Non block related data
    save = (3,window.player, window.time_of_day)
    pickle.dump(save, open(os.path.join(game_dir, world, "save.pkl"), "wb"))

    #blocks and sectors (window.model and window.model.sectors)
    if G.SAVE_MODE == G.REGION_SAVE_MODE:
        #Saves individual sectors in region files (4x4x4 sectors)
        blocks = window.model
        for secpos in window.model.sectors: #TODO: only save dirty sectors
            if not window.model.sectors[secpos]:
                continue #Skip writing empty sectors
            file = os.path.join(game_dir, world, sector_to_filename(secpos)) 
            if not os.path.exists(file):
                with open(file, "w") as f:
                    f.truncate(64*1024) #Preallocate the file to be 64kb
            with open(file, "rb+") as f: #Load up the region file
                f.seek(sector_to_offset(secpos)) #Seek to the sector offset
                cx, cy, cz = sector_to_blockpos(secpos)
                fstr = ""
                for x in xrange(cx, cx+8):
                    for y in xrange(cy, cy+8):
                        for z in xrange(cz, cz+8):
                            blk = blocks.get((x,y,z), air).id
                            if blk:
                                fstr += structuchar2.pack(blk.main, blk.sub)
                            else:
                                fstr += null2
                f.write(fstr)
    elif G.SAVE_MODE == G.FLATFILE_SAVE_MODE:
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

def sector_exists(sector, world=None):
    if world is None: world = "world"
    return os.path.lexists(os.path.join(G.game_dir, world, sector_to_filename(sector)))

def load_region(model, world=None, region=None, sector=None):
    if world is None: world = "world"
    sectors = model.sectors
    blocks = model
    SECTOR_SIZE = G.SECTOR_SIZE
    BLOCKS_DIR = G.BLOCKS_DIR
    if sector: region = sector_to_region(sector)
    rx,ry,rz = region
    rx,ry,rz = rx*32, ry*32, rz*32
    with open(os.path.join(G.game_dir, world, region_to_filename(region)), "rb") as f:
        #Load every chunk in this region (4x4x4)
        for cx in xrange(rx, rx+32, 8):
            for cy in xrange(ry, ry+32, 8):
                for cz in xrange(rz, rz+32, 8):
                    #Now load every block in this chunk (8x8x8)
                    fstr = f.read(1024)
                    if fstr != null1024:
                        fpos = 0
                        for x in xrange(cx, cx+8):
                            for y in xrange(cy, cy+8):
                                for z in xrange(cz, cz+8):
                                    read = fstr[fpos:fpos+2]
                                    fpos += 2
                                    if read != null2:
                                        position = x,y,z
                                        blocks[position] = BLOCKS_DIR[structuchar2.unpack(read)]
                                        sectors[(x/SECTOR_SIZE, y/SECTOR_SIZE, z/SECTOR_SIZE)].append(position)

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
    if G.SAVE_MODE == G.REGION_SAVE_MODE:
        pass #Sectors are loaded by world._show_sector
    elif G.SAVE_MODE == G.FLATFILE_SAVE_MODE:
        sectors = gamecontroller.model.sectors
        blocks = gamecontroller.model
        SECTOR_SIZE = G.SECTOR_SIZE
        BLOCKS_DIR = G.BLOCKS_DIR
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
