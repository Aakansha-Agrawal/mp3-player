from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title("MP3 Player")
root.iconbitmap(r'images/logo.ico')
root.geometry("500x400")

pygame.mixer.init()

#function for time
def play_time():
    #check to see if song is stopped
    if stopped:
        return

    #grab current song time
    current_time = pygame.mixer.music.get_pos()/1000
    #time format
    converted_time = time.strftime('%M.%S',time.gmtime(current_time))
    
    #REconstruct song with directory
    song = playlist_box.get(ACTIVE)
    song = f'C:/Users/aakan/Desktop/pp/mp3/audio/{song}.mp3'
    #find song total length
    song_mut = MP3(song)

    global song_length
    song_length = song_mut.info.length
    converted_song_length = time.strftime('%M.%S',time.gmtime(song_length))
    
    if int(song_slider.get()) == int(song_length):
        stop_song()
    elif paused:
        pass
    if paused:
        pass
    else:
        #move slider along 1 sec at a time
        next_time = int(song_slider.get()) + 1
        #output new time value 
        song_slider.config(to=song_length, value=next_time)

        #converting slider position as time format
        converted_time = time.strftime('%M.%S',time.gmtime(int(song_slider.get())))
        #output
        status_bar.config(text=f'Time Elapsed : {converted_time}  of  {converted_song_length} ')
    
    #timimg in status bar
    if current_time >= 1:
        status_bar.config(text=f'Time Elapsed : {converted_time}  of  {converted_song_length} ')
    status_bar.after(1000, play_time)

def add_song_menu():
    song = filedialog.askopenfilename(initialdir='audio/', title="Select Song", filetypes=(("MP3 Files","*.mp3"),))
    #strip out directory structure
    song = song.replace("C:/Users/aakan/Desktop/pp/mp3/audio/","")
    song = song.replace(".mp3","")

    playlist_box.insert(END, song)

def add_many():    
    songs = filedialog.askopenfilenames(initialdir='audio/', title="Select Song", filetypes=(("MP3 Files","*.mp3"),))
    #loop for list
    for song in songs:  
        #strip out directory structure
        song = song.replace("C:/Users/aakan/Desktop/pp/mp3/audio/","")
        song = song.replace(".mp3","")

        playlist_box.insert(END, song)
    
def remove_song():
    playlist_box.delete(ANCHOR)     #anchor deletes green selected one

def remove_songs():
    playlist_box.delete(0, END)

def play_song():
    global stopped
    stopped = False
    #REconstruct song with directory
    song = playlist_box.get(ACTIVE)
    song = f'C:/Users/aakan/Desktop/pp/mp3/audio/{song}.mp3'

    #load song with pygame mixer
    pygame.mixer.music.load(song)
    #play song
    pygame.mixer.music.play(loops=0)   #loops can be 0 or 5

    play_time()

    #my_label.config(text=song)

#create stop variable
global stopped
stopped = False

def stop_song():
    pygame.mixer.music.stop()
    playlist_box.selection_clear(ACTIVE)

    status_bar.config(text='')
    song_slider.config(value=0)

    global stopped
    stopped = True

#paused variable
global paused
paused = False

def pause_song(is_paused):
    global paused
    paused = is_paused
     
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True
    
def forward():
    #reset slider position and status bar
    status_bar.config(text='')
    song_slider.config(value=0)

    #get current aong number
    next = playlist_box.curselection()
    #print(next)
    next = next[0] + 1

    song = playlist_box.get(next)
    song = f'C:/Users/aakan/Desktop/pp/mp3/audio/{song}.mp3'
    #load song with pygame mixer
    pygame.mixer.music.load(song)
    #play song
    pygame.mixer.music.play(loops=5)   #loops can be 0 or 5
    #clear selection to active song
    playlist_box.selection_clear(0 ,END) 
    #move active bar
    playlist_box.activate(next)     
    #set active bar to next song
    playlist_box.selection_set(next, last=None)


def backward():
    #reset slider position and status bar
    status_bar.config(text='')
    song_slider.config(value=0)

    #get current aong number
    next = playlist_box.curselection()
    #print(next)
    next = next[0] - 1

    song = playlist_box.get(next)
    song = f'C:/Users/aakan/Desktop/pp/mp3/audio/{song}.mp3'
    #load song with pygame mixer
    pygame.mixer.music.load(song)
    #play song
    pygame.mixer.music.play(loops=5)   #loops can be 0 or 5
    #clear selection to active song
    playlist_box.selection_clear(0 ,END) 
    #move active bar
    playlist_box.activate(next)     
    #set active bar to next song
    playlist_box.selection_set(next, last=None)

def volume(a):
    pygame.mixer.music.set_volume(vol_slider.get())

def slider(x):
    song = playlist_box.get(ACTIVE)
    song = f'C:/Users/aakan/Desktop/pp/mp3/audio/{song}.mp3'
    #load song with pygame mixer
    pygame.mixer.music.load(song)
    #play song
    pygame.mixer.music.play(loops=0, start=song_slider.get()) 

#main frame
main_frame = Frame(root)
main_frame.pack(pady=20)

playlist_box = Listbox(main_frame, bg="black", fg="white",width=60, selectbackground="green",selectforeground="black")
playlist_box.grid(row=0, column=0)

#volume slider
vol_frame = LabelFrame(main_frame, text="Volume")
vol_frame.grid(row=0, column=1,padx=15)

vol_slider = ttk.Scale(vol_frame, from_=1, to=0, orient=VERTICAL, length=125,value=.5,command=volume)
vol_slider.pack(pady=10)

#create a sog slider
song_slider = ttk.Scale(main_frame, from_=0, to=100, orient=HORIZONTAL, length=360,value=0,command=slider)
song_slider.grid(row=2,column=0,pady=20)

#defining button images
back_btn_img = PhotoImage(file='images/back.png')
forw_btn_img = PhotoImage(file='images/forw.png')
play_btn_img = PhotoImage(file='images/play.png')
paus_btn_img = PhotoImage(file='images/pause.png')
stop_btn_img = PhotoImage(file='images/stop.png')

#button frame
control = Frame(main_frame)
control.grid(row=1, column=0,pady=25)

back_btn = Button(control, image=back_btn_img, borderwidth=0, command=backward)
forw_btn = Button(control, image=forw_btn_img, borderwidth=0, command=forward)
play_btn = Button(control, image=play_btn_img, borderwidth=0, command=play_song)
paus_btn = Button(control, image=paus_btn_img, borderwidth=0, command=lambda: pause_song(paused))
stop_btn = Button(control, image=stop_btn_img, borderwidth=0, command=stop_song)

back_btn.grid(row=0, column=0, padx=15)
forw_btn.grid(row=0, column=1, padx=15)
play_btn.grid(row=0, column=2, padx=15)
paus_btn.grid(row=0, column=3, padx=15)
stop_btn.grid(row=0, column=4, padx=15)

#menu
my_menu = Menu(root)
root.config(menu=my_menu)

add_song = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Add", menu=add_song)
add_song.add_command(label="Add Song", command=add_song_menu)
add_song.add_command(label="Add Songs", command=add_many)

#create delete song
del_song = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Remove",menu=del_song)
del_song.add_command(label="Remove Song", command=remove_song)
del_song.add_command(label="Remove Songs", command=remove_songs)

#create status bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

#label
my_label = Label(root, text='')
my_label.pack(pady=20)





root.mainloop()
