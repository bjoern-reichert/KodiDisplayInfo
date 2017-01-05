import json, warnings
from socket import timeout
try:
    import urllib2 as urllibopen # Python2
    warnings.filterwarnings("ignore", category=UserWarning, module='urllib2')
except ImportError:
    import urllib.request as urllibopen # Python3
    warnings.filterwarnings("ignore", category=UserWarning, module='urllib')

class KODI_WEBSERVER:
    
    ip_port = ""
    
    def __init__(self, helper, _ConfigDefault, draw_default):
        self.helper = helper
        self._ConfigDefault = _ConfigDefault
        self.draw_default = draw_default
        
        self.ip_port = 'http://'
        self.ip_port = self.ip_port+self._ConfigDefault['KODI.webserver.host']+':'+self._ConfigDefault['KODI.webserver.port']+'/'                 
       
    def getJSON(self, jsondata, get_parameter = 'jsonrpc?request='):
        self.draw_default.setInfoText("", self._ConfigDefault['color.white'])
        try:
            headers = {'content-type': 'application/json'}
            json_data = json.dumps(json.loads(jsondata))
            post_data = json_data.encode('utf-8')
            request = urllibopen.Request(self.ip_port + get_parameter, post_data, headers)
            
            if self._ConfigDefault['KODI.webserver.user']!="" and self._ConfigDefault['KODI.webserver.pass']!="":
                passman = urllibopen.HTTPPasswordMgrWithDefaultRealm()
                passman.add_password(None, self.ip_port, self._ConfigDefault['KODI.webserver.user'], self._ConfigDefault['KODI.webserver.pass'])
                urllibopen.install_opener(urllibopen.build_opener(urllibopen.HTTPBasicAuthHandler(passman)))
            
            result = urllibopen.urlopen(request,timeout=3).read()
            return json.loads(result.decode("utf-8"))
        except IOError:
            self.draw_default.setInfoText("NO KODI ACCESS!", self._ConfigDefault['color.red'])
            return json.loads('{"id":1,"jsonrpc":"2.0","result":[]}')
        except timeout:
            self.draw_default.setInfoText("NO KODI ACCESS!", self._ConfigDefault['color.red'])
            return json.loads('{"id":1,"jsonrpc":"2.0","result":[]}')

    def KODI_GetActivePlayers(self):
        try:
            parsed_json = self.getJSON('{"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1}')
            try:
                return parsed_json['result'][0]['playerid'], parsed_json['result'][0]['type']
            except KeyError:
                return -1, ""
            except IndexError:
                return -1, ""
        except ValueError:
            self.helper.printout("[warning]    ", self._ConfigDefault['mesg.red'])
            self.helper.printout('Decoding JSON has failed')
            return -1, ""
        
    def KODI_GetItemVideo(self, playerid):
        try:           
            parsed_json = self.getJSON('{"jsonrpc": "2.0", "method": "Player.GetItem", "params": { "properties": ["title","thumbnail"], "playerid": '+str(playerid)+' }, "id": "VideoGetItem"}')
            try:
                try:          
                    mid = parsed_json['result']['item']['id']
                except KeyError:
                    mid = 0
                
                title = parsed_json['result']['item']['title']
                if title=="":
                    title = parsed_json['result']['item']['label']
                
                thumbnail = ""
                if parsed_json['result']['item']['thumbnail']!="" and parsed_json['result']['item']['thumbnail'].find('.jpg') != -1:
                    thumbnail = self.ip_port + parsed_json['result']['item']['thumbnail'].replace("image://", "image/")[:-1]
                else:
                    thumbnail = self._ConfigDefault['basedirpath']+'img/kodi.png'
                    
                return mid, title, thumbnail
            except KeyError:
                return -1, "", ""
            except IndexError:
                return -1, "", ""
        except ValueError:
            self.helper.printout("[warning]    ", self._ConfigDefault['mesg.red'])
            self.helper.printout('Decoding JSON has failed')
            return -1, "", ""
        
    def KODI_GetItemAudio(self, playerid):
        try:            
            parsed_json = self.getJSON('{"jsonrpc": "2.0", "method": "Player.GetItem", "params": { "properties": ["title", "album", "artist", "track", "thumbnail"], "playerid": '+str(playerid)+' }, "id": "AudioGetItem"}')
            try:
                try:          
                    mid = parsed_json['result']['item']['id']
                except KeyError:
                    mid = 0
                
                track = parsed_json['result']['item']['track']
                
                title = parsed_json['result']['item']['title']
                if title=="":
                    title = parsed_json['result']['item']['label']
                
                thumbnail = ""
                if parsed_json['result']['item']['thumbnail']!="" and parsed_json['result']['item']['thumbnail'].find('.jpg') != -1:
                    thumbnail = self.ip_port + parsed_json['result']['item']['thumbnail'].replace("image://", "image/")[:-1]
                else:
                    thumbnail = self._ConfigDefault['basedirpath']+'img/kodi.png'
                    
                album = parsed_json['result']['item']['album']
                artist = ', '.join(parsed_json['result']['item']['artist'])

                return mid, str(track)+'. '+title, thumbnail, album, artist
            except KeyError:
                return -1, "", "", "", ""
            except IndexError:
                return -1, "", "", "", ""
        except ValueError:
            self.helper.printout("[warning]    ", self._ConfigDefault['mesg.red'])
            self.helper.printout('Decoding JSON has failed')
            return -1, "", "", "", ""
        
    def KODI_GetProperties(self, playerid):
        try:
            parsed_json = self.getJSON('{"jsonrpc": "2.0", "method": "Player.GetProperties", "params": { "playerid": '+str(playerid)+', "properties": ["speed","time","totaltime"] }, "id": 1}')
            try:
                speed = parsed_json['result']['speed']
                media_time = [int(parsed_json['result']['time']['hours']),int(parsed_json['result']['time']['minutes']),int(parsed_json['result']['time']['seconds'])]
                media_timetotal = [int(parsed_json['result']['totaltime']['hours']),int(parsed_json['result']['totaltime']['minutes']),int(parsed_json['result']['totaltime']['seconds'])]
                return speed, media_time, media_timetotal
            except KeyError as e:
                self.helper.printout("KeyError: " + str(e))
                return 0,[0,0,0],[0,0,0]
            except IndexError as e:
                self.helper.printout("IndexError: " + str(e))
                return 0,[0,0,0],[0,0,0]
        
        except ValueError:
            self.helper.printout("[warning]    ", self._ConfigDefault['mesg.red'])
            self.helper.printout('Decoding JSON has failed')
            return 0,[0,0,0],[0,0,0]
        
    def KODI_GetTotalCount(self, what = "video"):
        try:
            if what=="video":
                parsed_json = self.getJSON('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"limits": { "start" : 0, "end": 1 }}, "id": "libMovies"}')
            elif what=="songs":
                parsed_json = self.getJSON('{"jsonrpc": "2.0", "method": "AudioLibrary.GetSongs", "params": {"limits": { "start" : 0, "end": 1 }}, "id": "libSongs"}')
            elif what=="album":
                parsed_json = self.getJSON('{"jsonrpc": "2.0", "method": "AudioLibrary.GetAlbums", "params": {"limits": { "start" : 0, "end": 1 }}, "id": "libAlbums"}')
            try:
                return parsed_json['result']['limits']['total']
            except KeyError as e:
                self.helper.printout("KeyError: " + str(e))
                return 0
            except IndexError as e:
                self.helper.printout("IndexError: " + str(e))
                return 0
            except TypeError as e:
                #self.helper.printout("IndexError: " + str(e))
                return 0
        except ValueError:
            self.helper.printout("[warning]    ", self._ConfigDefault['mesg.red'])
            self.helper.printout('Decoding JSON has failed')
            return 0   
            
        