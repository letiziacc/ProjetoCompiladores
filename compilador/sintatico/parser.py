class Parser:
    def __init__(self, tokens):
        self.tokens = tokens   # Lista de tokens que vem do léxico
        self.i = 0             # Posição atual da lista
        self.tem_erro = False  # Flag de erro (quando houver erro sintático)

    
    def atual(self):
        # Retorna o token atual
        if self.i < len(self.tokens):
            return self.tokens[self.i]
        return ('EOF', 'EOF')

    def avanca(self):
        # Avança para o próximo token
        self.i += 1

    def consome(self, esperado):
        # Verifica se o token atua é o token esperado
        token, _ = self.atual()
        if token == esperado:
            self.avanca()
        else:
            self.erro(f"Esperado {esperado}, encontrado {token}")

    def erro(self, msg):
        # Registra erro sintático
        print(f"Erro sintático: {msg}")
        self.tem_erro = True

   
    def parse(self):
        # Analisa todos os comandos até o EOF
        while self.atual()[0] != 'EOF' and not self.tem_erro:
            self.comando()

        return not self.tem_erro  # True se não houve erro


    def comando(self):
        # Decide o tipo de comando que será analisado
        token, _ = self.atual()

        if token == 'var':
            self.atribuicao()

        elif token == 'echo':
            self.echo()

        elif token == 'while':
            self.while_stmt()

        elif token == 'if':
            self.if_stmt()

        elif token == 'function':
            self.funcao()

        elif token == 'ident':
            self.chamada_funcao()

        elif token in ['abre_chave', 'fecha_chave']:
            self.avanca()

        else:
            # ignora tokens irrelevantes
            self.avanca()

    def atribuicao(self):
        self.consome('var')
        self.consome('atribuicao')
        self.expressao()
        self.consome('ponto_virgula')

 
    def echo(self):
        self.consome('echo')
        self.expressao()

        while self.atual()[0] == 'ponto':
            self.consome('ponto')
            self.expressao()

        self.consome('ponto_virgula')


    def while_stmt(self):
        self.consome('while')
        self.consome('abre_paren')
        self.condicao()
        self.consome('fecha_paren')
        self.bloco()

    def if_stmt(self):
        self.consome('if')
        self.consome('abre_paren')
        self.condicao()
        self.consome('fecha_paren')
        self.bloco()

        if self.atual()[0] == 'else':
            self.consome('else')
            self.bloco()

    
    def funcao(self):
        self.consome('function')
        self.consome('ident')
        self.consome('abre_paren')

        # parâmetros
        if self.atual()[0] == 'var':
            self.consome('var')
            while self.atual()[0] == 'virgula':
                self.consome('virgula')
                self.consome('var')

        self.consome('fecha_paren')
        self.bloco()

   
    def chamada_funcao(self):
        self.consome('ident')
        self.consome('abre_paren')

        if self.atual()[0] in ['var', 'numero']:
            self.expressao()
            while self.atual()[0] == 'virgula':
                self.consome('virgula')
                self.expressao()

        self.consome('fecha_paren')
        self.consome('ponto_virgula')


    def bloco(self):
        self.consome('abre_chave')
        while self.atual()[0] != 'fecha_chave' and not self.tem_erro:
            self.comando()
        self.consome('fecha_chave')

   
    def expressao(self):
        self.termo()
        while self.atual()[0] in ['mais', 'menos']:
            self.avanca()
            self.termo()

    def termo(self):
        self.fator()
        while self.atual()[0] in ['vezes', 'divide']:
            self.avanca()
            self.fator()

    def fator(self):
        # Reconhece os elementos de uma expressão 
        token, _ = self.atual()

        # Número ou variável
        if token in ['numero', 'var', 'string', 'php_eol']:
            self.avanca()

        # Chamada de função dentro de expressão
        elif token == 'ident':
            self.avanca()
            if self.atual()[0] == 'abre_paren':
                self.consome('abre_paren')

                if self.atual()[0] != 'fecha_paren':
                    self.expressao()
                    while self.atual()[0] == 'virgula':
                        self.consome('virgula')
                        self.expressao()

                self.consome('fecha_paren')

        # Expressão entre parênteses
        elif token == 'abre_paren':
            self.consome('abre_paren')
            self.expressao()
            self.consome('fecha_paren')

        else:
            self.erro(f"Fator inválido: {token}")

    
    def condicao(self):
        self.expressao()

        if self.atual()[0] in [
            'maior_que', 'menor_que',
            'maior_igual', 'menor_igual',
            'igual', 'diferente'
        ]:
            self.avanca()
            self.expressao()
        else:
            self.erro("Operador relacional esperado")
