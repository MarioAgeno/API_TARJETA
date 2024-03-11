import pyodbc, os
from dotenv import load_dotenv

#-- Cargar las variables de entorno.
load_dotenv()

class Conexion:
	
	__SERVER = os.environ.get('SERVER')
	__DATA_BASE = os.environ.get('DATA_BASE')
	__USER = os.environ.get('USER_DB')
	__PASS = os.environ.get('PASS_UDB')
	__DRIVER = os.environ.get('DRIVER_ODBC')
	
	@classmethod
	def get_connection(self):
		return pyodbc.connect(
			f'Driver={self.__DRIVER};'
			f'Server={self.__SERVER};'
			f'Database={self.__DATA_BASE};'
			f'UID={self.__USER};'
			f'PWD={self.__PASS};'
		)
