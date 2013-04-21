from math import sin, cos, pi

from pyglet.gl import *
import pyglet

class Skydome(object):
    def __init__(self, filename, brightness=1.0, size=1.0, direction=0):
        self.direction = direction
        self.image = pyglet.image.load(filename)
        self.color = [brightness]*3
        
        t = self.image.get_texture().tex_coords
        u = t[3]
        pixel_width = u / self.image.width
        v = t[7]

        ustart = pixel_width
        uend = u - pixel_width
        vstart = 0
        vend = v

        vertex = list()
        uvs = list()
        count = 0

        def sphere_vert(i, j):
            i = i/10.0
            j = j/40.0
            s = sin(pi*i*0.5)
            z = cos(pi*i*0.5) * size
            x = sin(pi*j*2.0) * s * size
            y = cos(pi*j*2.0) * s * size

            u = (j*(uend - ustart)) + ustart
            v_length = vend - vstart
            v = (v_length-i*v_length) + vstart
            return (x, y, z), (u, v)
    
        for j in range(40):
            v, uv = sphere_vert(0, j)
            vertex.extend(v); uvs.extend(uv)
            v, uv = sphere_vert(1, j)
            vertex.extend(v); uvs.extend(uv)
            v, uv = sphere_vert(1, j+1)
            vertex.extend(v); uvs.extend(uv)
            count += 3
      
        for i in range(1, 10):
            for j in range(40):
                v, uv = sphere_vert(i, j)
                vertex.extend(v); uvs.extend(uv)
                v, uv = sphere_vert(i+1, j)
                vertex.extend(v); uvs.extend(uv)
                v, uv = sphere_vert(i+1, j+1)
                vertex.extend(v); uvs.extend(uv)
                
                v, uv = sphere_vert(i, j)
                vertex.extend(v); uvs.extend(uv)
                v, uv = sphere_vert(i+1, j+1)
                vertex.extend(v); uvs.extend(uv)
                v, uv = sphere_vert(i, j+1)
                vertex.extend(v); uvs.extend(uv)

                count += 6

        self.display = pyglet.graphics.vertex_list(count,
            ('v3f/static', vertex),
            ('t2f/static', uvs),
        )

    def draw(self):
        glPushMatrix()
        glBindTexture(GL_TEXTURE_2D, self.image.texture.id)
        glEnable(GL_TEXTURE_2D)
        glColor3f(*self.color)
        glRotatef(-self.direction, 0, 0, 1)
        self.display.draw(GL_TRIANGLES)
        glPopMatrix()
