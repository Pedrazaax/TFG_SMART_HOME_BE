# TFG_SMART_HOME_BE

# TFG_SMART_HOME_BE

## Introducción

El proyecto TFG_Smart_Home_BE es la parte backend de una solución de hogar inteligente. Este sistema está diseñado para gestionar y controlar dispositivos inteligentes en un entorno doméstico, proporcionando una interfaz de usuario intuitiva y funcionalidades avanzadas para mejorar la comodidad y seguridad del hogar.

## Arquitectura de software del proyecto

La arquitectura del proyecto sigue un enfoque modular y escalable, utilizando varios patrones de diseño para asegurar la mantenibilidad y extensibilidad del código. A continuación se describen los componentes principales y los patrones de diseño utilizados:

### Componentes principales

1. **Controlador (Controller)**: Maneja las solicitudes HTTP entrantes, procesa los datos y delega las tareas a los servicios correspondientes. Se encuentra en el directorio [`controller`](controller/).

2. **Servicios (Service)**: Contiene la lógica de negocio de la aplicación. Los servicios se encargan de realizar operaciones específicas y pueden interactuar con la capa de datos. Se encuentra en el directorio [`service`](service/).

3. **Base de datos (DB)**: Gestiona la persistencia de datos. Esta capa interactúa con la base de datos para realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar). Se encuentra en el directorio [`db`](db/).

4. **Aplicación principal (Main)**: Punto de entrada de la aplicación. Configura y arranca el servidor, y define las rutas principales. Se encuentra en el archivo [`main.py`](main.py).

### Patrones de diseño

1. **Patrón MVC (Modelo-Vista-Controlador)**: La arquitectura sigue el patrón MVC, separando la lógica de negocio (Modelo), la interfaz de usuario (Vista) y el control de flujo (Controlador).

2. **Inyección de dependencias**: Se utiliza para gestionar las dependencias entre los diferentes componentes, facilitando la prueba y el mantenimiento del código.

3. **Repositorio**: Este patrón se utiliza en la capa de datos para abstraer las operaciones de acceso a la base de datos, proporcionando una interfaz limpia y desacoplada.

4. **Singleton**: Algunos servicios y componentes se implementan como singletons para asegurar que solo exista una instancia de ellos durante el ciclo de vida de la aplicación.

Esta arquitectura modular y el uso de patrones de diseño permiten que el proyecto sea fácilmente mantenible y escalable, facilitando la incorporación de nuevas funcionalidades y la adaptación a futuros requerimientos.