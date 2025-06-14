# 📌 Projeto: Preditivo de Evasão Escolar

Bem-vindo ao repositório deste projeto!  
Aqui seguimos boas práticas de versionamento com **Git** para garantir organização, clareza e qualidade no nosso histórico de código.

---

## 🚀 Como clonar o projeto

Como o projeto é público, você pode clonar com HTTPS:

```bash
git clone https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
````

Depois, entre na pasta do projeto:

```bash
cd NOME_DO_REPOSITORIO
```

---

## 🌳 Estrutura e significado das branches

O projeto adota duas branches principais para organização do desenvolvimento:

| Branch    | Finalidade                                                                                                                                                                                                                          |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `main`    | ✅ **Branch de Produção:** Contém a versão mais estável e pronta para ser publicada em produção. Tudo o que estiver aqui foi testado e revisado. Nenhuma alteração vai direto para `main` sem passar por um PR e por testes prévios. |

---

## 📌 Regras para trabalhar com branches:

* ❌ **Nunca faça commits direto na `main`.**
* 🌱 **Cada nova feature, bugfix ou alteração deve ser feita em uma branch separada**, criada a partir da `main`.

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

---

### 🎯 Estrutura básica de um commit:

```
<tipo>(escopo opcional): descrição breve
```

* **Tipo:** Natureza da alteração (ex: feat, fix, docs...)
* **Escopo (opcional):** Módulo ou parte afetada (ex: login, auth, api)
* **Descrição breve:** Explicação curta e clara da alteração

---

### ✅ Exemplos práticos:

| Tipo     | Exemplo                                       | Quando usar                                           |
| -------- | --------------------------------------------- | ----------------------------------------------------- |
| feat     | `feat: adicionar página de login`             | Nova funcionalidade                                   |
| fix      | `fix: corrigir erro de autenticação`          | Correção de bug                                       |
| docs     | `docs: atualizar instruções de instalação`    | Alterações apenas na documentação                     |
| style    | `style: ajustar indentação no arquivo X`      | Alterações de formatação sem impacto no funcionamento |
| refactor | `refactor: melhorar performance da função Y`  | Refatorações sem mudança de comportamento externo     |
| test     | `test: adicionar testes unitários para login` | Adição ou ajuste de testes                            |
| chore    | `chore: atualizar dependências`               | Tarefas de manutenção geral (builds, configs)         |

---

### 📝 Boas práticas ao escrever commits:

✅ Escreva o commit no **imperativo** e de forma objetiva (ex: "adicionar página de login", e não "adicionada página de login")
✅ Evite mensagens genéricas como "atualizações" ou "mudanças"
✅ Commits pequenos e frequentes são melhores que grandes blocos de alterações
✅ Se necessário, faça **squash** antes de abrir um PR para manter o histórico limpo
✅ Sempre siga o formato `<tipo>(escopo opcional): descrição`

---

## 🛠️ Fluxo de trabalho recomendado

1. Atualize a `main`:

```bash
git checkout main
git pull origin main
```

2. Crie uma nova branch descritiva:

```bash
git checkout -b feat/nome-da-sua-feature
```

3. Faça suas alterações no código.

4. Adicione e faça commit:

```bash
git add .
git commit -m "feat: adicionar página de login"
```

5. Envie sua branch para o repositório remoto:

```bash
git push origin feat/nome-da-sua-feature
```

6. Abra um **Pull Request (PR)** da sua branch para a `main`.

---

## 💡 Dicas Finais

* 🔄 Sempre atualize sua branch com a última versão da `main` antes de abrir um PR.
* ✅ Mantenha seus commits pequenos e significativos.
* 🔍 Revise sua PR antes de solicitar o merge.
* 🚫 Nunca trabalhe diretamente nas branches `main` ou `main`.

---

## 📢 Exemplo de fluxo completo:

```bash
git checkout main
git pull origin main
git checkout -b feat/adicionar-login
# ... faça suas alterações no código ...
git add .
git commit -m "feat: adicionar página de login"
git push origin feat/adicionar-login
# Abra um Pull Request da sua branch para main
```

---

🚀 **Bons commits e boas contribuições!**

```

---
