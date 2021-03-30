import random
import string
import time
import sqlite3


def connection():
    con = sqlite3.connect('PassManager.db')
    return con

def add_pass(Service,password,mail,cur):
    cur.execute("INSERT INTO Manager (Service,Mail,Password) VALUES (?,?,?)",(Service,mail,password))

def create_password(c,y):
    password =""
    for i in range(y):
        password += random.choice(c)
    return password

def crear_tabla(cur):
    cur.execute("CREATE TABLE IF NOT EXISTS Manager (Service text, Mail text, Password text)")

def generar_contra():

    while True:
        print("*"*20)
        print("Que tipo de contraseña queres?")
        print("h: hexdigit(letras y numeros)")
        print("d: digits(numeros)")
        print("p: printable(letras, numeros y signos de puntuacion)")
        print("*"*20)

        res=input("-")

        if res == "h":
            characters=string.hexdigits
            break
        elif res == "d":
            characters=string.digits
            break
        elif res == "p":
            characters=string.printable[:-6]
            break
        else:
            print("Pone bien la respuesta gordo!!")
            continue

    print("Cuantos caracteres debe tener tu contraseña?")
    index = int(input("-"))

    new_password = create_password(characters,index)
    return new_password


def cuestionario_guardado(cur):
    print("Para que servicio queres gurdarla?")
    print("*"*20)
    service = str(input("-"))

    while True:
        print("Que mail vas a usar?")
        mail = str(input("-"))
        print(mail)
        if mail.find("@") != -1 and mail.find(".") != -1:
            break
        else:
            print("Pone un mail valido Example: prueba@prueba.com")
            continue

    print("Cual es la contraseña?")
    print("*"*20)
    password = str(input("-"))

    add_pass(service,password,mail,cur)

def mostrar_tabla(cur):
    table_names=""
    for row in cur.execute("SELECT name FROM PRAGMA_TABLE_INFO('Manager')"):
        table_names += str(row).replace("'","")
    print(table_names.replace(",",""))
    print("*"*50)
    for row in cur.execute('SELECT * FROM Manager'):
        print(str(row).replace(",",""))

def delete_pass(cur,service):
    cur.execute(f"DELETE FROM Manager where Service ='{service}'")


try:
    con = connection()
    cur = con.cursor()
    crear_tabla(cur)
    while True:

        print("*"*20)
        print("Que queres hacer?")
        print("1: Generar contraseña")
        print("2: Guardar contraseña")
        print("3: Ver contraseña")
        print("4: Borrar contraseña")
        print("e: exit")
        print("*"*20)
        r = input("-")

        if r == "1":
            new_pass=generar_contra()
            print(f"Tu contraseña es: {new_pass}")
            time.sleep(2)
        elif r=="2":
            cuestionario_guardado(cur)
        elif r=="3":
            mostrar_tabla(cur)
            time.sleep(2)
        elif r=="4":
            print("Que servicio desea eliminar?")
            service=input("-")
            delete_pass(cur,service)
        elif r=="e":
            break
        else:
            print("Pone bien la respuesta")
            continue

        con.commit()

    cur.close()
    con.close()
except KeyboardInterrupt:
    print("Se rompio")


