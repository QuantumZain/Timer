# current = -4.036304473876953

def convert(time):
    pos = True if time >= 0 else False
    time = abs(time)
    time_hours = time/3600
    time_h = int(time_hours)
    time_remaining = time_hours - time_h
    time_m = int(time_remaining*60)
    time_sec = time_remaining - time_m/60
    time_s = int(time_sec*3600)
    
    time_format = f'{time_m}:{time_s}' if pos else f'-{time_m}:{time_s}'
    if abs(time_h) > 0:
        time_format = f'{time_h}:{time_m}:{time_s}' if pos else f'-{time_h}:{time_m}:{time_s}'
    
    return time_format

# time = convert(current)
# print(time)