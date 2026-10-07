#!/usr/bin/env python3

# Import the necessary libraries
import time
import math
from ev3dev2.motor import *
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sensor.virtual import *

# Create the sensors and motors objects
motorA = LargeMotor(OUTPUT_A)
motorB = LargeMotor(OUTPUT_B)
left_motor = motorA
right_motor = motorB
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
steering_drive = MoveSteering(OUTPUT_A, OUTPUT_B)

spkr = Sound()
btn = Button()
radio = Radio()
obtr = ObjectTracker()

color_sensor_in1 = ColorSensor(INPUT_1)
ultrasonic_sensor_in2 = UltrasonicSensor(INPUT_2)
gyro_sensor_in3 = GyroSensor(INPUT_3)
gps_sensor_in4 = GPSSensor(INPUT_4)
pen_in5 = Pen(INPUT_5)

motorC = LargeMotor(OUTPUT_C) # Magnet

from ev3dev2.Training_Wheels import Training_Wheels
training_wheels = Training_Wheels(gps_sensor_in4, gyro_sensor_in3, steering_drive)

# Here is where your code starts

stan = "poshuk"

chas_obyizdu = 3
chas_povernennya = 3

print("=== ПОЧАТОК МІСІЇ ===")
print("Поточний стан: ПОШУК")


while True:

    if stan == "poshuk":
        print("\n[ПОШУК]")
        print("Робот їде вперед")

        tank_drive.on(20, 20)

        od = ultrasonic_sensor_in2.distance_centimeters
        print("Ультразвуковий датчик:", round(od, 1), "см")

        if od < 15:
            print("Перешкода знайдена!")
            print("Перехід: ПОШУК -> ОБ'ЇЗД")

            tank_drive.off(brake=True)
            spkr.beep()

            stan = "ob_yizd"

        time.sleep(0.2)


    elif stan == "ob_yizd":
        print("\n[ОБ'ЇЗД]")
        print("Поворот праворуч")

        training_wheels.turn_right()
        time.sleep(0.7)

        print("Їдемо вперед повз перешкоду")
        tank_drive.on(20, 20)

        # Показуємо дані сенсора під час об'їзду
        start = time.time()

        while time.time() - start < chas_obyizdu:
            od = ultrasonic_sensor_in2.distance_centimeters
            print("ОБ'ЇЗД | відстань:", round(od, 1), "см")
            time.sleep(0.5)

        tank_drive.off(brake=True)

        print("Перешкоду об'їхано")
        print("Перехід: ОБ'ЇЗД -> ПОВЕРНЕННЯ")

        stan = "povernennya"


    elif stan == "povernennya":
        print("\n[ПОВЕРНЕННЯ]")
        print("Розворот")

        training_wheels.turn_left()
        time.sleep(1.2)

        print("Робот їде назад")
        tank_drive.on(-20, -20)

        start = time.time()

        while time.time() - start < chas_povernennya:
            od = ultrasonic_sensor_in2.distance_centimeters
            gyro = gyro_sensor_in3.angle

            print(
                "ПОВЕРНЕННЯ | "
                "відстань:", round(od, 1), "см | "
                "гіроскоп:", gyro, "°"
            )

            time.sleep(0.5)

        tank_drive.off(brake=True)

        print("Повернення завершено")
        print("Перехід: ПОВЕРНЕННЯ -> ЗАВЕРШЕННЯ")

        stan = "zavershennya"


    elif stan == "zavershennya":
        print("\n[ЗАВЕРШЕННЯ]")
        print("Робот зупинився")

        tank_drive.off(brake=True)
        spkr.beep()

        break


print("\n=== МІСІЯ ЗАВЕРШЕНА ===")