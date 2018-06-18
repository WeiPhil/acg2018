###############################################################################################################
# Author: Philippe Weier
# This little python scripts takes a modifiated version of blender's smoke simulation output and outputs a
# a binary file readable by my Nori's implementation of voxelGrid.
###############################################################################################################

import struct
import numpy as np
import sys

SIZEOFCHAR = 1
SIZEOFFLOAT = 4
SIZEOFINT = 4
SIZEOFDOUBLE = 8


###############################################################################################################
# Note: Data is stored using blender coordinates system -> (x + x_res * (y + z * y_res))                      #
# but we read it in nori using nori's coordinate system. (z up) -> (x + x_res * (z + y * z_res))              #
###############################################################################################################

# We first parse the header
def read_smoke_header(f):
    version = f.read(SIZEOFFLOAT)
    print("# LOG # ","Version: " + version.decode())

    fluid_fields = f.read(SIZEOFFLOAT)
    fluid_fields = struct.unpack("i", fluid_fields)[0]
    print("# LOG # ","Fluid fields: " + str(fluid_fields))

    active_fields = f.read(SIZEOFFLOAT)
    active_fields = struct.unpack("i", active_fields)[0]
    print("# LOG # ","Active fields: " + str(active_fields))
    
    res = f.read(3*SIZEOFFLOAT)
    (res1,res2,res3) = struct.unpack("iii", res)
    print("# LOG # ","Res:(%d %d %d)"%(res1,res2,res3))
    
    dx = f.read(SIZEOFFLOAT)
    dx = struct.unpack("f", dx)[0]
    print("# LOG # ",dx)
    
    tot_res = res1*res2*res3
    in_len = SIZEOFFLOAT* tot_res
    
    print("# LOG # ",in_len)
    
    return (res1,res2,res3)
    
    
def getChunk(f,x_res,y_res,z_res):
    data = np.zeros((x_res,y_res,z_res))
    
    data1d = list()
    for i in range(0,x_res*y_res*z_res):
        data1d.append(struct.unpack("f", f.read(SIZEOFFLOAT))[0])
        
    for x in range(0,x_res):
        for y in range(0,y_res):
            for z in range(0,z_res):
                index = x + x_res * (y + z * y_res);
                data[x][y][z] = data1d[index]
    
    return (data,data1d)

def extractSmoke(filename):
    f = open(filename, "rb")

    magic = f.read(8*SIZEOFCHAR)
    if magic != b'BPHYSICS':
        raise Exception("not a blender physics cache")

    flavor = f.read(3*SIZEOFINT)
    (flavor,count,something) = struct.unpack("iii", flavor)

    print("# LOG # ","%d\t%d\t%d"%(flavor,count,something))

    if flavor==3: # point cache
        (res1,res2,res3) = read_smoke_header(f)
        print("# LOG # ",(res1,res2,res3))
        
        numCells = res1*res2*res3;
        
        info = f.read(5*SIZEOFCHAR)
        print("# LOG # ",info.decode())
        
        info = f.read(4*SIZEOFCHAR)
        print("# LOG # ",info.decode())
      
        (shadows,shadows1D) = getChunk(f,res1,res2,res3)
        
        info = f.read(9*SIZEOFCHAR)
        print("# LOG # ",info.decode())
        
        (density,density1D) = getChunk(f,res1,res2,res3)
        
        info = f.read(7*SIZEOFCHAR)
        print("# LOG # ",info.decode())
        
        info = f.read(4*SIZEOFCHAR)
        print("# LOG # ",info.decode())
        
        (heat,heat1D) = getChunk(f,res1,res2,res3)
        
        (heatOld,heatOld1D) = getChunk(f,res1,res2,res3)
        
        obstacles = f.read(numCells)
        
        (vx,vx1D) = getChunk(f,res1,res2,res3)
        (vy,vy1D) = getChunk(f,res1,res2,res3)
        (vz,vz1D) = getChunk(f,res1,res2,res3)
        
        dt = struct.unpack("f", f.read(SIZEOFFLOAT))[0]
        dx = struct.unpack("f", f.read(SIZEOFFLOAT))[0]
        print("# LOG # ",dt,dx)
        
        p0 = struct.unpack("f f f", f.read(3*SIZEOFFLOAT))
        p1 = struct.unpack("f f f", f.read(3*SIZEOFFLOAT))
        
        print("# LOG # ",p0)
        print("# LOG # ",p1)
        
        with open(filename+'.density', 'wb') as smokeDataFile:
            smokeDataFile.write(b'DENS')
            smokeDataFile.write(struct.pack('i', res1))
            smokeDataFile.write(struct.pack('i', res2))
            smokeDataFile.write(struct.pack('i', res3))
            smokeDataFile.write(struct.pack('%sf' % len(density1D), *density1D))
            print("# LOG # Smoke density wrote to '"+filename+".density'")
            
        with open(filename+'.albedo', 'wb') as smokeDataFile:
            smokeDataFile.write(b'ALBE')
            smokeDataFile.write(struct.pack('i', res1))
            smokeDataFile.write(struct.pack('i', res2))
            smokeDataFile.write(struct.pack('i', res3))
            smokeDataFile.write(struct.pack('%sf' % len(heat1D), *heat1D))
            print("# LOG # Smoke heat wrote to '"+filename+".albedo' ")
            
            
        # return (shadows,density,heat,heatOld,vx,vy,vz)


if __name__ == "__main__":
    filename = sys.argv[1]
    extractSmoke(filename)