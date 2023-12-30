#include <stdio.h>
#include <curl/curl.h>
#include "miniz.h"

// Estructura para almacenar los datos descargados
struct MemoryStruct
{
    char *memory;
    size_t size;
};

// Función de escritura para CURL
static size_t WriteMemoryCallback(void *contents, size_t size, size_t nmemb, void *userp)
{
    size_t realsize = size * nmemb;
    struct MemoryStruct *mem = (struct MemoryStruct *)userp;

    mem->memory = realloc(mem->memory, mem->size + realsize + 1);
    if (mem->memory == NULL)
    {
        // Si hay un error al asignar memoria, regresa 0 para indicar un error a CURL
        return 0;
    }

    // Copia los datos descargados al buffer de memoria
    memcpy(&(mem->memory[mem->size]), contents, realsize);
    mem->size += realsize;
    mem->memory[mem->size] = 0;

    return realsize;
}

int main(void) {
    CURL *curl;
    CURLcode res;

    // URL del archivo ZIP
    const char *url = "https://github.com/dmtzs/SmartTerrariumR/releases/download/Local_libraries/localLibraries.zip";

    // Inicializa la estructura CURL
    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();

    if (curl) {
        // Estructura para almacenar los datos descargados
        struct MemoryStruct chunk;
        chunk.memory = malloc(1); // Inicializa con un byte para evitar problemas con realloc
        chunk.size = 0;

        // Configura la URL para descargar
        curl_easy_setopt(curl, CURLOPT_URL, url);

        // Configura la función de escritura
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void *)&chunk);

        // Realiza la descarga
        res = curl_easy_perform(curl);

        // Verifica si la descarga fue exitosa
        if (res != CURLE_OK) {
            fprintf(stderr, "Error en la descarga: %s\n", curl_easy_strerror(res));
        }
        else {
            // Descomprime el archivo ZIP
            mz_zip_archive zip_archive = {0};
            if (mz_zip_reader_init_mem(&zip_archive, chunk.memory, chunk.size, 0) != MZ_TRUE) {
                fprintf(stderr, "Error al inicializar el lector ZIP\n");
            }
            else {
                int num_files = mz_zip_reader_get_num_files(&zip_archive);
                for (int i = 0; i < num_files; ++i) {
                    mz_zip_archive_file_stat file_stat;
                    if (mz_zip_reader_file_stat(&zip_archive, i, &file_stat) == MZ_TRUE) {
                        // Puedes procesar o extraer los archivos aquí
                        printf("Archivo %d: %s\n", i + 1, file_stat.m_filename);
                    }
                }
                mz_zip_reader_end(&zip_archive);
            }
        }

        // Limpia la estructura de datos
        free(chunk.memory);

        // Limpia y cierra CURL
        curl_easy_cleanup(curl);
    }

    // Limpia la inicialización global de CURL
    curl_global_cleanup();

    return 0;
}
