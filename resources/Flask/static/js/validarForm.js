function validarFormulario() {
    let rangoTempResAgua= document.getElementById("TempAguaReserva").value;
	let rangoTempTerrario= document.getElementById("TempTerrario").value;
	let rangoHumedad= document.getElementById("Humedad").value;

    let aux1= toString(rangoTempResAgua);
    let aux2= toString(rangoTempTerrario);
    let aux3= toString(rangoHumedad);

    if (rangoTempResAgua < 15.55 || rangoTempResAgua > 50) {
        return false;
    }
    else if (rangoTempTerrario < 15.55 || rangoTempTerrario > 50) {
        return false;
    }
    else if (rangoHumedad < 15.55 || rangoHumedad > 50) {
        return false;
    }
    else if (!aux1.includes(".")) {
        return false;
    }
    else if (!aux2.includes(".")) {
        return false;
    }
    else if (!aux3.includes(".")) {
        return false;
    }
}