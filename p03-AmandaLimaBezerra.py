from Lexer import lexer

class Parser:

  # Gerar o tokens, iniciar a posição do token e a lista de erros.
  def __init__(self):
    self.tokens = lexer()
    self.posicao = 0
    self.erros = []
    self.paser()
  
  # Pegar o token atual
  def token_atual(self):
    if self.posicao < len(self.tokens):
      return self.tokens[self.posicao]
    return 'EOF'
  
  # Consumir o token, se não for de acordo com expectativa chamar o modo pânico
  def consumir(self, token, expected):
    if token in expected:
      print('Consumido: ', token)
      self.posicao += 1
    else:
      print('Erro...Linha ', self.token_atual()[0:2])
      self.erros.append("Erro...Linha {:s}".format(self.token_atual()[0:2]))
      self.modo_panico()

  # Função principal
  def paser(self):
    self.main()
    if self.erros:
      print(self.erros)
      with open('Erros.txt', 'w', encoding='utf-8') as erros_arquivo:
        for item in self.erros:
          erros_arquivo.write(item + '\n')
    else:
      print('Sem erros!')

  # <main> ::= 'class' 'main' '{' <escopoMain> '}' | vazio  
  def main(self):
    if self.token_atual() == 'EOF':
      print('Arquivo vazio')
    else:
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['class'])
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['main'])
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['{'])
      self.escopoMain()
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['}'])

  # <escopoMain> ::= 'class' identificador '{' <defComeco2> '}' <escopoMain> | <defComeco> | vazio 
  def escopoMain(self):
    if self.token_atual()[7:len(self.token_atual())] == 'class':
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['class'])
      self.consumir(self.token_atual()[3:6], ['IDE'])
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['{'])
      self.escopoClass()
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['}'])
      self.escopoMain()
    elif self.token_atual()[7:len(self.token_atual())] == 'const':
      self.constante()
      self.escopoMain()
    elif self.token_atual()[7:len(self.token_atual())] == 'variables':
      self.variaveis()
      self.escopoMain()
    elif self.token_atual()[7:len(self.token_atual())] == 'methods':
      self.metodos()
      self.escopoMain()
    elif self.token_atual()[7:len(self.token_atual())] == 'print':
      self.print()
      self.escopoMain()
    elif self.token_atual()[7:len(self.token_atual())] == 'read':
      self.read()
      self.escopoMain()
    elif self.token_atual()[7:len(self.token_atual())] == 'if':
      self.comando_if()
      self.escopoMain()
    elif self.token_atual()[7:len(self.token_atual())] == 'for':
      self.comando_for()
      self.escopoMain()
    elif self.token_atual()[3:6] == 'IDE':
      self.consumir(self.token_atual()[3:6], ['IDE'])
      if self.token_atual()[7:len(self.token_atual())] == '[':
        self.atribuir_vetor_matriz()
      elif self.token_atual()[7:len(self.token_atual())] == '.':
        self.chamada_atributo()
        self.consumir(self.token_atual()[7:len(self.token_atual())], ['='])
        self.expressao()
        self.consumir(self.token_atual()[7:len(self.token_atual())], [';'])
      elif self.token_atual()[7:len(self.token_atual())] == '->':
        self.chamada_metodo()
        self.consumir(self.token_atual()[7:len(self.token_atual())], [';'])
      elif self.token_atual()[7:len(self.token_atual())] == '=':
        self.consumir(self.token_atual()[7:len(self.token_atual())], ['='])
        if self.token_atual()[3:6] == 'NRO':
          self.expressao()
        elif self.token_atual()[3:6] == 'IDE' or self.token_atual()[7:len(self.token_atual())] == 'main':
          self.consumir(self.token_atual()[3:6], ['IDE','PRE'])
          if self.token_atual()[7:len(self.token_atual())] == '->':
            self.chamada_metodo()
            self.expressao()
          elif self.token_atual()[7:len(self.token_atual())] in ['+','-','*','/','++','--','!=','==','<','<=','>','>=','!','&&','||']:
            self.expressao()
          elif self.token_atual()[7:len(self.token_atual())] == '.':
            self.chamada_atributo()
            self.expressao()
          elif self.token_atual()[7:len(self.token_atual())] == '[':
            self.acesso_vetor()
            self.expressao()
        elif self.token_atual()[7:len(self.token_atual())] == '(':
          self.expressao()
        self.consumir(self.token_atual()[7:len(self.token_atual())], [';'])
      self.escopoMain()

  # <defComeco2> ::= <defVar> <defComeco2> | <methods> <defComeco2> | <escopoMain2> | vazio  
  def escopoClass(self):
    if self.token_atual()[7:len(self.token_atual())] == 'class':
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['class'])
      self.consumir(self.token_atual()[3:6], ['IDE'])
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['{'])
      self.escopoClass()
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['}'])
      self.escopoMain()
    elif self.token_atual()[7:len(self.token_atual())] == 'variables':
      self.variaveis()
      self.escopoClass()
    elif self.token_atual()[7:len(self.token_atual())] == 'methods':
      self.metodos()
      self.escopoClass()
    elif self.token_atual()[7:len(self.token_atual())] == 'print':
      self.print()
      self.escopoClass()
    elif self.token_atual()[7:len(self.token_atual())] == 'read':
      self.read()
      self.escopoClass()
    elif self.token_atual()[7:len(self.token_atual())] == 'if':
      self.comando_if()
      self.escopoClass()
    elif self.token_atual()[7:len(self.token_atual())] == 'for':
      self.comando_for()
      self.escopoClass()
    elif self.token_atual()[3:6] == 'IDE':
      self.consumir(self.token_atual()[3:6], ['IDE'])
      if self.token_atual()[7:len(self.token_atual())] == '[':
        self.atribuir_vetor_matriz()
      elif self.token_atual()[7:len(self.token_atual())] == '.':
        self.chamada_atributo()
        self.consumir(self.token_atual()[7:len(self.token_atual())], ['='])
        self.expressao()
        self.consumir(self.token_atual()[7:len(self.token_atual())], [';'])
      elif self.token_atual()[7:len(self.token_atual())] == '->':
        self.chamada_metodo()
        self.consumir(self.token_atual()[7:len(self.token_atual())], [';'])
      elif self.token_atual()[7:len(self.token_atual())] == '=':
        self.consumir(self.token_atual()[7:len(self.token_atual())], ['='])
        if self.token_atual()[3:6] == 'NRO':
          self.expressao()
        elif self.token_atual()[3:6] == 'IDE' or self.token_atual()[7:len(self.token_atual())] == 'main':
          self.consumir(self.token_atual()[3:6], ['IDE','PRE'])
          if self.token_atual()[7:len(self.token_atual())] == '->':
            self.chamada_metodo()
            self.expressao()
          elif self.token_atual()[7:len(self.token_atual())] in ['+','-','*','/','++','--','!=','==','<','<=','>','>=','!','&&','||']:
            self.expressao()
          elif self.token_atual()[7:len(self.token_atual())] == '.':
            self.chamada_atributo()
            self.expressao()
          elif self.token_atual()[7:len(self.token_atual())] == '[':
            self.acesso_vetor()
            self.expressao()
        elif self.token_atual()[7:len(self.token_atual())] == '(':
          self.expressao()
        self.consumir(self.token_atual()[7:len(self.token_atual())], [';'])
      self.escopoClass()

  # <defConst> ::= 'const' '{' <listaConst> '}'
  def constante(self):
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['const'])
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['{'])
    self.lista_constante()
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['}'])

  # <defVar> ::= 'variables' '{' <listaConst> '}'
  def variaveis(self):
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['variables'])
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['{'])
    self.lista_constante()
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['}'])

  # <listaConst> ::= tipo <listaItens> ';' <listaConst> | <declVetor> | vazio
  def lista_constante(self):
    if self.token_atual()[3:6] == 'PRE':
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['int', 'float', 'boolean', 'string', 'void'])
      self.consumir(self.token_atual()[3:6], ['IDE'])
      if self.token_atual()[7:len(self.token_atual())] == '=' or self.token_atual()[7:len(self.token_atual())] == ',':
        self.lista_itens()
      elif self.token_atual()[7:len(self.token_atual())] == '[':
        self.vetor()   
      self.consumir(self.token_atual()[7:len(self.token_atual())], [';'])
      self.lista_constante()

  # <listaItens> ::= identificador <possFinal> <listaItens2>              
  # <listaItens2> ::= ',' identificador <possFinal> <listaItens2> 
  def lista_itens(self):
    if self.token_atual()[7:len(self.token_atual())] == '=':
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['='])
      self.valor()
      self.lista_itens()
    elif self.token_atual()[7:len(self.token_atual())] == ',':
      self.consumir(self.token_atual()[7:len(self.token_atual())], [','])
      self.valor()
      self.lista_itens()

  # <declVetor> ::= tipo identificador '[' <declVetor2> ']' <inicializacaoOpt> ';' | 
  # tipo identificador '[' <declVetor2> ']' '[' <declVetor2> ']' <inicializacaoOptMatriz> ';'
  # <declVetor2> ::= digito | numero 
  # <inicializacaoOpt> ::= '=' '{' <valores> '}' | 
  def vetor(self):
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['['])
    self.consumir(self.token_atual()[3:6], ['NRO', 'CAC'])
    self.consumir(self.token_atual()[7:len(self.token_atual())], [']'])
    if self.token_atual()[7:len(self.token_atual())] == '[':
      self.matriz()
    elif self.token_atual()[7:len(self.token_atual())] == '=':
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['='])
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['{'])
      self.valores()
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['}'])

  # <inicializacaoOptMatriz> ::= '=' '{' <linhaMatriz> | vazio
  def matriz(self):
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['['])
    self.consumir(self.token_atual()[3:6], ['NRO', 'CAC'])
    self.consumir(self.token_atual()[7:len(self.token_atual())], [']'])
    if self.token_atual()[7:len(self.token_atual())] == '=':
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['='])
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['{'])
      self.valores_matriz()
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['}'])

  # <valores> ::= <valorVetor> <valores_cont>
  # <valores_cont> ::= ',' <valorVetor> <valores_cont> | vazio
  # <valorVetor> ::= numero | digito | <acessovetor>
  def valores(self):
    if self.token_atual()[3:6] == 'IDE':
      self.consumir(self.token_atual()[3:6], ['IDE'])
      self.acesso_vetor()
    elif self.token_atual()[3:6] in ['NRO', 'CAC']:
      self.consumir(self.token_atual()[3:6], ['NRO', 'CAC'])
    if self.token_atual()[7:len(self.token_atual())] == ',':
      self.consumir(self.token_atual()[7:len(self.token_atual())], [','])
      self.valores()
  
  # <inicializacaoOptMatriz> ::= '=' '{' <linhaMatriz> | vazio   
  # <linhaMatriz> ::= '{' <valores> '}' ',' <linhaMatriz> | '{' <valores> '}' '}'
  def valores_matriz(self):
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['{'])
    self.valores()
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['}'])
    if self.token_atual()[7:len(self.token_atual())] == ',':
      self.consumir(self.token_atual()[7:len(self.token_atual())], [','])
      self.valores_matriz()

  # <methods> ::= 'methods' '{' <listaMetodos> '}'
  def metodos(self):
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['methods'])
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['{'])
    self.lista_metodos()
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['}'])
  
  # <listaMetodos> ::= tipo identificador '(' <listaParametros> ')' '{' <codigo> '}' | tipo identificador '(' <listaParametros> ')' '{' <codigo> '}' <listaMetodos>
  def lista_metodos(self):
    if self.token_atual()[3:6] == 'PRE':
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['int', 'float', 'boolean', 'string', 'void'])
      self.consumir(self.token_atual()[3:6], ['IDE'])
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['('])
      self.lista_paramentros()
      self.consumir(self.token_atual()[7:len(self.token_atual())], [')'])
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['{'])
      self.codigo()
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['}'])
      self.lista_metodos()

  # <listaParametros> ::= tipo identificador | tipo identificador ',' <listaParametros> | vazio
  def lista_paramentros(self):
    if self.token_atual()[3:6] == 'PRE':
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['int', 'float', 'boolean', 'string', 'void'])
      self.consumir(self.token_atual()[3:6], ['IDE'])
      if self.token_atual()[7:len(self.token_atual())] == ',':
        self.consumir(self.token_atual()[7:len(self.token_atual())], [','])
        self.lista_paramentros()

  # <codigo> ::= <defVar> <codigo>  
  #        | <comandoPrint> <codigo> 
  #        | <comandoRead> <codigo>
  #        | <comandoIf> <codigo>
  #        | 'return' <Expressao> ';'
  #        | 'return' ';'
  #        | identificador '=' <Expressao> ';' <codigo>
  #        | <atribvetor> <codigo>
  #        | <atribMatriz> <codigo>
  #        | <comandoFor> <codigo>
  #        | <chamadaAtributo> '=' <Expressao> ';' <codigo>
  #        | <chamadaMetodo> ';' <codigo>
  #        |
  def codigo(self):
    if self.token_atual()[7:len(self.token_atual())] == 'variables':
      self.variaveis()
      self.codigo()
    elif self.token_atual()[7:len(self.token_atual())] == 'print':
      self.print()
      self.codigo()
    elif self.token_atual()[7:len(self.token_atual())] == 'read':
      self.read()
      self.codigo()
    elif self.token_atual()[7:len(self.token_atual())] == 'if':
      self.comando_if()
      self.codigo()
    elif self.token_atual()[7:len(self.token_atual())] == 'for':
      self.comando_for()
      self.codigo()
    elif self.token_atual()[7:len(self.token_atual())] == 'return':
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['return'])
      if self.token_atual()[7:len(self.token_atual())] == ';':
        self.consumir(self.token_atual()[7:len(self.token_atual())], [';'])
      elif self.token_atual()[3:6] in ['NRO','IDE']:
        self.consumir(self.token_atual()[3:6], ['NRO','IDE'])
        if self.token_atual()[7:len(self.token_atual())] == ';':
          self.consumir(self.token_atual()[7:len(self.token_atual())], [';'])
        elif self.token_atual()[7:len(self.token_atual())] in ['+','-','*','/','++','--','!=','==','<','<=','>','>=','&&','||','!']:
          self.expressao()
          self.consumir(self.token_atual()[7:len(self.token_atual())], [';'])
    elif self.token_atual()[3:6] == 'IDE':
      self.consumir(self.token_atual()[3:6], ['IDE'])
      if self.token_atual()[7:len(self.token_atual())] == '[':
        self.atribuir_vetor_matriz()
      elif self.token_atual()[7:len(self.token_atual())] == '.':
        self.chamada_atributo()
        self.consumir(self.token_atual()[7:len(self.token_atual())], ['='])
        self.expressao()
        self.consumir(self.token_atual()[7:len(self.token_atual())], [';'])
      elif self.token_atual()[7:len(self.token_atual())] == '->':
        self.chamada_metodo()
        self.consumir(self.token_atual()[7:len(self.token_atual())], [';'])
      elif self.token_atual()[7:len(self.token_atual())] == '=':
        self.consumir(self.token_atual()[7:len(self.token_atual())], ['='])
        if self.token_atual()[3:6] == 'NRO':
          self.expressao()
        elif self.token_atual()[3:6] == 'IDE' or self.token_atual()[7:len(self.token_atual())] == 'main':
          self.consumir(self.token_atual()[3:6], ['IDE', 'PRE'])
          if self.token_atual()[7:len(self.token_atual())] == '->':
            self.chamada_metodo()
            self.expressao()
          elif self.token_atual()[7:len(self.token_atual())] in ['+','-','*','/','++','--','!=','==','<','<=','>','>=','!','&&','||']:
            self.expressao()
          elif self.token_atual()[7:len(self.token_atual())] == '.':
            self.chamada_atributo()
            self.expressao()
          elif self.token_atual()[7:len(self.token_atual())] == '[':
            self.acesso_vetor()
            self.expressao()
        elif self.token_atual()[7:len(self.token_atual())] == '(':
          self.expressao()
        self.consumir(self.token_atual()[7:len(self.token_atual())], [';'])
      self.codigo()

  def expressao(self):
    if self.token_atual()[7:len(self.token_atual())] == '(':
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['('])
      self.expressao() # 1
      self.consumir(self.token_atual()[7:len(self.token_atual())], [')'])
      self.expressao()
    elif self.token_atual()[7:len(self.token_atual())] == '!':
      self.expressao_logica()
    elif self.token_atual()[3:6] in ['IDE','NRO']:
      self.consumir(self.token_atual()[3:6], ['IDE','NRO'])
      self.expressao()
    elif self.token_atual()[7:len(self.token_atual())] in ['+','-','*','/','++','--']:
      self.expressao_aritmetica()
    elif self.token_atual()[7:len(self.token_atual())] in ['!=','==','<','<=','>','>=']:
      self.expressao_relacional() 
    elif self.token_atual()[7:len(self.token_atual())] in ['!','&&','||']:
      self.expressao_logica()
    elif self.token_atual()[7:len(self.token_atual())] == '[':
      self.acesso_vetor()
      self.expressao()
    elif self.token_atual()[7:len(self.token_atual())] == '->':
      self.chamada_metodo()
      self.expressao()
    elif self.token_atual()[7:len(self.token_atual())] == '.':
      self.chamada_atributo()
      self.expressao()

  def expressao_logica(self):
    if self.token_atual()[7:len(self.token_atual())] == '(':
      self.expressao()
    elif self.token_atual()[7:len(self.token_atual())] in ['&&','||']:
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['&&','||'])
      self.expressao_logica()
    elif self.token_atual()[3:6] in ['IDE', 'NRO'] or self.token_atual()[7:len(self.token_atual())] == 'true' or self.token_atual()[7:len(self.token_atual())] == 'false' or self.token_atual()[7:len(self.token_atual())] == 'main':
      self.consumir(self.token_atual()[3:6], ['IDE', 'NRO','PRE'])
      self.expressao()
    elif self.token_atual()[7:len(self.token_atual())] == '!':
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['!'])
      if self.token_atual()[3:6] in ['IDE', 'NRO']:
        self.consumir(self.token_atual()[3:6], ['IDE', 'NRO'])
      elif self.token_atual()[7:len(self.token_atual())] == 'main':
        self.consumir(self.token_atual()[3:6], ['PRE'])
      self.expressao()

  def expressao_relacional(self):
    if self.token_atual()[7:len(self.token_atual())] == '(':
      self.expressao()
    elif self.token_atual()[7:len(self.token_atual())] in ['!=','==','<','<=','>','>=']:
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['!=','==','<','<=','>','>='])
      self.expressao_relacional()
    elif self.token_atual()[3:6] in ['IDE', 'NRO']:
      self.consumir(self.token_atual()[3:6], ['IDE', 'NRO'])
      self.expressao()
    elif self.token_atual()[7:len(self.token_atual())] == '!':
      self.expressao_logica()
    
  def expressao_aritmetica(self):
    if self.token_atual()[7:len(self.token_atual())] == '(':
      self.expressao()
    elif self.token_atual()[7:len(self.token_atual())] in ['++','--']:
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['++','--'])
      if self.token_atual()[7:len(self.token_atual())] in ['+','-','*','/']:
        self.consumir(self.token_atual()[7:len(self.token_atual())], ['+','-','*','/'])
      self.expressao_aritmetica()
    elif self.token_atual()[7:len(self.token_atual())] in ['+','-','*','/']:
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['+','-','*','/'])
      self.expressao_aritmetica()
    elif self.token_atual()[3:6] in ['IDE','NRO']:
      self.consumir(self.token_atual()[3:6], ['IDE','NRO'])
      self.expressao()

  # <comandoPrint> ::= 'print' '(' <listaArgumentos> ')' ';'
  def print(self):
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['print'])
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['('])
    self.lista_argumentos()
    self.consumir(self.token_atual()[7:len(self.token_atual())], [')'])
    self.consumir(self.token_atual()[7:len(self.token_atual())], [';'])
  
  # <listaArgumentos> ::= <conteudoPrint> <listaArgumentos2> 
  # <listaArgumentos2> ::= ',' <conteudoPrint> <listaArgumentos2> | vazio 
  def lista_argumentos(self):
    self.valor()
    if self.token_atual()[7:len(self.token_atual())] == ',':
      self.consumir(self.token_atual()[7:len(self.token_atual())], [','])
      self.lista_argumentos()

  # <comandoRead> ::= 'read' '(' <listaArgumentosRead> ')' ';'
  def read(self):
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['read'])
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['('])
    self.conteudo_read()
    self.consumir(self.token_atual()[7:len(self.token_atual())], [')'])
    self.consumir(self.token_atual()[7:len(self.token_atual())], [';'])

  # <conteudoRead> ::= identificador | <acessoVetor> | <chamadaAtributo>
  def conteudo_read(self):
    self.consumir(self.token_atual()[3:6], ['IDE'])
    if self.token_atual()[7:len(self.token_atual())] == '.':
      self.chamada_atributo()
    elif self.token_atual()[7:len(self.token_atual())] == '[':
      self.acesso_vetor()

  # <valor> ::= numero | digito | cadeiaCaracteres | valBool | identificador | <acessoVetor> | <chamadaAtributo> | <chamadaMetodo>
  def valor(self):
    if self.token_atual()[3:6] in ['NRO','CAC','IDE','PRE']:
      if self.token_atual()[7:len(self.token_atual())] == 'main':
        self.consumir(self.token_atual()[7:len(self.token_atual())], ['main'])
        self.chamada_metodo()
      else:
        self.consumir(self.token_atual()[3:6], ['NRO','CAC','IDE','PRE'])
        if self.token_atual()[7:len(self.token_atual())] == '[':
          self.acesso_vetor()
        elif self.token_atual()[7:len(self.token_atual())] == '.':
          self.chamada_atributo()
        elif self.token_atual()[7:len(self.token_atual())] == '->':
          self.chamada_metodo()
    elif self.token_atual()[7:len(self.token_atual())] == 'true' or self.token_atual()[7:len(self.token_atual())] == 'false':
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['true', 'false'])

  # <acessovetor> ::= identificador '[' numero ']' | identificador '[' digito ']'
  def acesso_vetor(self):
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['['])
    self.consumir(self.token_atual()[3:6], ['NRO'])
    self.consumir(self.token_atual()[7:len(self.token_atual())], [']'])
    if self.token_atual()[7:len(self.token_atual())] == '[':
      self.acesso_matriz()

  # <indicesMatriz> ::= identificador '[' digito ']' '[' digito ']'
  def acesso_matriz(self):
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['['])
    self.consumir(self.token_atual()[3:6], ['NRO'])
    self.consumir(self.token_atual()[7:len(self.token_atual())], [']'])

  # <chamadaAtributo> ::= identificador '.' identificador
  def chamada_atributo(self):
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['.'])
    self.consumir(self.token_atual()[3:6], ['IDE'])

  # <chamadaMetodo> ::= <classeMetodo> '->' identificador '(' <args> ')'
  def chamada_metodo(self):
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['->'])
    self.consumir(self.token_atual()[3:6], ['IDE'])
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['('])
    self.lista_argumentos()
    self.consumir(self.token_atual()[7:len(self.token_atual())], [')'])

  # <comandoIf> ::= 'if' '(' <Expressao> ')' '{' <codigo> '}' <opcionalElse>
  # <opcionalElse> ::= 'else' '{' <codigo> '}' | vazio
  def comando_if(self):
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['if'])
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['('])
    self.expressao()
    self.consumir(self.token_atual()[7:len(self.token_atual())], [')'])
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['{'])
    self.codigo()
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['}'])
    if self.token_atual()[7:len(self.token_atual())] == 'else':
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['else'])
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['{'])
      self.codigo()
      self.consumir(self.token_atual()[7:len(self.token_atual())], ['}'])

  # <comandoFor> ::= 'for' '(' <valor> ';' <Expressao> ';' <Expressao> ')' '{' <codigo> '}'
  def comando_for(self):
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['for'])
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['('])
    self.valor()
    self.consumir(self.token_atual()[7:len(self.token_atual())], [';'])
    self.expressao()
    self.consumir(self.token_atual()[7:len(self.token_atual())], [';'])
    self.expressao()
    self.consumir(self.token_atual()[7:len(self.token_atual())], [')'])
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['{'])
    self.codigo()
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['}'])

  # <atribvetor> ::= <acessovetor> '=' <Expressao> ';'
  # <acessovetor> ::= identificador '[' numero ']' | identificador '[' digito ']'
  # <atribMatriz> ::= <indicesMatriz> '=' <Expressao> ';'
  def atribuir_vetor_matriz(self):
    self.acesso_vetor()
    self.consumir(self.token_atual()[7:len(self.token_atual())], ['='])
    self.expressao()
    self.consumir(self.token_atual()[7:len(self.token_atual())], [';'])

  def modo_panico(self):
    print('ENTROU NO MODO PANICO!')

vamos = Parser()