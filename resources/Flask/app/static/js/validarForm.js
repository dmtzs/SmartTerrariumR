$(function () {
	$("#Enviar").on("click", function () {
		let rangoTempResAgua = document.getElementById("TempAguaReserva").value;
		let rangoTempTerrario = document.getElementById("TempTerrario").value;
		let rangoHumedad = document.getElementById("Humedad").value;
		let timeDia = document.getElementById("timeDia").value;
		let timeNoche = document.getElementById("timeNoche").value;

		if ((rangoTempResAgua < 15.55 && rangoTempResAgua != "") || rangoTempResAgua > 50) {
			Swal.fire({
				title: "Por favor valida los campos del formulario",
				text: "Los campos no pueden llevar letras y el rango de los valores deben ser entre 15.55 y 50 o estar vacío para mantener configuración previa",
				icon: "error",
				showCancelButton: false,
				showConfirmButton: true,
			});
			return false;
		}
		else if ((rangoTempTerrario < 15.55 && rangoTempTerrario != "") || rangoTempTerrario > 50) {
			Swal.fire({
				title: "Por favor valida los campos del formulario",
				text: "Los campos no pueden llevar letras y el rango de los valores deben ser entre 15.55 y 50 o estar vacío para mantener configuración previa",
				icon: "error",
				showCancelButton: false,
				showConfirmButton: true,
			});
			return false;
		}
		else if ((rangoHumedad < 15.55 && rangoHumedad != "") || rangoHumedad > 50) {
			Swal.fire({
				title: "Por favor valida los campos del formulario",
				text: "Los campos no pueden llevar letras y el rango de los valores deben ser entre 15.55 y 50 o estar vacío para mantener configuración previa",
				icon: "error",
				showCancelButton: false,
				showConfirmButton: true,
			});
			return false;
		}
		else if (timeDia === timeNoche) {
			Swal.fire({
				title: "Por favor valida los campos del formulario",
				text: "Los horarios de día y noche no pueden ser el mismo",
				icon: "error",
				showCancelButton: false,
				showConfirmButton: true,
			});
			return false;
		}
	});
});