# affichage d'un répertoire dans une fenêtre tkinter
# jcy 12.08.26 + 
# pour exemple SI-C3b

import tkinter as tk
from tkinter import ttk # pour le treeview
from tkinter import filedialog # boite dialogue pour chercher un répertoire
from pathlib import Path # fonctions de répertoire
from tkinter import *
from datetime import datetime

node_paths = {} #garder les chemins complets

# afficher des détails sur un fihcier
def display_file_info(event):
    selected_nodes = tree.selection() #fichier sélectionné
    if not selected_nodes:
        return

    file_path = node_paths[selected_nodes[0]]
    if not file_path.is_file():
        return

    file_info = file_path.stat()
    print("Fichier:", file_path)
    print("Taille:", file_info.st_size, "octets")
    print("Date:", datetime.fromtimestamp(file_info.st_mtime))
    print("Type:", file_path.suffix or "sans extension")

# afficher un répertoire
def display_directory():
    tree.delete(*tree.get_children()) # vider le treeview
    node_paths.clear()
    selected_dir = filedialog.askdirectory()
    if not selected_dir:
        return
    root_folder = Path(selected_dir) # demander un répertoire

    # insérer le noeud racine (déjà ouvert)
    root_node = tree.insert("","end", text=f"📁 {root_folder.resolve()}",open=True )
    # garder l'info du chemin complet
    node_paths[root_node] = root_folder

    # appeler la recherche des noeuds enfants
    populate_tree(tree, root_node, root_folder)

    # afficher le tableau des node
    for node, path in node_paths.items():
        print(node, ":", path)

# recherche des noeuds enfants (récursif)
def populate_tree(tree, parent, folder):
    # pour tous les noeuds enfants du folder
    try:
        items = list(folder.iterdir())
    except PermissionError:
        return

    for item in items:
        item_name = f"📁 {item.name}" if item.is_dir() else f"🗎 {item.name}"
        node = tree.insert(parent, "end", text=item_name)
        node_paths[node] = item # garder l'info du chemin complet
        if item.is_dir():
            # cas d'un répertoire, rappeler les enfants de l'enfant (peut être long)
            populate_tree(tree,node,item)


# Fenêtre principale appelée window
window = tk.Tk()
window.title("File Explorer YL")
window.geometry("700x500")
window.configure(bg="Red") # Fond rouge pour rendre les écarts de grille très visibles

# configuration de 2 colonnes dans window, la seconde plus large
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)
window.rowconfigure(0, weight=1) # une ligne (pour le treeview)

# création du menu principal
menu_bar = tk.Menu(window)
file_menu = tk.Menu(menu_bar, tearoff=False) # menu non détachable
file_menu.add_command(label="display directory", command=display_directory)
file_menu.add_separator()
file_menu.add_command(label="Ecrire Hello", command=lambda : print("hello"))
file_menu.add_command(label="Quit", command=window.destroy)
menu_bar.add_cascade(label="File", menu=file_menu) #ajouter File au menu

menu_bar.add_cascade(label="Tools")

menu_bar.add_cascade(label="Help")
window.config(menu=menu_bar)

# création d'une frame pour le treeview (avec bordure visible)
tree_frame = tk.Frame(
    window, 
    bg="lightgray", 
    highlightbackground="blue", 
    highlightthickness=3,
    relief="solid",
    bd=1
)
# padX et padY permettent de voir les limites de la grille grâce au fond rouge de 'window'
tree_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5) 
tree_frame.rowconfigure(0, weight=1) # ligne du treeview
tree_frame.columnconfigure(0, weight=1) # première colonne de la frame

file_information = tk.Frame(
    window,
    bg="purple",
    highlightbackground="Red",
    highlightthickness=3,
    bd=3
)

file_information.grid(column=1,sticky="nsew", padx=5, pady=5)
file_information.columnconfigure(2, weight=1)

project_area = tk.Frame(
    window,
    bg="purple",
    highlightbackground="Red",
    highlightthickness=3,
    bd=3
)

file_information.grid(column=1,sticky="nsew", padx=5, pady=5)
file_information.columnconfigure(2, weight=1)

# Style avec bordures explicites pour le Treeview
style = ttk.Style()
style.configure(
    "Treeview",
    font=("Arial", 14),
    rowheight=28,
    background="lightyellow", #couleur du fond
    foreground="Red", #couleur d'écriture
    relief="solid",
    bd=2
)

# création du treeview et placement
tree = ttk.Treeview(tree_frame)
tree.heading("#0", text="Directory Tree")
tree.grid(row=0, column=0, sticky="nswe", padx=3, pady=3) # placement avec marges

label_test=Label(file_information, text="File information").pack()


# Quand on sélectionne un fichier, on appelle display_file_info
tree.bind("<<TreeviewSelect>>", display_file_info) 

# Fonction d'inspection : force l'affichage d'une bordure sur TOUS les widgets
def debug_borders(parent, color="purple"):
    for widget in parent.winfo_children():
        try:
            widget.config(highlightbackground=color, highlightthickness=2)
        except tk.TclError:
            pass
        debug_borders(widget, color)

debug_borders(window)

# lancement du prog principal
window.mainloop()