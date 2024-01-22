#!/usr/bin/python3

version_string = "Cut Screenshot Borders (csb.py) ver. 1.0 by may - 22.01.2024"

from PIL import Image
import numpy as np
import sys
import argparse

### defaults #########################################################################################################
pic = ""
bg = False
variance = 10.0
debug = False

### Array<Int> string2Int(String string) ##############################################################################
def string2Int(string):
  b = 2 * bitDepth
  o_array = [0] * bitDepth
  t_string = string[:(bitDepth*2)]

  for i in range(0,bitDepth):
    b = i*2
    o_array[i] = int( (t_string[b] + t_string[b+1]),16 )

  return o_array

#######################################################################################################################
parser = argparse.ArgumentParser()

parser.add_argument("-v", "--version", action="store_true", help="print actual version of csb")
parser.add_argument("-d", "--debug", action="store_true", help="enable debug mode")
parser.add_argument("-bg", type=str, help="specify a custom background color <hex-string>")
parser.add_argument("-V", "--variance", type=float, help="specify a custom variance <float>")
parser.add_argument("pic", nargs='?', help="file to process")

args = parser.parse_args()

if (args.version ):
  print(version_string)

if (args.debug ):
  debug = True
  print("Debug enabled")

if (args.bg ):
  bg = args.bg
  print("Custom Background: " + str(args.bg))

if (args.variance ):
  variance = args.variance
  print("Custom Variance: " + str(variance))

if (args.pic ):
  pic = (args.pic).strip("./")
else:
  print("No file specified. Exiting")
  sys.exit(0)

### Global Variables ###########################################
# pic = sys.argv[1]
im = Image.open(pic)
imnp = np.array(im)
bitDepth = len(imnp[0][0])
new_pic = ""
debug_rgba = [255,0,0]


l_prefix = len(pic)
suffix = pic.rsplit('.')[-1]
l_suffix = len(suffix)+1
prefix = pic[:(l_prefix-l_suffix)]

if (debug):
  print("DEBUG !")
  if (bitDepth > 3):
    debug_rgba = [255,0,0,0]
  new_pic = prefix + '_csb_edit_debug.' + suffix
else:
  new_pic = prefix + '_csb_edit.' + suffix

print("File: " + str(pic) + " : " + im.format, im.size, im.mode + " Color Channels: " + str(bitDepth) + " -> " + str(new_pic)  )


### Background detection #######################################
rgba = imnp[0][0]

if (bg):
  rgba = string2Int(bg) 
  print("Custom background color: " + str(rgba) )
else:
  print("Background Color detected: " + str(rgba) )

### Raster ####################################################
hPixel = len(imnp[0])
hits = []
ll = 0
dist = 0
maxDist = 0
maxBlock = [0,0,0]
line_type = "BG"
ack_type = "BG"
vLines = len(imnp)
cmLine = []
debug_cmLine = []
var_imnp = []

for p in range (0, hPixel):
  cmLine.append(rgba)                                           ### Load the comparing line (cmLine) with rgba values

vmLine = np.array(cmLine)                                       ### transfor Array to numpy-Array

if (debug):                                                     ### if Debug is enabled ...
  for p in range (0, hPixel):
    debug_cmLine.append(debug_rgba)                             ### Load the debug indicator line with debug_rgba values
  debug_vmLine = np.array(debug_cmLine)                         ### transfor Array to numpy-Array


for l in range(0,vLines):
  if np.array_equal(imnp[l],vmLine):
    line_type = "BG"
  else:
    var_imnp = np.var((imnp[l] - vmLine), axis=0)
    if ( (var_imnp[0] >= variance) or (var_imnp[1] >= variance) or (var_imnp[2] >= variance) ):
      line_type = "Line"
    else:
      line_type = "BG"

  if (line_type != ack_type):
    hit = [ll,l,(l-ll),ack_type]
    hits.append(hit)
    ack_type = line_type
    ll = l

    if (debug):
      imnp[l] = debug_vmLine 

last_position = hits[-1][1]
hit = [last_position,vLines,(vLines-last_position),line_type]
hits.append(hit)

if (debug):
  for v in range(len(hits)):
    print(v, hits[v])

for v in range(len(hits)):
  dist = hits[v][2]
  if (maxDist < dist):
    maxDist = dist
    maxBlock = hits[v]


print("Max image block detected between lines: " + str(maxBlock) )
if (debug):
  nim = Image.fromarray(imnp, mode=im.mode )
  nim.show()
else:
  nim = Image.fromarray(imnp[(maxBlock[0]+1):(maxBlock[1]-1)], mode=im.mode )


### write new image file ####################################

nim.save(new_pic, quality=95)
