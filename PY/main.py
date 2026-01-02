import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import subprocess
import sys
import base64
import requests

# ---------------------------
# Configurações GitHub
# ---------------------------
GITHUB_TOKEN = ""

REPO_JSON = "viniciuszile/Games"
BRANCH_JSON = "main"
JSON_PATH_GITHUB = "public/Data/jogos.json"

REPO_IMG = "viniciuszile/new---fotos"
BRANCH_IMG = "main"

# ---------------------------
# Diretório base
# ---------------------------
BASE_DIR = Path(__file__).resolve().parent
JSON_PATH = BASE_DIR / "dados.json"

# ---------------------------
# JSON local
# ---------------------------
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

def save_jogos(jogos):
    JSON_PATH.write_text(
        json.dumps(jogos, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

# ---------------------------
# GitHub
# ---------------------------
def upload_json_to_github():
    url = f"https://api.github.com/repos/{REPO_JSON}/contents/{JSON_PATH_GITHUB}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    r = requests.get(url, headers=headers)
    sha = r.json()["sha"] if r.status_code == 200 else None

    content = json.dumps(jogos, ensure_ascii=False, indent=2).encode("utf-8")
    content_b64 = base64.b64encode(content).decode()

    data = {
        "message": "Atualizando jogos",
        "content": content_b64,
        "branch": BRANCH_JSON
    }
    if sha:
        data["sha"] = sha

    requests.put(url, headers=headers, json=data)

def upload_image_to_github(local_path):
    filename = Path(local_path).name
    url = f"https://api.github.com/repos/{REPO_IMG}/contents/{filename}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return

    with open(local_path, "rb") as f:
        content_b64 = base64.b64encode(f.read()).decode()

    data = {
        "message": f"Upload {filename}",
        "content": content_b64,
        "branch": BRANCH_IMG
    }
    requests.put(url, headers=headers, json=data)

# ---------------------------
# Tkinter
# ---------------------------
root = tk.Tk()
root.title("CRUD Jogos")
root.state("zoomed")

jogos = load_jogos()

# ---------------------------
# Estrelas ⭐
# ---------------------------
nota_var = tk.StringVar(value="☆☆☆☆☆")
rating_value = tk.IntVar(value=0)
star_labels = []

def set_rating(value):
    rating_value.set(value)
    nota_var.set("★" * value + "☆" * (5 - value))
    update_stars()

def update_stars():
    for i, lbl in enumerate(star_labels, start=1):
        lbl.config(text="★" if i <= rating_value.get() else "☆")

# ---------------------------
# Atualizar tabela
# ---------------------------
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
            jogo.get("nota", ""),
            jogo.get("Motivo", ""),
            jogo.get("Plano de ação", "")
        ))

# ---------------------------
# Salvar / Editar
# ---------------------------
def save_entry():
    if dropado_var.get():
        data = {
            "nome": nome_var.get(),
            "imagem": imagem_var.get(),
            "plataforma": plataforma_var.get(),
            "inicio": inicio_var.get(),
            "situacao": "Dropado",
            "Horas De Jogo": horas_var.get(),
            "Motivo": motivo_var.get(),
            "Plano de ação": plano_var.get()
        }
    else:
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

    if tree.selection():
        jogos[int(tree.selection()[0])] = data
    else:
        jogos.append(data)

    save_jogos(jogos)
    refresh_tree()
    clear_form()
    upload_json_to_github()

# ---------------------------
# Deletar
# ---------------------------
def delete_entry():
    if not tree.selection():
        return
    idx = int(tree.selection()[0])
    if messagebox.askyesno("Confirmar", f"Deletar {jogos[idx]['nome']}?"):
        jogos.pop(idx)
        save_jogos(jogos)
        refresh_tree()
        clear_form()
        upload_json_to_github()

# ---------------------------
# Selecionar tabela
# ---------------------------
def on_tree_select(event):
    if not tree.selection():
        return
    jogo = jogos[int(tree.selection()[0])]

    nome_var.set(jogo.get("nome", ""))
    imagem_var.set(jogo.get("imagem", ""))
    plataforma_var.set(jogo.get("plataforma", ""))
    inicio_var.set(jogo.get("inicio", ""))
    termino_var.set(jogo.get("termino", ""))
    situacao_var.set(jogo.get("situacao", ""))
    horas_var.set(jogo.get("Horas De Jogo", ""))
    dificuldade_var.set(jogo.get("dificuldade", ""))
    replay_var.set(jogo.get("replay", ""))
    motivo_var.set(jogo.get("Motivo", ""))
    plano_var.set(jogo.get("Plano de ação", ""))

    nota = jogo.get("nota", "☆☆☆☆☆")
    nota_var.set(nota)
    rating_value.set(nota.count("★"))
    update_stars()

    is_dropado = jogo.get("situacao") == "Dropado"
    dropado_var.set(is_dropado)
    toggle_dropado()

    # se NÃO for dropado, restaura a situação corretamente
    if not is_dropado:
        situacao_var.set(jogo.get("situacao", ""))

# ---------------------------
# Limpar
# ---------------------------
def clear_form():
    for v in [nome_var, imagem_var, plataforma_var, inicio_var,
              termino_var, situacao_var, horas_var,
              dificuldade_var, replay_var, motivo_var, plano_var]:
        v.set("")
    dropado_var.set(False)
    set_rating(0)
    toggle_dropado()
    tree.selection_remove(tree.selection())

# ---------------------------
# Dropado
# ---------------------------
def toggle_dropado():
    if dropado_var.get():
        for e in old_entries.values():
            e.config(state="disabled")
        for lbl, ent in dropado_entries.values():
            lbl.grid()
            ent.grid()
        situacao_var.set("Dropado")
    else:
        for e in old_entries.values():
            e.config(state="normal")
        for lbl, ent in dropado_entries.values():
            lbl.grid_remove()
            ent.grid_remove()
        situacao_var.set("")

# ---------------------------
# FORMULÁRIO
# ---------------------------
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
motivo_var = tk.StringVar()
plano_var = tk.StringVar()
dropado_var = tk.BooleanVar()

fields = [
    ("Nome", nome_var),
    ("Imagem", imagem_var),
    ("Plataforma", plataforma_var),
    ("Início", inicio_var),
    ("Término", termino_var),
    ("Situação", situacao_var),
    ("Horas De Jogo", horas_var),
    ("Dificuldade", dificuldade_var),
    ("Replay", replay_var)
]

old_entries = {}
for i, (txt, var) in enumerate(fields):
    tk.Label(frame_form, text=txt).grid(row=i, column=0, sticky="w")
    ent = tk.Entry(frame_form, textvariable=var, width=25)
    ent.grid(row=i, column=1)
    old_entries[txt] = ent

# Nota ⭐⭐⭐⭐⭐
row_nota = len(fields)
tk.Label(frame_form, text="Nota").grid(row=row_nota, column=0, sticky="w")
stars_frame = tk.Frame(frame_form)
stars_frame.grid(row=row_nota, column=1, sticky="w")

for i in range(1, 6):
    lbl = tk.Label(stars_frame, text="☆", font=("Arial", 18))
    lbl.pack(side=tk.LEFT)
    lbl.bind("<Button-1>", lambda e, v=i: set_rating(v))
    star_labels.append(lbl)

tk.Checkbutton(frame_form, text="Dropado", variable=dropado_var,
               command=toggle_dropado).grid(row=row_nota+1, column=0, sticky="w")

dropado_entries = {
    "Motivo": (tk.Label(frame_form, text="Motivo"),
               tk.Entry(frame_form, textvariable=motivo_var, width=25)),
    "Plano": (tk.Label(frame_form, text="Plano de ação"),
              tk.Entry(frame_form, textvariable=plano_var, width=25))
}

for lbl, ent in dropado_entries.values():
    lbl.grid_remove()
    ent.grid_remove()

tk.Button(frame_form, text="Salvar", command=save_entry).grid(row=row_nota+3, column=0)
tk.Button(frame_form, text="Deletar", command=delete_entry).grid(row=row_nota+3, column=1)
tk.Button(frame_form, text="Limpar", command=clear_form).grid(row=row_nota+3, column=2)

# ---------------------------
# TABELA COM SCROLL
# ---------------------------
frame_table = tk.Frame(root)
frame_table.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

scroll_x = tk.Scrollbar(frame_table, orient="horizontal")
scroll_y = tk.Scrollbar(frame_table, orient="vertical")

cols = ["Nome","Plataforma","Início","Término","Situação",
        "Horas De Jogo","Dificuldade","Replay","Nota","Motivo","Plano de ação"]

tree = ttk.Treeview(
    frame_table,
    columns=cols,
    show="headings",
    xscrollcommand=scroll_x.set,
    yscrollcommand=scroll_y.set
)

scroll_x.config(command=tree.xview)
scroll_y.config(command=tree.yview)

scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

for c in cols:
    tree.heading(c, text=c)
    tree.column(c, width=160, anchor="w")

tree.bind("<<TreeviewSelect>>", on_tree_select)

refresh_tree()
root.mainloop()