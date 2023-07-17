from properties import get_openapi_instance

# Patrón singleton para instanciar un objeto de la api en todo el programa.
class OpenApiSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = get_openapi_instance()
        return cls._instance
