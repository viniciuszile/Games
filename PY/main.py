import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

# Diretório base (onde o script está)
BASE_DIR = Path(__file__).resolve().parent

# Caminho correto para o JSON
JSON_PATH = BASE_DIR / "public" / "Data" / "jogos.json"

# Carrega JSON com proteção
def load_jogos():
    if JSON_PATH.exists():
        try:
            text = JSON_PATH.read_text(encoding="utf-8").strip()
            if not text:
                return []
            return json.loads(text)
        except:
            return []
    return []

# Salva JSON
def save_jogos(jogos):
    JSON_PATH.write_text(json.dumps(jogos, ensure_ascii=False, indent=2), encoding="utf-8")

# Janela principal
root = tk.Tk()
root.title("CRUD Jogos")
root.geometry("900x500")

# Lista de jogos
jogos = load_jogos()

# Função para atualizar Treeview
def refresh_tree():
    for i in tree.get_children():
        tree.delete(i)
    for idx, jogo in enumerate(jogos):
        tree.insert("", "end", iid=idx, values=(
            jogo.get("nome", ""),
            jogo.get("plataforma", ""),
            jogo.get("inicio", ""),
            jogo.get("termino", ""),
            jogo.get("situacao", ""),
            jogo.get("Horas De Jogo", ""),
            jogo.get("dificuldade", ""),
            jogo.get("replay", ""),
            jogo.get("nota", "")
        ))

# Função para selecionar imagem
def select_image(entry):
    path = filedialog.askopenfilename(
        title="Selecionar imagem",
        filetypes=[("Imagens", "*.jpg *.png *.jpeg *.gif *.webp")]
    )
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, f"/Fotos-main/{Path(path).name}")

# Função para adicionar ou editar jogo
def save_entry():
    data = {
        "nome": nome_var.get(),
        "imagem": imagem_var.get(),
        "plataforma": plataforma_var.get(),
        "inicio": inicio_var.get(),
        "termino": termino_var.get(),
        "situacao": situacao_var.get(),
        "Horas De Jogo": horas_var.get(),
        "dificuldade": dificuldade_var.get(),
        "replay": replay_var.get(),
        "nota": nota_var.get()
    }
    selected = tree.selection()
    if selected:
        idx = int(selected[0])
        jogos[idx] = data
    else:
        jogos.append(data)
    save_jogos(jogos)
    refresh_tree()
    clear_form()

# Função para deletar
def delete_entry():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Aviso", "Selecione um jogo para deletar")
        return
    idx = int(selected[0])
    if messagebox.askyesno("Confirmação", f"Deletar {jogos[idx]['nome']}?"):
        jogos.pop(idx)
        save_jogos(jogos)
        refresh_tree()
        clear_form()

# Função para preencher formulário ao selecionar
def on_tree_select(event):
    selected = tree.selection()
    if not selected:
        return
    idx = int(selected[0])
    jogo = jogos[idx]
    nome_var.set(jogo.get("nome", ""))
    imagem_var.set(jogo.get("imagem", ""))
    plataforma_var.set(jogo.get("plataforma", ""))
    inicio_var.set(jogo.get("inicio", ""))
    termino_var.set(jogo.get("termino", ""))
    situacao_var.set(jogo.get("situacao", ""))
    horas_var.set(jogo.get("Horas De Jogo", ""))
    dificuldade_var.set(jogo.get("dificuldade", ""))
    replay_var.set(jogo.get("replay", ""))
    nota_var.set(jogo.get("nota", ""))

# Função para limpar formulário
def clear_form():
    nome_var.set("")
    imagem_var.set("")
    plataforma_var.set("")
    inicio_var.set("")
    termino_var.set("")
    situacao_var.set("")
    horas_var.set("")
    dificuldade_var.set("")
    replay_var.set("")
    nota_var.set("")
    tree.selection_remove(tree.selection())

# --- Formulário ---
frame_form = tk.Frame(root)
frame_form.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

nome_var = tk.StringVar()
imagem_var = tk.StringVar()
plataforma_var = tk.StringVar()
inicio_var = tk.StringVar()
termino_var = tk.StringVar()
situacao_var = tk.StringVar()
horas_var = tk.StringVar()
dificuldade_var = tk.StringVar()
replay_var = tk.StringVar()
nota_var = tk.StringVar()

fields = [
    ("Nome", nome_var),
    ("Imagem", imagem_var),
    ("Plataforma", plataforma_var),
    ("Início", inicio_var),
    ("Término", termino_var),
    ("Situação", situacao_var),
    ("Horas De Jogo", horas_var),
    ("Dificuldade", dificuldade_var),
    ("Replay", replay_var),
    ("Nota", nota_var)
]

for idx, (label_text, var) in enumerate(fields):
    tk.Label(frame_form, text=label_text).grid(row=idx, column=0, sticky=tk.W, pady=2)
    entry = tk.Entry(frame_form, textvariable=var, width=25)
    entry.grid(row=idx, column=1, pady=2)
    if label_text == "Imagem":
        tk.Button(frame_form, text="Selecionar", command=lambda e=entry: select_image(e)).grid(row=idx, column=2, padx=2)

tk.Button(frame_form, text="Salvar", command=save_entry).grid(row=len(fields), column=0, pady=10)
tk.Button(frame_form, text="Deletar", command=delete_entry).grid(row=len(fields), column=1, pady=10)
tk.Button(frame_form, text="Limpar", command=clear_form).grid(row=len(fields), column=2, pady=10)

# --- Lista de jogos ---
cols = ["Nome","Plataforma","Início","Término","Situação","Horas De Jogo","Dificuldade","Replay","Nota"]
tree = ttk.Treeview(root, columns=cols, show="headings", selectmode="browse")
for c in cols:
    tree.heading(c, text=c)
tree.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
tree.bind("<<TreeviewSelect>>", on_tree_select)

refresh_tree()
root.mainloop()
