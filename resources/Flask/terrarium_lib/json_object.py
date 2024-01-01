"""
This module manages the data stored in the appData json file that is used to configure the app at the moment we init the raspberry
so everything will stay with all the configuration added even if the raspberry turns off in a anormal way.

Diego Martínez Sánchez and Guillermo Ortega Romo.
"""
try:
    import os
    import json
except ImportError as err_imp:
    print(f"In file: {__file__} the following import error ocurred: {err_imp}")

# @Description: Class for manage the json appData in order to be used in the app or to update the same json file.
#               In this class are all the methods to read, write and update the data of the json file
class JsonObject():
    """
    This class is used to manage the data stored in the appData json file that is used to configure the app at the moment we init the raspberry
    so everything will stay with all the configuration added even if the raspberry turns off in a anormal way.

    #### Attributes:
    - filename: String that contains the path of the json file.
    - filename2: String that contains the path of the json file.
    - json_data: Object that contains the data of the json file.

    #### Methods:
    - read_data: Method to read the data from the json file.
    - write_data: Method to write all the data in the json file.
    - write_data_change_mode: Method to update in the json file the parameter of the state of the operation mode of the app.
    - write_data_change_light_mode: Method to update in the json file the parameter of the state of the lightmode of the app.
    - write_data_change_ranges: Method to update the ranges for the humidity and temperatures that the automatic mode will be managing.
    - write_data_day_update: Method that needs to update the day stored in the appData.json file in order to be used in the endpoint to verify
    if there's any available update for the production assets of the app.
    - write_data_hour_range: Update the hour ranges for automatic mode light managing
    """
    filename= "resources/appData.json"
    filename2= "../appData.json"

    def __init__(self) -> None:
        """
        Constructor for the JsonObject class.

        #### Attributes:
        - json_data: Object that contains the data of the json file.
        """
        self.json_data = None

    def read_data(self) -> None:
        """
        Method to read the data from the json file appData.
        
        Args:
        - None

        Returns:
        - None
        """
        aux_file= ""

        if os.path.isfile(self.filename):
            aux_file= self.filename
        else:
            aux_file= self.filename2

        try:
            with open(aux_file, "r") as json_file:
                self.json_data = json.load(json_file)
        except Exception:
            print("No se encontró el archivo appData.json en ninguna de las rutas")

    def write_data(self) -> None:
        """
        Method to write all the data in the json file appData.

        Args:
        - None

        Returns:
        - None
        """
        aux_file= ""
        self.json_data = json.dumps(self.json_data, indent=4)

        if os.path.isfile(self.filename):
            aux_file = self.filename
        else:
            aux_file = self.filename2

        try:
            with open(aux_file, "w") as json_file:
                json_file.write(self.json_data)
        except Exception:
            print("No se encontró el archivo appData.json en ninguna de las rutas")

    # @Description: Method to update in the json file the parameter of the state of the operation mode of the app.
    def write_data_change_mode(self, new_mode) -> None:
        """
        Method to update in the json file the parameter of the state of the operation mode of the app.

        Args:
        - new_mode: String that contains the new mode to be updated in the json file.

        Returns:
        - None
        """
        text = 1 if new_mode == "true" else 0
        self.json_data["configuracion"]["modo"] = text

        self.write_data()

    def write_data_change_light_mode(self, new_mode) -> None:
        """
        Method to update in the json file the parameter of the state of the lightmode of the app.

        Args:
        - new_mode: String that contains the new mode to be updated in the json file.

        Returns:
        - None
        """
        if new_mode == "true":
            self.json_data["configuracion"]["dia-noche"] = 1
        if new_mode == "false":
            self.json_data["configuracion"]["dia-noche"] = 0

        self.write_data()

    def write_data_change_ranges(self, received_range, temp_hum, range_temp_hum) -> None:
        """
        Method to update the ranges for the humidity and temperatures that the automatic mode will be managing.

        Args:
        - received_range: String that contains the new range to be updated in the json file.
        - temp_hum: String that contains the parameter to be updated in the json file.
        - range_temp_hum: String that contains the parameter to be updated in the json file.

        Returns:
        - None
        """
        self.json_data["configuracion"][temp_hum][range_temp_hum] = received_range

        self.write_data()

    def write_data_day_update(self, day) -> None:
        """
        Method that needs to update the day stored in the appData.json file in order to be used in the endpoint to verify
        if there's any available update for the production assets of the app.

        Args:
        - day: String that contains the new day to be updated in the json file.

        Returns:
        - None
        """
        self.json_data["updates"]["dia"] = day

        self.write_data()
        # We still need to review this method, maybe we need to add more things to make it work.

    def write_data_hour_range(self, hour, day_night) -> None:
        """
        Update the hour ranges for automatic mode light managing.

        Args:
        - hour: String that contains the new hour to be updated in the json file.
        - day_night: String that contains the parameter to be updated in the json file.

        Returns:
        - None
        """
        self.json_data["configuracion"]["horarios"][day_night] = hour

        self.write_data()
