from datetime import timedelta

class DrawToDisplay_VideoTime:

    # default for 320x240
    _drawSetting = {}   
    _drawSetting['videoinfo.progressbar.margin_top'] = 85
    _drawSetting['videoinfo.progressbar.height'] = 25
    
    _drawSetting['videoinfo.button.play'] = ""
    _drawSetting['videoinfo.button.break'] = ""
    
    _drawSetting['videoinfo.title.fontsize'] = 46
    _drawSetting['videoinfo.title.height_margin'] = 4
    
    _drawSetting['videoinfo.time_now.fontsize'] = 60
    _drawSetting['videoinfo.time_now.height_margin'] = 68
    _drawSetting['videoinfo.time_end.fontsize'] = 60
    _drawSetting['videoinfo.time_end.height_margin'] = 68
    
    _drawSetting['videoinfo.time.fontsize'] = 64
    _drawSetting['videoinfo.time.margin_left'] = 0
    _drawSetting['videoinfo.time.margin_top'] = 67
    
    def __init__(self, helper, _ConfigDefault):
        self.helper = helper
        self._ConfigDefault = _ConfigDefault
        
    def setPygameScreen(self, pygame, screen, draw_default):
        self.pygame = pygame
        self.screen = screen
        self.draw_default = draw_default
        
        getattr(self, 'SetupDrawSetting'+self._ConfigDefault['display.resolution'])()
    
    def SetupDrawSetting320x240(self):
        self._drawSetting['startscreen.logo'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/kodi_logo_320x240.png')
        
        self._drawSetting['videoinfo.button.play'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/button_play_320x240.png')
        self._drawSetting['videoinfo.button.break'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/button_break_320x240.png')
    
    def SetupDrawSetting480x272(self):
        self._drawSetting['startscreen.logo'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/kodi_logo_480x272.png')
        self._drawSetting['startscreen.clock.fontsize'] = 64
        self._drawSetting['startscreen.clock.height_margin'] = 102
        
        self._drawSetting['videoinfo.progressbar.margin_top'] = 92
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
        self._drawSetting['startscreen.logo'] = self.pygame.image.load(self._ConfigDefault['basedirpath']+'img/kodi_logo_480x320.png')
        self._drawSetting['startscreen.clock.fontsize'] = 75
        self._drawSetting['startscreen.clock.height_margin'] = 118
        
        self._drawSetting['videoinfo.progressbar.margin_top'] = 120
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
        
    def drawProgressBar(self, play_time, play_time_done):
        rect_bar = self.pygame.Rect((10,self._drawSetting['videoinfo.progressbar.margin_top']), (self.screen.get_width()-20,self._drawSetting['videoinfo.progressbar.height']))
        
        if play_time_done > 0:
            percent_done = int(( 1. * rect_bar.width / play_time ) * play_time_done)
        else:
            percent_done = 0
          
        rect_done = self.pygame.Rect(rect_bar)
        rect_done.width = percent_done
        self.pygame.draw.rect(self.screen, self._ConfigDefault['color.green'], rect_bar)
        self.pygame.draw.rect(self.screen, self._ConfigDefault['color.orange'], rect_done)
        self.pygame.draw.rect(self.screen, self._ConfigDefault['color.white'], rect_bar, 1)
        
    def drawProperties(self, video_title, time_now, speed, minutes_time, minutes_timetotal):
        self.draw_default.displaytext(str(time_now.strftime("%H:%M")), self._drawSetting['videoinfo.time_now.fontsize'], 10, self._drawSetting['videoinfo.time_now.height_margin'], 'left', (self._ConfigDefault['color.white']))
        addtonow = time_now + timedelta(minutes=(minutes_timetotal-minutes_time))
        self.draw_default.displaytext(str(addtonow.strftime("%H:%M")), self._drawSetting['videoinfo.time_end.fontsize'], self.screen.get_width()-10, self._drawSetting['videoinfo.time_end.height_margin'], 'right', (self._ConfigDefault['color.white']))
    
        margin_progessbar = self._drawSetting['videoinfo.progressbar.margin_top']+self._drawSetting['videoinfo.progressbar.height']
    
        self.draw_default.displaytext(str(minutes_time), self._drawSetting['videoinfo.time.fontsize'], 62+self._drawSetting['videoinfo.time.margin_left'], margin_progessbar+self._drawSetting['videoinfo.time.margin_top'], 'left', (self._ConfigDefault['color.white']))
        self.draw_default.displaytext(str(minutes_timetotal), self._drawSetting['videoinfo.time.fontsize'], self.screen.get_width()-10, margin_progessbar+self._drawSetting['videoinfo.time.margin_top'], 'right', (self._ConfigDefault['color.white']))  
                
        self.drawProgressBar(minutes_timetotal, minutes_time)
                
        if speed == 1:
            self.screen.blit(self._drawSetting['videoinfo.button.play'], (8, margin_progessbar+8))
        else:
            self.screen.blit(self._drawSetting['videoinfo.button.break'], (8, margin_progessbar+8)) #
            
        self.draw_default.displaytext(video_title, self._drawSetting['videoinfo.title.fontsize'], 10, self.screen.get_height()-self._drawSetting['videoinfo.title.height_margin'], 'left', (self._ConfigDefault['color.white']))