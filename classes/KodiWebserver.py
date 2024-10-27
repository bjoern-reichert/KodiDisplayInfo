import json
import warnings
import socket
try:
    import urllib2 as urllibopen  # Python2
    warnings.filterwarnings("ignore", category=UserWarning, module='urllib2')
except ImportError:
    import urllib.request as urllibopen  # Python3
    warnings.filterwarnings("ignore", category=UserWarning, module='urllib')


class KodiWebserver:
    
    __ip_port = ""

    def __init__(self, helper, _config_default, draw_default):
        self.helper = helper
        self._config_default = _config_default
        self.draw_default = draw_default

        self.__ip_port = 'http://'+self._config_default['KODI.webserver.host']+':'+self._config_default['KODI.webserver.port']+'/'

        if self._config_default['KODI.webserver.user'] != "" and self._config_default['KODI.webserver.pass'] != "":
            passman = urllibopen.HTTPPasswordMgrWithDefaultRealm()
            passman.add_password(None, self.__ip_port, self._config_default['KODI.webserver.user'], self._config_default['KODI.webserver.pass'])
            urllibopen.install_opener(urllibopen.build_opener(urllibopen.HTTPBasicAuthHandler(passman)))

    def __get_json(self, jsondata, get_parameter = 'jsonrpc?request='):
        self.draw_default.setinfotext("", self._config_default['color.white'])
        try:
            headers = {'content-type': 'application/json'}
            json_data = json.dumps(json.loads(jsondata))
            post_data = json_data.encode('utf-8')
            request = urllibopen.Request(self.__ip_port + get_parameter, post_data, headers)

            result = urllibopen.urlopen(request, timeout=3).read()
            return json.loads(result.decode("utf-8"))
        except socket.timeout:
            self.draw_default.setinfotext("NO KODI ACCESS!", self._config_default['color.red'])
            return json.loads('{"id":1,"jsonrpc":"2.0","result":[]}')
        except IOError:
            self.draw_default.setinfotext("NO KODI ACCESS!", self._config_default['color.red'])
            return json.loads('{"id":1,"jsonrpc":"2.0","result":[]}')

    def kodi_getactiveplayers(self):
        try:
            parsed_json = self.__get_json('{"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1}')
            try:
                return parsed_json['result'][0]['playerid'], parsed_json['result'][0]['type']
            except KeyError:
                return -1, ""  
            except IndexError:
                return -1, ""
        except ValueError:
            self.helper.printout("[warning]    ", self._config_default['mesg.red'])
            self.helper.printout('Decoding JSON has failed')
            return -1, ""
        
    def kodi_getitemvideo(self, playerid):
        try:
            parsed_json = self.__get_json('{"jsonrpc": "2.0", "method": "Player.GetItem", "params": { "properties": ["title","thumbnail","art","file"], "playerid": '+str(playerid)+' }, "id": "VideoGetItem"}')
            try:
                mid = 0
                try:          
                    mid = parsed_json['result']['item']['id']
                except KeyError:
                    pass
                
                title = parsed_json['result']['item']['title']
                if title == "":
                    title = parsed_json['result']['item']['label']
                
                thumbnail = self._config_default['basedirpath']+'img/kodi.png'
                try:
                    if parsed_json['result']['item']['art']['poster'] != "" and parsed_json['result']['item']['art']['poster'].find('.jpg') != -1:
                        thumbnail = parsed_json['result']['item']['art']['poster'].replace("image://", "")[:-1]
                    elif parsed_json['result']['item']['thumbnail'] != "" and parsed_json['result']['item']['thumbnail'].find('.jpg') != -1:
                        thumbnail = parsed_json['result']['item']['thumbnail'].replace("image://", "")[:-1]
                except KeyError:
                    pass

                file = parsed_json['result']['item']['file']

                return mid, title, thumbnail, file
            except KeyError:
                return -1, "", "", ""
            except IndexError:
                return -1, "", "", ""
        except ValueError:
            self.helper.printout("[warning]    ", self._config_default['mesg.red'])
            self.helper.printout('Decoding JSON has failed')
            return -1, "", "", ""
        
    def kodi_getitemaudio(self, playerid):
        try:
            parsed_json = self.__get_json('{"jsonrpc": "2.0", "method": "Player.GetItem", "params": { "properties": ["title", "album", "artist", "track", "year", "thumbnail"], "playerid": '+str(playerid)+' }, "id": "AudioGetItem"}')
            try:
                mid = 0
                try:          
                    mid = parsed_json['result']['item']['id']
                except KeyError:
                    pass
                
                track = parsed_json['result']['item']['track']
                
                title = parsed_json['result']['item']['title']
                if title == "":
                    title = parsed_json['result']['item']['label']
                
                thumbnail = self._config_default['basedirpath']+'img/kodi.png'
                try:
                    if parsed_json['result']['item']['thumbnail'] != "" and parsed_json['result']['item']['thumbnail'].find('.jpg') != -1:
                        thumbnail = parsed_json['result']['item']['thumbnail'].replace("image://", "")[:-1]
                except KeyError:
                    pass

                album = parsed_json['result']['item']['album']
                artist = ', '.join(parsed_json['result']['item']['artist'])
                
                year = parsed_json['result']['item']['year']
                if year!="":
                    album = album + " ("+str(year)+")"

                return mid, str(track)+'. '+title, thumbnail, album, artist, ""
            except KeyError:
                return -1, "", "", "", "", ""
            except IndexError:
                return -1, "", "", "", "", ""
        except ValueError:
            self.helper.printout("[warning]    ", self._config_default['mesg.red'])
            self.helper.printout('Decoding JSON has failed')
            return -1, "", "", "", "", ""
        
    def kodi_getproperties(self, playerid):
        try:
            parsed_json = self.__get_json('{"jsonrpc": "2.0", "method": "Player.GetProperties", "params": { "playerid": '+str(playerid)+', "properties": ["speed","time","totaltime"] }, "id": 1}')
            try:
                speed = parsed_json['result']['speed']
                media_time = [int(parsed_json['result']['time']['hours']), int(parsed_json['result']['time']['minutes']), int(parsed_json['result']['time']['seconds'])]
                media_timetotal = [int(parsed_json['result']['totaltime']['hours']), int(parsed_json['result']['totaltime']['minutes']), int(parsed_json['result']['totaltime']['seconds'])]
                return speed, media_time, media_timetotal
            except KeyError as e:
                self.helper.printout("KeyError: " + str(e))
                return 0, [0, 0, 0], [0, 0, 0]
            except IndexError as e:
                self.helper.printout("IndexError: " + str(e))
                return 0, [0, 0, 0], [0, 0, 0]
        
        except ValueError:
            self.helper.printout("[warning]    ", self._config_default['mesg.red'])
            self.helper.printout('Decoding JSON has failed')
            return 0, [0, 0, 0], [0, 0, 0]

    def kodi_gettotalcount(self, what = "video"):
        try:
            parsed_json = self.__get_json('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"limits": { "start" : 0, "end": 1 }}, "id": "libMovies"}')
            if what == "songs":
                parsed_json = self.__get_json('{"jsonrpc": "2.0", "method": "AudioLibrary.GetSongs", "params": {"limits": { "start" : 0, "end": 1 }}, "id": "libSongs"}')
            elif what == "album":
                parsed_json = self.__get_json('{"jsonrpc": "2.0", "method": "AudioLibrary.GetAlbums", "params": {"limits": { "start" : 0, "end": 1 }}, "id": "libAlbums"}')
            try:
                return parsed_json['result']['limits']['total']
            except KeyError as e:
                self.helper.printout("KeyError: " + str(e))
                return 0
            except IndexError as e:
                self.helper.printout("IndexError: " + str(e))
                return 0
            except TypeError as _:
                # self.helper.printout("IndexError: " + str(e))
                return 0
        except ValueError:
            self.helper.printout("[warning]    ", self._config_default['mesg.red'])
            self.helper.printout('Decoding JSON has failed')
            return 0