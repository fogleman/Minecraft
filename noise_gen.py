import random as rand 
import math

class NoiseParameters:
    def __init__(self, octaves, amplitude, smoothness, roughness, heightOffset):
        self.octaves = octaves
        self.amplitude = amplitude
        self.smoothness = smoothness
        self.roughness = roughness
        self.heightOffset = heightOffset

class NoiseGen:
    def __init__(self, seed):
        self.seed = seed
        self.noiseParams = NoiseParameters(
            7, 50, 450, 0.3, 20
        )

    def _getNoise2(self, n):
        n += self.seed 
        n = (int(n) << 13) ^ int(n)
        newn = (n * (n * n * 60493 + 19990303) + 1376312589) & 0x7fffffff
        return 1.0 - (float(newn) / 1073741824.0)

    def _getNoise(self, x, z):
        return self._getNoise2(x + z * 57)

    def _lerp(self, a, b, z):
        mu2 = (1.0 - math.cos(z * 3.14)) / 2.0
        return (a * (1 - mu2) + b * mu2)

    def _noise(self, x, z):
        floorX = float(int(x))
        floorZ = float(int(z))

        s = 0.0,
        t = 0.0,
        u = 0.0,
        v = 0.0;#Integer declaration

        s = self._getNoise(floorX,      floorZ)
        t = self._getNoise(floorX + 1,  floorZ)
        u = self._getNoise(floorX,      floorZ + 1)
        v = self._getNoise(floorX + 1,  floorZ + 1)

        rec1 = self._lerp(s, t, x - floorX)
        rec2 = self._lerp(u, v, x - floorX)
        rec3 = self._lerp(rec1, rec2, z - floorZ)
        return rec3

    def getHeight(self, x, z):
        totalValue = 0.0

        for a in range(self.noiseParams.octaves - 1):
            freq = math.pow(2.0, a)
            amp  = math.pow(self.noiseParams.roughness, a)
            totalValue += self._noise(
                (float(x)) * freq / self.noiseParams.smoothness,
                (float(z)) * freq / self.noiseParams.smoothness
            ) * self.noiseParams.amplitude

        result = (((totalValue / 2.1) + 1.2) * self.noiseParams.amplitude) + self.noiseParams.heightOffset

        return (totalValue / 5) + self.noiseParams.heightOffset
