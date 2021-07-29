//--------------------------------------------Importaciones de bibliotecas, constantes y variables--------------------------------------------
const { app, BrowserWindow, Menu, ipcMain } = require("electron"); //12308
const { exec } = require("child_process");
const path = require("path");
const waitPort = require("wait-port");
const Alert = require("electron-alert");

const params = {
	host: "localhost",
	port: 5000,
};

//Detectar sistema operativo
let OSName = process.platform;

var childString = "nothing";
if (OSName === "win32") {
	childString = "python resources/Flask/main.py";
}
if (OSName === "linux") {
	childString = "python3 resources/Flask/main.py";
}

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

const hijo = exec(childString, (error, stdout, stderr) => {
	if (error) {
		console.log(error.stack);
		console.log(`Error code: ${error.code}`);
		console.log(`Signal received: ${error.signal}`);
	}
	console.log(`Child Process STDOUT: ${stdout}`);
	console.log(`Child Process STDERR: ${stderr}`);
});

let mainWindow;

/// create a global var, wich will keep a reference to out loadingScreen window
let loadingScreen;
const createLoadingScreen = () => {
	/// create a browser window
	loadingScreen = new BrowserWindow(
		Object.assign({
			/// define width and height for the window
			width: 250,
			height: 400,
			/// remove the window frame, so it will become a frameless window
			frame: false,
			/// and set the transparency, to remove any window background color
			transparent: true,
			show: false,
		})
	);
	loadingScreen.setResizable(false);
	loadingScreen.loadURL("file://" + __dirname + "/resources/loading.html");
	loadingScreen.on("closed", () => (loadingScreen = null));
	loadingScreen.once("ready-to-show", () => {
		loadingScreen.show();
	});
};

//--------------------------------------------Función cerebro--------------------------------------------
function createWindow() {
	mainWindow = new BrowserWindow({
		fullscreen: true,
		/*width: 800,
        height: 480,*/
		title: "Terrario", //Esto se cambia por el mismo flask ya que se pone el tiítulo de la página en la que estás
		icon: __dirname + "../resources/Imgs/BoaEsmeraldaA.ico",
		minimizable: false,
		show: false,
		webPreferences: {
			preload: path.join(__dirname, "resources/preload.js"),
			nodeIntegration: true,
		},
	});

	mainWindow.setMenuBarVisibility(false);
	mainWindow.setResizable(false);
	//mainWindow.maximize();
	mainWindow.loadURL("http://127.0.0.1:5000/");

	mainWindow.webContents.session.clearCache();
	//espera a que cargue flask para mostrar la ventana (elimina la pantalla blanca al ejecutar la aplicacion)
	mainWindow.once("ready-to-show", () => {
		/// then close the loading screen window and show the main window
		if (loadingScreen) {
			setTimeout(() => {
				loadingScreen.close();
			}, 500);
		}
		mainWindow.show();
	});
}

//--------------------------------------------Eventos sobre la app--------------------------------------------
hijo.on("exit", (code) => {
	console.log(`Child process exited with exit code ${code}`);
});

app.whenReady().then(() => {
	//elimina el error de connection refused al iniciar la aplicacion
	createLoadingScreen();
	waitPort(params)
		.then((open) => {
			createWindow();
			if (open) console.log("The port is now open!");
			else console.log("The port did not open before the timeout...");
		})
		.catch((err) => {
			console.err(
				`An unknown error occured while waiting for the port: ${err}`
			);
		});
	// const mainMenu= Menu.buildFromTemplate(template);
	// Menu.setApplicationMenu(mainMenu);
});

app.on("activate", () => {
	if (BrowserWindow.getAllWindows().length == 0) {
		createWindow();
	}
});

app.on("window-all-closed", () => {
	if (process.platform !== "darwin") {
		if (OSName === "win32") {
			exec('taskkill /IM "python.exe" /F');
		}
		if (OSName === "linux") {
			exec('pkill -xf "python3 resources/Flask/main.py"');
		}
		app.quit();
	}
});

ipcMain.on("window-close", () => {
	if (OSName === "win32") {
		exec('taskkill /IM "python.exe" /F');
	}
	if (OSName === "linux") {
		exec('pkill -xf "python3 resources/Flask/main.py"');
		//exec('reboot');
	}
	app.quit();
});

// ipcMain.on("alertaFormError", () => {
// 	let alert = new Alert();

// 	let swalOptions = {
// 		title: "Por favor valida los campos del formulario",
// 		text: "Los campos no pueden llevar letras y el rango de los valores deben ser entre 15.55 y 50",
// 		icon: "error",
// 		showCancelButton: false,
// 		showConfirmButton: true,
// 	};

// 	alert.fireFrameless(swalOptions, mainWindow, true, false);
// });

// ipcMain.on("alertaFormSuccess", () => {
// 	let alert = new Alert();

// 	let swalOptions = {
// 		title: "Datos aplicados con éxito",
// 		text: "Los cambios se veran reflejados en el modo automático de la aplicación",
// 		icon: "success",
// 		showCancelButton: false,
// 		showConfirmButton: true,
// 	};

// 	alert.fireFrameless(swalOptions, mainWindow, true, false);
// 	/*Probar sweet alert: https://sweetalert2.github.io/*/
// });

//Buscar proceso en linux: ps -ef | grep python3
