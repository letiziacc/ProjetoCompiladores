class Semantico:
	def __init__(self,tokens_lexemas):
		
		self.tabelaSimbolos = {} # Tabela de símbolos (armazena variáveis e funções)
		self.codigo 		= tokens_lexemas # Lista de tokens e lexemas (vinda do léxico)
		self.i      		= -1 # Ponteiro para percorrer o código
		self.startTabelaSimbolos() # Inicia o mapeamento das variáveis

	# $a = $b
	# func c(){ 
	#	$a;
	#}
	# func d(){ 
	#	$f;
	#}
	# $t;
	# c()
	# d()

	"""
	0 $a
	1 $b
	2 $t
	3 $a
	3 $f
	"""	

	def avanca(self):
		# Avança para o próximo token
		token, lexe = self.pega()
		self.i = self.i + 1
		if self.i < len(self.codigo)-1:
			return self.codigo[self.i][0], self.codigo[self.i][1]
		else:
			return token, lexe
	

	def volta(self):
		# Volta/retrocede um token
		token, lexe = self.pega()
		self.i = self.i - 1
		if self.i >= 0:
			return self.codigo[self.i][0], self.codigo[self.i][1]
		else:
			return token, lexe
		
		
	def pega(self):
		# Pega o token atual
		return self.codigo[self.i][0], self.codigo[self.i][1] 

	def exibe(self):
		# Exibe a tabela de símbolos
		for k, v in self.tabelaSimbolos.items():
			print(k, v)

	def startTabelaSimbolos(self):
		# Criação da tabela
		escopos = ['GLOBAL']

		abriu_chaves = []
		instrucao_parenteses = []
		
		posicao = 0
		for i, c in enumerate(self.codigo):
			token = c[0]
			lexema = c[1]

			if token in ['if', 'while']:
				instrucao_parenteses.append('(')
			
			if token == 'fecha_paren' and len(instrucao_parenteses):
				instrucao_parenteses.pop()

			if token == 'function':
				escopos.append(self.codigo[i+1][1])

			if token == "abre_chave" and len(escopos) > 1:
				abriu_chaves.append('{')

			if token == 'fecha_chave':
				if len(escopos) > 1 and len(abriu_chaves) == 1:
					escopos.pop()
				if len(abriu_chaves) > 0:
					abriu_chaves.pop()

			if token == 'ident':
				escopoAtual = 'GLOBAL'
			else:
				escopoAtual = escopos[len(escopos)-1]

			# Adiciona as variáveis globais
			if (token == 'var' or (token == 'ident' and lexema not in ['floatval', 'readline'])) and (lexema, escopoAtual) not in self.tabelaSimbolos and escopoAtual == 'GLOBAL' and not len(instrucao_parenteses):
				self.tabelaSimbolos[(lexema, escopoAtual)] = {
					"tipo": token,
					"end_rel": posicao if token != 'ident' else -1,
					"end_proc": -1,
					"inicializado": False 
				}
				if token != 'ident':
					posicao = posicao + 1

		# Pega as variáveis dos escopos locais
		ultimaPosicaoGlobal = posicao
		abriu_chaves = []
		instrucao_parenteses = []

		for i, c in enumerate(self.codigo):
			token = c[0]
			lexema = c[1]

			if token in ['if', 'while']:
				instrucao_parenteses.append('(')
			
			if token == 'fecha_paren' and len(instrucao_parenteses):
				instrucao_parenteses.pop()

			if token == 'function':
				posicao = ultimaPosicaoGlobal  
				escopos.append(self.codigo[i+1][1])

			if token == "abre_chave" and len(escopos) == 1:
				abriu_chaves.append('{')

			if token == 'fecha_chave':
				if len(escopos) > 1 and not len(abriu_chaves):
					escopos.pop()

				if len(abriu_chaves) > 0:
					abriu_chaves.pop()

				

			escopoAtual = escopos[len(escopos)-1]

			# Adiciona as variáveis locais
			if token == 'var' and (lexema, escopoAtual) not in self.tabelaSimbolos and escopoAtual != 'GLOBAL' and not len(instrucao_parenteses):
				self.tabelaSimbolos[(lexema, escopoAtual)] = {
					"tipo": "var",
					"end_rel": posicao,
					"end_proc": -1,
					"inicializado": False 
				}

				posicao = posicao + 1


	def mapeiaEscopoVariavel(self, escopos):
		token, lexe = self.pega()
		
		if (token == 'var' and (lexe, escopos[-1]) in self.tabelaSimbolos):
			return escopos[-1]
		else:
			return 'GLOBAL'


	def verificaAtribuicao(self, escopos):
		token, lexe = self.avanca()
		# Verifica toda a atribuição e com isso verifica se existe alguma variavel não declarada ou se divide por 0
		while lexe != ';':
			if token == 'var':
				escopo = self.mapeiaEscopoVariavel(escopos)
				if ((lexe, escopo) in self.tabelaSimbolos and self.tabelaSimbolos[(lexe, escopo)]['inicializado'] == False):
					print(f'ERRO SEMÂNTICO: váriavel não iniciada: {lexe}')
					return False
				if token == 'divide':
					_, lexe = self.avanca()
					if lexe == 0:
						print(f'ERRO SEMÂNTICO: váriavel {lexe} não pode ser dividida por zero')
						return False	
			
			token, lexe = self.avanca()

		return True
			


	def regrasSemanticas(self):
		"""
			1 verificar se uma variável que está sendo utilizada foi inicializada 
			2 verificar se uma variável não está sendo dividida por zero
			3 verificar se uma variável está dentro de algum escopo
		"""
		escopos = ['GLOBAL']
		abriu_chaves = []
		dentro_parenteses_funcao = []
		dentro_parenteses_instrucao = []

		while self.i < len(self.codigo):
			token, lexem = self.avanca()

			# Seção de pilhas: 
			
			if token == 'function':
				token, lexem = self.avanca()
				escopos.append(lexem)
				abriu_chaves.append('{')
				dentro_parenteses_funcao.append('(')

			elif token == 'fecha_chave':
				if len(escopos) == 1:
					escopos.pop()
				if len(abriu_chaves) > 0:
					abriu_chaves.pop()

			
			elif token in ['if', 'while']:
				dentro_parenteses_instrucao.append(token)

			elif token == 'fecha_paren':
				if len(dentro_parenteses_funcao):
					dentro_parenteses_funcao.pop()
				else:
					dentro_parenteses_instrucao.pop()

			elif token == 'var':
				escopo = self.mapeiaEscopoVariavel(escopos)
				token_avanc, _ = self.avanca()
				if token_avanc == 'atribuicao':
					result = self.verificaAtribuicao(escopos)
					if result:
						self.tabelaSimbolos[(lexem, escopo)]['inicializado'] = True
					else:
						return False
					
				elif token_avanc == 'ponto_virgula':
					self.tabelaSimbolos[(lexem, escopo)]['inicializado'] = False

				elif len(dentro_parenteses_funcao):
					self.tabelaSimbolos[(lexem, escopo)]['inicializado'] = True
					self.volta()
			
				elif len(dentro_parenteses_instrucao) and not self.tabelaSimbolos[(lexem, escopo)]['inicializado']:
					print(f'ERRO SEMÂNTICO: variável {lexem} dentro de instrução {dentro_parenteses_instrucao[-1]} não iniciada')
					return False

					
			elif token == 'echo':
				result = self.verificaAtribuicao(escopos)
				if not result:
					return False
				


		return True

					