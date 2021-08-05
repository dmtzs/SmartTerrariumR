# Notas para la aplicación

## Interfaz principal
- Conectar a una API del clima para mostrar el clima actual
- Boton para controlar la bomba de agua que vaciara el traste de agua de la serpienteI(tal vez se necesite modificar el programa de arduino si se quiere implementar)
- Mostrar estado del sensor para la reserva de agua saber si se necesita llenar o no
- Mostrar temperatura de la reserva de agua pues debe estar entre tibia casi caliente

## Cosas electron
- Generar ejecutable para proteger el código, checar si se puede hacer via comandos y ver si es más fácil distribuir el ejecutable o primero el código y sobre la rasp ejecutar los comandos de creación del ejecutable y después borrar el repositorio correspondiente.
<br>
Crea paquete json para modificarlo posteriormente aunque es para crear proyecto de nodejs

```
npm init
```

Para instalar electron
```
npm install electron
```

### En linux
Instalar node
```
sudo apt install nodejs
```
Instalar npm
```
sudo apt install npm
```

"start": "electron index.js" -> en linux, archivo: package.json
//"start": "electron ." -> en windows, archivo: package.json

Si en linux se tiene problemas para ejecutar lo de flask:
[Ejecutar correctamente flask](https://medium.com/@sanzidkawsar/the-python-flask-problem-oserror-errno-98-address-already-in-use-flask-49daaccaef4f)

## Archivo json -> appData
- Continuar creando el archivo json en donde se tomará alguna de las configuraciones de la app como los rangos de las temperaturas, humedad, etc
- Continuar agregando mas cosas que nos interesen que se quede en ese archivo como configuración de la app
- Los rangos de humedad y temperaturas es para que el usuario defina que si baja de esos rangos se active lo que debe activarse
- El estado de los focos es para que el usuario indique qué foco es el que se debe de encender en caso la temperatura del terrario baje del rango que el usuario desea
- Los nombres de usuario es para mostrarle algunas cosas de la app con su nombre para ese sentimiento de pertenencia
- Lo que está antes de la configuración es para mostrar un poco de info general de la app.
- Lo de modo app es para que se inicie en modo automático de manera predeterminada

## Actualizaciones futuras
- Checar la viabilidad de la implementacion de api de tiempo para saber que hora es y activar o desactivar el modo dia y noche
- Checar la viabilidad de la implementacion de cambiar entre español e inglés, en este caso sería para inglés porque la de español ya está hecha
- Checar viabilidad para implementar widgets en temperaturas y humedad de la app, que sea una opción que el usuario pueda cambiar

## Preparar rasp para el arduino
- [Permisos puerto serial](https://askubuntu.com/questions/58119/changing-permissions-on-serial-port)
- De igual forma se podría usar un script para automatizar estos pasos necesarios de manera obligatoria
- Comando: sudo usermod -a -G dialout $USER
- [Teclado matricial físico](https://descubrearduino.com/conectar-teclado-a-raspberry-pi/)
- [Teclado html](https://www.youtube.com/watch?v=uGohVJhgSN8&t=594s)
- [Teclado jquery](https://www.jose-aguilar.com/blog/teclado-virtual-con-jquery/)
- Para checar proceso de python: ps -ef | grep python3
- Para la pantalla táctil: sudo ./LCD7B-show

## Control de versiones
Algo común es realizar el manejo de versiones mediante 3 números: X.Y.Z y cada uno indica una cosa diferente:

- El primero (X) se le conoce como versión mayor y nos indica la versión principal del software. Ejemplo: 1.0.0, 3.0.0
- El segundo (Y) se le conoce como versión menor y nos indica nuevas funcionalidades. Ejemplo: 1.2.0, 3.3.0
- El tercero (Z) se le conoce como revisión y nos indica que se hizo una revisión del código por algun fallo. Ejemplo: 1.2.2, 3.3.4

¿cómo sabemos cuando cambiarlos y cuál cambiar?

- Versión mayor o X, cuando agreguemos nuevas funcionalidades importantes, puede ser como un nuevo modulo o característica clave para la funcionalidad.
- Versión menor o Y, cuando hacemos correcciones menores, cuando arreglamos un error y se agregan funcionalidades que no son cruciales para el proyecto.
- Revisión o Z, cada vez que entregamos el proyecto.