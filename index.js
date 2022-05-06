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
var childString = "nothing";
var commando= ""

if (OSName === "win32") {
	childString = "./Server.exe";
	//childString = "./resources/Flask/main.py";
}
if (OSName === "linux") {
	childString= "./Server"
}
if (OSName !== "darwin") {
	var hijo = execFile(childString, (error, stdout, stderr) => {
		if (error) {
			console.log(error.stack);
			console.log(`Error code: ${error.code}`);
			console.log(`Signal received: ${error.signal}`);
			console.log(`Child Process STDOUT: ${stdout}`);
			console.log(`Child Process STDERR: ${stderr}`);
			
			childString = "./resources/Flask/main.py";
			if (OSName === "win32") {
				commando= "py -3.9 " + childString;
			}
			if (OSName === "linux") {
				commando= "python3 " + childString;
			}
			hijo = exec(commando, (error, stdout, stderr) => {
				if (error) {
					console.log(error.stack);
					console.log(`Error code: ${error.code}`);
					console.log(`Signal received: ${error.signal}`);
					console.log(`Child Process STDOUT: ${stdout}`);
					console.log(`Child Process STDERR: ${stderr}`);
				}
			});
		}
	});
}

// Create a global var, wich will keep a reference to out loadingScreen window and main window
let mainWindow;
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
		"file://" + __dirname + "/resources/Flask/app/templates/loading.html"//Maybe this needs to change but maybe not
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
		/*width: 1000,
        height: 680,*/
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

if (OSName !== "darwin") {
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
}
else {
	console.log("The application only supports Linux and Windows systems")
}

app.on("activate", () => {
	if (BrowserWindow.getAllWindows().length == 0) {
		createWindow();
	}
});

app.on("window-all-closed", () => {
	if (OSName === "win32") {
		exec('taskkill /IM "Server.exe" /F');
	}
	if (OSName === "linux") {
		exec(`pkill -xf "${childString}"`);
		if (commando != "") {
			exec(`pkill -xf "${commando} ./resources/Flask/main.py"`);
		}
	}
	app.quit();
});

ipcMain.on("window-close", () => {
	if (OSName === "win32") {
		exec('taskkill /IM "Server.exe" /F');
	}
	if (OSName === "linux") {
		if (commando != "") {
			exec(`pkill -xf "${commando} ./resources/Flask/main.py"`);
		}
		else {
			exec('pkill -xf "./Server"');
			exec('reboot');
		}
	}
app.quit();
});

// Look for the process in linux: ps -ef | grep python3 o ps aux | grep python3
