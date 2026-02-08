# Arquivo responsável por executar o código objeto gerado pelo compilador

from interpretador.main import Interpretador
with open ("compilador/asm.txt", 'r') as arquivo:
    arquivoOBJ = arquivo.readlines()

# Cria a máquina virtual (interpretador)
# Passa o código objeto como parâmetro
vm = Interpretador(arquivoOBJ)
vm.executa()
