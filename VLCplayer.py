
import os
import vlc
import time
from dotenv import load_dotenv


load_dotenv()
# rtsp://rtsp.stream/pattern demo link
# http://10.133.0.187:6400
rstp_link_loc = os.getenv('rstp_link')

player=vlc.MediaPlayer('http://10.133.0.187:6400')
player.play()

while 1:
    time.sleep(1)
    player.video_take_snapshot(0, './medie/snapshot2.tmp.png', 0, 0)