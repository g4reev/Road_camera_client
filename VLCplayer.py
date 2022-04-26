import vlc

player=vlc.MediaPlayer('Rtsp:\\Admin:Q1w2e3r4t%@10.133.1.124:554')
player.play()

while 1:
    time.sleep(1)
    player.video_take_snapshot(0, '.snapshot.tmp.png', 0, 0)