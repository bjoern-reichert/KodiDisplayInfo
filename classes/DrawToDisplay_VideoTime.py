from datetime import timedelta

class DrawToDisplay_VideoTime:
    
    # default for 320x240
    _drawSetting = {}   
    _drawSetting['videoinfo.progressbar.margin_top'] = 85
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
    
    def __init__(self, helper, _ConfigDefault):
        self.helper = helper
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
        
    def wraplines(self, title, fontsize):
        width_text = self.screen.get_width()-20
        font=self.pygame.font.Font(self._ConfigDefault['basedirpath']+"fonts/MC360.ttf", fontsize)
        return self.helper.wrapline(title, font, width_text)
        
    def drawProperties(self, video_title, time_now, speed, media_time, media_totaltime):
        margin_top = 0
        videoinfo_title_fontsize = self._drawSetting['videoinfo.title.fontsize']
        
        self.time = self.helper.format_to_seconds(media_time[0], media_time[1], media_time[2])
        self.totaltime = self.helper.format_to_seconds(media_totaltime[0], media_totaltime[1], media_totaltime[2])

        lines = self.wraplines(video_title, self._drawSetting['videoinfo.title.fontsize'])
        if len(lines)>1:  
            if self._ConfigDefault['display.resolution']=="480x320":
                videoinfo_title_fontsize = 49
                margin_top = -22
                second_title_height_margin = -46
            if self._ConfigDefault['display.resolution']=="480x272":
                self._drawSetting['videoinfo.title.height_margin'] = 0
                videoinfo_title_fontsize = 42
                margin_top = -11
                second_title_height_margin = -40
            if self._ConfigDefault['display.resolution']=="320x240":
                videoinfo_title_fontsize = 38
                margin_top = -16
                second_title_height_margin = -36
                lines = self.wraplines(video_title, videoinfo_title_fontsize)
             
            lines = lines[0:2]
            lines.reverse()
            for (i, line) in enumerate(lines):
                if i > 1: # max 2
                    break
                self.draw_default.displaytext(line, videoinfo_title_fontsize, 10, self.screen.get_height()-self._drawSetting['videoinfo.title.height_margin']+(second_title_height_margin*i), 'left', self._ConfigDefault['color.white'])
        else:
            self.draw_default.displaytext(video_title, self._drawSetting['videoinfo.title.fontsize'], 10, self.screen.get_height()-self._drawSetting['videoinfo.title.height_margin'], 'left', self._ConfigDefault['color.white'])
        
        self.draw_default.displaytext(str(time_now.strftime("%H:%M")), self._drawSetting['videoinfo.time_now.fontsize'], 10, self._drawSetting['videoinfo.time_now.height_margin'], 'left', self._ConfigDefault['color.white'])

       
        addtonow = time_now + timedelta(seconds=(self.totaltime-self.time))
        self.draw_default.displaytext(str(addtonow.strftime("%H:%M")), self._drawSetting['videoinfo.time_end.fontsize'], self.screen.get_width()-10, self._drawSetting['videoinfo.time_end.height_margin'], 'right', self._ConfigDefault['color.white'])
    
        margin_progessbar = self._drawSetting['videoinfo.progressbar.margin_top']+self._drawSetting['videoinfo.progressbar.height']+margin_top

        if self._ConfigDefault['config.formattime_video']=="minutes":
            self.draw_default.displaytext(str(self.helper.format_to_minutes(media_time[0], media_time[1])), self._drawSetting['videoinfo.time.fontsize'], 62+self._drawSetting['videoinfo.time.margin_left'], margin_progessbar+self._drawSetting['videoinfo.time.margin_top'], 'left', self._ConfigDefault['color.white'])
            self.draw_default.displaytext(str(self.helper.format_to_minutes(media_totaltime[0], media_totaltime[1])), self._drawSetting['videoinfo.time.fontsize'], self.screen.get_width()-10, margin_progessbar+self._drawSetting['videoinfo.time.margin_top'], 'right', self._ConfigDefault['color.white'])  
        elif self._ConfigDefault['config.formattime_video']=="short" or self._ConfigDefault['config.formattime_video']=="long":
            fontsize = 64
            margintop = 9
            if self._ConfigDefault['config.formattime_video']=="long":
                fontsize = 53
                margintop = 15
                
            if self._ConfigDefault['display.resolution']=="320x240" and self._ConfigDefault['config.formattime_video']=="long":
                fontsize = 34
                margintop = 16
            elif self._ConfigDefault['display.resolution']=="320x240" and self._ConfigDefault['config.formattime_video']=="short":
                fontsize = 46
                margintop = 9
            
            self.draw_default.displaytext(self.helper.format_to_string(media_time[0], media_time[1], media_time[2], self._ConfigDefault['config.formattime_video']), fontsize, 62+self._drawSetting['videoinfo.time.margin_left'], margin_progessbar+self._drawSetting['videoinfo.time.margin_top']-margintop, 'left', self._ConfigDefault['color.white'])
            self.draw_default.displaytext(self.helper.format_to_string(media_totaltime[0], media_totaltime[1], media_totaltime[2], self._ConfigDefault['config.formattime_video']), fontsize, self.screen.get_width()-10, margin_progessbar+self._drawSetting['videoinfo.time.margin_top']-margintop, 'right', self._ConfigDefault['color.white'])  
               
        self.drawProgressBar(margin_top)
                
        if speed == 1:
            self.screen.blit(self._drawSetting['videoinfo.button.play'], (8, margin_progessbar+8))
        else:
            self.screen.blit(self._drawSetting['videoinfo.button.break'], (8, margin_progessbar+8))