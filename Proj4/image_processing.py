from byuimage import Image
import sys

def display(filename):
    im=Image(filename)
    im.show()

def darken(filename, output, percent):
    """Write your code here"""
    image=Image(filename)
    for pixel in image:
        pixel.blue*=1-percent
        pixel.green*=1-percent
        pixel.red*=1-percent
    image.save(output)

def sepia(filename, output):
    """Write your code here"""
    image=Image(filename)
    for pixel in image:
        true_red = 0.393*pixel.red + 0.769*pixel.green + 0.189*pixel.blue
        true_green = 0.349*pixel.red + 0.686*pixel.green + 0.168*pixel.blue
        true_blue = 0.272*pixel.red + 0.534*pixel.green + 0.131*pixel.blue
        pixel.blue=true_blue
        if pixel.blue>255:
            pixel.blue=255
        pixel.green=true_green
        if pixel.green>255:
            pixel.green=255
        pixel.red=true_red
        if pixel.red > 255:
            pixel.red = 255
    image.save(output)

def grayscale(filename, output):
    """Write your code here"""
    image=Image(filename)
    for pixel in image:
        average = (pixel.red + pixel.green + pixel.blue) / 3
        pixel.blue=average
        pixel.green=average
        pixel.red=average
    image.save(output)

def make_borders(filename, output, thickness, red, green, blue):
    old=Image(filename)
    new=Image.blank(old.width+2*thickness,old.height+2*thickness)
    for x in range(new.width):
        for y in range(new.height):
            npix=new.get_pixel(x,y)
            if x<thickness or y<thickness: #Left and Top Borders
                npix.red=red
                npix.green=green
                npix.blue=blue
            elif x>old.width+thickness-1 or y>old.height+thickness-1: #Right and Bottom Borders
                npix.red=red
                npix.green=green
                npix.blue=blue
            else: #Copy Old Image
                opix=old.get_pixel(x-thickness,y-thickness)
                npix.red=opix.red
                npix.green=opix.green
                npix.blue=opix.blue
    new.save(output)

def flipped(filename,output):
    old=Image(filename)
    new=Image.blank(old.width,old.height)
    for y in range(old.height):
        for x in range(old.width):
            op=old.get_pixel(x,y)
            np=new.get_pixel(x,new.height-y-1)
            np.red=op.red
            np.green=op.green
            np.blue=op.blue
    new.save(output)

def mirror(filename,output):
    old=Image(filename)
    new=Image.blank(old.width,old.height)
    for y in range(old.height):
        for x in range(old.width):
            op=old.get_pixel(x,y)
            np=new.get_pixel(new.width-x-1,y)
            np.red=op.red
            np.green=op.green
            np.blue=op.blue
    new.save(output)

def collage(f1,f2,f3,f4,output,thickness):
    im1,im2,im3,im4=Image(f1),Image(f2),Image(f3),Image(f4)
    new=Image.blank(3*thickness+im1.width+im2.width, 3*thickness+im1.height+im3.height)
    for x in range(new.width):
        for y in range(new.height):
            np=new.get_pixel(x,y)
            #Check for Vertical Border
            if x<thickness or (x>=thickness+im1.width and x<2*thickness+im1.width) or x>=2*thickness+im1.width+im2.width:
                np.blue=0
                np.green=0
                np.red=0
            #Check for Horizontal Border
            elif y<thickness or (y>=thickness+im1.height and y<2*thickness+im1.height) or y>=2*thickness+im1.height+im3.height:
                np.blue=0
                np.green=0
                np.red=0
            #Check for Image 1
            elif x<thickness+im1.width and y<thickness+im1.height:
                op=im1.get_pixel(x-thickness,y-thickness)
                np.red=op.red
                np.blue=op.blue
                np.green=op.green
            #Check for Image 2
            elif y<thickness+im1.height:
                op=im2.get_pixel(x-2*thickness-im1.width,y-thickness)
                np.red=op.red
                np.blue=op.blue
                np.green=op.green
            #Check for Image 3
            elif x<im1.width+thickness:
                op=im3.get_pixel(x-thickness,y-2*thickness-im1.height)
                np.red=op.red
                np.blue=op.blue
                np.green=op.green
            #Check for Image 4
            else:
                op=im4.get_pixel(x-2*thickness-im1.width,y-2*thickness-im1.height)
                np.red=op.red
                np.blue=op.blue
                np.green=op.green
            
    new.save(output)

def detect_green(pixel,factor=1.3,threshold=100):
    average = (pixel.red + pixel.green + pixel.blue) / 3
    if pixel.green >= factor * average and pixel.green > threshold:
        return True
    else:
        return False
    
def greenscreen(fr,b,output,threshold,factor):
    front,new=Image(fr),Image(b)
    for x in range(new.width):
        for y in range(new.height):
            front_pixel=front.get_pixel(x,y)
            if not detect_green(front_pixel,factor,threshold):
                new_pixel=new.get_pixel(x,y)
                new_pixel.green=front_pixel.green
                new_pixel.blue=front_pixel.blue
                new_pixel.red=front_pixel.red
    new.save(output)

def validate_commands(args):
    if args[1] == '-d' and len(args)>2:
        print('Valid Command: working on it')
        display(args[2])
        return True
    elif args[1] == '-k' and len(args)>4:
        print('Valid Command: working on it')
        darken(args[2],args[3],float(args[4]))
        return True
    elif args[1] == '-s' and len(args)>3:
        print('Valid Command: working on it')
        sepia(args[2],args[3])
        return True
    elif args[1] == '-g' and len(args)>3:
        print('Valid Command: working on it')
        grayscale(args[2],args[3])
        return True
    elif args[1] == '-b' and len(args)>7:
        print('Valid Command: working on it')
        make_borders(args[2],args[3],int(args[4]),int(args[5]),int(args[6]),int(args[7]))
        return True
    elif args[1] == '-f' and len(args)>3:
        print('Valid Command: working on it')
        flipped(args[2],args[3])
        return True
    elif args[1] == '-m' and len(args)>3:
        print('Valid Command: working on it')
        mirror(args[2],args[3])
        return True
    elif args[1] == '-c' and len(args)>7:
        print('Valid Command: working on it')
        collage(args[2],args[3],args[4],args[5],args[6],int(args[7]))
        return True
    elif args[1] == '-y' and len(args)>6:
        print('Valid Command: working on it')
        greenscreen(args[2],args[3],args[4],int(args[5]),float(args[6]))
        return True
    print("Ummm, invalid command. What are you doing?")
    return False

if __name__ == '__main__':
    validate_commands(sys.argv)