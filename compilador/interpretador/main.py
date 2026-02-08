class Interpretador:

    def __init__(self, codigo):
        self.codigo = codigo
        self.D = []     # pilha de dados
        self.C = []     # pilha de controle (retorno)
        self.pc = 0

    # ----------------------

    def topo(self):
        return self.D[-1]

    def empilha(self, v):
        self.D.append(v)

    def desempilha(self):
        return self.D.pop()

    # ----------------------

    def executa(self):

        while self.pc < len(self.codigo):

            instr = self.codigo[self.pc].split()
            op = instr[0]

            # ======================
            # CONTROLE
            # ======================

            if op == 'INPP':
                self.pc += 1


            elif op == 'PARA':
                break


            elif op == 'DSVI':
                self.pc = int(instr[1])


            elif op == 'DSVF':
                destino = int(instr[1])
                cond = self.desempilha()

                if cond == 0:
                    self.pc = destino
                else:
                    self.pc += 1


            # ======================
            # PILHA DE DADOS
            # ======================

            elif op == 'ALME':
                qnt = int(instr[1])
                for _ in range(qnt):
                    self.empilha(0)
                self.pc += 1


            elif op == 'DESM':
                qnt = int(instr[1])
                for _ in range(qnt):
                    self.desempilha()
                self.pc += 1


            elif op == 'CRCT':
                self.empilha(float(instr[1]))
                self.pc += 1


            elif op == 'CRVL':
                end = int(instr[1])
                self.empilha(self.D[end])
                self.pc += 1


            elif op == 'ARMZ':
                end = int(instr[1])
                valor = self.desempilha()
                self.D[end] = valor
                self.pc += 1


            # ======================
            # ARITMÉTICA
            # ======================

            elif op == 'SOMA':
                b = self.desempilha()
                a = self.desempilha()
                self.empilha(a + b)
                self.pc += 1


            elif op == 'SUBT':
                b = self.desempilha()
                a = self.desempilha()
                self.empilha(a - b)
                self.pc += 1


            elif op == 'MULT':
                b = self.desempilha()
                a = self.desempilha()
                self.empilha(a * b)
                self.pc += 1


            elif op == 'DIVI':
                b = self.desempilha()
                a = self.desempilha()
                self.empilha(a / b)
                self.pc += 1


            # ======================
            # COMPARAÇÃO
            # ======================

            elif op == 'CPMA':
                b = self.desempilha()
                a = self.desempilha()
                self.empilha(1 if a > b else 0)
                self.pc += 1


            elif op == 'CPME':
                b = self.desempilha()
                a = self.desempilha()
                self.empilha(1 if a < b else 0)
                self.pc += 1


            elif op == 'CMAI':
                b = self.desempilha()
                a = self.desempilha()
                self.empilha(1 if a >= b else 0)
                self.pc += 1


            elif op == 'CPMI':
                b = self.desempilha()
                a = self.desempilha()
                self.empilha(1 if a <= b else 0)
                self.pc += 1


            elif op == 'CPIG':
                b = self.desempilha()
                a = self.desempilha()
                self.empilha(1 if a == b else 0)
                self.pc += 1


            elif op == 'CDES':
                b = self.desempilha()
                a = self.desempilha()
                self.empilha(1 if a != b else 0)
                self.pc += 1


            # ======================
            # PROCEDIMENTOS
            # ======================

            elif op == 'PUSHER':
                retorno = int(instr[1])
                self.C.append(retorno)
                self.pc += 1


            elif op == 'PARAM':
                end = int(instr[1])

                # copia o valor real da pilha D
                self.empilha(self.D[end])
                self.pc += 1


            elif op == 'CHPR':
                destino = int(instr[1])
                self.pc = destino


            elif op == 'RTPR':
                self.pc = self.C.pop()


            # ======================
            # I/O
            # ======================

            elif op == 'IMPR':
                print(self.desempilha())
                self.pc += 1


            elif op == 'LEIT':
                v = float(input())
                self.empilha(v)
                self.pc += 1


            else:
                raise Exception(f"Instrução inválida: {self.codigo[self.pc]}")
