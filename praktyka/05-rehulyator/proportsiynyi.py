from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.virtual import GPSSensor
import time

tank = MoveTank(OUTPUT_A, OUTPUT_B)
color = ColorSensor(INPUT_1)          # ⚠️ у Gears порт обов'язковий
gps = GPSSensor(INPUT_4)              # лише щоб зупинити секундомір на фініші
time.sleep(0.5)

PORIH = 50                            # з роботи 4: біле 100, чорне 1

BAZA = 30
Kp   = 1

def obmezhyty(v):
    """SpeedPercent поза ±100 у Gears падає з ValueError."""
    return max(-100, min(100, v))


pochatok = time.time()
while time.time() - pochatok < 120 and gps.y < 85:
    v = color.reflected_light_intensity
    # ↓↓↓ сюди — код кроку 2, 3 або 4 ↓↓↓
    e = color.reflected_light_intensity - PORIH
    korekciya = Kp * e
    tank.on(SpeedPercent(BAZA + korekciya),
            SpeedPercent(BAZA - korekciya))

tank.off()
print("час до кінця траси: %.1f с" % (time.time() - pochatok))