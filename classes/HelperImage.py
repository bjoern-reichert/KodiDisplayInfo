import io, os
from PIL import Image
import socket
try:
    import urllib2 as urllibopen # Python2
    from urllib import unquote
except ImportError:
    import urllib.request as urllibopen # Python3
    from urllib.parse import unquote
try:
    import httplib  # Python2
except ImportError:
    import http.client as httplib # Python3

class HelperImage:

    def __init__(self, helper, config_default):
        self.__pygame = None
        self.__screen = None
        self.__helper = helper
        self.__config_default = config_default

    def set_pygamescreen(self, pygame, screen):
        self.__pygame = pygame
        self.__screen = screen

    @staticmethod
    def is_internetreachable():
        try:
            socket.setdefaulttimeout(3)
            host = socket.gethostbyname("8.8.8.8")
            s = socket.create_connection((host, 53), 2)
            s.close()
            return True
        except (Exception,):
            return False

    def scaleimage(self, url, file, max_width, max_heigth):
        isinternetreachable = self.is_internetreachable()
        if url != "":
            try:
                url = unquote(url).replace(" ", "%20")
                file = unquote(file).replace(" ", "%20")

                #load
                default = self.__helper.get_default_kodilogo()
                if url.startswith('http') & isinternetreachable == True:
                    im = io.BytesIO(urllibopen.urlopen(url).read())
                elif file != "":
                    filename, file_extension = os.path.splitext(file)
                    im = file.replace(file_extension, "-poster.jpg")
                    if not os.path.exists(im):
                        im = default
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

                image_resize = image_resize.resize((width,heigth), Image.LANCZOS)

                image = Image.new("RGBA", (max_width, max_heigth))
                posx = int((max_width-width)/2)
                posy = int((max_heigth-heigth)/2)
                image.paste(image_resize, (posx,posy))

                # convert
                mode = image.mode
                size = image.size
                data = image.tobytes()
                return self.__pygame.image.fromstring(data, size, mode)
            except IOError:
                return ""
        return ""