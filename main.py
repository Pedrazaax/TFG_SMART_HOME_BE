'''
Patrón singleton para instanciar un objeto de la api en todo el programa.
'''

from properties import get_openapi_instance

class SingletonOpenApi:
    '''
    Clase singleton para instanciar un objeto de la api en todo el programa. 
    '''
    _instance = None

    @classmethod
    def get_instance(cls):
        '''
        Instancia un objeto de la api si no existe y lo devuelve.
        '''
        if cls._instance is None:
            cls._instance = get_openapi_instance()
        return cls._instance
