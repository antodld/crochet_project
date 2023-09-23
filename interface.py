import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter
from cadrillage import draw_fig
import numpy as np
from scipy.signal import convolve2d

# Fonction pour charger une image
def get_image_path():
    global image_label, img
    file_path = filedialog.askopenfilename()
    return file_path

# Fonction pour changer la couleur d'une case
def change_color(event):
    x, y = event.x, event.y
    col = x // cell_width
    row = y // cell_height
    color = askcolor()[1]  # Demande à l'utilisateur de choisir une couleur
    canvas.itemconfig(cells[row][col], fill=color)

# Fonction pour convertir une couleur hexadécimale en RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(color):
    return '#{:02x}{:02x}{:02x}'.format(color[0],color[1],color[2])

# Fonction pour exporter la matrice en RGB
def export_matrix():
    rgb_matrix = [[hex_to_rgb(canvas.itemcget(cell, "fill")) for cell in row] for row in cells[::-1]]
    draw_fig(np.array(rgb_matrix)/255)

# Fonction pour faire pivoter le quadrillage de 90 degrés
def rotate_grid():
    global rows, cols, cells
    new_cells = [[None for _ in range(rows)] for _ in range(cols)]

    for i in range(rows):
        for j in range(cols):
            new_cells[j][rows - 1 - i] = cells[i][j]
            x1, y1, x2, y2 = canvas.coords(cells[i][j])
            canvas.coords(cells[i][j], y1, 400 - x2, y2, 400 - x1)

    cells = new_cells
    rows, cols = cols, rows

def convert_to_low_resolution(input_path, new_width, new_height):
    # Apply a filter to locally average pixel values (3x3 kernel in this example)
    kernel = np.ones((2,2)) / (2**2)  # Normalization for a 3x3 kernel
    try:
        # Open the input image
        img = Image.open(input_path)
        img_mat= np.array(img)
        
        averaged_matrix = np.zeros((img_mat.shape[0],img_mat.shape[1],3))

        # Apply the filter
        for _ in range(0):
            for channel in range(averaged_matrix.shape[2]):
                averaged_matrix[:, :, channel] = convolve2d(img_mat[:, :, channel], kernel, mode = "same" ,boundary='fill')
        
        # img = Image.fromarray(averaged_matrix.astype('uint8'))



        # Resize the image
        low_res_img = img.resize((new_width, new_height), Image.NEAREST)
        
        for _ in range(1):
            low_res_img = low_res_img.filter(ImageFilter.SHARPEN)

        # Convert the low-resolution image to a numpy matrix
        low_res_matrix = np.array(low_res_img)

        return low_res_img
    
    except Exception as e:
        print("An error occurred:", e)

input_image_path = "bob.png"
input_image_path = get_image_path()


maille_size = 0.5 # taille d'une maille mm
granny_square_size = 15 #cm

img = convert_to_low_resolution(input_image_path,int(granny_square_size /maille_size),int(granny_square_size / maille_size))

img_mat = np.array(img)
img_mat = np.array([[ [ img_mat[i,j,k] for k in range(3) ] for j in range(img_mat.shape[1])] for i in range(img_mat.shape[0]) ])


# Crée une fenêtre principale
root = tk.Tk()
root.title("Quadrillage de Couleurs Modifiable avec Export et Rotation")

# Dimensions du quadrillage
rows = img_mat.shape[0]
cols = img_mat.shape[1]

# Crée un canevas pour afficher le quadrillage
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Calcule la largeur et la hauteur des cellules du quadrillage
cell_width = 400 // cols
cell_height = 400 // rows

# Initialise une liste pour stocker les ID des rectangles (cellules)
cells = []

# Dessine le quadrillage initial de couleurs
for i in range(rows):
    row = []
    for j in range(cols):
        x1 = j * cell_width
        y1 = i * cell_height
        x2 = x1 + cell_width
        y2 = y1 + cell_height
        rect = canvas.create_rectangle(x1, y1, x2, y2, fill=rgb_to_hex(img_mat[i,j]))
        row.append(rect)
    cells.append(row)

# Lie un événement de clic à chaque case pour permettre la modification de la couleur
for i in range(rows):
    for j in range(cols):
        canvas.tag_bind(cells[i][j], '<Button-1>', change_color)

# Ajoute un bouton "Export" pour obtenir la matrice en RGB
export_button = tk.Button(root, text="Export", command=export_matrix)
export_button.pack()

# Ajoute un bouton "Rotate" pour tourner le quadrillage de 90 degrés
rotate_button = tk.Button(root, text="Rotate", command=rotate_grid)
rotate_button.pack()

# Lance la boucle principale de l'interface graphique
root.mainloop()
