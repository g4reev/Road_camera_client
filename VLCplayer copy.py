
import os
import vlc
import time
from dotenv import load_dotenv


load_dotenv()
# rtsp://rtsp.stream/pattern demo link
rstp_link_loc = os.getenv('rstp_link')

player=vlc.MediaPlayer(rstp_link_loc)
# player.play()

while 1:
    time.sleep(1)
    player.video_take_snapshot(0, './medie/snapshot2.tmp.png', 0, 0)