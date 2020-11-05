
### now

```
self.World = {}
{[x, y, z]: TEXTURE}
```

## TEXTURE:

```
GRASS = tex_coords((1, 0), (0, 1), (0, 0))
SAND = tex_coords((1, 1), (1, 1), (1, 1))
BRICK = tex_coords((2, 0), (2, 0), (2, 0))
STONE = tex_coords((2, 1), (2, 1), (2, 1))
```

### want to be

```
self.World = {}
{[chunk_id]: {[x, y, z]: [block_states, ]}}
```
