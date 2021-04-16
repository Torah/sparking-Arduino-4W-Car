/*
基于mixly项目修改引用库和调整控制得到
*/
import sensor
from Maix import FPIOA,GPIO
import lcd
import image
import KPU as kpu
from machine import Timer
from machine import PWM


tim0 = Timer(Timer.TIMER0,Timer.CHANNEL0, mode=Timer.MODE_PWM)
pse4=PWM(tim0, freq=50, duty=2.5, pin=15)
tim1 = Timer(Timer.TIMER1,Timer.CHANNEL0, mode=Timer.MODE_PWM)
pse5=PWM(tim1, freq=50, duty=2.5, pin=17)
pse4.duty(90/18.0+2.5)
pse5.duty(90/18.0+2.5)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
sensor.skip_frames(10)
sensor.set_vflip(1)
sensor.set_hmirror(1)
lcd.init(freq=15000000,color=0x0000)
anchor= (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
KPU = kpu.load(0x300000)
kpu.init_yolo2(KPU,0.5,0.3,5,anchor)
X1 = 90
Y1 = 90
while True:
    img = sensor.snapshot()
    code = kpu.run_yolo2(KPU,img)
    if code:
        for i in code:
            img = img.draw_rectangle(i.rect(),(255,0,0),2,0)
            x = i.x() + i.w() // 2
            y = i.y() + i.h() // 2
            img = img.draw_cross([x,y],(255,0,0),30,1)
            if x < 155:
                X1 = X1 - 1
                if X1 < 20:
                    X1 = 20
            if x > 165:
                X1 = X1 + 1
                if X1 > 160:
                    X1 = 160
            print(Y1)
            pse4.duty(Y1/18.0+2.5)
            if y < 115:
                Y1 = Y1 - 1
                if Y1 < 20:
                    Y1 = 20
            if y > 125:
                Y1 = Y1 + 1
                if Y1 > 120:
                    Y1 = 120
            print(X1)
            pse5.duty(X1/18.0+2.5)
    lcd.display(img)
