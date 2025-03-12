Autor: Carlos Pedraza Antona

# TFG_SMART_HOME_BE

El proyecto TFG_Smart_Home_BE es la parte backend de una solución de hogar inteligente. Este sistema está diseñado para gestionar y controlar dispositivos inteligentes en un entorno doméstico, proporcionando una interfaz de usuario intuitiva y funcionalidades avanzadas para mejorar la comodidad y seguridad del hogar.

## Ejecución en local

A continuación, se van a detallar los pasos a seguir para ejecutar en local el proyecto.

1. **Clonar el repositorio**

```bash
git clone https://github.com/Pedrazaax/TFG_SMART_HOME_BE.git
```

2. **Instalar las dependencias**

```bash
pip install -r requirements.txt
```

3. **Configurar las variables de entorno**
    - Crear un archivo `.env` en la raíz del proyecto.
    - Añadir las siguientes variables de entorno al archivo `.env`:
    
    ``` bash
    ACCESS_ID
    ACCESS_KEY
    API_ENDPOINT
    MQ_ENDPOINT
    API_KEY_NVD
    URL_DB
    ```

4. **Ejecutar la aplicación**

```bash
python -m uvicorn app:app --reload
```

## Arquitectura de software del proyecto

La arquitectura del proyecto sigue un enfoque modular y escalable, utilizando varios patrones de diseño para asegurar la mantenibilidad y extensibilidad del código. A continuación se describen los componentes principales y los patrones de diseño utilizados:

### Componentes principales

1. **Configuración (Config)**: Contiene las variables de configuración de la aplicación, como la URL de la base de datos, las credenciales de acceso a la API, etc. Se encuentra en el directorio [`config`](config/).

#### Archivos dentro de la carpeta Config

- **`main.py`**: Este archivo contiene la inicialización de una instancia singleton necesaria para el arranque de la aplicación.

- **`properties.py`**: Este archivo contiene funciones auxiliares para obtener instancias de configuración de la API de TUYA en la nube.

- **`requirements.txt`**: En este archivo se encuentran las dependencias necesarias para la ejecución del proyecto.

2. **Controlador (Controller)**: Maneja las solicitudes HTTP entrantes, procesa los datos y delega las tareas a los servicios correspondientes. Se encuentra en el directorio [`controller`](controller/).

#### Archivos dentro de la carpeta Controller

- **`api_tuya_controller.py`**: Este archivo maneja las solicitudes relacionadas con la API de Tuya. Incluye endpoints para interactuar con los servicios de Tuya, como obtener información de dispositivos y controlar dispositivos.

- **`auth_users_controller.py`**: Este archivo maneja las solicitudes relacionadas con la autenticación y autorización de usuarios. Incluye endpoints para el registro, inicio de sesión y obtención de perfiles de usuario.

- **`consumo_controller.py`**: Este archivo maneja las solicitudes relacionadas con el consumo de energía de los dispositivos. Incluye endpoints para obtener y actualizar datos de consumo.

- **`device_controller.py`**: Este archivo maneja las solicitudes relacionadas con los dispositivos inteligentes. Incluye endpoints para agregar, eliminar, actualizar y obtener información de los dispositivos.

- **`historylogs_controller.py`**: Este archivo maneja las solicitudes relacionadas con los registros históricos. Incluye endpoints para obtener y gestionar los logs históricos de los dispositivos.

- **`local_device_controller.py`**: Este archivo maneja las solicitudes relacionadas con los dispositivos locales. Incluye endpoints para agregar, eliminar, actualizar y obtener información de los dispositivos locales.

- **`local_measures_controller.py`**: Este archivo maneja las solicitudes relacionadas con las medidas locales de los dispositivos. Incluye endpoints para obtener y actualizar datos de medidas locales.

- **`room_controller.py`**: Este archivo maneja las solicitudes relacionadas con la gestión de habitaciones. Incluye endpoints para agregar, eliminar, actualizar y obtener información de las habitaciones.

- **`user_controller.py`**: Este archivo maneja las solicitudes relacionadas con la gestión de usuarios. Incluye endpoints para agregar, eliminar, actualizar y obtener información de los usuarios.

3. **Servicios (Service)**: Contiene la lógica de negocio de la aplicación. Los servicios se encargan de realizar operaciones específicas y pueden interactuar con la capa de datos. Se encuentra en el directorio [`service`](service/).

#### Archivos dentro de la carpeta Service

- **`api_tuya_service.py`**: Este archivo contiene la lógica de negocio relacionada con la API de Tuya. Incluye funciones para interactuar con los servicios de Tuya, como obtener información de dispositivos y controlar dispositivos.

- **`consumo_service.py`**: Este archivo contiene la lógica de negocio relacionada con el consumo de energía de los dispositivos. Incluye funciones para obtener y actualizar datos de consumo.

- **`device_service.py`**: Este archivo contiene la lógica de negocio relacionada con los dispositivos inteligentes. Incluye funciones para agregar, eliminar, actualizar y obtener información de los dispositivos.

- **`historylogs_service.py`**: Este archivo contiene la lógica de negocio relacionada con los registros históricos. Incluye funciones para obtener y gestionar los logs históricos de los dispositivos.

- **`local_device_service.py`**: Este archivo contiene la lógica de negocio relacionada con los dispositivos locales. Incluye funciones para agregar, eliminar, actualizar y obtener información de los dispositivos locales.

- **`room_service.py`**: Este archivo contiene la lógica de negocio relacionada con la gestión de habitaciones. Incluye funciones para agregar, eliminar, actualizar y obtener información de las habitaciones.

- **`user_service.py`**: Este archivo contiene la lógica de negocio relacionada con la gestión de usuarios. Incluye funciones para agregar, eliminar, actualizar y obtener información de los usuarios.

Gestiona la persistencia de datos. Esta capa interactúa con la base de datos para realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar). Se encuentra en el directorio [`db`](db/).

#### Estructura de la carpeta DB

La carpeta `db` está organizada en tres subdirectorios principales:

- **Models**: Contiene las definiciones de los modelos de datos que representan las entidades de la base de datos.
- **Schemas**: Contiene los esquemas de datos utilizados para la validación y serialización de los datos.
- **Client**: Contiene la configuración del cliente de la base de datos para conectarse a la base de datos.

#### Archivos dentro de la carpeta Models

- **`device.py`**: Este archivo define el modelo de datos para los dispositivos inteligentes. Incluye atributos como el nombre del dispositivo, el ID del dispositivo, el tipo de dispositivo, la clave, los comandos, el tiempo de creación, el tiempo de actualización, la IP, el estado en línea y el modelo.

- **`keys_api.py`**: Este archivo define el modelo de datos para las claves de la API. Incluye atributos como el ID de la clave, el nombre de la clave y el valor de la clave.

- **`prueba_consumo.py`**: Este archivo define el modelo de datos para las pruebas de consumo de energía. Incluye atributos como el ID de la prueba, el nombre de la prueba, el valor de consumo y la fecha de la prueba.

- **`room.py`**: Este archivo define el modelo de datos para las habitaciones. Incluye atributos como el ID de la habitación, el nombre de la habitación y la lista de dispositivos asociados a la habitación.

- **`user.py`**: Este archivo define el modelo de datos para los usuarios. Incluye atributos como el ID del usuario, el nombre de usuario, la contraseña, el correo electrónico y el rol del usuario.

#### Archivos dentro de la carpeta Schemas

- **`device_schema.py`**: Este archivo define el esquema de datos para los dispositivos inteligentes. Se utiliza para la validación y serialización de los datos de los dispositivos.

- **`keys_api_schema.py`**: Este archivo define el esquema de datos para las claves de la API. Se utiliza para la validación y serialización de los datos de las claves de la API.

- **`prueba_consumo_schema.py`**: Este archivo define el esquema de datos para las pruebas de consumo de energía. Se utiliza para la validación y serialización de los datos de las pruebas de consumo.

- **`room_schema.py`**: Este archivo define el esquema de datos para las habitaciones. Se utiliza para la validación y serialización de los datos de las habitaciones.

- **`user_schema.py`**: Este archivo define el esquema de datos para los usuarios. Se utiliza para la validación y serialización de los datos de los usuarios.

#### Archivo dentro de la carpeta Client

- **`client.py`**: Este archivo contiene la configuración del cliente de la base de datos. Se utiliza para establecer la conexión con la base de datos y realizar operaciones CRUD en las colecciones de la base de datos.

5. **Aplicación principal (app)**: Punto de entrada de la aplicación. Configura y arranca el servidor, y define las rutas principales. Se encuentra en el archivo [`app.py`](app.py).

### Patrones de diseño

1. **Patrón MVC (Modelo-Vista-Controlador)**: La arquitectura sigue el patrón MVC, separando la lógica de negocio (Modelo), la interfaz de usuario (Vista) y el control de flujo (Controlador).

2. **Inyección de dependencias**: Se utiliza para gestionar las dependencias entre los diferentes componentes, facilitando la prueba y el mantenimiento del código.

3. **Repositorio**: Este patrón se utiliza en la capa de datos para abstraer las operaciones de acceso a la base de datos, proporcionando una interfaz limpia y desacoplada.

4. **Singleton**: Algunos servicios y componentes se implementan como singletons para asegurar que solo exista una instancia de ellos durante el ciclo de vida de la aplicación.

Esta arquitectura modular y el uso de patrones de diseño permiten que el proyecto sea fácilmente mantenible y escalable, facilitando la incorporación de nuevas funcionalidades y la adaptación a futuros requerimientos.