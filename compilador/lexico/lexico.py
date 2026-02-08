import ply.lex as lex


class Lexico:
    # Palavras reservadas
    def __init__(self):
        self.reserved = {

            'echo'  : 'echo',
            'if'    : 'if',
            'else'  : 'else',
            'while' : 'while',
            'function' : 'function',
            'PHP_EOL' : 'php_eol',
            'floatval(readline())' : 'floatval',
        }

        # Lista de tokens
        self.tokens = [
            'inicio', 'fim', 'comentario', 'comentario_linha',
            'abre_paren', 'fecha_paren',
            'abre_chave', 'fecha_chave',  
            'ponto_virgula', 'virgula',
            'ponto', 'igual', 'diferente',
            'menor_que', 'maior_que', 'menor_igual', 'maior_igual', 'atribuicao',
            'mais', 'menos', 'vezes', 'divide',
            'numero', 'ident', 'var',
            
            
        ] + list(self.reserved.values())

        # Definição dos tokens
        self.t_inicio = r'<\?php'
        self.t_fim = r'\?>'
        self.t_abre_paren = r'\('
        self.t_fecha_paren = r'\)'
        self.t_abre_chave = r'\{'
        self.t_fecha_chave = r'\}'
        self.t_ponto_virgula = r';'
        self.t_virgula = r','
        self.t_ponto = r'\.'
        self.t_igual = r'=='
        self.t_atribuicao = r'='
        self.t_diferente = r'!='
        self.t_maior_igual = r'>='
        self.t_maior_que = r'>'
        self.t_menor_igual = r'<='
        self.t_menor_que = r'<'
        self.t_mais = r'\+'
        self.t_menos = r'-' 
        self.t_vezes = r'\*'

        self.t_divide = r'/'

        self.t_ignore = ' \t'

    def t_comentario_linha(self, t):
        r'//.*'
        return t

    def t_comentario(self, t):
        r'/\*[\s\S]*?\*/'
        t.lexer.lineno += t.value.count('\n')
        return t

    def t_ident(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value, 'ident')  
        return t

    def t_var(self, t):
        r'\$[a-zA-Z_][a-zA-Z0-9_]*'
        return t

    def t_numero(self, t):
        r'\d+\.\d+|\d+'
        return t

    # Controle de linhas
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Controle de  erros

    def t_error(self, t):
        print(f"Caracter ilegal '{t.value[0]}' na linha {t.lineno}")
        t.lexer.skip(1)

    def constroi(self):
        self.lexer = lex.lex(module=self)
        return self.lexer
