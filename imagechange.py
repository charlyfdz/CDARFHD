from PIL import Image

imageFile = "assets/logo.gif"

im1 = Image.open(imageFile)

width = 200
height = 200

im2 = im1.resize((width, height), Image.NEAREST)      # use nearest neighbour
im3 = im1.resize((width, height), Image.BILINEAR)     # linear interpolation in a 2x2 environment
im4 = im1.resize((width, height), Image.BICUBIC)      # cubic spline interpolation in a 4x4 environment
im5 = im1.resize((width, height), Image.ANTIALIAS)    # best down-sizing filter
ext = ".gif"
im2.save("NEAREST" + ext)
im3.save("BILINEAR" + ext)
im4.save("BICUBIC" + ext)
im5.save("ANTIALIAS" + ext)

