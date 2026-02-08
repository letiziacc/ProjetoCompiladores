from lexico.lexico import Lexico
from sintatico.parser import Parser
from semantico.semantico import Semantico
from codigoObjeto.main import GeradorCodigoObjeto

cod = """
<?php
$e = 0;
$f = 0.0;
$g = 0.0;
$h = 0.0;

function dois($j, $k, $l) {
    $cont = 0.0;
    $quant = 0.0;
    $quant = floatval(readline());
    $cont = floatval(readline());

    while ($cont <= $quant) {
        echo $cont . PHP_EOL;
        $cont = $cont + 1;
    }

    $l = $l + $j + $cont;

    echo $k . PHP_EOL;
    echo $l . PHP_EOL;
}

/* Corpo principal */

echo $e . PHP_EOL; /* real */

$f = floatval(readline());
$g = floatval(readline());
$h = floatval(readline());

$d = $e / $f; /* real */

dois($h, $d, $h);
"""
lexico = Lexico()
lexer = lexico.constroi()
lexer.input(cod)

# print(f"{'TOKEN':<15} {'LEXEMA':<20} {'LINHA':<6} {'POSIÇÃO'}")
# print("-" * 55)

tokens_lexema = []
for tok in lexer:
    # print(f"{tok.type:<15} {str(tok.value):<20} {tok.lineno:<6} {tok.lexpos}")
    tokens_lexema.append([tok.type, tok.value])

# -=-=-=-=-=-=- sintatico -=-=-=-=-=-=-
parser = Parser(tokens_lexema)
p = parser.parse()

if not p:
    print("Erro na Análise Sintática!")

# -=-=-=-=-=-=- semantico -=-=-=-=-=-=-
semant = Semantico(tokens_lexema)
# semant.exibe()
s = semant.regrasSemanticas()

if s and p:

    g = GeradorCodigoObjeto(tokens_lexema, semant.tabelaSimbolos)
    retorno = g.gerar()
    cod = retorno
    with open('compilador/asm.txt', 'w') as arquivo:
        for num, instrucao in enumerate(cod):
            arquivo.write(instrucao+'\n')   
            print(num, instrucao)  
else:
    print("Erro no frontend") 