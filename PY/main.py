 
# ==========================================
# CRUD JOGOS 2026
# ==========================================

import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import base64
import requests
import os
import time

from dotenv import load_dotenv

# ==========================================
# TERMINAL
# ==========================================
def linha():
    print("─" * 70)

def titulo(txt):
    linha()
    print(f"🎮 {txt}")
    linha()

def log(txt):
    agora = time.strftime("%H:%M:%S")
    print(f"[{agora}] ℹ️ {txt}")

def ok(txt):
    agora = time.strftime("%H:%M:%S")
    print(f"[{agora}] ✅ {txt}")

def warn(txt):
    agora = time.strftime("%H:%M:%S")
    print(f"[{agora}] ⚠️ {txt}")

def err(txt):
    agora = time.strftime("%H:%M:%S")
    print(f"[{agora}] ❌ {txt}")

titulo("CRUD Jogos 2026")

# ==========================================
# ENV
# ==========================================
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise Exception("GITHUB_TOKEN não encontrado")

ok("Token carregado")

# ==========================================
# CONFIG GITHUB
# ==========================================
REPO_JSON = "viniciuszile/Games"
JSON_GITHUB_PATH = "public/Data/jogos_2026.json"
BRANCH_JSON = "main"

REPO_IMG = "viniciuszile/Games-Fotos-2025"
BRANCH_IMG = "main"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

# ==========================================
# PATHS
# ==========================================
BASE_DIR = Path(__file__).resolve().parent

JSON_LOCAL = (
    BASE_DIR.parent /
    "public" /
    "Data" /
    "jogos_2026.json"
)

# ==========================================
# BAIXAR JSON
# ==========================================
def baixar_json():

    log("Sincronizando JSON...")

    url = (
        f"https://api.github.com/repos/"
        f"{REPO_JSON}/contents/{JSON_GITHUB_PATH}"
    )

    response = requests.get(
        url,
        headers=HEADERS
    )

    if response.status_code != 200:

        err(response.text)

        if JSON_LOCAL.exists():

            warn("Usando JSON local")

            try:
                return json.loads(
                    JSON_LOCAL.read_text(
                        encoding="utf-8"
                    )
                )

            except:
                return []

        return []

    data = response.json()

    content = base64.b64decode(
        data["content"]
    ).decode("utf-8")

    JSON_LOCAL.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    JSON_LOCAL.write_text(
        content,
        encoding="utf-8"
    )

    ok("JSON sincronizado")

    return json.loads(content)

# ==========================================
# UPLOAD JSON
# ==========================================
def upload_json(jogos):

    titulo("UPLOAD JSON")

    url = (
        f"https://api.github.com/repos/"
        f"{REPO_JSON}/contents/{JSON_GITHUB_PATH}"
    )

    response = requests.get(
        url,
        headers=HEADERS
    )

    sha = None

    if response.status_code == 200:

        sha = response.json()["sha"]

        ok("SHA obtido")

    content = base64.b64encode(
        json.dumps(
            jogos,
            ensure_ascii=False,
            indent=2
        ).encode("utf-8")
    ).decode()

    data = {
        "message": "Atualizando jogos 2026",
        "content": content,
        "branch": BRANCH_JSON
    }

    if sha:
        data["sha"] = sha

    response = requests.put(
        url,
        headers=HEADERS,
        json=data
    )

    if response.status_code in [200, 201]:

        ok("JSON enviado GitHub")

    else:

        err(response.text)

        messagebox.showerror(
            "GitHub",
            response.text
        )

# ==========================================
# UPLOAD IMAGEM
# ==========================================
def upload_imagem(path):

    titulo("UPLOAD IMAGEM")

    nome = (
        Path(path)
        .name
        .lower()
        .replace(" ", "-")
    )

    url_api = (
        f"https://api.github.com/repos/"
        f"{REPO_IMG}/contents/{nome}"
    )

    response = requests.get(
        url_api,
        headers=HEADERS
    )

    if response.status_code == 200:

        warn("Imagem já existe")

        return (
            f"https://raw.githubusercontent.com/"
            f"{REPO_IMG}/{BRANCH_IMG}/{nome}"
        )

    with open(path, "rb") as f:

        content = base64.b64encode(
            f.read()
        ).decode()

    data = {
        "message": f"Upload {nome}",
        "content": content,
        "branch": BRANCH_IMG
    }

    response = requests.put(
        url_api,
        headers=HEADERS,
        json=data
    )

    if response.status_code not in [200, 201]:

        err(response.text)

        return ""

    ok("Imagem enviada")

    return (
        f"https://raw.githubusercontent.com/"
        f"{REPO_IMG}/{BRANCH_IMG}/{nome}"
    )

# ==========================================
# TKINTER
# ==========================================
root = tk.Tk()

root.title("CRUD Jogos 2026")

root.state("zoomed")

style = ttk.Style()
style.theme_use("clam")

# ==========================================
# DADOS
# ==========================================
jogos = baixar_json()

indice_edicao = None

# ==========================================
# VARIÁVEIS
# ==========================================
nome = tk.StringVar()
imagem = tk.StringVar()
plataforma = tk.StringVar()
inicio = tk.StringVar()
termino = tk.StringVar()
situacao = tk.StringVar()
horas = tk.StringVar()
dificuldade = tk.StringVar()
replay = tk.StringVar()

motivo = tk.StringVar()
plano = tk.StringVar()

pausado = tk.BooleanVar()

nota = tk.StringVar(value="☆☆☆☆☆")

stars = []

# ==========================================
# ESTRELAS
# ==========================================
def set_rating(v):

    nota.set(
        "★" * v + "☆" * (5 - v)
    )

    for i, s in enumerate(stars, 1):

        s.config(
            text="★" if i <= v else "☆"
        )

# ==========================================
# IMAGEM
# ==========================================
def escolher_imagem():

    path = filedialog.askopenfilename(
        filetypes=[
            ("Imagens", "*.png *.jpg *.jpeg *.webp")
        ]
    )

    if not path:
        return

    imagem.set(
        upload_imagem(path)
    )

# ==========================================
# TOGGLE PAUSADO
# ==========================================
def toggle_pausado():

    if pausado.get():

        situacao.set("pausado")

        frame_pausado.grid(
            row=11,
            column=0,
            columnspan=3,
            sticky="w",
            pady=(10, 10)
        )

    else:

        if situacao.get() == "pausado":
            situacao.set("")

        frame_pausado.grid_remove()

# ==========================================
# SELECIONAR
# ==========================================
def ao_selecionar(event):

    global indice_edicao

    if not tree.selection():
        return

    indice_edicao = int(
        tree.selection()[0]
    )

    j = jogos[indice_edicao]

    nome.set(j.get("nome", ""))
    imagem.set(j.get("imagem", ""))
    plataforma.set(j.get("plataforma", ""))
    inicio.set(j.get("inicio", ""))
    termino.set(j.get("termino", ""))
    situacao.set(j.get("situacao", ""))
    horas.set(j.get("Horas De Jogo", ""))
    dificuldade.set(j.get("dificuldade", ""))
    replay.set(j.get("replay", ""))

    set_rating(
        j.get("nota", "☆☆☆☆☆").count("★")
    )

    if j.get("situacao") == "pausado":

        pausado.set(True)

        motivo.set(
            j.get("Motivo", "")
        )

        plano.set(
            j.get("Plano de ação", "")
        )

        frame_pausado.grid(
            row=11,
            column=0,
            columnspan=3,
            sticky="w",
            pady=(10, 10)
        )

    else:

        pausado.set(False)

        motivo.set("")
        plano.set("")

        frame_pausado.grid_remove()

# ==========================================
# SALVAR
# ==========================================
def salvar():

    global indice_edicao

    data = {
        "nome": nome.get(),
        "imagem": imagem.get(),
        "plataforma": plataforma.get(),
        "inicio": inicio.get(),
        "termino": termino.get(),
        "situacao": (
            "pausado"
            if pausado.get()
            else situacao.get()
        ),
        "Horas De Jogo": horas.get(),
        "dificuldade": dificuldade.get(),
        "replay": replay.get(),
        "nota": nota.get()
    }

    if pausado.get():

        data["Motivo"] = motivo.get()

        data["Plano de ação"] = plano.get()

    if indice_edicao is not None:

        jogos[indice_edicao] = data

        ok("Jogo atualizado")

    else:

        jogos.append(data)

        ok("Novo jogo adicionado")

    JSON_LOCAL.write_text(
        json.dumps(
            jogos,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    upload_json(jogos)

    atualizar()

    limpar()

# ==========================================
# DELETE
# ==========================================
def deletar():

    global indice_edicao

    if indice_edicao is None:
        return

    confirm = messagebox.askyesno(
        "Confirmação",
        f"Deletar {jogos[indice_edicao]['nome']}?"
    )

    if not confirm:
        return

    jogos.pop(indice_edicao)

    JSON_LOCAL.write_text(
        json.dumps(
            jogos,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    upload_json(jogos)

    atualizar()

    limpar()

# ==========================================
# LIMPAR
# ==========================================
def limpar():

    global indice_edicao

    for v in [
        nome,
        imagem,
        plataforma,
        inicio,
        termino,
        situacao,
        horas,
        dificuldade,
        replay,
        motivo,
        plano
    ]:
        v.set("")

    pausado.set(False)

    set_rating(0)

    frame_pausado.grid_remove()

    indice_edicao = None

    tree.selection_remove(
        tree.selection()
    )

# ==========================================
# LADO ESQUERDO
# ==========================================
side = tk.Frame(
    root,
    bg="#1e1e1e",
    padx=15,
    pady=15,
    width=320
)

side.pack(
    side=tk.LEFT,
    fill=tk.Y
)

def campo(txt, var, row):

    tk.Label(
        side,
        text=txt,
        fg="white",
        bg="#1e1e1e"
    ).grid(
        row=row,
        column=0,
        sticky="w",
        pady=5
    )

    tk.Entry(
        side,
        textvariable=var,
        width=30
    ).grid(
        row=row,
        column=1,
        pady=5
    )

campo("Nome", nome, 0)

campo("Imagem", imagem, 1)

tk.Button(
    side,
    text="Selecionar",
    command=escolher_imagem
).grid(
    row=1,
    column=2
)

campo("Plataforma", plataforma, 2)
campo("Início", inicio, 3)
campo("Término", termino, 4)
campo("Situação", situacao, 5)
campo("Horas", horas, 6)
campo("Dificuldade", dificuldade, 7)
campo("Replay", replay, 8)

# ==========================================
# ESTRELAS
# ==========================================
tk.Label(
    side,
    text="Nota",
    fg="white",
    bg="#1e1e1e"
).grid(
    row=9,
    column=0,
    sticky="w"
)

star_frame = tk.Frame(
    side,
    bg="#1e1e1e"
)

star_frame.grid(
    row=9,
    column=1,
    sticky="w"
)

for i in range(1, 6):

    lbl = tk.Label(
        star_frame,
        text="☆",
        font=("Arial", 18),
        fg="gold",
        bg="#1e1e1e",
        cursor="hand2"
    )

    lbl.pack(side=tk.LEFT)

    lbl.bind(
        "<Button-1>",
        lambda e, v=i: set_rating(v)
    )

    stars.append(lbl)

# ==========================================
# PAUSADO
# ==========================================
tk.Checkbutton(
    side,
    text="Pausado",
    variable=pausado,
    command=toggle_pausado,
    bg="#1e1e1e",
    fg="white",
    activebackground="#1e1e1e",
    activeforeground="white",
    selectcolor="#1e1e1e"
).grid(
    row=10,
    column=0,
    sticky="w",
    pady=(10, 5)
)

frame_pausado = tk.Frame(
    side,
    bg="#1e1e1e"
)

# MOTIVO
tk.Label(
    frame_pausado,
    text="Motivo",
    fg="white",
    bg="#1e1e1e",
    width=12,
    anchor="w"
).grid(
    row=0,
    column=0,
    padx=(0, 10),
    pady=4,
    sticky="w"
)

entry_motivo = tk.Entry(
    frame_pausado,
    textvariable=motivo,
    width=38
)

entry_motivo.grid(
    row=0,
    column=1,
    pady=4,
    sticky="w"
)

# PLANO
tk.Label(
    frame_pausado,
    text="Plano de ação",
    fg="white",
    bg="#1e1e1e",
    width=12,
    anchor="w"
).grid(
    row=1,
    column=0,
    padx=(0, 10),
    pady=4,
    sticky="w"
)

entry_plano = tk.Entry(
    frame_pausado,
    textvariable=plano,
    width=38
)

entry_plano.grid(
    row=1,
    column=1,
    pady=4,
    sticky="w"
)

frame_pausado.grid_remove()

# ==========================================
# BOTÕES
# ==========================================
tk.Button(
    side,
    text="Salvar / Atualizar",
    width=28,
    command=salvar
).grid(
    row=20,
    column=0,
    columnspan=3,
    pady=10
)

tk.Button(
    side,
    text="Deletar",
    width=28,
    command=deletar
).grid(
    row=21,
    column=0,
    columnspan=3
)

# ==========================================
# TABELA
# ==========================================
frame_table = tk.Frame(root)

frame_table.pack(
    side=tk.RIGHT,
    fill=tk.BOTH,
    expand=True
)

cols = (
    "Nome",
    "Plataforma",
    "Início",
    "Término",
    "Situação",
    "Horas",
    "Dificuldade",
    "Replay",
    "Nota",
    "Motivo",
    "Plano"
)

tree = ttk.Treeview(
    frame_table,
    columns=cols,
    show="headings"
)

scroll_y = ttk.Scrollbar(
    frame_table,
    orient="vertical",
    command=tree.yview
)

scroll_x = ttk.Scrollbar(
    frame_table,
    orient="horizontal",
    command=tree.xview
)

tree.configure(
    yscrollcommand=scroll_y.set,
    xscrollcommand=scroll_x.set
)

tree.grid(
    row=0,
    column=0,
    sticky="nsew"
)

scroll_y.grid(
    row=0,
    column=1,
    sticky="ns"
)

scroll_x.grid(
    row=1,
    column=0,
    sticky="ew"
)

frame_table.grid_rowconfigure(
    0,
    weight=1
)

frame_table.grid_columnconfigure(
    0,
    weight=1
)

larguras = {
    "Nome": 260,
    "Plataforma": 140,
    "Início": 120,
    "Término": 120,
    "Situação": 120,
    "Horas": 100,
    "Dificuldade": 120,
    "Replay": 100,
    "Nota": 120,
    "Motivo": 320,
    "Plano": 420
}

for c in cols:

    tree.heading(c, text=c)

    tree.column(
        c,
        width=larguras.get(c, 150),
        minwidth=100,
        stretch=False
    )

tree.bind(
    "<<TreeviewSelect>>",
    ao_selecionar
)

# ==========================================
# UPDATE TREE
# ==========================================
def atualizar():

    tree.delete(*tree.get_children())

    for i, j in enumerate(jogos):

        tree.insert(
            "",
            "end",
            iid=i,
            values=(
                j.get("nome"),
                j.get("plataforma"),
                j.get("inicio"),
                j.get("termino"),
                j.get("situacao"),
                j.get("Horas De Jogo"),
                j.get("dificuldade"),
                j.get("replay"),
                j.get("nota"),
                j.get("Motivo"),
                j.get("Plano de ação")
            )
        )

    ok(f"{len(jogos)} jogos carregados")

# ==========================================
# START
# ==========================================
atualizar()

root.mainloop()

