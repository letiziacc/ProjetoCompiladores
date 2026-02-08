# ProjetoCompiladores

Este projeto foi desenvolvido para a disciplina de **Projeto de Compiladores** e implementa um compilador completo em Python, incluindo análise léxica, sintática, semântica, geração de código objeto e execução em uma máquina virtual.


## Estrutura do Projeto
O projeto está organizado da seguinte forma:

```text
ProjetoCompiladores/
││
├── lexico/ # Analisador léxico
├── sintatico/ # Analisador sintático
├── semantico/ # Analisador semântico
├── codigoObjeto/ # Gerador de código objeto
├── interpretador/ # Máquina virtual para execução
│
├── compilador/
│ ├── codigo.txt # Código-fonte de entrada
│ └── asm.txt # Código objeto gerado
│
├── compila.py # Executa todas as etapas do compilador
├── executa.py # Executa o código objeto
└── README.md
```
---

## Pré-requisitos

- Python **3.6 ou superior**
- Biblioteca **PLY** (Python Lex-Yacc) - https://www.dabeaz.com/ply/ply.html

Instalação do PLY:

```bash
pip install ply
```

# Como executar
1- Compilar o código-fonte

Certifique-se de que o arquivo:
```
compilador/codigo.txt
```
contém o código a ser compilado.

Execute:
```
python compila.py
```
Esse comando realiza:

- Análise léxica
- Análise sintática
- Análise semântica
- Geração do código objeto

O resultado será salvo em:
```
compilador/asm.txt
```
2️- Executar o código objeto

Após a compilação, execute:
```
python executa.py
```
Esse script utiliza o interpretador para rodar o código objeto gerado.

# Fluxo do compilador

O funcionamento do sistema segue as seguintes etapas:
```
Código-fonte (codigo.txt)
        ↓
Análise léxica
        ↓
Análise sintática
        ↓
Análise semântica
        ↓
Geração de código objeto (asm.txt)
        ↓
Execução na máquina virtual
```
# Autor
O projeto foi desenvolvido por Letízia Manuella Serqueira Eugênio
