import base64

# message = "snAk3_Terra4M3l0n"
message = "dmtzs"
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_message = base64_bytes.decode('ascii')

print(base64_message)

base64_message = "ZG10enM="
base64_bytes = base64_message.encode('ascii')
message_bytes = base64.b64decode(base64_bytes)
message = message_bytes.decode('ascii')

print(message)

# Usuario original: dmtzs
# Usuario codificado: ZG10enM=

# Contraseña original: snAk3_Terra4M3l0n
# Contraseña codificada: c25BazNfVGVycmE0TTNsMG4=

# Pasar a base64 la contraseña y usuario y después de eso encriptar el resultado con AES guardando llave secreta en variables de entorno en la raspberry