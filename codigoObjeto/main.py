class GeradorCodigoObjeto:

    def __init__(self, tokens_lexemas, tabela_simbolos):
        self.tokens = tokens_lexemas
        self.TS = tabela_simbolos

        self.C = []
        self.i = 0
        self.escopo = 'GLOBAL'
        self.pilha_while = []
        self.pilha_if = []


    # utilidades

    def atual(self):
        return self.tokens[self.i]

    def avanca(self):
        self.i += 1

    def gera(self, instr):
        self.C.append(instr)


    def busca_simbolo(self, nome):

        # tenta no escopo atual
        s = self.TS.get((nome, self.escopo))
        if s:
            return s

        return self.TS.get((nome, 'GLOBAL'))


    def gera_chamada_procedimento(self):

        _, nome_proc = self.atual()

        # endereço de retorno (próxima instrução depois da chamada)
        ret = len(self.C) 
        self.gera(f'PUSHER')

        self.avanca()   # nome
        self.avanca()   # (

        # parâmetros
        while self.atual()[0] != 'fecha_paren':

            token, lex = self.atual()

            if token == 'var':
                simb = self.busca_simbolo(lex)
                self.gera(f'PARAM {simb["end_rel"]}')

            self.avanca()

        self.avanca()  # )
        self.C[ret] += f' {len(self.C)+1}' # PUSHER para o final da chamada

        # busca endereço do procedimento
        proc = self.TS.get((nome_proc, 'GLOBAL'))

        self.gera(f'CHPR {proc["end_proc"]+1}')


    def gera_pulo_while(self):

        # marca início do while
        inicio = len(self.C)
        self.pilha_while.append(inicio)

        self.avanca()  # (

        posfixa, op = self.infixa_para_posfixa(False)

        for item in posfixa:
            if item['tipo'] == 'NUM':
                self.gera(f"CRCT {item['valor']}")
            elif item['tipo'] == 'VAR':
                simb = self.busca_simbolo(item['valor'])
                self.gera(f"CRVL {simb['end_rel']}")
            elif item['tipo'] == 'OP':
                self.gera(self.map_op(item['valor']))

        self.gera(op)

        # gera DSVF sem destino ainda
        self.gera("DSVF ?")

        # salva posição desse DSVF
        self.pilha_while.append(len(self.C)-1)


    def gera_if(self):

        self.avanca()  # (

        posfixa, op = self.infixa_para_posfixa(False)

        for item in posfixa:
            if item['tipo'] == 'NUM':
                self.gera(f"CRCT {item['valor']}")
            elif item['tipo'] == 'VAR':
                simb = self.busca_simbolo(item['valor'])
                self.gera(f"CRVL {simb['end_rel']}")
            elif item['tipo'] == 'OP':
                self.gera(self.map_op(item['valor']))

        self.gera(op)

        self.gera("DSVF ?")

        # empilha posição do DSVF
        self.pilha_if.append(len(self.C)-1)



    def gera_else(self):

        # cria salto pro fim do if
        self.gera("DSVI ?")

        if len(self.pilha_if):
            dsvf_pos = self.pilha_if.pop()

            # remenda DSVF para começar o else
            self.C[dsvf_pos] = f"DSVF {len(self.C)}"

        # empilha esse DSVI pra remendar depois
        self.pilha_if.append(len(self.C)-1)

        self.avanca()


    # principal
    def gerar(self):

        self.gera("INPP")
        self.aloca_globais()

        while self.i < len(self.tokens):
            self.gera_comando()

        self.gera("PARA")
        return self.C


    # aloca vars
    def aloca_globais(self):
        for (nome, esc), s in self.TS.items():
            if esc == 'GLOBAL':
                self.gera("ALME 1")


    def aloca_locais(self, qnt_param):
        conta_vars = 0
        for (nome, esc), s in self.TS.items():
            if esc == self.escopo:
                conta_vars += 1
        
        total = conta_vars - qnt_param
        for i in range(total):
            self.gera("ALME 1")

        return total

    def gera_comando(self):

        token, lex = self.atual()

        if token == 'var' and self.tokens[self.i+1][0] == 'atribuicao':
            if self.tokens[self.i+2][1] != 'floatval':
                self.gera_atribuicao()
            else:
                self.gera_leit()
                simb = self.busca_simbolo(lex)
                self.gera(f"ARMZ {simb['end_rel']}")

        elif token == 'echo':
            self.gera_print()

        elif token == 'function':
            self.gera_procedimento()

        elif token == 'ident' and lex not in ['floatval', 'readline']:
            self.gera_chamada_procedimento()

        elif token == 'while':
            self.gera_pulo_while()

        elif token == 'if':
            self.gera_if()
        
        elif token == 'else':
            self.gera_else()

        else:
            self.avanca()


    # atribuição
    def gera_atribuicao(self):

        _, var = self.atual()
        simb = self.busca_simbolo(var)

        self.avanca()      # var
        self.avanca()      # =

        self.gera_expressao()

        self.gera(f"ARMZ {simb['end_rel']}")

        self.avanca()      # ;


    # expressão
    def gera_expressao(self):

        posfixa, _ = self.infixa_para_posfixa()

        for item in posfixa:

            if item['tipo'] == 'NUM':
                self.gera(f"CRCT {item['valor']}")

            elif item['tipo'] == 'VAR':
                simb = self.busca_simbolo(item['valor'])
                self.gera(f"CRVL {simb['end_rel']}")

            elif item['tipo'] == 'OP':

                if item['valor'] == 'mais':
                    self.gera("SOMA")

                elif item['valor'] == 'menos':
                    self.gera("SUBT")

                elif item['valor'] == 'vezes':
                    self.gera("MULT")

                elif item['valor'] == 'divide':
                    self.gera("DIVI")



    def map_op(self, op):

        return {
            'mais': 'SOMA',
            'menos': 'SUBT',
            'vezes': 'MULT',
            'divide': 'DIVI'
        }[op]


    # entrada e/ saida
    def gera_print(self):

        self.avanca()  # echo
        self.gera_expressao()
        self.gera("IMPR")
        self.avanca()  # ;


    def gera_leit(self):
        self.gera("LEIT")
        self.avanca()  # ;


    # procedimento 
    def gera_procedimento(self):

        self.avanca()  # function
        _, nome = self.atual()

        self.escopo = nome
        # chave usada para saber no futuro o chpr (posicao)
        self.TS[(nome, 'GLOBAL')]['end_proc'] = len(self.C)

        # pula o bloco no fluxo principal
        pos = len(self.C)
        self.gera("DSVI ?")

        self.avanca()   # nome
        self.avanca()   # (

        # vamos salvar a qnt de parametros pois depois não vamos contabilizar com o ALME 1 em um novo procedimento
        qnt_param = 0
        while self.atual()[0] != 'fecha_paren':
            if self.atual()[0] == 'var':
                qnt_param += 1
            self.avanca()
        self.avanca()

        total = self.aloca_locais(qnt_param)

        self.gera_bloco()

        self.gera(f"DESM {total}")
        self.gera("RTPR")

        self.C[pos] = f"DSVI {len(self.C)}"

        self.escopo = 'GLOBAL'


    # auxiliares
    def gera_bloco(self):

        self.avanca()  # consome '{'

        nivel = 1

        while nivel > 0:

            token, _ = self.atual()

            if token == 'abre_chave':
                nivel += 1
                self.avanca()

            elif token == 'fecha_chave':
                nivel -= 1
                self.avanca()

                # fecha WHILE se existir
                if self.pilha_while:
                    dsvf_pos = self.pilha_while.pop()
                    inicio = self.pilha_while.pop()

                    self.gera(f"DSVI {inicio}")
                    self.C[dsvf_pos] = f"DSVF {len(self.C)}"

                # fecha IF/ELSE se existir
                if self.pilha_if:
                    if self.atual()[0] == 'else':
                        # vamos ter guardado a posicao para o DSVF
                        pos = self.pilha_if.pop()
                        self.C[pos] = f"DSVF {len(self.C)+1}"
                    else:
                        pos = self.pilha_if.pop()
                        self.C[pos] = f"DSVI {len(self.C)+1}"
                        

            else:
                self.gera_comando()



    # tranformando para posfixa
    def infixa_para_posfixa(self, vem_atrib=True):

        saida = []
        pilha = []
        opLogico = None
        if vem_atrib:
            while self.atual()[0] != 'ponto_virgula':

                token, lex = self.atual()

                if token == 'numero':
                    saida.append({'tipo':'NUM','valor':lex})

                elif token == 'var':
                    saida.append({'tipo':'VAR','valor':lex})

                elif token in ['mais','menos','vezes','divide']:
                    pilha.append(token)

                self.avanca()
        else:
            abre_parent = ['(']
            self.avanca()
            while len(abre_parent):

                token, lex = self.atual()

                if token == 'abre_paren':
                    abre_parent.append('(')
                elif token == 'fecha_paren':
                    abre_parent.pop()

                if token == 'numero':
                    saida.append({'tipo':'NUM','valor':lex})

                elif token == 'var':
                    saida.append({'tipo':'VAR','valor':lex})

                elif token in ['mais','menos','vezes','divide']:
                    pilha.append(token)

                
                if token == 'maior_que':
                    opLogico = 'CPMA'
                elif token == 'menor_que':
                    opLogico = 'CPME'
                elif token == 'maior_igual':
                    opLogico = 'CMAI'
                elif token == 'menor_igual':
                    opLogico = 'CPMI'
                elif token == 'igual':
                    opLogico = 'CPIG'
                elif token == 'diferente':
                    opLogico = 'CDES'

                self.avanca()


        while pilha:
            saida.append({'tipo':'OP','valor':pilha.pop()})

        return saida, opLogico

