class Semantico:
	def __init__(self,tokens_lexemas):
		# [[token lexema], [token, lexema]]
	    # VAR, $cont
		self.tabelaSimbolos = {}
		self.codigo 		= tokens_lexemas
		self.i      		= -1
		self.startTabelaSimbolos()

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
		token, lexe = self.pega()
		self.i = self.i + 1
		if self.i < len(self.codigo)-1:
			return self.codigo[self.i][0], self.codigo[self.i][1]
		else:
			return token, lexe
	

	def volta(self):
		token, lexe = self.pega()
		self.i = self.i - 1
		if self.i >= 0:
			return self.codigo[self.i][0], self.codigo[self.i][1]
		else:
			return token, lexe
		
		
	def pega(self):
		return self.codigo[self.i][0], self.codigo[self.i][1] 

	def exibe(self):
		for k, v in self.tabelaSimbolos.items():
			print(k, v)

	def startTabelaSimbolos(self):
		escopos = ['GLOBAL']

		# pilhas auxiliares para verificar se estamos em um escopo ou se estamos dentro de uma expr de uma estrutura como if
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

			# mapeando somente todas variaveis globais e verificando se não estamos dentro de um parenteses de um if ou while, ai pega
			if (token == 'var' or (token == 'ident' and lexema not in ['floatval', 'readline'])) and (lexema, escopoAtual) not in self.tabelaSimbolos and escopoAtual == 'GLOBAL' and not len(instrucao_parenteses):
				self.tabelaSimbolos[(lexema, escopoAtual)] = {
					"tipo": token,
					"end_rel": posicao if token != 'ident' else -1,
					"end_proc": -1,
					"inicializado": False # ainda nao sabemos nessa parte do codigo
				}
				if token != 'ident':
					posicao = posicao + 1

		# agora pegar somente as variaveis dos escopos locais
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

			# mapeando agora todas variaveis locais e verificando se não estamos dentro de um parenteses de um if ou while, ai pega
			if token == 'var' and (lexema, escopoAtual) not in self.tabelaSimbolos and escopoAtual != 'GLOBAL' and not len(instrucao_parenteses):
				self.tabelaSimbolos[(lexema, escopoAtual)] = {
					"tipo": "var",
					"end_rel": posicao,
					"end_proc": -1,
					"inicializado": False # ainda nao sabemos nessa parte do codigo
				}

				posicao = posicao + 1


	def mapeiaEscopoVariavel(self, escopos):
		token, lexe = self.pega()
		# se acharmos o escopo local da variavel, ela pertence a ele, senao, provavelmente ao global
		if (token == 'var' and (lexe, escopos[-1]) in self.tabelaSimbolos):
			return escopos[-1]
		else:
			return 'GLOBAL'


	def verificaAtribuicao(self, escopos):
		token, lexe = self.avanca()
		# verificando toda a atribuicao e com isso verifica se existe alguma variavel não declarada ou se divide por 0
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
			1 verificar se uma variavel que está sendo utilizada foi inicializada 
			2 verificar se uma variavel não está sendo dividido por zero
			3 verificar se uma variavel está dentro do escopo
		"""
		escopos = ['GLOBAL']
		abriu_chaves = []
		dentro_parenteses_funcao = []
		dentro_parenteses_instrucao = []

		while self.i < len(self.codigo):
			token, lexem = self.avanca()

			# seção de pilhas: 
			# "escopos" e "abriu chaves", trabalham juntos
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

			# dentro de parenteses em uma instrucao é outra pilha auxilicar a verificação se uma variavel está dentro de um if, while
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

				# caso seja variaveis por parametro, assumir que vão vir com valores
				elif len(dentro_parenteses_funcao):
					self.tabelaSimbolos[(lexem, escopo)]['inicializado'] = True
					# quando for final de ) de uma funcao, voltar 1 posicao pois depois ali em cima, ele andaria novamente, e precisamos remover esse parenteses antes
					self.volta()
			
				# se estiver dentro de parenteses, entao verificar se a var foi inicializada
				elif len(dentro_parenteses_instrucao) and not self.tabelaSimbolos[(lexem, escopo)]['inicializado']:
					print(f'ERRO SEMÂNTICO: variável {lexem} dentro de instrução {dentro_parenteses_instrucao[-1]} não iniciada')
					return False

					
			elif token == 'echo':
				result = self.verificaAtribuicao(escopos)
				if not result:
					return False
				


		return True

					