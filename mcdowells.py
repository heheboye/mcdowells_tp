from openpyxl import Workbook, load_workbook
import colorama
import time
import os

colorama.init()

WHITE = "\x1b[1;37;40m"
RED = "\x1b[1;31;222m"

custom_date = time.strftime("%d %m %Y")
raw_date = time.asctime()
headers = [["Cliente", "Fecha", "Combo S", "Combo D", "Combo T", "Flurby", "Total"]]
rows = []
total_sales = []

# Current directory.
cd = os.path.dirname(os.path.abspath(__file__))

# Txt directory.
txt_path = os.path.join(cd, "Txt")

# Excel directory.
excel_path = os.path.join(cd, "Excel")

### FUNCTIONS ###

def clear_console():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def verify(user_input):
    while user_input.isalpha() == False or user_input == "":
        clear_console()
        print(f"""\n{WHITE}El campo no puede estar vacio y solo se aceptan letras.
Intente nuevamente: """, end = "")
        user_input = input(f"{RED}")
    clear_console()
    return user_input.capitalize()

def int_convert(user_input):
    while user_input.isdecimal() == False or user_input == "":
        clear_console()
        print(f"""\n{WHITE}El campo no puede estar vacio y solo se aceptan numeros enteros.
Intente nuevamente: """, end = "")
        user_input = input(f"{RED}")
    user_input = int(user_input)
    clear_console()
    return user_input

def emp_in(emp):
    if os.path.exists(f"Txt/Registro {custom_date}.txt"):
        f = open(f"Txt/Registro {custom_date}.txt", "a")
        f.write(f"IN {raw_date} Encargad@ {emp}\n")
        f.close()
    else:
        try:
            os.mkdir(txt_path)
        except FileExistsError:
            f = open(f"Txt/Registro {custom_date}.txt", "a")
            f.write(f"IN {raw_date} Encargad@ {emp}\n")
            f.close()
    
def emp_out(emp):
    if os.path.exists(f"Txt/Registro {custom_date}.txt"):
        f = open(f"Txt/Registro {custom_date}.txt", "a")
        f.write(f"OUT {raw_date} Encargad@ {emp} ${sum(total_sales)}\n")
        f.write("#"*50+"\n")
        f.close()
    else:
        try:
            os.mkdir(txt_path)
        except FileExistsError:
            f = open(f"Txt/Registro {custom_date}.txt", "a")
            f.write(f"OUT {raw_date} Encargad@ {emp} ${sum(total_sales)}\n")
            f.write("#"*50+"\n")
            f.close()

def reg_sale():
    if os.path.exists(f"Excel/Registro {time.strftime('%d %m %Y')}.xlsx"):
        wb = load_workbook(filename = f"Excel/Registro {time.strftime('%d %m %Y')}.xlsx")
        ws = wb.active
        for row in rows:
            ws.append(row)
        wb.save(f"Excel/Registro {time.strftime('%d %m %Y')}.xlsx")
    else:
        wb = Workbook()
        ws = wb.active
        for head in headers:
            ws.append(head)
        for row in rows:
            ws.append(row)
        try:
            os.mkdir(excel_path)
        except FileExistsError:
            wb.save(f"Excel/Registro {time.strftime('%d %m %Y')}.xlsx")

### PRIMER MENU ###

print(f"\n{WHITE}Bienvenido a McDowell's\n", end = "")
print("\nIngrese su nombre encargad@: ", end = "")
encargado = input(f"{RED}")
encargado = verify(encargado)
emp_in(encargado)

###################

while True:
    print(f"""{WHITE}
McDowell's
Recuerda que siempre hay que recibir al cliente con una sonrisa :)

1 ??? Ingreso de nuevo pedido
2 ??? Cambio de turno
3 ??? Apagar sistema

""", end = "")
    option = input(">>> ")
    option = int_convert(option)
    clear_console()
    if option == 1:
        clear_console()
        print(f"{WHITE}Nombre del cliente: ", end = "")
        customer = input(f"{RED}")
        customer = verify(customer)
        print(f"{WHITE}Ingrese cantidad Combo S: ", end = "")
        can_cs = input(f"{RED}")
        can_cs = int_convert(can_cs)
        print(f"{WHITE}Ingrese cantidad Combo D: ", end = "")
        can_cd = input(f"{RED}")
        can_cd = int_convert(can_cd)
        print(f"{WHITE}Ingrese cantidad Combo T: ", end = "")
        can_ct = input(f"{RED}")
        can_ct = int_convert(can_ct)
        print(f"{WHITE}Ingrese cantidad Flurby: ", end = "")
        can_p = input(f"{RED}")
        can_p = int_convert(can_p)
        total = (can_cs * 650) + (can_cd * 700) + (can_ct * 800) + (can_p * 250)
        print(f"\n{WHITE}Total $ {total}")
        print(f"Abona con $ ", end = "")
        pago = input(f"{RED}")
        pago = int_convert(pago)
        if (pago - total) < 0:
            print(f"{RED}{customer}{WHITE} se olvid?? la billetera. Transacci??n cancelada.")
            time.sleep(3)
            clear_console()
            continue
        else:
            print(f"{WHITE}El vuelto de {RED}{customer}{WHITE} es de $ {RED}{pago - total}")
            time.sleep(3)
            clear_console()
            total_sales.append(total)
            rows.append([customer, raw_date, can_cs, can_cd, can_ct, can_p, total])
            reg_sale()
            rows = []
    if option == 2:
        emp_out(encargado)
        total_sales = []
        print(f"\n{WHITE}Bienvenido a McDowell's\n", end = "")
        print("\nIngrese su nombre encargad@: ", end = "")
        encargado = input(f"{RED}")
        encargado = verify(encargado)
        emp_in(encargado)
        clear_console()
    if option == 3:
        emp_out(encargado)
        print("\nGuargado informacion del encargado anterior...")
        time.sleep(3)
        clear_console()
        print("\nPrograma cerrado exitosamente.", end = "")
        break
