import pyaudio
import numpy as np
import aubio
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller as MController
from collections import deque 
from scipy import stats as st
import win32gui

jump,w,a,s,d,leftc = 1,1,1,1,1,1
beforeModePitch = 0
before2Pitch = 0.0
arrPitch = deque([0,0,0,0,0,0,0,0,0,0])
modePitch = 0.0
shiftCondition = 0
freq = False
debugMode = True
firstString = True
thirdString = True
fifthString = True
mcMode = True
mouse = Controller()
keyboard = MController()
windowText = "Minecraft* 1.20.1 - Multiplayer (3rd-party Server)"

# initialise pyaudio
p = pyaudio.PyAudio()

# open stream
buffer_size = 1024
pyaudio_format = pyaudio.paFloat32
n_channels = 1
samplerate = 44100
stream = p.open(format=pyaudio_format,
                channels=n_channels,
                rate=samplerate,
                input=True,
                frames_per_buffer=buffer_size)
outputsink = None
record_duration = None

# setup pitch
tolerance = 0.2
win_s = 4096 # fft size
hop_s = buffer_size # hop size
pitch_o = aubio.pitch("default", win_s, hop_s, samplerate)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)

print("*** starting recording")
while True:
    try:
        audiobuffer = stream.read(buffer_size)
        signal = np.fromstring(audiobuffer, dtype=np.float32)

        pitch = pitch_o(signal)[0]
        confidence = pitch_o.get_confidence()
        roundPitch = round(pitch)
        arrPitch.popleft()
        arrPitch.append(roundPitch)
        if freq: 
            print("{} / {}".format(pitch,confidence))
            print(modePitch)
        beforePitch = st.mode(arrPitch)
        modePitch = beforePitch.mode

        if outputsink:
            outputsink(signal, len(signal))

        if mcMode and beforeModePitch == 0 and win32gui.GetWindowText(win32gui.GetForegroundWindow()) == windowText:
            if 39.8 < modePitch < 40.2:
                keyboard.tap(Key.esc)
                if debugMode and firstString: print("escape")
            if 40.8 < modePitch < 41.2:
                keyboard.tap('1')
                if debugMode and firstString: print("1")
            if 41.8 < modePitch < 42.2:
                keyboard.tap('2')
                if debugMode and firstString: print("2")
            if 42.8 < modePitch < 43.2:
                keyboard.tap('3')
                if debugMode and firstString: print("3")
            if 43.8 < modePitch < 44.2:
                keyboard.tap('4')
                if debugMode and firstString: print("4")
            if 44.8 < modePitch < 45.2:
                keyboard.tap('5')
                if debugMode and firstString: print("5")
            if 45.8 < modePitch < 46.2:
                keyboard.tap('6')
                if debugMode and firstString: print("6")
            if 46.8 < modePitch < 47.2:
                keyboard.tap('7')
                if debugMode and firstString: print("7")
            if 47.8 < modePitch < 48.2:
                keyboard.tap('8')
                if debugMode and firstString: print("8")
            if 48.8 < modePitch < 49.2:
                keyboard.tap('9')
                if debugMode and firstString: print("9")

            if 49.8 < modePitch < 50.2:
                keyboard.tap(Key.ctrl_l)     
                if debugMode and thirdString: print("control") 
            if 50.8 < modePitch < 51.2 and jump:
                keyboard.press(Key.space)
                if debugMode and thirdString: print("jump") 
                jump = 0
            if 51.8 < modePitch < 52.2 and not shiftCondition:
                keyboard.press(Key.shift)
                shiftCondition = 1
                if debugMode and thirdString: print("shift on") 
            elif 51.8 < modePitch < 52.2 and shiftCondition:
                keyboard.release(Key.shift)
                shiftCondition = 0
                if debugMode and thirdString: print("shift off") 
            if 52.8 < modePitch < 53.2:
                keyboard.tap('e')      
                if debugMode and thirdString: print("e") 
            if 53.8 < modePitch < 54.2:
                keyboard.tap('q')      
                if debugMode and thirdString: print("q") 
            if 54.8 < modePitch < 55.2 and leftc:
                mouse.press(Button.left)    
                if debugMode and thirdString: print("Left Click") 
                leftc = 0
            if 55.8 < modePitch < 56.2:
                mouse.click(Button.right)
                if debugMode and thirdString: print("Right Click") 
            if 56.8 < modePitch < 57.2:
                keyboard.tap(Key.f3)       
                if debugMode and thirdString: print("f3") 
            if 57.8 < modePitch < 58.2:
                keyboard.tap(Key.f5)        
                if debugMode and thirdString: print("f5") 
            if 58.8 < modePitch < 59.2:
                keyboard.press(Key.f3)  
                keyboard.tap('b')   
                keyboard.release(Key.f3) 
                if debugMode and fifthString: print("hitbox") 

            if 59.8 < modePitch < 60.2 and w:
                keyboard.press('w')  
                if debugMode and fifthString: print("w") 
                w = 0
            if 60.8 < modePitch < 61.2 and a:
                keyboard.press('a')  
                if debugMode and fifthString: print("a") 
                a = 0
            if 61.8 < modePitch < 62.2 and s:
                keyboard.press('s')  
                if debugMode and fifthString: print("s") 
                s = 0
            if 62.8 < modePitch < 63.2 and d:
                keyboard.press('d')
                if debugMode and fifthString: print("d") 
                d = 0
            if 63.8 < modePitch < 64.2:
                mouse.move(0, -50)             
                if debugMode and fifthString: print("up") 
            if 64.8 < modePitch < 65.2:
                mouse.move(-50, 0) 
                if debugMode and fifthString: print("left") 
            if 65.8 < modePitch < 66.2:
                mouse.move(0, 50) 
                if debugMode and fifthString: print("down")  
            if 66.8 < modePitch < 67.2:
                mouse.move(50, 0) 
                if debugMode and fifthString: print("right") 
            if 67.8 < modePitch < 68.2:
                keyboard.press('w')  
                keyboard.press(Key.space)   
                jump = 0
                w = 0
                if debugMode and fifthString: print("Jump Forward") 

        elif pitch == 0:
            if not jump:
                keyboard.release(Key.space)
                jump = 1
            if not w:
                keyboard.release('w')
                w = 1
            if not a:
                keyboard.release('a')
                a = 1
            if not s:
                keyboard.release('s')
                s = 1
            if not d:
                keyboard.release('d')
                d = 1
            if not leftc:
                mouse.release(Button.left)
                leftc = 1    
            
    except KeyboardInterrupt:
        print("*** Ctrl+C pressed, exiting")
        break

    beforePitch = st.mode(arrPitch)
    modePitch = beforePitch.mode
    before2Pitch = pitch
    beforeModePitch = modePitch

print("*** done recording")
stream.stop_stream()
stream.close()
p.terminate()