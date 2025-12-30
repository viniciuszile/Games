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
# Funções JSON local
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
# Funções GitHub
# ---------------------------
def upload_json_to_github():
    url_get = f"https://api.github.com/repos/{REPO_JSON}/contents/{JSON_PATH_GITHUB}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    r = requests.get(url_get, headers=headers)
    sha = None
    if r.status_code == 200:
        sha = r.json()["sha"]

    content = json.dumps(jogos, ensure_ascii=False, indent=2).encode("utf-8")
    content_b64 = base64.b64encode(content).decode()

    data = {
        "message": "Atualizando JSON de jogos",
        "content": content_b64,
        "branch": BRANCH_JSON
    }
    if sha:
        data["sha"] = sha

    r = requests.put(url_get, headers=headers, json=data)
    if r.status_code in [200, 201]:
        print("JSON enviado para o GitHub com sucesso!")
    else:
        print("Erro ao enviar JSON:", r.text)

def upload_image_to_github(local_path):
    filename = Path(local_path).name
    url_get = f"https://api.github.com/repos/{REPO_IMG}/contents/{filename}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    # Verifica se o arquivo já existe
    r = requests.get(url_get, headers=headers)
    if r.status_code == 200:
        # Já existe, usar o mesmo nome
        print(f"Imagem {filename} já existe, usando a existente.")
    else:
        # Não existe, faz upload
        with open(local_path, "rb") as f:
            content_b64 = base64.b64encode(f.read()).decode()
        data = {
            "message": f"Upload da imagem {filename}",
            "content": content_b64,
            "branch": BRANCH_IMG
        }
        r = requests.put(url_get, headers=headers, json=data)
        if r.status_code in [200, 201]:
            print(f"Imagem {filename} enviada com sucesso!")
        else:
            print("Erro ao enviar imagem:", r.text)

# ---------------------------
# Abrir end.py ao fechar
# ---------------------------
def iniciar_end():
    end_path = BASE_DIR / "end.py"
    if end_path.exists():
        subprocess.Popen(
            f'start cmd /k "cd {BASE_DIR} && python end.py"',
            shell=True
        )
    else:
        print("end.py não encontrado!")

def on_close():
    root.destroy()
    iniciar_end()
    sys.exit()

# ---------------------------
# Tkinter
# ---------------------------
root = tk.Tk()
root.title("CRUD Jogos")
root.geometry("950x550")
root.protocol("WM_DELETE_WINDOW", on_close)

jogos = load_jogos()

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
# Selecionar imagem
# ---------------------------
def select_image(entry):
    path = filedialog.askopenfilename(
        title="Selecionar imagem",
        filetypes=[("Imagens", "*.jpg *.png *.jpeg *.gif *.webp")]
    )
    if path:
        filename = Path(path).name
        # URL Raw
        url = f"https://raw.githubusercontent.com/viniciuszile/new---fotos/refs/heads/main/{filename}"
        entry.delete(0, tk.END)
        entry.insert(0, url)
        # Faz upload apenas se não existir
        upload_image_to_github(path)

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

    selected = tree.selection()
    if selected:
        idx = int(selected[0])
        jogos[idx] = data
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
        upload_json_to_github()

# ---------------------------
# Preencher formulário
# ---------------------------
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
    motivo_var.set(jogo.get("Motivo", ""))
    plano_var.set(jogo.get("Plano de ação", ""))
    if jogo.get("situacao") == "Dropado":
        dropado_var.set(True)
        toggle_dropado()
    else:
        dropado_var.set(False)
        toggle_dropado()

# ---------------------------
# Limpar formulário
# ---------------------------
def clear_form():
    for var in [nome_var, imagem_var, plataforma_var, inicio_var, termino_var,
                situacao_var, horas_var, dificuldade_var, replay_var, nota_var,
                motivo_var, plano_var]:
        var.set("")
    dropado_var.set(False)
    toggle_dropado()
    tree.selection_remove(tree.selection())

# ---------------------------
# Toggle Dropado
# ---------------------------
def toggle_dropado():
    if dropado_var.get():
        for entry in old_entries.values():
            entry.config(state="disabled")
        for label, entry in dropado_entries.values():
            label.grid()
            entry.grid()
        situacao_var.set("Dropado")
    else:
        for entry in old_entries.values():
            entry.config(state="normal")
        for label, entry in dropado_entries.values():
            label.grid_remove()
            entry.grid_remove()
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
nota_var = tk.StringVar()
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
    ("Replay", replay_var),
    ("Nota", nota_var)
]

old_entries = {}
for idx, (label_text, var) in enumerate(fields):
    tk.Label(frame_form, text=label_text).grid(row=idx, column=0, sticky=tk.W, pady=2)
    entry = tk.Entry(frame_form, textvariable=var, width=25)
    entry.grid(row=idx, column=1, pady=2)
    old_entries[label_text] = entry
    if label_text == "Imagem":
        tk.Button(frame_form, text="Selecionar", command=lambda e=entry: select_image(e)).grid(row=idx, column=2, padx=2)

tk.Button(frame_form, text="Salvar", command=save_entry).grid(row=len(fields)+1, column=0, pady=10)
tk.Button(frame_form, text="Deletar", command=delete_entry).grid(row=len(fields)+1, column=1, pady=10)
tk.Button(frame_form, text="Limpar", command=clear_form).grid(row=len(fields)+1, column=2, pady=10)

tk.Checkbutton(frame_form, text="Dropado", variable=dropado_var, command=toggle_dropado).grid(row=len(fields), column=0, sticky=tk.W, pady=10)

dropado_entries = {}
dropado_entries["Motivo"] = (tk.Label(frame_form, text="Motivo"), tk.Entry(frame_form, textvariable=motivo_var, width=25))
dropado_entries["Plano de ação"] = (tk.Label(frame_form, text="Plano de ação"), tk.Entry(frame_form, textvariable=plano_var, width=25))
for label, entry in dropado_entries.values():
    label.grid_remove()
    entry.grid_remove()

# ---------------------------
# Tabela
# ---------------------------
cols = ["Nome","Plataforma","Início","Término","Situação","Horas De Jogo",
        "Dificuldade","Replay","Nota","Motivo","Plano de ação"]

tree = ttk.Treeview(root, columns=cols, show="headings", selectmode="browse")
for c in cols:
    tree.heading(c, text=c)
tree.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
tree.bind("<<TreeviewSelect>>", on_tree_select)

refresh_tree()

# ---------------------------
# Iniciar janela
# ---------------------------
root.mainloop()
