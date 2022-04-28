
import vlc
import time



# rtsp://rtsp.stream/pattern demo link

player=vlc.MediaPlayer('rtsp://rtsp.stream/pattern')
player.play()

while 1:
    time.sleep(1)
    player.video_take_snapshot(0, '.snapshot.tmp.png', 0, 0)