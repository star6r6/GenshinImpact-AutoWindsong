import pyautogui
import threading
import time

note_to_key_dict = {
    'H1': 'q',
    'H2': 'w',
    'H3': 'e',
    'H4': 'r',
    'H5': 't',
    'H6': 'y',
    'H7': 'u',
    '1': 'a',
    '2': 's',
    '3': 'd',
    '4': 'f',
    '5': 'g',
    '6': 'h',
    '7': 'j',
    'L1': 'z',
    'L2': 'x',
    'L3': 'c',
    'L4': 'v',
    'L5': 'b',
    'L6': 'n',
    'L7': 'm'
}


class AutoWindsong(object):
    def __init__(self, score, music_speed=120):
        self.score = score
        self.step_time = 60 / music_speed
        self.speed = 1

    def play(self, speed=1):
        self.speed = speed
        for i in range(5, 0, -1):
            print('启动倒计时：%s秒' % (i))
            time.sleep(1)
        for note_info_list in self.score:
            self._play_note_in_same_pos(note_info_list)

    def _play_note_in_same_pos(self, note_info_list):
        thread_list = []
        for track_id, note_info in enumerate(note_info_list):
            t = threading.Thread(target=self._play_note, args=(note_info, track_id,))
            t.start()
            thread_list.append(t)
        for t in thread_list:
            t.join()

    def _play_note(self, note_info, track_id):
        note = note_info[0]
        if len(note_info) >= 2:
            during_time = note_info[1] / 4 * self.step_time / self.speed
        else:
            during_time = 1 / 4 * self.step_time / self.speed
        if len(note_info) >= 3:
            need_hold = note_info[2]
        else:
            need_hold = 0
        key = note_to_key_dict.get(note)
        print('track_id:', track_id, note, key, during_time, need_hold)
        if need_hold:
            pyautogui.keyDown(key)
            time.sleep(during_time)
            pyautogui.keyUp(key)
        else:
            pyautogui.press(key)
            time.sleep(during_time)