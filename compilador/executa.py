# arquivo que vai ler o asm.txt / arquivo obj gerado

from interpretador.main import Interpretador
with open ("compilador/asm.txt", 'r') as arquivo:
    arquivoOBJ = arquivo.readlines()

vm = Interpretador(arquivoOBJ)
vm.executa()
