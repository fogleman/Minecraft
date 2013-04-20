import main
import json
import os
from time import gmtime, strftime

class saveModule(object):
    def __init__(self):
        self.coordDictSave = { str(main.GRASS):'GRASS', str(main.SAND):'SAND', str(main.BRICK):'BRICK', str(main.STONE):'STONE' }
        self.coordDictLoad = { 'GRASS':main.GRASS, 'SAND':main.SAND, 'BRICK':main.BRICK, 'STONE':main.STONE }
        
        self.saveGameFile = 'savegame.sav'
        
    def printStuff(self, txt):
        print(strftime("%d-%m-%Y %H:%M:%S|", gmtime()) + str(txt) ) 
    
    def hasSaveGame(self):
        if os.path.exists(self.saveGameFile) == True:
            return True
        else:
            return False
    
    def loadWorld(self, model):
        self.printStuff('start loading...') 
        fh = open(self.saveGameFile, 'r')
        worldMod = fh.read()
        fh.close()
        
        worldMod = worldMod.split('\n')
        
        for blockLine in worldMod:
            if blockLine != '':
                coords, blockType = blockLine.split('=>')
                model.add_block( tuple(json.loads(coords)), self.coordDictLoad[blockType], False )
        
        self.printStuff('loading completed')
        
    def saveWorld(self, model):
        self.printStuff('start saving...')
        fh = open(self.saveGameFile, 'w')
        worldString = ''
        
        for block in model.world:
            worldString += json.dumps(block) + '=>' + self.coordDictSave[ str(model.world[block]) ] + '\n'

        fh.write(worldString)
        fh.close()
        self.printStuff('saving completed')
