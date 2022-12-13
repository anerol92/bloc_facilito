from tkinter import filedialog, ttk
from tkinter.messagebox import askyesno, showinfo
from consts import *
import tkinter as tk 
from io import open
from os import remove

dir = '' #ruta del fichero
typefont = '' #tipo de fuente
size = 0 #tamaño de fuente 

class bloc(tk.Frame):

    def __init__(self, window):           
        self.create_elements()   #crea los elementos del programa

    def create_elements(self):
        self.create_window()  #crea la ventana principal             
        self.create_textbox() #crea el campo de texto
        self.create_menu()  #crea el menu superior
        self.create_font()  #cambia las propiedades de la fuente (tamaño, fuente)                  

    def create_window(self):
        self.wind = window
        self.wind.title('Bloc de notas')  
        self.wind.configure(bg='white')
        self.wind.attributes('-topmost', True) #posiciona la ventana del programa por encima de todas
        self.wind.iconbitmap(ICONO)
    
    def create_menu(self):
        menubar = tk.Menu(self.wind)
        archivo = tk.Menu(menubar, tearoff=0)
        archivo.add_command(label='Nuevo     ', command=callback_new)
        archivo.add_command(label='Abrir     ', command=callback_open)
        archivo.add_command(label='Guardar     ', command=callback_save)
        archivo.add_command(label='Guardar como     ', command=callback_save_as)
        archivo.add_separator()
        archivo.add_command(label='Eliminar     ', command=callback_delete)
        menubar.add_cascade(label='Archivo', menu=archivo)      

        colores = tk.Menu(menubar, tearoff=0)
        global color_palette
        color_palette = tk.IntVar()        
        colores.add_radiobutton(
            label='Blue Sky',
            variable=color_palette,
            value=1,
            command=paleta_colores
        )
        colores.add_radiobutton(
            label='Brown Space',
            variable=color_palette,
            value=2,
            command=paleta_colores
        ) 
        colores.add_radiobutton(
            label='Dark Blue',
            variable=color_palette,
            value=3,
            command=paleta_colores
        )    
        colores.add_radiobutton(
            label='purple Cool',
            variable=color_palette,
            value=4,
            command=paleta_colores
        )  
        colores.add_radiobutton(
            label='Default value',
            variable=color_palette,
            value=5,
            command=paleta_colores
        )

        menubar.add_cascade(label='Apariencia', menu=colores)        
        self.wind.config(menu=menubar)    

    def create_textbox(self):        
        scroll = tk.Scrollbar(self.wind)
        global text
        text = tk.Text(self.wind, padx=15, pady=50, height=HEIGHT, width=WIDTH)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        text.pack(side=tk.LEFT, fill=tk.Y) 
        scroll.config(command=text.yview)
        text.config(yscrollcommand=scroll.set)     

    def create_font(self):
        self.font = tk.Label(text = 'Fuente: ').place(x = 5, y = 5)   
        global comboFont      
        comboFont = ttk.Combobox(state='readonly',
        values=[
                'System', 
                'Terminal',
                'Fixedsys',
                'Modern',
                'Roman',
                'Script',
                'Courier',
                'MS Serif',
                'MS Sans Serif',
                'Small Fonts',
                'Marlett',
                'Arial',
                'Arabic Transparent',
                'Arial Baltic'
                'Arial Black',
                'Bahnschrift Light',
                'Bahnschrift SemiLight',
                'Bahnschrift',
                'Bahnschrift SemiBold',
                'Bahnschrift Light SemiCondensed',
                'Bahnschrift SemiLight SemiConde',
                'Bahnschrift SemiCondensed',
                'Bahnschrift SemiBold SemiConden',
                'Bahnschrift Light Condensed',
                'Bahnschrift SemiLight Condensed',
                'Bahnschrift Condensed',
                'Bahnschrift SemiBold Condensed',
                'Calibri',
                'Calibri Light',
                'Cambria',
                'Cambria Math',
                'Candara',
                'Candara Light',
                'Comic Sans MS',
                'Consolas',
                'Constantia',
                'Corbel',
                'Corbel Light',
                'Courier New',
                'Courier New Baltic'
                ])
        comboFont.place(x=55, y=5)
        comboFont.current(0)        
            
        self.size = tk.Label(text = 'Tamaño: ').place(x=225, y=5)
        global comboSize
        comboSize = ttk.Combobox(state='readonly',
        values=['16','18','20','22','24','26','28','30'])
        comboSize.place(x=295, y=5)
        comboSize.current(0)           
        btnSelect = tk.Button(self.wind, command=select_font,text='Seleccionar').place(x=450, y=5)
       

#CALLBACKS        
def callback_new(): #crear un nuevo archivo
    global dir
    dir = ''
    text.delete(1.0,tk.END)

def callback_open(): #abrir un archivo ya existente 
    global dir
    dir = filedialog.askopenfile(initialdir='.', filetype=(('Archivo de texto','*.txt'),),
    title='Abrir archivo de texto')   
    if dir != '':
        file = open(dir.name, 'r')
        content = file.read()        
        text.delete(1.0, tk.END)
        text.insert('insert', content)       
        file.close()      

def callback_save(): #guardar un archivo nuevo o los cambios del mismo
    if dir != '':
        content = text.get(1.0, 'end-1c') #1c quitar el salto de línea
        file = open(dir.name, 'w+')
        file.write(content)
        file.close()
    else:
        callback_save_as()

def callback_save_as(): #guardar como... crea una copia del archivo principal
    global dir
    file = filedialog.asksaveasfile(title='Guardar archivo', mode='w', defaultextension='.txt')
    if file != None:
        dir = file.name        
        content = text.get(1.0, 'end-1c') #1c quitar el salto de línea
        file = open(dir, 'w+')
        file.write(content)
        file.close()
    else:
        dir = ''

def callback_delete(): #elimina el archivo de texto que tenemos abierto
    respuesta = askyesno("Eliminar archivo",
            "¿Seguro que quiere elimiar el archivo?")
    if respuesta == "no":
       showinfo(title="Cancelado",
                message="El archivo no fue eliminado.")
    else:
        global dir
        if dir != None:
            dir = dir.name        
            remove(dir)
            text.delete(1.0,tk.END)
            dir = ''
        else:
            dir = ''

        showinfo(title="Eliminado",
                      message="El archivo ha sido eliminado.")

def paleta_colores(): 
    valor_tema = color_palette.get()
    if valor_tema == 1:        
        text['bg'] = '#D9EAFF'
        text['foreground'] = '#000'
    elif valor_tema == 2:        
        text['bg'] = '#818274'
        text['foreground'] = '#fff'
    elif valor_tema == 3:        
        text['bg'] = '#3A5299'
        text['foreground'] = '#fff'
    elif valor_tema == 4:        
        text['bg'] = '#593E9E'
        text['foreground'] = '#fff'
    elif valor_tema == 5:        
        text['bg'] = '#fff'
        text['foreground'] = '#000'
    else:
        text['bg'] = '#fff'
        text['foreground'] = '#000'

def select_font():
    global typefont
    typefont = comboFont.get()     
    global size
    size = comboSize.get()
    text.configure(font=(typefont,size))

if __name__ == '__main__':
    window = tk.Tk()
    application = bloc(window) 
    window.mainloop()
