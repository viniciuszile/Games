# 🎮 Game Tracker – GitHub as Database

Projeto pessoal para **gerenciamento de jogos**, utilizando o **GitHub como banco de dados**, com **CRUD em Python** e **frontend em React** para visualização interativa.

A ideia central é eliminar a necessidade de um backend tradicional, usando apenas:

* JSON versionado no GitHub
* Repositório de imagens como CDN
* Automação via GitHub API

---

## 📌 Visão Geral

Este projeto é dividido em três partes principais:

1. **Banco de dados**

   * Arquivo JSON armazenado em um repositório GitHub
   * Repositório separado para imagens (capas dos jogos)

2. **CRUD Desktop (Python)**

   * Interface gráfica para criar, editar e atualizar jogos
   * Upload automático de JSON e imagens via GitHub API

3. **Frontend Web (React)**

   * Consome os dados diretamente do GitHub
   * Exibe os jogos em cards interativos com filtros e ordenações

---

## 🧠 Conceito

> O GitHub funciona como um banco de dados público, versionado e acessível via HTTP.

Cada alteração feita no CRUD:

* Atualiza o JSON no repositório
* Mantém histórico de mudanças
* Dispensa banco SQL ou backend próprio

---

## 🛠️ CRUD em Python (Tkinter)

Aplicação desktop responsável por **gerenciar os dados**.

### Funcionalidades

* ➕ Adicionar jogos
* ✏️ Editar jogos existentes
* ⭐ Sistema de notas por estrelas
* ❌ Marcar jogos como *Dropados*

  * Motivo
  * Plano de ação
* 🖼️ Upload automático de imagens
* 🔄 Sincronização direta com o GitHub

### Tecnologias

* Python
* Tkinter
* Requests
* GitHub REST API
* JSON
* Base64 (upload de imagens)

---

## 🌐 Frontend em React

Aplicação web focada apenas em **leitura e visualização dos dados**.

### Funcionalidades

* 🎴 Cards com animação de flip
* 🔍 Filtros:

  * Todos
  * Concluídos
  * Em andamento
  * Dropados
* ↕️ Ordenações:

  * Nome
  * Tempo de jogo
  * Rank
* 📊 Contadores automáticos:

  * Zerados
  * Em andamento
  * Dropados
  * Total
* 🧭 Menu flutuante de navegação

### Fonte de dados

Os dados são carregados diretamente do GitHub:

```txt
https://raw.githubusercontent.com/<usuario>/<repositorio>/main/public/Data/jogos_2025.json
```

Nenhum backend, nenhuma API própria.

---

## 🔄 Fluxo do Projeto

```text
[CRUD Python]
     ↓ (GitHub API)
[JSON + Imagens no GitHub]
     ↓ (fetch)
[Frontend React]
```

---

## 📂 Estrutura Geral

```text
📦 Games
 ┣ 📂 public/Data
 ┃ ┗ jogos_2025.json
 ┣ 📂 frontend
 ┃ ┗ React App
 ┗ 📂 crud-python
   ┗ app Tkinter
```

```text
📦 Games-Fotos-2025
 ┗ 🖼️ Capas dos jogos
```

---

## 🎯 Objetivo do Projeto

* Criar um **tracker pessoal de jogos**
* Explorar o GitHub como:

  * Banco de dados
  * CDN de imagens
  * Sistema de versionamento
* Integrar **Python + React** em um projeto real
* Manter tudo simples, escalável e versionado

---

## 🚀 Tecnologias Utilizadas

* **Python**

  * Tkinter
  * Requests
* **React**

  * Hooks (`useState`, `useEffect`)
  * Fetch API
* **GitHub**

  * Repositórios como storage
  * GitHub REST API
* **JSON**
* **HTML / CSS / JavaScript**

---

## 📌 Observações

* O CRUD é local (desktop)
* O site é somente leitura
* Todo o controle de dados acontece via GitHub

---
