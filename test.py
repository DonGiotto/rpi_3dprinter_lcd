from time import sleep

string = "DisplayUnitFront.gcode"

for i in range(len(string)):
    print string[i:19] + " " + string[:i]
    sleep(1)
