from machine import Pin,PWM,I2C,ADC
from time import sleep
import ssd1306

i2c = I2C(scl=Pin(5), sda=Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

rled = Pin(0, Pin.OUT)
gled = Pin(16, Pin.OUT)
bled = Pin(15, Pin.OUT)

btn = Pin(2, Pin.IN, Pin.PULL_UP)
of : int
count = 0

sensor = ADC(0)

def initialize_motor_pins():
    pin1 = Pin(14,Pin.OUT) # IN1
    pin2 = Pin(12,Pin.OUT) # IN2
    enable = Pin(13,Pin.OUT) # ENA
    
    enable.value(1)   
    
    return pin1 , pin2

def move(speed,motorPins):
    
    motorPins[0].value(0) # IN1 = 1
    motorPins[1].value(1) # IN2 = 0

def stop(motorPins):
    
    motorPins[0].value(0) # IN1 = 0
    motorPins[1].value(0) # IN2 = 0

def button ():
    global of,count
    
    bvalue = not(btn.value())
    if bvalue == 1:
        count += 1
        sleep(.2)
        
    if count%2 == 0:
        of = 0
    else:
        of = 1
        
motorPins = initialize_motor_pins()

while 1:
    button()
    stop(motorPins)
    
    if of == 1:
        value = 1024-(sensor.read())
        
        rled.off()
        bled.off()
        gled.on()
    
        print(value)
        print(' ')
        print(count)
        
        if value < 400 :
            move(1024,motorPins)
            bled.on()
            for i in range(89):
                prec = str(100 - ((200-value)/2))
                value = 1024-(sensor.read())
                oled.fill(0)
                oled.text('Irrigating',25,5)
                oled.text(prec,50,20)
                oled.rect(20,40,88,10,1)
                oled.fill_rect(20,40,i,10,1)
                oled.fill_rect(21,41,i-5,8,0)
                oled.show()
                button()
                if of == 0:
                    break
        else:
            stop(motorPins)
            bled.off()
            oled.fill(0)
            oled.show()

    else:
        oled.fill(0)
        oled.show()
        bled.off()
        gled.off()
        rled.on()
    
        print(count)