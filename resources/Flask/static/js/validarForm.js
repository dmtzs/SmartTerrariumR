$(function () {
	$("#Enviar").on("click", function () {
		let rangoTempResAgua = document.getElementById("TempAguaReserva").value;
		let rangoTempTerrario = document.getElementById("TempTerrario").value;
		let rangoHumedad = document.getElementById("Humedad").value;

		if ((rangoTempResAgua < 15.55 && rangoTempResAgua != "") || rangoTempResAgua > 50) {
			Swal.fire({
				title: "Por favor valida los campos del formulario",
				text: "Los campos no pueden llevar letras y el rango de los valores deben ser entre 15.55 y 50",
				icon: "error",
				showCancelButton: false,
				showConfirmButton: true,
			});
		}
		else if ((rangoTempTerrario < 15.55 && rangoTempTerrario != "") || rangoTempTerrario > 50) {
			Swal.fire({
				title: "Por favor valida los campos del formulario",
				text: "Los campos no pueden llevar letras y el rango de los valores deben ser entre 15.55 y 50",
				icon: "error",
				showCancelButton: false,
				showConfirmButton: true,
			});
		}
		else if ((rangoHumedad < 15.55 && rangoHumedad != "") || rangoHumedad > 50) {
			Swal.fire({
				title: "Por favor valida los campos del formulario",
				text: "Los campos no pueden llevar letras y el rango de los valores deben ser entre 15.55 y 50",
				icon: "error",
				showCancelButton: false,
				showConfirmButton: true,
			});
		}
		else {
			Swal.fire({
				title: "Datos aplicados con éxito",
				text: "Los cambios se veran reflejados en el modo automático de la aplicación",
				icon: "success",
				showCancelButton: false,
				showConfirmButton: true,
			});
		}
	});
});
