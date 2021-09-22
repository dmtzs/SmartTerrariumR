//--------------------------------------------Importaciones de bibliotecas, constantes y variables--------------------------------------------
const { app, BrowserWindow, ipcMain } = require("electron");
const { exec, execFile } = require("child_process");
const path = require("path");
const waitPort = require("wait-port");

const params = {
	host: "localhost",
	port: 5000,
};

//Detectar sistema operativo
let OSName = process.platform;

var childString = "nothing";
if (OSName === "win32") {
	childString = "./Server.exe";
}
if (OSName === "linux") {
	childString = "./Server";
}

const hijo = execFile(childString, (error, stdout, stderr) => {
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
	loadingScreen.loadURL(
		"file://" + __dirname + "/resources/Flask/templates/loading.html"
	);
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
		//icon: NativeImage.createFromPath("resources/Imgs/Boapng.png"),
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
			exec('taskkill /IM "Server.exe" /F');
		}
		if (OSName === "linux") {
			exec('pkill -xf "./Server"');
		}
		app.quit();
	}
});

ipcMain.on("window-close", () => {
	if (OSName === "win32") {
		exec('taskkill /IM "Server.exe" /F');
	}
	if (OSName === "linux") {
		exec('pkill -xf "./Server"');
		//exec('reboot');
	}
	app.quit();
});

//Buscar proceso en linux: ps -ef | grep python3
