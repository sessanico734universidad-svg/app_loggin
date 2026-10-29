
"""Servicio de autenticación SIMULADO, en memoria.

No es un sistema de producción: los usuarios se pierden al cerrar la app,
no hay límite de intentos, ni sesiones, ni base de datos.
Lo que sí hace bien desde ahora: nunca guarda la contraseña, solo su hash con sal.
"""
import hashlib
import hmac
import os

LONGITUD_MINIMA_PASSWORD = 8
ITERACIONES = 600_000


class ServicioAutenticacion:

    def __init__(self):
        # "ana@correo.com" -> {"nombre": ..., "sal": ..., "hash": ...}
        self._usuarios = {}

    def registrar(self, nombre, apellido, usuario, password, correo):
        clave = usuario.strip().lower()
        minimo = LONGITUD_MINIMA_PASSWORD
        if len(password) < minimo:
            raise ValueError(f"La contraseña necesita al menos {minimo} caracteres.")
        if clave in self._usuarios:
            raise ValueError("Ese usuario ya está registrado.")
        if not nombre.strip():
            raise ValueError("El nombre es obligatorio.")
        if not apellido.strip():
            raise ValueError("El apellido es obligatorio.")
        if not correo.strip():
            raise ValueError("El correo es obligatorio.")
        if not usuario.strip():
            raise ValueError("El usuario es obligatorio.")


        sal = os.urandom(16)
        self._usuarios[clave] = {
            "nombre": nombre.strip(),
            "apellido": apellido.strip(),
            "correo": correo.strip(),
            "sal": sal,
            "hash": self._calcular_hash(password, sal),
            "correo": correo.strip()
        }

    def autenticar(self, identificador, password):
        busqueda = identificador.strip().lower()
        datos_usuario = None
        if busqueda in self._usuarios:
            datos_usuario = self._usuarios[busqueda]
        else:
            for u in self._usuarios.values():
                if u["correo"] == busqueda:
                    datos_usuario = u
                    break 

        if datos_usuario is None:
            return False
    
        sal = datos_usuario["sal"]
        hash_guardado = datos_usuario["hash"]
        
        hash_intento = self._calcular_hash(password, sal)
        return hmac.compare_digest(hash_guardado, hash_intento)

    @staticmethod
    def _calcular_hash(password, sal):
        return hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), sal, ITERACIONES
        )