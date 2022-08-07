from PIL import Image
import io, os
try:
    import urllib2 as urllibopen # Python2
    from urllib import unquote
except ImportError:
    import urllib.request as urllibopen # Python3
    from urllib.parse import unquote
try:
    import httplib  # Python2
except:
    import http.client as httplib # Python3

class HelperImage():

    def __init__(self, _ConfigDefault):
        self._ConfigDefault = _ConfigDefault

    def setPygameScreen(self, pygame, screen):
        self.pygame = pygame
        self.screen = screen

    def isInternetReachable(self):
        conn = httplib.HTTPSConnection("8.8.8.8", timeout=3)
        try:
            conn.request("HEAD", "/")
            return True
        except Exception:
            return False
        finally:
            conn.close()

    def scaleImage(self, url, file, max_width, max_heigth):
        isInternetReachable = self.isInternetReachable()
        if url!="":
            try:
                url = unquote(url)
                file = unquote(file)

                #load
                im = ""
                if url.startswith('http') & isInternetReachable == True:
                    im = io.BytesIO(urllibopen.urlopen(url).read())
                elif file!="":
                    filename, file_extension = os.path.splitext(file)
                    im = file.replace(file_extension, "-poster.jpg")
                    if not os.path.exists(im):
                        im = ""
                else:
                    im = url

                if im == "":
                    im = self._ConfigDefault['basedirpath']+'img/kodi.png'

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