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

def nupuvajutus(i): # vaatab kas nuppu on vajutatud
    if i == 0 and GPIO.input(nupp) == GPIO.LOW: #kui nupu pole varem vajutatud ja nupu vajutati
        GPIO.output(sinine, GPIO.HIGH)          # sinine tuli läheb kinni
        time.sleep(0.01)
        GPIO.output(sinine, GPIO.LOW)
        return 1                                #nuppu on vajutatud
    return 0


def põlemine(led, aeg, tuli): # lülitab mingi ledi sisse mingiks aja järguks ja vaatab kas lülitit on vajutatud
    GPIO.output(led, GPIO.HIGH) 
    for b in range(int(aeg * 100)): #vaatab korduvalt kas lülitit on vajutatud
        if tuli == 0:
            tuli = nupuvajutus(tuli)
        time.sleep(0.01)
    GPIO.output(led, GPIO.LOW)
    return tuli
    



GPIO.setup(nupp, GPIO.IN, pull_up_down=GPIO.PUD_UP) #kui nuppu setup
GPIO.setup(sinine, GPIO.OUT)
GPIO.setup(jalapunane, GPIO.OUT)
GPIO.setup(jalaroheline, GPIO.OUT)
GPIO.setup(autopunane, GPIO.OUT)
GPIO.setup(autokollane, GPIO.OUT)
GPIO.setup(autoroheline, GPIO.OUT)

#jalakäiate punase tule siiselülitamine
GPIO.output(jalapunane, GPIO.HIGH)

GPIO.output(autoroheline, GPIO.LOW) #kui seda poleks algaks programm auto foor rohelise tulega mingipärast

lüliti_sees = 0 

try:
    while True:
        if lüliti_sees == 1: #kui lülitit on vajutatud hakkab järgmine tsükkel jalakäia foor rohelise tulega
            lüliti_sees = 0
            GPIO.output(jalapunane, GPIO.LOW)
            GPIO.output(jalaroheline, GPIO.HIGH)
            lüliti_sees = põlemine(autopunane, 5, lüliti_sees)
            GPIO.output(jalaroheline, GPIO.LOW)
            GPIO.output(jalapunane, GPIO.HIGH)
            lüliti_sees = põlemine(autokollane, 1, lüliti_sees)
            lüliti_sees = põlemine(autoroheline, 5, lüliti_sees)
            for i in range(3):
                lüliti_sees = põlemine(autokollane, 0.33, lüliti_sees)
                for i in range(33):
                    if lüliti_sees == 0:
                        lüliti_sees = nupuvajutus(lüliti_sees)
                    time.sleep(0.01)




        else:
            #autode foori tsükkel
            lüliti_sees = põlemine(autopunane, 5, lüliti_sees)
            lüliti_sees = põlemine(autokollane, 1, lüliti_sees)
            lüliti_sees = põlemine(autoroheline, 5, lüliti_sees)
            for i in range(3):
                lüliti_sees = põlemine(autokollane, 0.33, lüliti_sees)
                for i in range(33):
                    if lüliti_sees == 0:
                        lüliti_sees = nupuvajutus(lüliti_sees)
                    time.sleep(0.01)
                
            

except KeyboardInterrupt: 
    print("Keyboard interrupt")
    GPIO.cleanup()