from decouple import config
from O365 import Account
import pyodbc
import time

def main(cursor):
    #read the last mail not read from the user and only from,subject and body
    scope = ['https://graph.microsoft.com/.default']

    #obtain correo from dbo.configuraciones_casilla last row
    cursor.execute("SELECT email FROM dbo.configuraciones_casilla ORDER BY id DESC")
    try:
        row = cursor.fetchone()
        correo = row[0]
    except:
        print('No hay correo configurado en la tabla configuraciones_casilla')
        exit()

    cursor.execute("SELECT id_usuario, api_key, id_tenant FROM dbo.configuraciones_configuracion ORDER BY id DESC")
    try:
        row = cursor.fetchone()
        id_usuario = row[0]
        api_key = row[1]
        id_tenant = row[2]
    except:
        print('No hay configuracion en la tabla configuraciones_configuracion')
        exit()

    credentials = (id_usuario, api_key)

    account = Account(credentials, auth_flow_type='credentials', tenant_id=id_tenant)

    if account.authenticate(scopes=scope):
        # print('Authenticated!')
        mailbox = account.mailbox(correo)
        messages = mailbox.get_messages(limit=1, query='isRead eq false')
        for message in messages:
            #obtener el usuario que tenga el campo updated_at mas antiguos
            cursor.execute("SELECT Q1.id, Q2.email FROM dbo.correos_ejecutivo AS Q1 INNER JOIN dbo.usuarios_usuario AS Q2 ON Q1.usuario_id = Q2.id ORDER BY Q1.updated_at ASC")
            try:
                row = cursor.fetchone()
                id = row[0]
                ejecutivo = row[1]
                # print(ejecutivo)
            except:
                print('No ejecutivos asociados')
                exit()
            cursor.execute(f"UPDATE dbo.correos_ejecutivo SET updated_at = GETDATE() WHERE id = {id}")
            conn.commit()
            to_forward = message.forward()
            to_forward.to.add(ejecutivo)
            to_forward.body = f'Enviado por: {message.sender}\n\n\n'
            to_forward.send()
            #update the updated_at field
    else:
        print('Failed to authenticate!')


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

    except Exception as e:
        print(e)
        time.sleep(5)
    finally:
        cursor.close()
        conn.close()