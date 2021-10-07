import os
import shutil
from tkinter import *
from tkinter import filedialog, ttk
import pygame


class App:
    list_all_song = []
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
        image_prev_song = PhotoImage(file=r'../mp3player/images/previous_song.png')
        button_prev_song = Button(add_del_frame, image=image_prev_song, command=self.add_song)
        button_prev_song.image = image_prev_song
        button_prev_song.grid(row=0, column=0, padx=5)

        add_del_frame.grid(row=0)

    # Frame for song list
    def frame_song_list(self):
        list_frame = Frame(self.root)
        self.listbox = Listbox(list_frame, bg=self.bg, selectmode=EXTENDED, width=60, height=10)
        self.listbox.bind('<Double-Button-1>', self.func_double_click)
        self.listbox.pack()
        list_frame.grid(row=1, pady=15)

    def frame_current_song(self):
        current_song_frame = Frame(self.root)
        self.label_cur_song = Label(current_song_frame, text='Choose song to play',
                                    bg='dark grey', fg='white', width=60, height=2)
        self.label_cur_song.pack()
        current_song_frame.grid(row=2, pady=5)

    # Frame for manipulate songs via buttons
    def frame_controller_button(self):
        button_frame = Frame(self.root)

        # button previous song
        image_prev_song = PhotoImage(file=r'../mp3player/images/previous_song.png')
        button_prev_song = Button(button_frame, image=image_prev_song, command=self.function_prev_song)
        button_prev_song.image = image_prev_song
        button_prev_song.grid(row=0, column=0, padx=5)

        # button current song
        self.image_pause_song = PhotoImage(file=r'../mp3player/images/pause-control-song.png')
        self.image_play_song = PhotoImage(file=r'../mp3player/images/play-control-song.png')
        self.button_current_song = Button(button_frame, text='play',
                                          image=self.image_play_song, command=self.play_stop_song)
        self.button_current_song.image = self.image_play_song
        self.button_current_song.grid(row=0, column=1, padx=5)

        if os.path.exists('mp3'):
            for song in os.listdir('mp3'):
                path_to_mp3_folder = os.path.abspath('mp3')
                self.list_all_song.append(fr'{path_to_mp3_folder}\{song}')
                self.listbox.insert(END, song.replace('.mp3', ''))
        elif not os.path.exists('mp3'):
            os.mkdir('mp3')

        # button next song
        image_next_song = PhotoImage(file=r'../mp3player/images/next_song.png')
        button_next_song = Button(button_frame, image=image_next_song, command=self.function_next_song)
        button_next_song.image = image_next_song
        button_next_song.grid(row=0, column=2, padx=5)

        self.volume_slider = ttk.Scale(button_frame, from_=0, to=1, orient=HORIZONTAL,
                                       value=0.5, command=self.change_volume, length=70)
        self.volume_slider.grid(row=0, column=3, padx=5)

        button_frame.grid(row=3)

########################################################################################################################
#                                     Create all functions needed for button
    # identify selected song
    def song_to_play(self):
        index = int(self.listbox.curselection()[0])
        self.cur_song = self.list_all_song[index]
        self.label_cur_song['text'] = os.path.basename(self.cur_song).replace('.mp3', '')
        self.func_play_song()

    # function for playing song
    def func_play_song(self):
        song = self.cur_song
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

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
                self.func_play_song()

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
        print(self.cur_song)
        self.func_play_song()

    def folder_song(self):
        if os.path.exists('mp3'):
            self.listbox.insert(END, os.listdir('mp3'))
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
                new_location = os.path.abspath(copy_file)
                self.list_all_song.append(new_location)

                print("File copied successfully.")
                name_song = os.path.basename(some_song)
                name_song = name_song.replace('.mp3', '')
                self.listbox.insert(END, name_song)
                print(f'some_song: {some_song}')
                print(self.list_all_song)

    def func_double_click(self, event):
        self.song_to_play()
        self.button_current_song['text'] = 'stop'
        self.button_current_song.config(image=self.image_pause_song)

    @staticmethod
    def change_volume(event):
        volume = float(event)
        pygame.mixer.music.set_volume(volume)


if __name__ == '__main__':
    app = App()
