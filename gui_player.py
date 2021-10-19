import os
import shutil
from tkinter import *
from tkinter import filedialog, ttk
import time
import pygame
from mutagen.mp3 import MP3
import random


class App:
    list_all_song = []
    name_of_song = []
    index = 0

    def __init__(self):
        pygame.mixer.init()
        self.root = Tk()
        self.root.title('MP3 Player')
        self.root.iconbitmap('images/MP3.ico')
        self.root.resizable(width=False, height=False)
        self.bg = 'grey'
        self.font = 'Times new Roman 13 bold'
        self.conf = {'padx': (40, 10), 'pady': 10}
        self.cur_song = ''
        self.cur_time = 0
        self.song_volume = 0.5
        self.text = 'newest'
        self.id = None
        self.is_on = False
        self.same_song_on = False
        self.frame_add_del_music()
        self.frame_song_list()
        self.frame_current_song()
        self.frame_controller_button()
        self.root.mainloop()

########################################################################################################################
#                                                       Create frame
    # Frame add song, folder or delete song
    def frame_add_del_music(self):
        add_del_frame = Frame(self.root)
        image_browse_song = PhotoImage(file=r'../mp3player/images/browse.png')
        button_prev_song = Button(add_del_frame, image=image_browse_song, command=self.add_song)
        button_prev_song.image = image_browse_song
        button_prev_song.grid(row=0, column=0, padx=5)

        self.main_menu = Menu()
        self.root.config(menu=self.main_menu)
        self.sort_by_date = Menu(self.main_menu)
        self.sort_by_date.add_command(label='By date', command=self.sort_by_newest_song)
        self.main_menu.add_cascade(label='Sort song', menu=self.sort_by_date)

        image_repeat_song = PhotoImage(file=r'../mp3player/images/repeat_song.png')
        self.button_repeat_song = Button(add_del_frame, image=image_repeat_song, bg='white')
        self.button_repeat_song.image = image_repeat_song
        self.button_repeat_song.bind('<Button-1>', self.same_song)
        self.button_repeat_song.grid(row=0, column=2, padx=5)

        image_random_song = PhotoImage(file=r'../mp3player/images/random_song.png')
        self.button_random_song = Button(add_del_frame, image=image_random_song, bg='white')
        self.button_random_song.image = image_random_song
        self.button_random_song.bind('<Button-1>', self.switch_is_on)
        self.button_random_song.grid(row=0, column=3, padx=5)
        add_del_frame.grid(row=0)

    # Frame for song list
    def frame_song_list(self):
        list_frame = Frame(self.root)
        self.listbox = Listbox(list_frame, bg=self.bg, selectmode=EXTENDED, width=60, height=10)
        self.listbox.bind('<Double-Button-1>', self.func_double_click)
        self.listbox.pack()
        list_frame.grid(row=1, pady=15)

########################################################################################################################

    def frame_current_song(self):
        current_song_frame = Frame(self.root)
        self.label_cur_song = Label(current_song_frame, text='Choose song to play',
                                    bg='dark grey', fg='white', width=60, height=2)
        self.label_cur_song.grid(row=0, column=0)
        self.position_slider = ttk.Scale(current_song_frame, from_=0, to=100, orient=HORIZONTAL,
                                         value=0, length=300, command=self.song_info)
        self.position_slider.grid(row=1, column=0)
        current_song_frame.grid(row=2, pady=5)

    # Frame for manipulate songs via buttons
    def frame_controller_button(self):
        button_frame = Frame(self.root)

        self.time_song = Label(button_frame, text='00:00 / 00:00')
        self.time_song.grid(row=0, column=0, padx=5)

        # button previous song
        image_prev_song = PhotoImage(file=r'../mp3player/images/previous_song.png')
        button_prev_song = Button(button_frame, image=image_prev_song, command=self.function_prev_song)
        button_prev_song.image = image_prev_song
        button_prev_song.grid(row=0, column=1, padx=5)

        # button current song
        self.image_pause_song = PhotoImage(file=r'../mp3player/images/pause-control-song.png')
        self.image_play_song = PhotoImage(file=r'../mp3player/images/play-control-song.png')
        self.button_current_song = Button(button_frame, text='play',
                                          image=self.image_play_song, command=self.play_stop_song)
        self.button_current_song.image = self.image_play_song
        self.button_current_song.grid(row=0, column=2, padx=5)

        self.folder_song()

        # button next song
        image_next_song = PhotoImage(file=r'../mp3player/images/next_song.png')
        button_next_song = Button(button_frame, image=image_next_song, command=self.function_next_song)
        button_next_song.image = image_next_song
        button_next_song.grid(row=0, column=3, padx=5)

        self.image_unmute = PhotoImage(file=r'../mp3player/images/unmute_song.png')
        self.image_mute = PhotoImage(file=r'../mp3player/images/mute_song.png')
        self.mute_unmute = Button(button_frame, image=self.image_unmute, text='unmute', command=self.mute_volume)
        self.mute_unmute.image = self.image_unmute
        self.mute_unmute.grid(row=0, column=4, padx=5)

        self.volume_slider = ttk.Scale(button_frame, from_=0, to=1, orient=HORIZONTAL,
                                       command=self.change_volume, length=70, value=self.song_volume)
        self.volume_slider.grid(row=0, column=5, padx=5)

        button_frame.grid(row=3)

########################################################################################################################
#                                     Create all functions needed for button
    # identify selected song
    def song_to_play(self):
        print('def song_to_play():')
        index = int(self.listbox.curselection()[0])
        self.cur_song = self.list_all_song[index]
        self.label_cur_song['text'] = os.path.basename(self.cur_song).replace('.mp3', '')
        self.cur_time = 0
        self.position_slider.config(value=int(self.cur_time))
        self.func_play_song()

    # function for playing song
    def func_play_song(self):
        print('def func_play_song():')
        song = self.cur_song
        pygame.mixer.music.set_volume(self.song_volume)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(start=0)
        self.track_play()

    def track_play(self):
        print(f'self.is_on = {self.is_on} in track_play')
        print(f'self.same_song_on = {self.same_song_on} in track_play')
        if self.is_on:
            self.button_random_song.config(bg='light grey')
        else:
            self.button_random_song.config(bg='white')

        if self.same_song_on:
            self.button_repeat_song.config(bg='light grey')
        else:
            self.button_repeat_song.config(bg='white')

        song_mp3 = MP3(self.cur_song)
        self.len_song = song_mp3.info.length
        self.position_slider.config(to=int(self.len_song), value=int(self.cur_time))
        print('def track_play():')
        self.cur_time += 1
        if int(self.cur_time) == int(self.len_song):
            if self.same_song_on:
                self.label_cur_song['text'] = os.path.basename(self.cur_song).replace('.mp3', '')
                self.cur_time = 0
                self.position_slider.config(value=int(self.cur_time))
                self.func_play_song()
            elif not self.same_song_on:
                if self.is_on:
                    index = random.randint(0, len(self.list_all_song)-1)
                    self.cur_song = self.list_all_song[index]
                    self.label_cur_song['text'] = os.path.basename(self.cur_song).replace('.mp3', '')
                    self.cur_time = 0
                    self.position_slider.config(value=int(self.cur_time))
                    self.func_play_song()
                elif not self.is_on:
                    self.cur_time = 0
                    self.function_next_song()
        convert_len_song = time.strftime('%M:%S', time.gmtime(self.len_song))
        convert_cur_time = time.strftime('%M:%S', time.gmtime(self.cur_time))
        self.position_slider.config(to=int(self.len_song), value=int(self.cur_time))
        self.time_song.config(text=f'{convert_cur_time} / {convert_len_song}')
        if self.id is not None:
            self.root.after_cancel(self.id)
        self.id = self.root.after(1000, self.track_play)

    def song_info(self, x):
        print('def song_info')
        self.cur_time = int(self.position_slider.get())
        self.position_slider.config(value=int(self.cur_time))
        pygame.mixer.music.play(start=int(self.position_slider.get()))

    # switch between play and stop song
    def play_stop_song(self):
        if self.cur_song == '':
            if self.button_current_song['text'] == 'play':
                self.button_current_song['text'] = 'stop'
                self.button_current_song.config(image=self.image_pause_song)
                self.song_to_play()
        elif self.cur_song != '':
            index = self.list_all_song.index(self.cur_song)
            self.cur_song = self.list_all_song[index]
            if self.button_current_song['text'] == 'stop':
                self.button_current_song.config(image=self.image_play_song)
                self.button_current_song['text'] = 'play'
                pygame.mixer.music.pause()
            elif self.button_current_song['text'] == 'play':
                self.button_current_song['text'] = 'stop'
                self.button_current_song.config(image=self.image_pause_song)
                pygame.mixer.music.unpause()

    # Function for previous song
    def function_prev_song(self):
        self.button_current_song['text'] = 'stop'
        self.button_current_song.config(image=self.image_pause_song)
        index = self.list_all_song.index(self.cur_song) - 1
        self.cur_song = self.list_all_song[index]
        self.label_cur_song['text'] = os.path.basename(self.cur_song).replace('.mp3', '')
        print(self.cur_song)
        self.func_play_song()

    # Function for next song
    def function_next_song(self):
        self.button_current_song['text'] = 'stop'
        self.button_current_song.config(image=self.image_pause_song)
        index = self.list_all_song.index(self.cur_song) + 1
        if self.cur_song == self.list_all_song[-1]:
            index = 0
        self.cur_song = self.list_all_song[index]
        self.label_cur_song['text'] = os.path.basename(self.cur_song).replace('.mp3', '')
        self.func_play_song()

    def folder_song(self):
        if os.path.exists('mp3'):
            for song in os.listdir('mp3'):
                path_to_mp3_folder = os.path.abspath('mp3')
                self.list_all_song.append(fr'{path_to_mp3_folder}\{song}')
                self.listbox.insert(END, song.replace('.mp3', ''))
        elif not os.path.exists('mp3'):
            os.mkdir('mp3')

    # Add new song to folder and to frame, if folder does not exist - create new folder
    def add_song(self):
        # path_to_userprofile = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        song = filedialog.askopenfilenames(title='song', filetype=(('mp3 Files', '*.mp3'),))
        destination = 'mp3'

        for some_song in song:
            if os.path.basename(some_song) in os.listdir('mp3'):
                print('Same file error')
                raise shutil.SameFileError
            else:
                copy_file = shutil.copy(some_song, destination)
                self.new_location = os.path.abspath(copy_file)
                self.list_all_song.append(self.new_location)
                print("File copied successfully.")
                name_song = os.path.basename(some_song)
                name_song = name_song.replace('.mp3', '')
                # self.name_of_song.append(self.name_song)
                self.listbox.insert(END, name_song)

    def func_double_click(self, event):
        self.song_to_play()
        self.button_current_song['text'] = 'stop'
        self.button_current_song.config(image=self.image_pause_song)

    def sort_by_newest_song(self):
        if self.text == 'newest':
            self.time_sorted_list = sorted(self.list_all_song, key=os.path.getmtime)
            self.time_sorted_list.reverse()
            sorted_filename_list = [os.path.basename(i) for i in self.time_sorted_list]
            self.listbox.delete(0, END)
            for sorted_list in sorted_filename_list:
                sort = sorted_list.replace('.mp3', '')
                self.listbox.insert(END, sort)
            self.list_all_song = self.time_sorted_list
            self.text = 'oldest'
        elif self.text == 'oldest':
            self.time_sorted_list.reverse()
            self.listbox.delete(0, END)
            sorted_filename_list = [os.path.basename(i) for i in self.time_sorted_list]
            for sorted_list in sorted_filename_list:
                sort = sorted_list.replace('.mp3', '')
                self.listbox.insert(END, sort)
            self.list_all_song = self.time_sorted_list
            self.text = 'newest'

    def change_volume(self, event):
        self.volume = float(event)
        pygame.mixer.music.set_volume(self.volume)

    def mute_volume(self):
        if self.mute_unmute['text'] == 'mute':
            pygame.mixer.music.set_volume(50)
            self.volume_slider.set(0.5)
            self.mute_unmute.config(image=self.image_unmute)
            self.mute_unmute['text'] = 'unmute'
        elif self.mute_unmute['text'] == 'unmute':
            mute_volume = 0
            self.volume_slider.set(0.0)
            pygame.mixer.music.set_volume(mute_volume)
            self.mute_unmute.config(image=self.image_mute)
            self.mute_unmute['text'] = 'mute'

    def sort_by_name(self):
        pass

    def switch_is_on(self, x):
        if not self.is_on:
            self.is_on = True
        else:
            self.is_on = False

        print(f'self.is_on = {self.is_on} in switch_is_on')

    def same_song(self, x):
        if not self.same_song_on:
            self.same_song_on = True
        else:
            self.same_song_on = False

        print(f'self.same_song_on = {self.same_song_on} in same_song')


if __name__ == '__main__':
    app = App()
