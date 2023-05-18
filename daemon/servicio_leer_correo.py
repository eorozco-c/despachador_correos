from decouple import config
from O365 import Account
from datetime import datetime
import pyodbc
import time
import logging
import os
import zoneinfo

#obtener la hora actual
STG = zoneinfo.ZoneInfo("America/Santiago")

datetime_now = datetime.now(STG)
#validar si existe la carpeta logs, si no existe crearla
if not os.path.exists('./logs'):
    os.makedirs('./logs')

#configurar el log
logging.basicConfig(filename=f"./logs/servicio_correo_{datetime_now.strftime('%Y-%m-%d_%H-%M-%S')}.log",
                filemode='a',
                format='[%(asctime)s] | %(levelname)s | %(message)s',
                datefmt='%d-%m-%Y %H:%M:%S',
                level=logging.INFO)
logging.info('Iniciando servicio de correo')

print('Iniciando servicio de correo')

def main(cursor):
    #read the last mail not read from the user and only from,subject and body
    scope = ['https://graph.microsoft.com/.default']

    #obtain correo from dbo.configuraciones_casilla last row
    cursor.execute("SELECT Q2.email FROM dbo.configuraciones_configuracion AS Q1 INNER JOIN dbo.configuraciones_casilla AS Q2 ON Q1.casilla_id = Q2.id")
    try:
        row = cursor.fetchone()
        correo = row[0]
    except:
        logging.info('No hay correo configurado en la tabla configuraciones_casilla')
        print('No hay correo configurado en la tabla configuraciones_casilla')
        exit()
    cursor.execute("SELECT id_usuario, api_key, id_tenant, id FROM dbo.configuraciones_configuracion ORDER BY id DESC")
    try:
        row = cursor.fetchone()
        id_usuario = row[0]
        api_key = row[1]
        id_tenant = row[2]
        id_conf = row[3]
    except:
        logging.info('No hay configuracion en la tabla configuraciones_configuracion')
        print('No hay configuracion en la tabla configuraciones_configuracion')
        exit()

    credentials = (id_usuario, api_key)

    account = Account(credentials, auth_flow_type='credentials', tenant_id=id_tenant)

    if account.authenticate(scopes=scope):
        mailbox = account.mailbox(correo)
        messages = mailbox.get_messages(limit=1, query='isRead eq false')
        for message in messages:
            #obtener el usuario que tenga el campo updated_at mas antiguos
            cursor.execute("SELECT Q2.id, Q2.email, Q1.id AS id_ejecutivo FROM dbo.correos_ejecutivo AS Q1 INNER JOIN dbo.usuarios_usuario AS Q2 ON Q1.usuario_id = Q2.id ORDER BY Q1.updated_at ASC")
            try:
                row = cursor.fetchone()
                id = row[0]
                ejecutivo = row[1]
                id_ejecutivo = row[2]
            except:
                logging.info('No hay ejecutivos asociados')
                print('No hay ejecutivos asociados')
                break
            cursor.execute(f"UPDATE dbo.correos_ejecutivo SET updated_at = GETDATE() WHERE id = {id_ejecutivo}")
            to_forward = message.forward()
            to_forward.to.add(ejecutivo)
            to_forward.body = f'Enviado por: {message.sender}\n\n\n'
            to_forward.send()
            logging.info(f"Se deriva correo a ejecutivo: {ejecutivo} -> titulo {message.subject}")
            #clear all variables when have ' and replace for ""
            subject = message.subject
            subject = subject.replace("'", "")
            body = message.body
            body = body.replace("'", "")
            print(f"Se deriva correo a ejecutivo: {ejecutivo}")
            #update the updated_at field
            cursor.execute(f"INSERT INTO dbo.correos_correo (subject,body,desde,created_at,updated_at,configuracion_id,estado_id,ejecutivo_id) VALUES ('{subject}','{body}','{message.sender}',GETDATE(),GETDATE(),{id_conf},2,{id})")
            cursor.commit()
    else:
        logging.error('Fallo en la autenticacion, favor validar expiracion de credenciales')
        print('Fallo en la autenticacion, favor validar expiracion de credenciales')

while True:
    try:
        #connect to mssql express
        conn_str = (
            r"Driver={ODBC Driver 17 for SQL Server};"
            rf"Server={config('DBSERVER')};"
            rf"Database={config('DATABASE')};"
            rf"UID={config('DBUSER')};"
            rf"PWD={config('DBPASS')};"
        )
        # connect to db
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        main(cursor)
        time.sleep(5)
    except KeyboardInterrupt:
        logging.info('Servicio de correo finalizado')
        print('Servicio de correo finalizado')
        break
    except Exception as e:
        logging.error(f"Ocurrio un error: {e}")
        print(f"Ocurrio un error: {e}")
        time.sleep(5)
    finally:
        cursor.close()
        conn.close()

