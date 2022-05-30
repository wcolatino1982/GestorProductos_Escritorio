from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import sqlite3
from funciones import centrar_ventana_product, centrar_ventana_edit
import platform

# ---------------------------------
# Idenfificando el sistema operacional
sistema = platform.system()
if sistema == 'Darwin':
    logoimg = 'recursos/tienda.icns'
elif sistema == 'Windows':
    logoimg = 'recursos/tienda.ico'
else:
    logoimg = 'recursos/tienda.png'


# ---------------------------------

class Product:
    db = 'database/productos.db'

    def __init__(self, root):
        self.window = root
        self.window.title('App Gestor de Productos')
        self.window.resizable(1, 1)  # para no redimensionar(0,0)
        self.window.wm_iconbitmap(logoimg)
        # Centrar ventana
        centrar_ventana_product(root)
        # Frame Principal
        frame = LabelFrame(self.window, text="Registrar un nuevo producto", labelanchor='n')
        frame.grid(row=0, column=0, columnspan=4, padx=20, pady=20)

        # Etiqueta nombre
        self.label_name = Label(frame, text="Nombre: ")
        self.label_name.focus()
        self.label_name.grid(row=1, column=0)
        # Campo nombre
        self.input_name = Entry(frame)
        self.input_name.grid(row=1, column=1)
        # Etiqueta Precio
        self.label_price = Label(frame, text='Precio: ')
        self.label_price.grid(row=1, column=2)
        # Campo Precio
        validatecommand = root.register(self.valida_formato)  # vinculado a la funcion valida_formato()
        self.input_price = Entry(frame, validate='key', validatecommand=(validatecommand, "%S"))
        self.input_price.grid(row=1, column=3)
        # Etiqueta Categoria
        self.label_category = Label(frame, text='Categoria: ')
        self.label_category.grid(row=2, column=0)
        # Campo Categoria
        self.input_category = Entry(frame)
        self.input_category.grid(row=2, column=1)
        # Etiqueta Estoque
        self.label_stock = Label(frame, text='Estoque: ')
        self.label_stock.grid(row=2, column=2)
        # Campo Estoque
        validatecommand = root.register(self.valida_formato)
        self.input_stock = Entry(frame, validate='key', validatecommand=(validatecommand, "%S"))
        self.input_stock.grid(row=2, column=3)
        # Boton Guardar
        self.button_save = Button(frame, text='Guardar Producto', command=self.add_product)
        self.button_save.bind("<Return>", self.add_product)  # acciona el boton al precionar enter após seleccionado
        self.button_save.grid(row=3, column=0, columnspan=4, sticky='we')
        # Mensaje Informativo al usuario
        self.message = Label(text='', anchor='center')
        self.message.grid(row=4, column=0, columnspan=4, sticky='we')

        # TABLA DE PRODCUTOS (Treeview)
        # Estilo propio
        s = ttk.Style()
        s.configure('my.Treeview', highlightthickness=0, bd=0, font=('Calibri', 11))  # fuente de la tabla
        s.configure('my.Treeview.Heading', font=('Calibri', 13, 'bold'))  # fuente de las cabeceras
        s.layout('my.Treeview', [('my.Treeview.treearea', {'sticky': 'nswe'})])  # eliminase los bordes
        # Estrutura de la tabla
        self.tabla = ttk.Treeview(height=20, columns=('#0', '#1', '#2'), style='my.Treeview')
        self.tabla.grid(row=5, column=0, columnspan=4)
        self.tabla.heading('#0', text='NOMBRE   ⚙', anchor='center')
        self.tabla.heading('#1', text='PRECIO', anchor='center')
        self.tabla.heading('#2', text='CATEG   ⚙', anchor='center')
        self.tabla.heading('#3', text='CANT', anchor='center')
        self.tabla.column('#1', anchor='center')
        self.tabla.column('#3', anchor='center')
        # Boton Editar
        self.button_edit = ttk.Button(text='Editar', command=self.edit_product)
        self.button_edit.bind("<Return>", self.edit_product)
        self.button_edit.grid(row=6, column=0, columnspan=2, sticky='we')
        # Boton Eliminar
        self.button_erase = ttk.Button(text='Eliminar', command=self.del_product)
        self.button_erase.bind("<Return>", self.del_product)
        self.button_erase.grid(row=6, column=2, columnspan=2, sticky='we')
        # Barra de desplazamiento
        barra = Scrollbar(self.window, orient='vertical', command=self.tabla.yview)
        barra.grid(column=4, row=5, sticky='ns')
        self.tabla.configure(yscrollcommand=barra.set)

        self.get_products()

    # ----------- FUNCIONES -----------------------------
    # Consulta Banco de Datos
    def db_consulta(self, query, parametros=()):
        with sqlite3.connect(self.db) as con:  # inicia conexion con la base de datos
            cur = con.cursor()
            result = cur.execute(query, parametros)  # preparamos la consulta
            con.commit()  # ejecuta la consulta
        return result

    def get_products(self):
        # limpiar los datos de la tabla al iniciar
        regTable = self.tabla.get_children()
        for r in regTable:
            self.tabla.delete(r)
        # Escribir los datos en pantalla
        query = 'SELECT * FROM producto ORDER BY id ASC'
        register = self.db_consulta(query)
        for r in register:
            print(r)  # para Debug
            self.tabla.insert("", 0, text=r[1], values=(r[2], r[3], r[4]))

    def add_product(self, event=None):
        if (self.valida_nombre() and self.valida_precio() and
                self.valida_categoria() and self.valida_estoque()):
            # prepara la consulta y coleta los datos
            query = 'INSERT INTO producto VALUES(NULL, ?, ?, ?, ?)'
            parametros = (self.input_name.get().upper(), self.input_price.get(),
                          self.input_category.get().upper(), self.input_stock.get())
            self.db_consulta(query, parametros)  # inserta los datos
            self.msg('PRODUCTO AÑADIDO CON ÉXITO', 'acqua')
            self.input_name.delete(0, END)  # borra el campo del formulario
            self.input_price.delete(0, END)
            self.input_category.delete(0, END)
            self.input_stock.delete(0, END)
        elif (not self.valida_nombre() or not self.valida_precio()
              or not self.valida_categoria() or not self.valida_estoque()):
            self.msg('¡TODOS LOS CAMPOS SON OBLIGATORIOS!', 'amarillo')
        self.get_products()

    def del_product(self):
        # Comprobar se el item esta seleccionado
        self.msg("")  # self.message['text'] = " "
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
            nombre_item = self.tabla.item(self.tabla.selection())['text']
        except IndexError:
            self.msg('SELECCIONE UN PRODUCTO', 'amarillo')
            return
        r = messagebox.askretrycancel(message='¿Realmente Desea Borrar %s?' % (nombre_item), title='DELETAR')
        self.msg("")
        if r == True:
            query = 'DELETE FROM producto WHERE nombre == ?'
            self.db_consulta(query, (nombre_item,))
            self.msg('PRODUCTO ELIMINADO CON ÉXITO', 'acqua')
            self.get_products()  # actualiza la tabla de productos
        else:
            self.msg('PRODUCTO NO HA SIDO ELIMINADO', 'rojo')
        '''# debug
        print(self.tabla.item(self.tabla.selection())['text'])
        print(self.tabla.item(self.tabla.selection())['values'])
        print(self.tabla.item(self.tabla.selection())['values'][0])'''

    def edit_product(self):
        self.msg('')
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError:
            self.msg('SELECCIONE UN PRODUCTO', 'amarillo')
            return

        old_name = self.tabla.item(self.tabla.selection())['text']
        old_price = self.tabla.item(self.tabla.selection())['values'][0]
        old_category = self.tabla.item(self.tabla.selection())['values'][1]
        old_stock = self.tabla.item(self.tabla.selection())['values'][2]

        # Ventana Editar
        self.window_edit = Toplevel()  # se pone por delante de las demás
        self.window_edit.title("Editar Producto")
        self.window_edit.resizable(1, 1)
        self.window_edit.wm_iconbitmap(logoimg)
        # Centrar ventana Editar
        root.iconify()
        centrar_ventana_edit(self.window_edit)

        title = Label(self.window_edit, text='Edición de Productos', font=('Calibri', 30, 'bold'))
        title.grid(row=0, column=0, columnspan=20)
        # Contenedor Frame principal de Editar
        frame_ep = LabelFrame(self.window_edit, text='Editar el siguiente Producto', labelanchor=N)
        frame_ep.grid(row=1, column=0, columnspan=20, padx=20, pady=20)
        # Label nombre antiguo
        self.show_old_name = Label(frame_ep, textvariable=StringVar(self.window_edit, value=old_name))
        self.show_old_name.grid(row=2, column=0)
        # Campo nombre nuevo
        self.input_new_name = Entry(frame_ep)
        self.input_new_name.grid(row=3, column=0)
        # Label precio antiguo
        self.show_old_price = Label(frame_ep, textvariable=StringVar(self.window_edit, value=('€ ', old_price)))
        self.show_old_price.grid(row=2, column=1)
        # print(dict(self.show_old_price))
        # Campo precio nuevo
        validatecommand = root.register(self.valida_formato)
        self.input_new_price = Entry(frame_ep, validate='key', validatecommand=(validatecommand, "%S"))
        self.input_new_price.grid(row=3, column=1)
        # Label Categoria antigua
        self.show_old_category = Label(frame_ep, textvariable=StringVar(self.window_edit, value=(old_category)))
        self.show_old_category.grid(row=4, column=0)
        # Campo nueva categoria
        self.input_new_category = Entry(frame_ep)
        self.input_new_category.grid(row=5, column=0)
        # Label Estoque antiguo
        self.show_old_stock = Label(frame_ep, textvariable=StringVar(self.window_edit, value=('Cantidad: ', old_stock)))
        self.show_old_stock.grid(row=4, column=1)
        # Campo nuevo estoque
        validatecommand = root.register(self.valida_formato)
        self.input_new_stock = Entry(frame_ep, validate='key', validatecommand=(validatecommand, "%S"))
        self.input_new_stock.grid(row=5, column=1)
        # Boton Actualizar
        self.button_update = ttk.Button(frame_ep, text='Actualizar Producto', command=lambda:
        self.update_product(self.input_new_name.get().upper(), old_name,
                            self.input_new_price.get(), old_price,
                            self.input_new_category.get().upper(), old_category,
                            self.input_new_stock.get(), old_stock))
        self.button_update.grid(row=6, columnspan=4, sticky='we')

    def update_product(self, new_name, old_name, new_price, old_price,
                       new_category, old_category, new_stock, old_stock):
        producto_modificado = False
        query = 'UPDATE producto SET nombre=?, precio=?, categoria=?, estoque=?' \
                'WHERE nombre=? AND precio=? AND categoria=? AND estoque=?'
        lista1 = [new_name, new_price, new_category, new_stock]
        lista2 = [old_name, old_price, old_category, old_stock]
        p1 = []  # parametros 1
        var = 0
        for i in lista1:
            if i != '':
                p1.append(i)
            else:
                p1.append(lista2[var])
            var += 1
        parametros = (p1[0], p1[1], p1[2], p1[3], old_name, old_price, old_category, old_stock)
        # Se un campo new_ está vacio, recibe lo mismo que el campo old_
        # se todos los campos new_ estan vacios, es decir, son iguales a old_ el producto no se modifica
        if p1 != lista2:
            producto_modificado = True

        if producto_modificado == True:
            self.db_consulta(query, parametros)
            self.window_edit.destroy()  # cerra la ventana de edición
            root.deiconify()
            self.msg('EL PRODUCTO HA SIDO ACTUALIZADO CON ÉXITO', 'acqua')
            self.get_products()
        else:
            root.deiconify()
            self.window_edit.destroy()
            self.msg('EL PRODUCTO NO HA SIDO ACTUALIZADO', 'rojo')

    # ------- VALIDACIONES ---------------------------------
    def valida_nombre(self):
        nombre_introducido = self.input_name.get()
        return len(nombre_introducido) != 0

    def valida_precio(self):
        precio_introducido = self.input_price.get()
        return len(precio_introducido) != 0

    def valida_categoria(self):
        categoria_introducido = self.input_category.get()
        return len(categoria_introducido) != 0

    def valida_estoque(self):
        estoque_introducido = self.input_stock.get()
        return len(estoque_introducido) != 0

    def valida_formato(self, num):  # valida formatos de input para precio e estoque
        return num in '0123456789.'

    # -------- DEFINICIONES --------------------------
    def msg(self, message, color=None):
        define = {
            'acqua': '#7FFFD4',
            'amarillo': '#FFFF33',
            'rojo': '#EF5350'
        }
        if color in define:
            bg = define[color]
        else:
            bg = None
        self.message['text'] = message
        self.message['bg'] = bg


# ----------------------------------
if __name__ == '__main__':
    root = Tk()  # instancia de la ventana principal
    root.update()  # actualiza el root para centrar la ventana
    app = Product(root)  # se envia a la clase producto el control de la ventana root

    root.mainloop()  # mantener abierta la ventana