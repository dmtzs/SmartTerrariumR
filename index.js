//--------------------------------------------Libraries imports constants and variables--------------------------------------------
const { app, BrowserWindow, ipcMain } = require("electron");
const { exec, execFile } = require("child_process");
const path = require("path");
const waitPort = require("wait-port");

// Variabels and constants
const params = {
	host: "localhost",
	port: 5000,
};

let OSName = process.platform;
let mainUser= process.env.USER;
let serverPath= `/home/${mainUser}/Documents/SmartTerrariumR/`
var childString = "nothing";

try {//Check if at last we can put in a function the part of const hijo because that part maybe we can do it more modular
	if (OSName === "win32") {
		childString = "./Server.exe";
	}
	if (OSName === "linux") {
		childString = `${serverPath}Server`;
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
} catch (error) {
	if (OSName === "win32") {
		childString = "python ./resources/Flask/main.py";
	}
	if (OSName === "linux") {
		childString = "python3 ./resources/Flask/main.py";
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
}

let mainWindow;

// Create a global var, wich will keep a reference to out loadingScreen window
let loadingScreen;
const createLoadingScreen = () => {
	// create a browser window
	loadingScreen = new BrowserWindow(
		Object.assign({
			// define width and height for the window
			width: 250,
			height: 400,
			// remove the window frame, so it will become a frameless window
			frame: false,
			// and set the transparency, to remove any window background color
			transparent: true,
			show: false,
		})
	);
	loadingScreen.setResizable(false);
	loadingScreen.loadURL(
		"file://" + __dirname + "/resources/Flask/templates/loading.html"//Maybe this needs to change but maybe not
	);
	loadingScreen.on("closed", () => (loadingScreen = null));
	loadingScreen.once("ready-to-show", () => {
		loadingScreen.show();
	});
};

//--------------------------------------------Brain function--------------------------------------------
function createWindow() {
	mainWindow = new BrowserWindow({
		fullscreen: true,
		/*width: 800,
        height: 480,*/
		title: "Terrario",
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
	// It waits until the flask is loaded in order to show the window (deletes the white screen at the execution moment of the app)
	mainWindow.once("ready-to-show", () => {
		// Then close the loading screen window and show the main window
		if (loadingScreen) {
			setTimeout(() => {
				loadingScreen.close();
			}, 500);
		}
		mainWindow.show();
	});
}

//--------------------------------------------Events over the app--------------------------------------------
hijo.on("exit", (code) => {
	console.log(`Child process exited with exit code ${code}`);
});

app.whenReady().then(() => {
	// Deletes the error connection refused when we start the application
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
		try {
			if (OSName === "win32") {
				exec('taskkill /IM "Server.exe" /F');
			}
			if (OSName === "linux") {
				exec('pkill -xf "' + `${serverPath}Server` + '"');
			}
		} catch (error) {
			if (OSName === "win32") {
				exec('taskkill /IM "Server.exe" /F');// We still need to check this what todo for windows exception
			}
			if (OSName === "linux") {
				exec('pkill -xf "python3 ./resources/Flask/main.py"');
			}
		}
		app.quit();
	}
});

ipcMain.on("window-close", () => {
	try {
		if (OSName === "win32") {
			exec('taskkill /IM "Server.exe" /F');
		}
		if (OSName === "linux") {
			exec('pkill -xf "' + `${serverPath}Server` + '"');
			//exec('pkill -xf "./Server"');
			//exec('reboot');
		}
	} catch (error) {
		if (OSName === "win32") {
			exec('taskkill /IM "Server.exe" /F');//We still need to check this what todo for windows exception
		}
		if (OSName === "linux") {
			exec('pkill -xf "python3 ./resources/Flask/main.py"');
			//exec('reboot');
		}
	}
	app.quit();
});

// Look for the process in linux: ps -ef | grep python3 o ps aux | grep python3
