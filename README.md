# GDCode - Terrarium manager

## The project
The purpose of this project is to manage the parameters of my pet that is a snake.
<br>
The data that will be processed is going to be the temperature and humidity with a dht22 sensor, a submersible temperature sensor and an automatic system for spreading water in order to humidify the terrarium every time the humidity is over 50%.
<br>
The spotlights will be turned on or off according to the temperature and it will light the night or day according to the time of day that will be received through an external API connected with the application.
<br>
Also the water will be warm with another sensor for keep warm the reserve of water and the trough will be filled automatically when the water float sensor is activated.
<br>
More functionalities are going to be developed with the time
<br><br>

## Documentation
We dont have a document as documentation but all code has comments in order to be used as documentation for each method created in the project.
<br>
Also please see below the list of the hardware which are going to be used in this project.

## Rasp Berry python program
The user interface will be developed with python using electron and flask microframework for the graphic interface in order to show all the data we need with an interface which is builded with css.
<br>
The program will process the data that comes from the arduino via USB and the python program will be processing this data.
All this in order to be showed through a display connected to the raspberry.
<br>

### Installation, libraries and considerations
* For its correct installation and use you need first python3 installed in your raspberry.
* The project uses Ubuntu mate OS(arm64 bits version).
* The model of the raspberry is pi4 B+.
* You can use raspberry models like pi3 and pi3 B but are not still tested in this ones.
* USB cable for connect both boards between them.
* Execute "python3 InstalacionBase.py" in order to install all python libraries and configuration needed for this project.
<br><br>

## Arduino program
The Arduino is used in order to acquire the parameters we want to show through the LCD of the raspberry and also receive data from the raspberry to do some actions with the arduino.
<br>
All the necesary data will be displayed in the display of the raspberry for its correct manage from the user.

### Installation, libraries and considerations
This libraries should be installed only if you want to develop by yourself the arduino, if not it is not neccesary.
* First you need to use an Arduino uno board in order to use the same pins as the program, if not consider that you will need to change the default pins.
* You need the IDE of Arduino for upload the Arduino program to your board.
* You need to install from the IDE the dht.h library from adafruit in order to read the dht sensor and include it in the program.
* You need to install from the IDE the OneWire.h library from Paul Stoffregen to read the submersible sensor.
* You need to install from the IDE the DallasTemperature.h library from Miles Burton in order to be use with OneWire library.
* If you´re using s linux distribution to upload the file to the Arduino remember to enable the permissions of writing over the USB port.

## Sensor´s and materials list used
* dht22 humidity and temperature sensor
* DS18B20 submersible sensor
* Horn of 2 inches of 1.5 watts
* Water float sensor
* Raspberry pi 4 B+
* LCD touch display of 7 inches
* 256 gb SD
* 3 relays
* 1 L298D chip (H bridge)

## Connection diagram
Here is the diagram connection about how you need to connect all components, to which pin´s, etc.
![](resources/Imgs/Diagrama.png)

<br><br>

# The project is open and still on development