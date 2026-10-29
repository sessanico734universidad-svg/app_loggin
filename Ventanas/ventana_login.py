from pathlib import Path

from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QLineEdit
from Controladores.auntentificadores import ServicioAutenticacion


RUTA_UI = Path(__file__).parent / "login.ui"


class VentanaLogin(QWidget):
    """Controla la pantalla de inicio de sesión. El diseño vive en login.ui."""

    def __init__(self, servicio):
        super().__init__()
        uic.loadUi(RUTA_UI, self)
        self._conectar_eventos()
        self.servicio = servicio

    def _conectar_eventos(self):
        self.btn_login.clicked.connect(self.iniciar_sesion)
        self.chk_mostrar_password.toggled.connect(self.alternar_password)
        self.btn_ir_registro.clicked.connect(self.ir_a_registro)
        self.input_password.returnPressed.connect(self.iniciar_sesion)

    def alternar_password(self, visible):
        if visible:
            self.input_password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.input_password.setEchoMode(QLineEdit.EchoMode.Password)

    def ir_a_registro(self):
        from .ventana_registro import VentanaRegistro
        self.ventana = VentanaRegistro(servicio=self.servicio)
        self.ventana.show()
        self.close()

    def iniciar_sesion(self):
        usuario = self.input_usuario.text().strip()
        password = self.input_password.text()

        error = self._validar(usuario, password)
        if error:
            self._mostrar_mensaje(error, tipo="error")
            return

        self._mostrar_mensaje(
            "Datos completos. Ya puede ingresar.", tipo="exito")
        
    def _validar(self, identificador, password):
        if self.servicio.autenticar(identificador, password) == False:
            return "Usuario o contraseña incorrectos."

        else:
            return None

    def _mostrar_mensaje(self, texto, tipo="info"):
        self.label_mensaje.setText(texto)
        self.label_mensaje.setProperty("tipo", tipo)
        self.label_mensaje.style().unpolish(self.label_mensaje)
        self.label_mensaje.style().polish(self.label_mensaje)