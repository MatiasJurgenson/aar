import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

nupp = 16
sinine = 18
jalapunane = 22
jalaroheline = 36
autopunane = 11
autokollane = 13
autoroheline = 15

def põlemine(led, aeg): # lülitab mingi ledi sisse mingiks aja järguks
    GPIO.output(led, GPIO.HIGH)
    time.sleep(aeg)
    GPIO.output(led, GPIO.LOW)

def tsüklilõpp(): #korduv tsükli osa autofooril
    põlemine(autokollane, 1)
    põlemine(autoroheline, 5)
    for i in range(3):
        põlemine(autokollane, 0.33)
        time.sleep(0.33)

jalakäia = 0 # olenevalt selle väärtusest vaadab programm kas nuppu on autofoori tsükli ajal vajutatud (0 puhul pole nuppu vajutatud)

def jalakäiatsükkel(channel): # funktsioon mis annab teada kas nuppu on vajutatud
    GPIO.output(sinine, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(sinine, GPIO.LOW)
    global jalakäia 
    jalakäia = 1 

GPIO.setup(nupp, GPIO.IN, pull_up_down=GPIO.PUD_UP) #nuppu setup
GPIO.setup(sinine, GPIO.OUT)
GPIO.setup(jalapunane, GPIO.OUT)
GPIO.setup(jalaroheline, GPIO.OUT)
GPIO.setup(autopunane, GPIO.OUT)
GPIO.setup(autokollane, GPIO.OUT)
GPIO.setup(autoroheline, GPIO.OUT)

GPIO.add_event_detect(nupp, GPIO.RISING, callback=jalakäiatsükkel) #kui nuppu vajutadakse siis käivitadakse funktsioon jalakäiatsükkel

#jalakäiate punase tule siiselülitamine
GPIO.output(jalapunane, GPIO.HIGH)


try:
    while True:
        if jalakäia == 1:
            GPIO.output(jalapunane, GPIO.LOW)
            GPIO.output(jalaroheline, GPIO.HIGH)
            põlemine(autopunane, 5)
            GPIO.output(jalaroheline, GPIO.LOW)
            GPIO.output(jalapunane, GPIO.HIGH)
            tsüklilõpp()
            jalakäia = 0
        else:
            põlemine(autopunane, 5)
            tsüklilõpp()
            
        

except KeyboardInterrupt:
    print("Keyboard interrupt")
    GPIO.cleanup()

