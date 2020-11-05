
# now form of self.World

```
self.World = {
    [x, y, z]: TEXTURE
    }
```

## TEXTURE are:

```
GRASS = tex_coords((1, 0), (0, 1), (0, 0))
SAND = tex_coords((1, 1), (1, 1), (1, 1))
BRICK = tex_coords((2, 0), (2, 0), (2, 0))
STONE = tex_coords((2, 1), (2, 1), (2, 1))
```

# the form want to be of self.World

```
self.World = {
    [chunk_id]: {
        [x1, y1, z1]: 
        [block_id, block_states, [x2, y2 z2]]
        }
    }
```

## inputs

```
x/y/z 1 -> the poi in the world
x/y/z 2 -> the poi in the subchunk
block_id : grass block/brick/stone····
block_states : sand:[float/on ground]
chunk_id : [0, 0]/[0, 1]
```
