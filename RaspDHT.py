def codigo2():
    import Adafruit_DHT as dht
    from time import sleep
    #Set DATA pin
    DHT = 4
    while True:
        #Read Temp and Hum from DHT22
        h,t = dht.read_retry(dht.DHT22, DHT)
        #Print Temperature and Humidity on Shell window
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t,h))
        sleep(5) #Wait 5 seconds and read again

def codigo1():
    import Adafruit_DHT as dht

    DHT_SENSOR = dht.DHT22
    DHT_PIN = 4

    while True:
        humidity, temperature = dht.read_retry(DHT_SENSOR, DHT_PIN)

        if humidity is not None and temperature is not None:
            print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
        else:
            print("Failed to retrieve data from humidity sensor")