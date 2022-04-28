
import vlc



# rtsp://rtsp.stream/pattern demo link


ffmpeg -i "rtsp://rtsp.stream/pattern" -frames 1 -f image2 snapshot.jpg

packet_size = 4096

process = (
    ffmpeg
    .input('rtsp://%s:8554/default')
    .output('-', format='h264')
    .run_async(pipe_stdout=True)
)

while process.poll() is None:
    packet = process.stdout.read(packet_size)
    try:
        tcp_socket.send(packet)
    except socket.error:
        process.stdout.close()
        process.wait()
        break

out, _ = (
    ffmpeg
    .input(in_filename)
    .filter('select', 'gte(n,{})'.format(frame_num))
    .output('pipe:', vframes=1, format='image2', vcodec='mjpeg')
    .run(capture_stdout=True)
)
# import vlc

# player=vlc.MediaPlayer('Rtsp://Admin:Q1w2e3r4t%@10.133.1.124:554')
# player.play()

# while 1:
#    time.sleep(1)
#    player.video_take_snapshot(0, '.snapshot.tmp.png', 0, 0)