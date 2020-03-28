import pygame
import os
import time
from converter import convert
import random

# the code here is shit; but atleast it works and that's all I care about
no_error = True
while True:
    time_input = input('specify time intervals: ')
    time_input = time_input.replace(' ', '')
    time_input = time_input.split(',')
    for inputs in time_input:
        if not inputs.isnumeric():
            print('Incorrect input only numbers are allowed')
            no_error = False
        break
    if no_error:
        break

time_input_lst = [int(time) for time in time_input]

time_intervals = time_input_lst #[1,31,3]  # time interval between each alarm in seconds
alrm_num = 0
repeat = len(time_intervals)  # number of alarms


# initialize pygame mixer and load audio file
pygame.mixer.init()
pygame.mixer.music.load('GOAT.wav')  # alarm's file name here


# Adjusts window in top right corner (copy pasted from stackexchange)
x, y = 950, 60  # play around with these values if u wish to change it
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)


# Game presets and initialization
fps = 30  # frames per sec
width, height = 410, 350  # width and height of the window
grey = (37, 35, 35) # colors in rgb
gred = (67, 45, 45)
red = (255, 15 , 15)
yellow = (234, 230, 30)
white = (245, 245, 245)
whitred = (255, 225, 235)

pygame.init()
screen = pygame.display.set_mode((width, height), )
clock = pygame.time.Clock()
pygame.display.set_caption('Pandora Alarm')
# font and text
font = pygame.font.Font('freesansbold.ttf', 100)


# the big boy game loop

# crappy timer variables
pause = False
pause_time = 0
color = white
bg = grey
time_list = [0]
pause_stamps = [0]
paused_times =[0]
total_pause = 0
reset_timer = False
confirm = False

start_time = time.time()+1  # crappy alarm variables
playing = False  # if alarm goes off
alarm = False # triggers alarm
end =  False
while True:
    screen.fill(bg)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if confirm:
                    reset_timer = True
                if playing:
                    pygame.mixer.music.fadeout(300)
                    alarm = False
                    confirm = True
                    total_pause = 0  # reset total_pause time
                    paused_times.clear()
                    # alrm_num += 1

                    # start_time = time.time()+1
                    # confirm = False
                    playing = not playing
                    # confirm = False # NOT SURE ABOUT THIS EITHER
                else:
                    pause = not pause if confirm is False else pause
                    if reset_timer and not pause:
                        start_time = time.time() + 1
                        alrm_num += 1
                        reset_timer = False
                        confirm = False #  NOT SURE ABOUT THIS
                    elif pause is True:
                        onpress = time.time()
                        pause_stamps.append(time_list[-1])
                        time_list.clear()
                        bg, color = gred, whitred
                    elif not(pause and confirm):
                        bg, color = grey, white
                        total_pause += paused_times[-1]
                        paused_times.clear()

    # if reset_timer:
    #     start_time = time.time()+1
    #     reset_timer = False

    now = time.time()
    if pause:
        pause_time = now - onpress
        paused_times.append(pause_time)

    if alrm_num == repeat:
        if not end:
            pygame.mixer.music.load('the_end.mp3')
            pygame.mixer.music.play(-1)
        end = True
        timer = 0
        bg = (230, 95, 147) #(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        color = (54, 170, 180) #(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        # alrm_num += 1

    current = now - start_time - total_pause

    if not end or confirm:
        timer = time_intervals[alrm_num] - current if not pause else pause_stamps[-1]
        time_list.append(timer)

    if confirm is True:
        timer = 0
        color = white

    if timer < 0 and not playing:
        alarm = True


    if alarm is True:
        playing = True
        pygame.mixer.music.play()
        alarm = False
        

    if not confirm:
        if timer < 30 and not end:
            color = yellow
        if timer < 0:
            color = red
        if timer > 30:
            color = white

    pos_x, pos_y = width//2, height//2
    if color == red:
        pos_x = (random.random()-0.5)*6 + pos_x
        pos_x = int(pos_x)
        # pos_y = (random.random()-0.5)*6 + pos_y
    
    text = font.render(convert(timer),True, color)
    textRect = text.get_rect()
    textRect.center = (pos_x, pos_y)
    screen.blit(text, textRect)


    pygame.display.update()
    clock.tick(fps)
