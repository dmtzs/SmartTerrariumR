function validarFormulario() {
    let rangoTempResAgua= document.getElementById("TempAguaReserva").value;
    let rangoTempTerrario= document.getElementById("TempTerrario").value;
    let rangoHumedad= document.getElementById("Humedad").value;

    if (rangoTempResAgua== null || rangoTempResAgua== "" || rangoTempResAgua.length < 5 || rangoTempResAgua.length > 5 || !Number.isNaN(rangoTempResAgua)) {
        return false;
    }
    else if (rangoTempTerrario== null || rangoTempTerrario== "" || rangoTempTerrario.length < 5 || rangoTempTerrario.length > 5 || !Number.isNaN(rangoTempTerrario)) {
        return false;
    }
    else if (rangoHumedad== null || rangoHumedad== "" || rangoHumedad.length < 5 || rangoHumedad.length > 5 || !Number.isNaN(rangoHumedad)) {
        return false;
    }
}