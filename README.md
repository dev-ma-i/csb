# Cut Screenshot Borders 

``
usage: csb.py [-h] [-v] [-d] [-bg BG] [-V VARIANCE] [pic]

positional arguments:
  pic                   file to process

options:
  -h, --help                          show this help message and exit
  -v, --version                       print actual version of csb
  -d, --debug                         enable debug mode
  -bg BG                              specify a custom background color <hex-string>
  -V VARIANCE, --variance VARIANCE    specify a custom variance <float>
```

Sometimes you receive pictures from social media sites which can't be directly saved to your cell-phone. If so, the only way to keep a copy is a screenshot. 
But usually such an image also contains additional information like: the name of the posting account, an app identification and/or additional text. 
Suff you may not want to forward if reposted. 
Cut Screenshot Borders (csb.py) is a python script that will automatically crop the top and bottom borders of a screenshot.

CSD.py will "guess" the background color by analysing the first pixel in the uppel left corner of the specified image.
If this is not what you want, you can coose another color by using the "-bg" option followed by a Hex-Sring. E.g. use the string ffffff for "white", 000000 for "black" or ffff00 for "yellow"
CAUTION: Check the bit-depth of the picture. Some use RGB32 instead of RGB24. In this case the background color must also be a 8 char string (instead of 6)

The script will look for the "biggest coherent block of lines" that doesn't correlate to the background color - and then excise it. Depending on the image and the used variance this may not alway work correctly.
Using the "debug" option will insert red lines whenever a deviating block gets detected. A debug image will be written where you can see the lines.

CSB will compare the actual line vs a line filled with the background color. If they differ and the variance is greater then the given threshold, a new block gets detected.
The "variance" option will let you fine-tune this detection threshold. Default is 10.0
Raising the variance will increase the tollerance on when a new block gets detected.

CSB.py creates a croped copy of the original image with a tailing "_csb_edit" to its filename or a "_bc_edit_debug" when used in debug-mode. 
The original file will be left unchanged.
