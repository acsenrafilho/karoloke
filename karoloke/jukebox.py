import cv2

import karoloke.monitors as monitors
import karoloke.player as player
from karoloke.general_config import MUSIC_DB, SCORE_DB
from karoloke.menu import music_selection


# def start_the_party():
monitor = monitors.select_best_monitor()

while True:
    music_code = music_selection(monitor)
    if music_code:
        video_path = player.choose_music(music_code, MUSIC_DB)
        if video_path:
            vlc_player = player.vlc_media_player(video_path)
            end_status = player.start_video(vlc_player, monitor)
        if end_status == 1:
            score_video = player.random_score_video(SCORE_DB)
            player.start_video(
                player.vlc_media_player(score_video), monitor
            )

    if cv2.waitKey(0) & 0xFF == ord('q') or music_code is None:
        break
