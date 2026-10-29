from pathlib import Path

from PyQt6.QtWidgets import QWidget, QLineEdit

from PyQt6 import uic

RUTA_UI = Path(__file__).parent / "registro.ui"

class VentanaRegistro(QWidget):

    def __init__(self, servicio):
        super().__init__()
        uic.loadUi(RUTA_UI, self)
        self._conectar_eventos()
        self.servicios = servicio

    def _conectar_eventos(self):
        self.pb_crear.clicked.connect(self.crear_cuenta)
        self.ckb_mostrar_contrasea.toggled.connect(self.alternar_password)
        self.pb_volver_a_login.clicked.connect(self.volver_al_login)
        self.campo_repetir_contrasena.returnPressed.connect(self.crear_cuenta)
        self.campo_contrasena.textChanged.connect(self.evaluar_contrasena)

    def alternar_password(self, visible):
        if visible:
            self.campo_contrasena.setEchoMode(QLineEdit.EchoMode.Normal)
            self.campo_repetir_contrasena.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.campo_repetir_contrasena.setEchoMode(QLineEdit.EchoMode.Password)
            self.campo_contrasena.setEchoMode(QLineEdit.EchoMode.Password)
        
    def volver_al_login(self):
        from .ventana_login import VentanaLogin
    
        self.ventana = VentanaLogin(servicio=self.servicios) 
        self.ventana.show()
        self.close()

    def crear_cuenta(self):
        datos = self._leer_formulario()
        error = self._validar(datos)
        if error:
            self._mostrar_mensaje(error, tipo="error")
            return

        try:
            self.servicios.registrar(
                    nombre=datos["nombre"],
                    apellido=datos["apellido"],
                    usuario=datos["usuario"],
                    password=datos["contrasena"],  # 👈 Mapeás explícitamente al parámetro 'password'
                    correo=datos["correo"]         # 👈 Mapeás explícitamente al parámetro 'correo'
                        )
        except ValueError as error:
            self._mostrar_mensaje(str(error), tipo="error")
            return

        self._mostrar_mensaje("Cuenta creada. Ya podés volver e iniciar sesión.", tipo="exito")

    def _leer_formulario(self):
        return {
            "nombre": self.Campo_nombre.text().strip(),
            "apellido": self.Campo_apellido.text().strip(),
            "usuario": self.campo_usuario.text().strip(),
            "correo": self.campo_correo.text().strip(),
            "contrasena": self.campo_contrasena.text(),
            "repetir_contrasena": self.campo_repetir_contrasena.text(),
        }

    def _validar(self, datos):
        if not datos["nombre"] or not datos["apellido"] or not datos["usuario"] or not datos["correo"]:
            return "Nombre, apellido, usuario y correo son obligatorios."

        if len(datos["contrasena"]) < 8:
            return f"La contraseña debe tener al menos {8} caracteres."

        if datos["contrasena"] != datos["repetir_contrasena"]:
            return "Las contraseñas no coinciden."

        return None

    def _mostrar_mensaje(self, texto, tipo="info"):
        self.label_mensaje.setText(texto)
        self.label_mensaje.setProperty("tipo", tipo)
        self.label_mensaje.style().unpolish(self.label_mensaje)
        self.label_mensaje.style().polish(self.label_mensaje)

    def evaluar_contrasena(self, texto):
        largo = len(texto)
    
        if largo == 0:
            self.progressBar.setValue(0)
            self.progressBar.setProperty("fuerza", "")
            
        elif largo < 8:
            self.progressBar.setValue(33)
            self.progressBar.setProperty("fuerza", "debil")

        else: 
            tiene_digito = any(c.isdigit() for c in texto)

            if tiene_digito:
                self.progressBar.setValue(66)
                self.progressBar.setProperty("fuerza", "media")
                tiene_mayuscula = any(c.isupper() for c in texto)

                if tiene_mayuscula:
                    self.progressBar.setValue(100)
                    self.progressBar.setProperty("fuerza", "fuerte")
        
    
        self.progressBar.style().unpolish(self.progressBar)
        self.progressBar.style().polish(self.progressBar)