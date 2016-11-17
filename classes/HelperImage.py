import cStringIO
from PIL import Image
try:
    from urllib2 import urlopen # Python2
except ImportError:
    from urllib.request import urlopen # Python3
    
class HelperImage():
    
    def setPygameScreen(self, pygame, screen):
        self.pygame = pygame
        self.screen = screen
    
    def scaleImage(self, url, max_width, max_heigth):

        if url!="":
            try:
                #load
                if url.startswith('http://'):
                    im = cStringIO.StringIO(urlopen(url).read())
                else:
                    im = url
                
                image_resize = Image.open(im)
        
                #resize
                width = max_width
                wpercent = (max_width/float(image_resize.size[0]))
                heigth = int((float(image_resize.size[1]) * float(wpercent)))
            
                if heigth > max_heigth:
                    heigth = max_heigth
                    hpercent = (max_heigth/float(image_resize.size[1]))
                    width = int((float(image_resize.size[0]) * float(hpercent)))

                image_resize = image_resize.resize((width,heigth), Image.ANTIALIAS)

                image = Image.new("RGBA", (max_width, max_heigth))
                posx = int((max_width-width)/2)
                posy = int((max_heigth-heigth)/2)
                image.paste(image_resize, (posx,posy))

                # convert
                mode = image.mode
                size = image.size
                data = image.tobytes()
                return self.pygame.image.fromstring(data, size, mode)
            except IOError:
                return ""
        return ""
    