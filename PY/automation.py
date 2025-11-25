import subprocess
import os
import time

# Caminho do projeto
project_path = r"C:\Users\Zile\Downloads\My_Games_2025-main"
project_path_py = r"C:\Users\Zile\Downloads\My_Games_2025-main\PY"

# 1. Abre CMD e roda npm start
subprocess.Popen(
    fr'start cmd /k "cd {project_path} && npm start"',
    shell=True
)

# Aguarda o servidor iniciar um pouco
time.sleep(2)

# 2. Roda o main.py (CRUD)
subprocess.Popen(
    fr'start cmd /k "cd {project_path_py} && python main.py"',
    shell=True
)
