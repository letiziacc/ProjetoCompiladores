class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0
        self.tem_erro = False  # flag de erro

    # =========================
    # UTILIDADES
    # =========================
    def atual(self):
        if self.i < len(self.tokens):
            return self.tokens[self.i]
        return ('EOF', 'EOF')

    def avanca(self):
        self.i += 1

    def consome(self, esperado):
        token, _ = self.atual()
        if token == esperado:
            self.avanca()
        else:
            self.erro(f"Esperado {esperado}, encontrado {token}")

    def erro(self, msg):
        print(f"Erro sintático: {msg}")
        self.tem_erro = True

    # =========================
    # INÍCIO DO PARSER
    # =========================
    def parse(self):
        while self.atual()[0] != 'EOF' and not self.tem_erro:
            self.comando()

        return not self.tem_erro  # True se não houve erro

    # =========================
    # COMANDOS
    # =========================
    def comando(self):
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

    # =========================
    # ATRIBUIÇÃO
    # var = expressão;
    # =========================
    def atribuicao(self):
        self.consome('var')
        self.consome('atribuicao')
        self.expressao()
        self.consome('ponto_virgula')

    # =========================
    # ECHO
    # echo expressão . expressão;
    # =========================
    def echo(self):
        self.consome('echo')
        self.expressao()

        while self.atual()[0] == 'ponto':
            self.consome('ponto')
            self.expressao()

        self.consome('ponto_virgula')

    # =========================
    # WHILE
    # =========================
    def while_stmt(self):
        self.consome('while')
        self.consome('abre_paren')
        self.condicao()
        self.consome('fecha_paren')
        self.bloco()

    # =========================
    # IF
    # =========================
    def if_stmt(self):
        self.consome('if')
        self.consome('abre_paren')
        self.condicao()
        self.consome('fecha_paren')
        self.bloco()

        if self.atual()[0] == 'else':
            self.consome('else')
            self.bloco()

    # =========================
    # FUNÇÃO
    # =========================
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

    # =========================
    # CHAMADA DE FUNÇÃO
    # =========================
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

    # =========================
    # BLOCO
    # =========================
    def bloco(self):
        self.consome('abre_chave')
        while self.atual()[0] != 'fecha_chave' and not self.tem_erro:
            self.comando()
        self.consome('fecha_chave')

    # =========================
    # EXPRESSÕES ARITMÉTICAS
    # =========================
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
        token, _ = self.atual()

        # número ou variável
        if token in ['numero', 'var', 'string', 'php_eol']:
            self.avanca()

        # chamada de função dentro de expressão
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

        # expressão entre parênteses
        elif token == 'abre_paren':
            self.consome('abre_paren')
            self.expressao()
            self.consome('fecha_paren')

        else:
            self.erro(f"Fator inválido: {token}")

    # =========================
    # CONDIÇÃO
    # =========================
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
