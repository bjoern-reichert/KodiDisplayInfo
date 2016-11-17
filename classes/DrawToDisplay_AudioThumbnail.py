from datetime import timedelta

class DrawToDisplay_AudioThumbnail:
    
    # default for 320x240
    _drawSetting = {}
    _drawSetting['videoinfo.image_width_height'] = 0
    
    _drawSetting['videoinfo.margin_top_media_album'] = 33
    _drawSetting['videoinfo.margin_top_media_artist'] = 60
    _drawSetting['videoinfo.margin_top_media_artist.maxcount'] = 2
    _drawSetting['videoinfo.margin_top_media_title'] = 55
    _drawSetting['videoinfo.margin_top_media_title.maxcount'] = 2
     
    _drawSetting['videoinfo.progressbar.margin_top'] = 150
    _drawSetting['videoinfo.progressbar.height'] = 25
    
    _drawSetting['videoinfo.button.play'] = ""
    _drawSetting['videoinfo.button.break'] = ""
    
    _drawSetting['videoinfo.title.fontsize'] = 43
    _drawSetting['videoinfo.title.height_margin'] = 4
    
    _drawSetting['videoinfo.time_now.fontsize'] = 60
    _drawSetting['videoinfo.time_now.height_margin'] = 68
    _drawSetting['videoinfo.time_end.fontsize'] = 60
    _drawSetting['videoinfo.time_end.height_margin'] = 68
    
    _drawSetting['videoinfo.time.fontsize'] = 64
    _drawSetting['videoinfo.time.margin_left'] = 0
    _drawSetting['videoinfo.time.margin_top'] = 67
    
    # in seconds
    time = 0
    totaltime = 0
    
    thumbnail = ""
    
    def __init__(self, helper, image, _ConfigDefault):
        self.helper = helper
        self.image = image
        self._ConfigDefault = _ConfigDefault
        
    def setPygameScreen(self, pygame, screen, draw_default):
        self.pygame = pygame
        self.screen = screen
        self.draw_default = draw_default
        
        getattr(self, 'SetupDrawSetting'+self._ConfigDefault['display.resolution'])()
    
    def SetupDrawSetting320x240(self):       
        self._drawSetting['videoinfo.button.play'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/button_play_320x240.png')
        self._drawSetting['videoinfo.button.break'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/button_break_320x240.png')
    
    def SetupDrawSetting480x272(self):       
        self._drawSetting['videoinfo.image_width_height'] = 160
        
        self._drawSetting['videoinfo.margin_top_media_album'] = 33
        self._drawSetting['videoinfo.margin_top_media_artist'] = 65
        self._drawSetting['videoinfo.margin_top_media_artist.maxcount'] = 2
        self._drawSetting['videoinfo.margin_top_media_title'] = 65
        self._drawSetting['videoinfo.margin_top_media_title.maxcount'] = 2
        
        self._drawSetting['videoinfo.progressbar.margin_top'] = 162
        self._drawSetting['videoinfo.progressbar.height'] = 34
        
        self._drawSetting['videoinfo.button.play'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/button_play_480x320.png')
        self._drawSetting['videoinfo.button.break'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/button_break_480x320.png')
    
        self._drawSetting['videoinfo.title.fontsize'] = 60
        self._drawSetting['videoinfo.title.height_margin'] = 5
    
        self._drawSetting['videoinfo.time_now.fontsize'] = 80
        self._drawSetting['videoinfo.time_now.height_margin'] = 86
        self._drawSetting['videoinfo.time_end.fontsize'] = 80
        self._drawSetting['videoinfo.time_end.height_margin'] = 86
        
        self._drawSetting['videoinfo.time.fontsize'] = 81
        self._drawSetting['videoinfo.time.margin_left'] = 14
        self._drawSetting['videoinfo.time.margin_top'] = 83
    
    def SetupDrawSetting480x320(self):       
        self._drawSetting['videoinfo.image_width_height'] = 200
        
        self._drawSetting['videoinfo.margin_top_media_album'] = 33
        self._drawSetting['videoinfo.margin_top_media_artist'] = 69
        self._drawSetting['videoinfo.margin_top_media_artist.maxcount'] = 2
        self._drawSetting['videoinfo.margin_top_media_title'] = 69
        self._drawSetting['videoinfo.margin_top_media_title.maxcount'] = 3
        
        self._drawSetting['videoinfo.progressbar.margin_top'] = 205
        self._drawSetting['videoinfo.progressbar.height'] = 34
        
        self._drawSetting['videoinfo.button.play'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/button_play_480x320.png')
        self._drawSetting['videoinfo.button.break'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/button_break_480x320.png')
    
        self._drawSetting['videoinfo.title.fontsize'] = 60
        self._drawSetting['videoinfo.title.height_margin'] = 5
    
        self._drawSetting['videoinfo.time_now.fontsize'] = 80
        self._drawSetting['videoinfo.time_now.height_margin'] = 86
        self._drawSetting['videoinfo.time_end.fontsize'] = 80
        self._drawSetting['videoinfo.time_end.height_margin'] = 86
        
        self._drawSetting['videoinfo.time.fontsize'] = 81
        self._drawSetting['videoinfo.time.margin_left'] = 14
        self._drawSetting['videoinfo.time.margin_top'] = 83
        
    def setThumbnail(self, url):
        max_width = self._drawSetting['videoinfo.image_width_height']-20
        max_heigth = self._drawSetting['videoinfo.image_width_height']-20

        if self._ConfigDefault['display.resolution']!="320x240":
            self.thumbnail = self.image.scaleImage(url, max_width, max_heigth)
        
    def drawProgressBar(self, margin_top = 0):
        rect_bar = self.pygame.Rect((10,self._drawSetting['videoinfo.progressbar.margin_top']+margin_top), (self.screen.get_width()-20,self._drawSetting['videoinfo.progressbar.height']))
        
        if self.totaltime > 0:
            percent_done = int(( 1. * rect_bar.width / self.totaltime) * self.time)
        else:
            percent_done = 0
          
        rect_done = self.pygame.Rect(rect_bar)
        rect_done.width = percent_done
        self.pygame.draw.rect(self.screen, self._ConfigDefault['color.green'], rect_bar)
        self.pygame.draw.rect(self.screen, self._ConfigDefault['color.orange'], rect_done)
        self.pygame.draw.rect(self.screen, self._ConfigDefault['color.white'], rect_bar, 1)
        
    def drawProperties(self, media_title, time_now, speed, media_time, media_totaltime, media_album, media_artist):        
        self.time = self.helper.format_to_seconds(media_time[0], media_time[1], media_time[2])
        self.totaltime = self.helper.format_to_seconds(media_totaltime[0], media_totaltime[1], media_totaltime[2])

        width_text = (self.screen.get_width()-self._drawSetting['videoinfo.image_width_height'])-20
        margin_top_media_title = self._drawSetting['videoinfo.margin_top_media_title']
        image_width_height = self._drawSetting['videoinfo.image_width_height']
        if self._ConfigDefault['display.resolution']=="320x240":
            image_width_height = 10
            width_text = self.screen.get_width()-20
        
        self.draw_default.displaytext(media_album, 24, image_width_height+5, self._drawSetting['videoinfo.margin_top_media_album'], 'left', (self._ConfigDefault['color.white']))
        
        font=self.pygame.font.Font(self._ConfigDefault['basedirpath']+"fonts/MC360.ttf", 24)
        lines_artist = self.helper.wrapline(str(media_artist), font, width_text)
        
        lines_artist_index = 0
        for (i, line) in enumerate(lines_artist):
            if (i+1) > self._drawSetting['videoinfo.margin_top_media_artist.maxcount']:
                break
            self.draw_default.displaytext(line, 24, image_width_height+5, self._drawSetting['videoinfo.margin_top_media_artist']+(24*i), 'left', (self._ConfigDefault['color.grey']))
            lines_artist_index = lines_artist_index + 1
        
        font=self.pygame.font.Font(self._ConfigDefault['basedirpath']+"fonts/MC360.ttf", 28)
        lines = self.helper.wrapline(str(media_title), font, width_text)
        
        for (i, line) in enumerate(lines):
            if lines_artist_index>1:
                if (i+1) > self._drawSetting['videoinfo.margin_top_media_title.maxcount']:
                    break
            self.draw_default.displaytext(line, 28, image_width_height+5, margin_top_media_title+(24*lines_artist_index)+12+(28*i), 'left', (self._ConfigDefault['color.white']))

        margin_progessbar = self._drawSetting['videoinfo.progressbar.margin_top']+self._drawSetting['videoinfo.progressbar.height']
 
        if self._ConfigDefault['config.formattime_audio']=="short" or self._ConfigDefault['config.formattime_audio']=="long":
            fontsize = 64
            margintop = 9
            if self._ConfigDefault['config.formattime_audio']=="long":
                fontsize = 53
                margintop = 15
                
            if self._ConfigDefault['display.resolution']=="320x240" and self._ConfigDefault['config.formattime_audio']=="long":
                fontsize = 34
                margintop = 16
            elif self._ConfigDefault['display.resolution']=="320x240" and self._ConfigDefault['config.formattime_audio']=="short":
                fontsize = 46
                margintop = 9
            
            self.draw_default.displaytext(self.helper.format_to_string(media_time[0], media_time[1], media_time[2], self._ConfigDefault['config.formattime_audio']), fontsize, 62+self._drawSetting['videoinfo.time.margin_left'], margin_progessbar+self._drawSetting['videoinfo.time.margin_top']-margintop, 'left', (self._ConfigDefault['color.white']))
            self.draw_default.displaytext(self.helper.format_to_string(media_totaltime[0], media_totaltime[1], media_totaltime[2], self._ConfigDefault['config.formattime_audio']), fontsize, self.screen.get_width()-10, margin_progessbar+self._drawSetting['videoinfo.time.margin_top']-margintop, 'right', (self._ConfigDefault['color.white']))  
               
        self.drawProgressBar()
                
        if speed == 1:
            self.screen.blit(self._drawSetting['videoinfo.button.play'], (8, margin_progessbar+8))
        else:
            self.screen.blit(self._drawSetting['videoinfo.button.break'], (8, margin_progessbar+8))
            
        if self.thumbnail!="": 
            self.screen.blit(self.thumbnail,(10,10))