# affichage d'un répertoire dans une fenêtre tkinter
# Yuri LIMA 12.08.26 
# SI-C3b

import tkinter as tk
from tkinter import ttk # pour le treeview
from tkinter import filedialog # boite dialogue pour chercher un répertoire
from pathlib import Path # fonctions de répertoire
from tkinter import *
from datetime import datetime
import os

node_paths = {} #garder les chemins complets

# afficher des détails sur un fichier
def display_file_info(event):
    selected_nodes = tree.selection() #fichier sélectionné
    if not selected_nodes:
        return

    file_path = node_paths[selected_nodes[0]]
    if not file_path.is_file():
        return

    file_info = file_path.stat()
    
    # Mise à jour dynamique des champs d'information
    entry_name.config(state="normal")
    entry_name.delete(0, END)
    entry_name.insert(0, file_path.name)
    entry_name.config(state="readonly")

    entry_path.config(state="normal")
    entry_path.delete(0, END)
    entry_path.insert(0, str(file_path.parent))
    entry_path.config(state="readonly")

    entry_type.config(state="normal")
    entry_type.delete(0, END)
    entry_type.insert(0, file_path.suffix or "Fichier")
    entry_type.config(state="readonly")

    entry_size.config(state="normal")
    entry_size.delete(0, END)
    size_kb = round(file_info.st_size / 1024, 2)
    entry_size.insert(0, f"{size_kb} KB")
    entry_size.config(state="readonly")

    entry_modified.config(state="normal")
    entry_modified.delete(0, END)
    mod_time = datetime.fromtimestamp(file_info.st_mtime).strftime("%d.%m.%Y")
    entry_modified.insert(0, mod_time)
    entry_modified.config(state="readonly")

    entry_permissions.config(state="normal")
    entry_permissions.delete(0, END)
    perms = []
    if os.access(file_path, os.R_OK): perms.append("Read")
    if os.access(file_path, os.W_OK): perms.append("Write")
    entry_permissions.insert(0, " / ".join(perms) if perms else "None")
    entry_permissions.config(state="readonly")

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
window.title("yuuriy")
window.geometry("700x500")
window.configure(bg="Red") # Fond rouge pour rendre les écarts de grille très visibles

# configuration de 3 colonnes dans window
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
file_information.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

project_area = tk.Frame(
    window,
    bg="purple",
    highlightbackground="Red",
    highlightthickness=3,
    bd=3
)
project_area.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

# Style avec bordures explicites pour le Treeview
style = ttk.Style()
style.configure(
    "Treeview",
    font=("Arial", 10),
    rowheight=28,
    foreground="Red", #couleur d'écriture
    relief="solid",
    bd=2
)

# création du treeview et placement
tree = ttk.Treeview(tree_frame)
tree.heading("#0", text="Directory Tree")
tree.grid(row=0, column=0, sticky="nswe", padx=3, pady=3) # placement avec marges

# éléments de la section file information
label_title = Label(file_information, text="File Information", font=("Arial", 10, "bold"))
label_title.pack(anchor="w", padx=5, pady=2)

Label(file_information, text="Name:").pack(anchor="w", padx=5)
entry_name = Entry(file_information, state="readonly")
entry_name.pack(fill="x", padx=5, pady=(0, 5))

Label(file_information, text="Path:").pack(anchor="w", padx=5)
entry_path = Entry(file_information, state="readonly")
entry_path.pack(fill="x", padx=5, pady=(0, 5))

Label(file_information, text="Type:").pack(anchor="w", padx=5)
entry_type = Entry(file_information, state="readonly")
entry_type.pack(fill="x", padx=5, pady=(0, 5))

Label(file_information, text="Size:").pack(anchor="w", padx=5)
entry_size = Entry(file_information, state="readonly")
entry_size.pack(fill="x", padx=5, pady=(0, 5))

Label(file_information, text="Modified:").pack(anchor="w", padx=5)
entry_modified = Entry(file_information, state="readonly")
entry_modified.pack(fill="x", padx=5, pady=(0, 5))

Label(file_information, text="Permissions:").pack(anchor="w", padx=5)
entry_permissions = Entry(file_information, state="readonly")
entry_permissions.pack(fill="x", padx=5, pady=(0, 5))

# quand on sélectionne un fichier, on appelle display_file_info
tree.bind("<<TreeviewSelect>>", display_file_info) 

# lancement du prog principal
window.mainloop()