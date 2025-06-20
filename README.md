---

# 📌 Projeto: Preditivo de Evasão Escolar

Bem-vindo ao repositório deste projeto!

## 🧠 Overview do Projeto

Projeto que realiza **análises preditivas sobre evasão escolar no Brasil**, com o objetivo de **reduzir os casos de evasão**, analisando dados e prevendo situações de risco.

---

Aqui seguimos boas práticas de versionamento com **Git** para garantir organização, clareza e qualidade no nosso histórico de código.

---

## 🚀 Como clonar o projeto

Como o projeto é público, você pode clonar com HTTPS:

```bash
git clone https://github.com/matheusdesacarvalholimeira/https-github.com-matheusdesacarvalholimeira-Projeto_Analise_EVASAO_ESCOLAR
```

Depois, entre na pasta do projeto:

```bash
cd Projeto_Analise_EVASAO_ESCOLAR
```

---

## 🛠️ Requisitos e Instalação

### 📌 Tecnologias utilizadas:

* Python 3.10
* PySpark
* Pandas
* Matplotlib
* Seaborn
* Jupyter Notebook

---

### 📥 Preparando o ambiente no Linux(Ubuntu):

#### 1. Instalar o Python 3.10 e dependências básicas:

```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-distutils python3-pip
sudo apt install openjdk-17-jdk
```

---

#### 2. Criar o ambiente virtual:

```bash
python3.10 -m venv venv
```

---

#### 3. Ativar o ambiente virtual:

```bash
source venv/bin/activate
```

---

#### 4. Instalar as bibliotecas necessárias:

```bash
pip install pyspark pandas matplotlib seaborn jupyter
```

---

#### 5. Rodar o Jupyter Notebook (se quiser visualizar os notebooks do projeto):

```bash
jupyter notebook
```

---

## ✅ Como executar o projeto localmente (Jupyter + Script Python)

### Opção 1: Usando dois terminais

**Terminal 1 → Rodar o Jupyter Notebook:**

```bash
source venv/bin/activate
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64/
jupyter notebook
```

👉 O terminal ficará com os logs do Jupyter.
👉 O Jupyter abrirá no navegador em: [http://localhost:8888](http://localhost:8888)

---

**Terminal 2 → Rodar o script Python:**

Abra uma nova aba ou janela de terminal:

```bash
source venv/bin/activate
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64/
python projeto_pyspark/src/data_processing.py
```

---

## 🌳 Estrutura e significado das branches

| Branch | Finalidade                                                                                                                          |
| ------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| `main` | ✅ **Branch de Produção:** Contém a versão mais estável e pronta para ser publicada. Tudo o que estiver aqui foi testado e revisado. |

---

## 📌 Regras para trabalhar com branches:

* ❌ **Nunca faça commits direto na `main`.**
* 🌱 **Cada nova feature, correção de bug ou alteração deve ser feita em uma branch separada**, criada a partir da `main`.

### Exemplos de nomes de branches:

| Tipo de Tarefa      | Exemplo de Nome de Branch        |
| ------------------- | -------------------------------- |
| Nova funcionalidade | `feat/adicionar-login`           |
| Correção de bug     | `fix/corrigir-login`             |
| Documentação        | `docs/ajustar-readme`            |
| Refatoração         | `refactor/melhorar-auth-service` |

---

## ✅ Boas práticas de commits com Conventional Commits

Seguimos o padrão **[Conventional Commits](https://www.conventionalcommits.org/)** para manter o histórico do projeto limpo, claro e semântico.

### 🎯 Estrutura básica de um commit:

```
<tipo>(escopo opcional): descrição breve
```

---

### ✅ Exemplos práticos:

| Tipo     | Exemplo                                       | Quando usar                                       |
| -------- | --------------------------------------------- | ------------------------------------------------- |
| feat     | `feat: adicionar página de login`             | Nova funcionalidade                               |
| fix      | `fix: corrigir erro de autenticação`          | Correção de bug                                   |
| docs     | `docs: atualizar instruções de instalação`    | Alterações na documentação                        |
| style    | `style: ajustar indentação no arquivo X`      | Alterações de formatação (sem impacto funcional)  |
| refactor | `refactor: melhorar performance da função Y`  | Refatorações sem mudança de comportamento externo |
| test     | `test: adicionar testes unitários para login` | Adição ou ajuste de testes                        |
| chore    | `chore: atualizar dependências`               | Tarefas de manutenção geral (builds, configs)     |

---

### 📝 Boas práticas ao escrever commits:

✅ Escreva o commit no **imperativo** e de forma objetiva (ex: "adicionar página de login", e não "adicionada página de login")
✅ Evite mensagens genéricas como "atualizações" ou "mudanças"
✅ Prefira **commits pequenos e frequentes**
✅ Se necessário, faça **squash** antes de abrir um PR
✅ Sempre siga o formato `<tipo>(escopo opcional): descrição`

---

## 🛠️ Fluxo de trabalho recomendado

```bash
git checkout main
git pull origin main
git checkout -b feat/nome-da-sua-feature
# ... faça suas alterações no código ...
git add .
git commit -m "feat: adicionar página de login"
git push origin feat/nome-da-sua-feature
# Abra um Pull Request da sua branch para main
```

---

## ✅ Como executar os testes unitários

O projeto possui testes unitários localizados na pasta `tests/`, utilizando **Pytest** e **PySpark**.

---

### 📥 Instalar o Pytest no ambiente virtual:

Ative o ambiente virtual (se ainda não estiver ativo):

```bash
source venv/bin/activate
```

Instale o Pytest:

```bash
pip install pytest
```

---

### ✅ Executar os testes:

Na raiz do projeto, execute:

```bash
pytest
```
Aqui está a seção sobre MFA adicionada ao final do seu README, com instruções claras para garantir segurança e privacidade local:

---

## 🔐 Autenticação por MFA (Multi-Factor Authentication)

Este projeto possui um mecanismo simples de **MFA local** para adicionar uma camada extra de segurança na execução de scripts Python sensíveis, como o `data_processing.py`.

---

### ✅ Como funciona o MFA local:

Antes da execução do script, o sistema solicita um código **TOTP (Time-based One-Time Password)**, gerado a partir de uma chave secreta definida no seu `.env`.

👉 Você pode usar apps como:

* **Microsoft Authenticator**
* **Google Authenticator**
* **Authy**

---

### 📌 Configuração do MFA:

#### 1. Adicione a variável `MFA_SECRET` ao seu arquivo `.env`:

Exemplo de `.env`:

```
PROJECT_BASE_PATH=/seu/caminho/do/projeto
MFA_SECRET=SUA_CHAVE_SECRETA_GERADA
```

> 📌 **Importante:**
> O `.env` **não está versionado no Git** por segurança.
> **Nunca suba sua chave MFA para o repositório!**

---

#### 2. Gerando uma nova chave secreta MFA (se você quiser criar uma):

Você pode usar bibliotecas como **`pyotp`** para gerar:

```python
import pyotp
print(pyotp.random_base32())
```

Copie essa chave e adicione no seu app Authenticator.

---
