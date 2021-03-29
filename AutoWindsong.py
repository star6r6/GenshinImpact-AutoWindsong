# -*- coding: UTF-8 -*-
# author: star6r6

import pyautogui
import threading
import time

DEBUG = False

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
        self.pending_key_info_list = []
        self._playing_key_info_list = []
        self._playing_index = 0
        self._existed_track_thread_list = []
        self._finished_thread_count = 0
        # 关闭pyautogui的输入延时
        pyautogui.PAUSE = 0

    def play(self, speed=1):
        self.speed = speed
        print('演奏即将开始，请将点击原神并保持在原神界面！')
        for i in range(5, 0, -1):
            print('启动倒计时：%s秒...' % (i))
            time.sleep(1)
        self._init_pending_thread_list()
        self._play()

    def _play(self):
        for idx, key_info_list in enumerate(self.pending_key_info_list):
            self._playing_index = idx
            self._playing_key_info_list = key_info_list
            self._wait_for_all_threads_finish()
        print('演奏完毕！')
        exit(0)

    def _init_pending_thread_list(self):
        for note_info_node in self.score:
            key_info_list = []
            if isinstance(note_info_node, list):
                for track_id, note_info_string in enumerate(note_info_node):
                    key_info = self._get_pending_play_note_info(note_info_string)
                    key_info_list.append(key_info)
                    self._get_more_track_thread(track_id)
            else:
                note_info_string = note_info_node
                key_info = self._get_pending_play_note_info(note_info_string)
                key_info_list.append(key_info)
                self._get_more_track_thread(0)
            self.pending_key_info_list.append(key_info_list)

    def _get_more_track_thread(self, track_id):
        if len(self._existed_track_thread_list) == track_id:
            self._create_track_thread(track_id)

    def _wait_for_all_threads_finish(self):
        while self._finished_thread_count != len(self._playing_key_info_list):
            time.sleep(0.001)
        self._finished_thread_count = 0

    def _get_pending_play_note_info(self, note_info_string):
        note_info = note_info_string.split()
        note = note_info[0]
        if len(note_info) >= 2:
            during_time = int(note_info[1]) / 4 * self.step_time / self.speed
        else:
            during_time = 1 / 4 * self.step_time / self.speed
        return [note, during_time]

    def _create_track_thread(self, track_id):
        t = threading.Thread(target=self._play_note, args=(track_id,))
        t.setDaemon(True)
        t.start()
        self._existed_track_thread_list.append(t)

    def _play_note(self, track_id):
        last_played_index = -1
        last_play_time = None
        while True:
            time.sleep(0.001)
            if last_played_index != self._playing_index and track_id < len(self._playing_key_info_list):
                last_played_index = self._playing_index
                note = self._playing_key_info_list[track_id][0]
                key = note_to_key_dict.get(note)
                during_time = self._playing_key_info_list[track_id][1]
                if DEBUG:
                    print('track_id:', track_id, note, key, during_time)
                if DEBUG and last_play_time:
                    print('before press cost time:', time.time() - last_play_time)
                pyautogui.press(key)
                if DEBUG and last_play_time:
                    print('after press cost time:', time.time() - last_play_time)
                time.sleep(during_time)
                self._finished_thread_count += 1
                if DEBUG and last_play_time:
                    print('real cost time:', time.time() - last_play_time)
                last_play_time = time.time()
