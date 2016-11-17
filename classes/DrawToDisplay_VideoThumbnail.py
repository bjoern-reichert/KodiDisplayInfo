from datetime import timedelta

class DrawToDisplay_VideoThumbnail:
    
    # default for 320x240
    _drawSetting = {}   
    _drawSetting['videoinfo.progressbar.margin_left'] = 160
    _drawSetting['videoinfo.progressbar.width'] = 25
    
    _drawSetting['videoinfo.button.play'] = ""
    _drawSetting['videoinfo.button.break'] = ""
    
    _drawSetting['videoinfo.title.fontsize'] = 43
    _drawSetting['videoinfo.title.height_margin'] = 4
    
    _drawSetting['videoinfo.time_now.fontsize'] = 35
    _drawSetting['videoinfo.time_now.height_margin'] = 16
    _drawSetting['videoinfo.time_end.fontsize'] = 35
    _drawSetting['videoinfo.time_end.height_margin'] = 54
    
    _drawSetting['videoinfo.time.fontsize'] = 64
    _drawSetting['videoinfo.time.margin_top'] = 67
    _drawSetting['videoinfo.time.margin_bottom'] = 2
    
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
        self._drawSetting['videoinfo.progressbar.margin_left'] = 220
        self._drawSetting['videoinfo.progressbar.width'] = 34
        
        self._drawSetting['videoinfo.button.play'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/button_play_480x320.png')
        self._drawSetting['videoinfo.button.break'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/button_break_480x320.png')
    
        self._drawSetting['videoinfo.title.fontsize'] = 60
        self._drawSetting['videoinfo.title.height_margin'] = 5
    
        self._drawSetting['videoinfo.time_now.fontsize'] = 60
        self._drawSetting['videoinfo.time_now.height_margin'] = 9
        self._drawSetting['videoinfo.time_end.fontsize'] = 60
        self._drawSetting['videoinfo.time_end.height_margin'] = 76
        
        self._drawSetting['videoinfo.time.fontsize'] = 81
        self._drawSetting['videoinfo.time.margin_top'] = 83
        self._drawSetting['videoinfo.time.margin_bottom'] = 6
    
    def SetupDrawSetting480x320(self):        
        self._drawSetting['videoinfo.progressbar.margin_left'] = 220
        self._drawSetting['videoinfo.progressbar.width'] = 34
        
        self._drawSetting['videoinfo.button.play'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/button_play_480x320.png')
        self._drawSetting['videoinfo.button.break'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/button_break_480x320.png')
    
        self._drawSetting['videoinfo.title.fontsize'] = 60
        self._drawSetting['videoinfo.title.height_margin'] = 5
    
        self._drawSetting['videoinfo.time_now.fontsize'] = 60
        self._drawSetting['videoinfo.time_now.height_margin'] = 9
        self._drawSetting['videoinfo.time_end.fontsize'] = 60
        self._drawSetting['videoinfo.time_end.height_margin'] = 76
        
        self._drawSetting['videoinfo.time.fontsize'] = 81
        self._drawSetting['videoinfo.time.margin_top'] = 83
        self._drawSetting['videoinfo.time.margin_bottom'] = 6
        
    def drawProgressBar(self):
        rect_bar = self.pygame.Rect((self._drawSetting['videoinfo.progressbar.margin_left'],10), (self._drawSetting['videoinfo.progressbar.width'],self.screen.get_height()-20))
        
        if self.totaltime > 0:
            percent_done = int(( 1. * rect_bar.height / self.totaltime) * self.time)
        else:
            percent_done = 0
          
        rect_done = self.pygame.Rect(rect_bar)
        rect_done.height = percent_done
        self.pygame.draw.rect(self.screen, self._ConfigDefault['color.green'], rect_bar)
        self.pygame.draw.rect(self.screen, self._ConfigDefault['color.orange'], rect_done)
        self.pygame.draw.rect(self.screen, self._ConfigDefault['color.white'], rect_bar, 1)
        
    def setThumbnail(self, url):
        max_width = self._drawSetting['videoinfo.progressbar.margin_left']-20
        max_heigth = self.screen.get_height()-20

        self.thumbnail = self.image.scaleImage(url, max_width, max_heigth)
                
    def drawProperties(self, video_title, time_now, speed, media_time, media_totaltime):        
        self.time = self.helper.format_to_seconds(media_time[0], media_time[1], media_time[2])
        self.totaltime = self.helper.format_to_seconds(media_totaltime[0], media_totaltime[1], media_totaltime[2])

        self.draw_default.displaytext(str(time_now.strftime("%H:%M")), self._drawSetting['videoinfo.time_now.fontsize'], self.screen.get_width()-10, (self.screen.get_height()/2)-self._drawSetting['videoinfo.time_now.height_margin'], 'right', (self._ConfigDefault['color.white']))
        
        addtonow = time_now + timedelta(seconds=(self.totaltime-self.time))
        self.draw_default.displaytext(str(addtonow.strftime("%H:%M")), self._drawSetting['videoinfo.time_end.fontsize'], self.screen.get_width()-10, (self.screen.get_height()/2)+self._drawSetting['videoinfo.time_end.height_margin'], 'right', (self._ConfigDefault['color.white']))
    
        margin_left = 10
        if self._ConfigDefault['display.resolution']=="320x240":
            margin_left = 8
        margin_progessbar = self._drawSetting['videoinfo.progressbar.margin_left']+self._drawSetting['videoinfo.progressbar.width']

        if self._ConfigDefault['config.formattime_video']=="minutes":
            self.draw_default.displaytext(str(self.helper.format_to_minutes(media_time[0], media_time[1])), self._drawSetting['videoinfo.time.fontsize'], margin_progessbar+margin_left, self._drawSetting['videoinfo.time.margin_top'], 'left', (self._ConfigDefault['color.white']))
            self.draw_default.displaytext(str(self.helper.format_to_minutes(media_totaltime[0], media_totaltime[1])), self._drawSetting['videoinfo.time.fontsize'], margin_progessbar+margin_left, self.screen.get_height()+self._drawSetting['videoinfo.time.margin_bottom'], 'left', (self._ConfigDefault['color.white']))  
        elif self._ConfigDefault['config.formattime_video']=="short" or self._ConfigDefault['config.formattime_video']=="long":
            self._drawSetting['videoinfo.time.fontsize'] = 59
            self._drawSetting['videoinfo.time.margin_top'] = 64
            self._drawSetting['videoinfo.time.margin_bottom'] = 0
            if self._ConfigDefault['display.resolution']=="320x240":
                self._drawSetting['videoinfo.time.fontsize'] = 34
                self._drawSetting['videoinfo.time.margin_top'] = 41
                self._drawSetting['videoinfo.time.margin_bottom'] = -3

            self.draw_default.displaytext(self.helper.format_to_string(media_time[0], media_time[1], media_time[2], self._ConfigDefault['config.formattime_video']), self._drawSetting['videoinfo.time.fontsize'], margin_progessbar+margin_left, self._drawSetting['videoinfo.time.margin_top'], 'left', (self._ConfigDefault['color.white']))
            self.draw_default.displaytext(self.helper.format_to_string(media_totaltime[0], media_totaltime[1], media_totaltime[2], self._ConfigDefault['config.formattime_video']), self._drawSetting['videoinfo.time.fontsize'], margin_progessbar+margin_left, self.screen.get_height()+self._drawSetting['videoinfo.time.margin_bottom'], 'left', (self._ConfigDefault['color.white']))
               
        self.drawProgressBar()
                      
        if speed == 1:
            self.screen.blit(self._drawSetting['videoinfo.button.play'], (margin_progessbar+10, (self.screen.get_height()/2)-(self._drawSetting['videoinfo.button.play'].get_rect().size[1]/2) ))
        else:
            self.screen.blit(self._drawSetting['videoinfo.button.break'], (margin_progessbar+10, (self.screen.get_height()/2)-(self._drawSetting['videoinfo.button.play'].get_rect().size[1]/2) ))
            
        if self.thumbnail!="": 
            self.screen.blit(self.thumbnail,(10,10))
        