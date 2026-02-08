# Importa os módulos responsáveis por cada fase do compilador
from lexico.lexico import Lexico
from sintatico.parser import Parser
from semantico.semantico import Semantico
from codigoObjeto.main import GeradorCodigoObjeto

# Abre e lê o arquivo de código-fonte que será compilado
with open('compilador/codigo.txt', 'r') as arquivo:
        cod = arquivo.read()

# Análise léxica
lexico = Lexico()
lexer = lexico.constroi()
lexer.input(cod)

tokens_lexema = []
for tok in lexer:
    tokens_lexema.append([tok.type, tok.value])

# Análise sintática
parser = Parser(tokens_lexema)
p = parser.parse()

if not p:
    print("Erro na Análise Sintática!")

# Análise semântica
semant = Semantico(tokens_lexema)
# semant.exibe()
s = semant.regrasSemanticas()

# Geração do código objeto (se não houver erros das etapas anteriores)
if s and p:

    g = GeradorCodigoObjeto(tokens_lexema, semant.tabelaSimbolos)
    retorno = g.gerar()
    cod = retorno
    # Salva o código objeto no arquivo asm.txt
    with open('compilador/asm.txt', 'w') as arquivo:
        for num, instrucao in enumerate(cod):
            arquivo.write(instrucao+'\n')   
            print(num, instrucao)  
else:
    print("Erro no frontend")    # Caso haja erro no frontend (léxico/sintático/semântico)