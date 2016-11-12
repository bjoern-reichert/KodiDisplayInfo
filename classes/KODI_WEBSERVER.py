import urllib2
import json
from socket import timeout

class KODI_WEBSERVER:
    
    ip_port = ""
    
    def __init__(self, helper, _ConfigDefault, draw_default):
        self.helper = helper
        self._ConfigDefault = _ConfigDefault
        self.draw_default = draw_default
        
        self.ip_port = 'http://'
        if self._ConfigDefault['KODI.webserver.user']!="" and self._ConfigDefault['KODI.webserver.pass']!="":
            self.ip_port = self.ip_port+self._ConfigDefault['KODI.webserver.user']+':'+self._ConfigDefault['KODI.webserver.pass']+'@'
        self.ip_port = self.ip_port+self._ConfigDefault['KODI.webserver.host']+':'+self._ConfigDefault['KODI.webserver.port']+'/'
       
    def getJSON(self, jsondata, get_parameter = 'jsonrpc?request='):
        self.draw_default.setInfoText("", self._ConfigDefault['color.white'])
        try:
            headers = {'content-type': 'application/json'}
            json_data = json.dumps(json.loads(jsondata))
            post_data = json_data.encode('utf-8')
            request = urllib2.Request(self.ip_port + get_parameter, post_data, headers)
            
            result = urllib2.urlopen(request,timeout=3).read()
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
                return 0, ""
            except IndexError:
                return 0, ""
        except ValueError:
            self.helper.printout("[warning]    ", self._ConfigDefault['mesg.red'])
            print 'Decoding JSON has failed'
            return ""
        
    def KODI_GetItem(self, playerid, playertype):
        try:
            if playertype == "video":
                player_params_id = "VideoGetItem"
            elif playertype == "audio":
                player_params_id = "AudioGetItem"
            else:
                return 0, "", ""
            
            parsed_json = self.getJSON('{"jsonrpc": "2.0", "method": "Player.GetItem", "params": { "properties": ["title","thumbnail"], "playerid": '+str(playerid)+' }, "id": "'+str(player_params_id)+'"}')
            try:
                try:          
                    mid = parsed_json['result']['item']['id']
                except KeyError:
                    mid = 0
                
                title = parsed_json['result']['item']['title']
                if title=="":
                    title = parsed_json['result']['item']['label']
                
                thumbnail = ""
                if parsed_json['result']['item']['thumbnail']!="": # and parsed_json['result']['item']['thumbnail'].find('.jpg') != -1
                    thumbnail = self.ip_port + parsed_json['result']['item']['thumbnail'].replace("image://", "image/")[:-1];

                return mid, title, thumbnail
            except KeyError:
                return -1, "", ""
            except IndexError:
                return -1, "", ""
        except ValueError:
            self.helper.printout("[warning]    ", self._ConfigDefault['mesg.red'])
            print 'Decoding JSON has failed'
            return -1, "", "" 
        
    def KODI_GetProperties(self, playerid):
        try:
            parsed_json = self.getJSON('{"jsonrpc": "2.0", "method": "Player.GetProperties", "params": { "playerid": '+str(playerid)+', "properties": ["speed","time","totaltime"] }, "id": 1}')
            try:
                speed = parsed_json['result']['speed']
                media_time = [int(parsed_json['result']['time']['hours']),int(parsed_json['result']['time']['minutes']),int(parsed_json['result']['time']['seconds'])]
                media_timetotal = [int(parsed_json['result']['totaltime']['hours']),int(parsed_json['result']['totaltime']['minutes']),int(parsed_json['result']['totaltime']['seconds'])]
                return speed, media_time, media_timetotal
            except KeyError, e:
                print "KeyError: " + str(e)
                return 0,[0,0,0],[0,0,0]
            except IndexError, e:
                print "IndexError: " + str(e)
                return 0,[0,0,0],[0,0,0]
        
        except ValueError:
            self.helper.printout("[warning]    ", self._ConfigDefault['mesg.red'])
            print 'Decoding JSON has failed'
            return 0,[0,0,0],[0,0,0]