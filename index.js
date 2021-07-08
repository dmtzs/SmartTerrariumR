//--------------------------------------------Importaciones de bibliotecas, constantes y variables--------------------------------------------
const { app, BrowserWindow,  Menu, ipcMain}= require("electron");//12308
const { exec } = require("child_process");
const path = require('path');

// const template= [
//     {
//         label: "Reiniciar",
//         submenu: [
//             {
//                 label: "reiniciar sistema",
//                 accelerator: "Alt+F4",
//                 click(){
//                     exec('taskkill /IM "python.exe" /F');
//                     //exec('pkill -xf "python3 ./Flask/main.py"');
//                     //exec('reboot');
//                     //Queda pendiente función para validar sistema operativo, si es mac no se ejecuta la app si no ejecutar el kill correspondiente.
//                     app.quit();
//                 }
//             }
//         ]
//     }
// ];

//Cambiar a python3 cuando sea en la rasp
const hijo = exec('python3 resources/Flask/main.py', function (error, stdout, stderr) {
    if (error) {
      console.log(error.stack);
      console.log('Error code: '+error.code);
      console.log('Signal received: '+error.signal);
    }
    console.log('Child Process STDOUT: '+stdout);
    console.log('Child Process STDERR: '+stderr);
  });

let mainWindow;

//--------------------------------------------Función cerebro--------------------------------------------
function createWindow() {
    mainWindow = new BrowserWindow({
        fullscreen: true,
        /*width: 800,
        height: 480,*/
        title: "Terrario",//Esto se cambia por el mismo flask ya que se pone el tiítulo de la página en la que estás
        icon: __dirname + "../resources/Imgs/BoaEsmeraldaA.ico",
        minimizable: false,
        show: false,
        webPreferences: {
            preload: path.join(__dirname, 'resources/preload.js'),
            nodeIntegration: true
        }
    })
    
    mainWindow.setMenuBarVisibility(false)
    mainWindow.setResizable(false)
    //mainWindow.maximize();
    mainWindow.loadURL("http://127.0.0.1:5000/")
    //mainWindow.loadFile(__dirname + "./templates/index.html")
    mainWindow.webContents.session.clearCache();
    //espera a que cargue flask para mostrar la ventana (elimina la pantalla blanca al ejecutar la aplicacion)
    mainWindow.once('ready-to-show', () => {
        mainWindow.show()
    })
}


//--------------------------------------------Eventos sobre la app--------------------------------------------
hijo.on('exit', (code) => {
    console.log('Child process exited with exit code '+code);
  })

app.whenReady().then(() => {
    createWindow()
    // const mainMenu= Menu.buildFromTemplate(template);
    // Menu.setApplicationMenu(mainMenu);
});

app.on("window-all-closed", () => {
    if (process.platform!== "darwin") {
        //exec('taskkill /IM "python.exe" /F');
        exec('pkill -xf "python3 ./resources/Flask/main.py"')
        app.quit()
    }
});

app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length== 0) {
        createWindow()
    }
});

ipcMain.on('window-close', function () {
    //exec('taskkill /IM "python.exe" /F');
    exec('pkill -xf "python3 ./resources/Flask/main.py"');
    //exec('reboot');
    //Queda pendiente función para validar sistema operativo, si es mac no se ejecuta la app si no ejecutar el kill correspondiente.
    app.quit();
});