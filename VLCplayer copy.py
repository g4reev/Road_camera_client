
import os
import vlc
import time
from dotenv import load_dotenv


load_dotenv()
# rtsp://rtsp.stream/pattern demo link
rstp_link_loc = os.getenv('rstp_link')

player=vlc.MediaPlayer('rtsp://10.133.2.163:8554/stream')
player.play()

while 1:
    time.sleep(1)
    player.video_take_snapshot(0, '.snapshot.tmp.png', 0, 0)