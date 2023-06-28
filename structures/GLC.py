class GLC():
    """
    Uma classe para representar uma Gramática Livre de Contexto.
    
    ...

    Atributos
    ---------
    nao_terminais : List
        Lista de não terminais.
        
    terminais : List
        Lista de terminais.
    
    producoes : List
        Lista que mapeia as produções.
    
    simbolo_inicial : Str
        Símbolo inicial da gramática.

    mapeamento : Dict
        Dicionário que mapea as produções.

    tabela_analise : Multi List
        Tabela criada para análise da gramática.
    
    Métodos
    -------
    
    """
    def __init__(self, nao_terminais, terminais, producoes, simbolo_inicial):
        self.nao_terminais = nao_terminais
        self.terminais = terminais
        self.producoes = producoes
        self.simbolo_inicial = simbolo_inicial
        self.mapeamento = None
        if type(producoes) != dict:
            self._arrumar_producoes()
        self.tabela_analise = criar_tabela_de_analise(self)

    def get_nao_terminais(self):
        return self.nao_terminais

    def get_terminais(self):
        return self.terminais

    def get_simbolo_inicial(self):
        return self.simbolo_inicial

    def get_producoes(self):
        return self.producoes

    def _arrumar_producoes(self):
        novas_producoes = {}
        novas_producoes[self.simbolo_inicial] = []
        for simbolo in self.nao_terminais:
            novas_producoes[simbolo] = []
        for producao in self.producoes:
            par = producao.split('->')
            novas_producoes[par[0]].append(par[1])
        self.producoes = novas_producoes

    def display(self):
        print('Terminais (T): ', ', '.join(self.terminais))
        print('Não-terminais (N): ', ', '.join(self.nao_terminais))
        print('Símbolo inicial (S): ', self.simbolo_inicial)
        print('Produções:')
        for simb, prod in self.producoes.items():
            print(f'{simb} -> {" | ".join(prod)}')

    def reconhecer(self, sentenca):
        if self.tabela_analise == None:
            print("Erro: Não foi possível criar a tabela de análise porque a GLC não é LL(1)")
            return False
        # INSERIR: APPEND
        # RETIRAR: POP
        # TOPO: STACK[len(stack)-1]
        sentenca += '$'
        sentenca = split_into_symbols(sentenca,self.terminais + ['$'],self.nao_terminais)
        stack = []
        stack.append('$')
        stack.append(self.simbolo_inicial)

        # INDICE PARA AVALIAR A SENTENCA
        cabecote = 0
        while(True):
            print(stack)
            topo = stack[len(stack)-1]
            if topo == sentenca[cabecote]:
                # Aceite
                if topo == '$':
                    return True
                # TOPO == CABECOTE != $
                if topo in self.terminais:
                    # DESEMPILHE O TOPO
                    antigo_topo = stack.pop()
                    # AVANCA NA ENTRADA
                    cabecote += 1
                else:
                    print("ERRO: Esperava um terminal no topo e no cabeçote")
                    return False
            elif topo in self.nao_terminais and sentenca[cabecote] in self.terminais:
                acao = self.tabela_analise[topo][sentenca[cabecote]]
                if acao == -1:
                    print("ERRO: Tabela[%s][%s] = Erro" % (topo, sentenca[cabecote]))
                    return False
                else:
                    # RETIRA O TOPO DA PILHA
                    stack.pop()
                    producao = self.mapeamento[acao]
                    simbolos = producao.split('->')
                    corpo = ''.join(simbolos[1::])
                    corpo = split_into_symbols(corpo,self.terminais + ['$'],self.nao_terminais)
                    if corpo != ['&']:
                        while(corpo != []):
                            stack.append(corpo.pop())
            else:
                return False

def criar_tabela_de_analise(glc):
    firsts = calculate_firsts(glc)

    follows = calculate_follows(glc, firsts)

    intersections = isLL1(glc.get_nao_terminais(), firsts, follows)

    if len(intersections) != 0:
        print('ERRO: A gramática não é LL(1)')
        print("Existe interseção entre os conjuntos First e Follow nos seguintes não-terminais: ", intersections)
        return None

    map = map_productions(glc)
    glc.mapeamento = map
    analysis_table = init_analysis_table(glc.get_terminais(), glc.get_nao_terminais())

    # PREENCHENDO A TABELA DE ANALISE
    # ANALISAR SE JÁ NAO EXISTE UMA ENTRADA DEFINIDA QUANDO FOR COLOCAR ALGO
    # SE EXISTIR, INDIQUE QUE HOUVE CONFLITO NA CÉLULA
    for non_terminal in analysis_table.keys():
        for production in glc.producoes[non_terminal]:
            number = map[non_terminal+'->'+production]
            symbols_alfa = split_into_symbols(production, glc.get_terminais(), glc.get_nao_terminais())
            first_alfa = first_of_sequence(production, firsts, symbols_alfa)
            for a in (first_alfa - set('&')):
                if analysis_table[non_terminal][a] == -1:
                    analysis_table[non_terminal][a] = number
                else:
                    # CONFLITO
                    print("Conflito em T[%s,%s]" % (non_terminal,a))
                    return None
            if '&' in first_alfa:
                for b in follows[non_terminal]:
                    if analysis_table[non_terminal][b] == -1:
                        analysis_table[non_terminal][b] = number
                    else:
                        print("Conflito em T[%s,%s]" % (non_terminal,b))
                        return None
    print("===== TABELA DE ANALISE =====")
    columns = list(analysis_table.keys())
    rows = list(analysis_table[columns[1]].keys())

    # Exibir cabeçalho da tabela invertida
    print('{:<4}'.format(''), end='')  # Espaço em branco no canto superior esquerdo
    for row in rows:
        print('{:<4}'.format(row), end='')
    print()

    # Exibir linhas da tabela invertida
    for col in columns[1:]:
        print('{:<4}'.format(col), end='')
        for row in rows:
            print('{:<4}'.format(analysis_table[col][row]), end='')
        print()
    return analysis_table


def isLL1(N, firsts, follows):
    intersections = []
    for non_terminal in N:
        if firsts[non_terminal].intersection(follows[non_terminal]) != set():
            intersections.append(non_terminal)
    return intersections

def init_analysis_table(T, N):
    analysis_table = dict()
    T.append('$')
    for non_terminal in N:
        analysis_table[non_terminal] = dict()
        for terminal in T:
            analysis_table[non_terminal][terminal] = -1
    return analysis_table

def map_productions(glc):
    map = dict()
    i = 0
    for non_terminal in glc.nao_terminais:
        for production in glc.producoes[non_terminal]:
            value = non_terminal+'->'+production
            map[value] = i
            map[i] = value
            i += 1
    return map

def calculate_firsts(glc):
    # CALCULA O FIRST PARA CADA SÍMBOLO   
    #{X : FIRST(X) for X} in (N U T)
    first = {s: set((s,)) for s in glc.terminais + ['&']}
    for X in glc.nao_terminais:
        first[X] = set()

    new_added = True
    while new_added:
        new_added = False
        for head, bodies in glc.producoes.items():
            for body in bodies:
                symbol = get_first_symbol(body, glc.terminais, glc.nao_terminais)

                if symbol in glc.terminais + ['&']:
                    new_first = first[head].union(first[symbol])

                elif symbol in glc.nao_terminais:
                    f = first[symbol]
                    new_first = first[head].union(f - set('&'))

                    while '&' in f:
                        # PEGA O CORPO DA PRODUCAO SEM O PRIMEIRO SÍMBOLO
                        body = body[len(symbol):]
                        if body == '':
                            new_first = new_first.union('&')
                            break

                        symbol = get_first_symbol(body, glc.terminais, glc.nao_terminais)
                        f = first[symbol]
                        new_first = new_first.union(f - set('&'))

                else:
                    raise Exception(f'Symbol {symbol} not in GLC (N U T)')

                if new_first != first[head]:
                    new_added = True
                    first[head] = new_first

    return first

def split_into_symbols(body, T, N):
    # DIVIDE O CORPO DE UMA PRODUÇÃO EM UMA LISTA DE SÍMBOLOS EM T U N
    symbols = []
    while len(body) > 0:
        symbol = get_first_symbol(body, T, N)
        symbols.append(symbol)

        body = body[len(symbol) :]

    return symbols

def get_first_symbol(body, T, N):
    # OBTEM O PRIMEIRO SÍMBOLO DO CORPO DE UMA PRODUÇÃO
    # CORRESPONDE A UM SÍMBOLO EM T U N
    symbols = T + N
    symbols.append('&')
    for i, _ in enumerate(body):
        if body[: i + 1] in symbols:
            return body[: i + 1]

    return body


def calculate_follows(glc, firsts=None):
    # CALCULA O FOLLOW PARA CADA SÍMBOLO   
    # {X : FOLLOW(X) for X} in (N U T)

    # DEVE CALCULAR O FIRST SE AINDA NÃO EXISTE
    if firsts is None:
        firsts = calculate_firsts(glc)

    follows = {s: set(()) for s in glc.nao_terminais}
    follows[glc.simbolo_inicial] = set('$')

    # DICIONARIO PARA GUARDAR OS CASOS: FOLLOW(A) EM FOLLOW(B)
    # SERA GUARDADADA DESSA FORMA: inside[A] = [B]
    inside = {n: set(()) for n in glc.nao_terminais}


    new_added = True
    while(new_added):
        new_added = False
        for head, bodies in glc.producoes.items():
            for body in bodies:
                symbols = split_into_symbols(body, glc.terminais, glc.nao_terminais)
                for i in range(len(symbols)):
                    # CASO 1: PRODUCAO X -> aBC ou X -> ABC
                    if symbols[i] in glc.nao_terminais:
                        target = symbols[i]
                        # PARA VERIFICAR SE HOUVE MUDANCA
                        old = follows[target]

                        beta = ''.join(symbols[i+1:])
                        # CASO 1.1: BETA É DIFERENTE DA SENTENCA VAZIA
                        # ACAO: FIRST(BETA)/{&} EM FOLLOW(TARGET)
                        if beta != '':
                            symbols_beta = split_into_symbols(beta, glc.terminais, glc.nao_terminais)
                            first_beta = first_of_sequence(beta, firsts, symbols_beta)

                            # FIRST(BETA)\{&} EM FOLLOW(TARGET)
                            follows[target].update((first_beta - set('&')))
                            if '&' in first_beta:
                                # FOLLOW(HEAD) EM FOLLOW(TARGET)
                                if head != target:
                                    inside[head].add(target)
                        # CASO 1.2: BETA É IGUAL A SENTENCA VAZIA (X->alfaB)
                        # ACAO: FOLLOW(HEAD) EM FOLLOW(TARGET)
                        else:
                            if head != target:
                                inside[head].add(target)
                        if old != follows[target]:
                            new_added = True

    new_added = True
    while(new_added):
        new_added = False
        for non_terminal in inside.keys():
            for dependent in inside[non_terminal]:
                old = follows[dependent]
                follows[dependent].update(follows[non_terminal])
                if old != follows[dependent]:
                    new_added = True
    return follows

# Se A→αBβ, ENTÃO TUDO EM FIRST(β) EXCETO & ESTÁ EM FOLLOW(B).
def first_of_sequence(beta, firsts, symbols):
    first_sequence = set()
    for i in range(len(symbols)):
        # print(firsts[symbols[i]])
        if '&' not in firsts[symbols[i]]:
            first_sequence.update(firsts[symbols[i]])
            break
        first_sequence.update((firsts[symbols[i]] - set('&')))
        if i == len(symbols) - 1:
            first_sequence.add('&')
    return first_sequence

def fatorar(glc):
    j = 0
    # RESOLVE PRIMEIRO O NAO DETERMINISMO DIRETO
    for nao_terminal in glc.nao_terminais:
        j = resolver_nao_determinismo_direto(glc, nao_terminal, j)
    # SE ENCONTRAR UMA NAO DETERMINISMO INDIRETO, RESOLVA-O
    # print(glc.producoes)
    contador = 0
    for nao_terminal in glc.nao_terminais:
        if contador > 10:
            print(" ERRO: Não foi possível fatorar a gramática.")
            return False
        existe_nao_determinismo_indireto = encontrar_nao_determinismo_indireto(glc, nao_terminal)
        if existe_nao_determinismo_indireto:
            print("existe não determinismo indireto")
            contador += 1
            j = resolver_nao_determinismo_direto(glc, nao_terminal, j)


def remover_recursao_esquerda_indireta(glc):
    novas_producoes = {N : [] for N in glc.nao_terminais}
    for i, Ai in enumerate(glc.nao_terminais):
        for j in range(i):
            Aj = glc.nao_terminais[j]
            for prodAi in glc.producoes[Ai]:
                if Aj == prodAi[: len(Aj)]:
                    glc.producoes[Ai].remove(prodAi)
                    for prodAj in glc.producoes[Aj]:
                        prod = prodAj + prodAi[len(Aj):]
                        if prod not in novas_producoes[Ai]:
                            novas_producoes[Ai].append(prod)

                else:
                    prod = prodAi
                    if prod not in novas_producoes[Ai]:
                        novas_producoes[Ai].append(prod)
        else:
            for prodAi in glc.producoes[Ai]:
                prod = prodAi
                if prod not in novas_producoes[Ai]:
                    novas_producoes[Ai].append(prod)

    glc.producoes = novas_producoes

    return glc


def remover_recursao_esquerda_direta(glc):
    new_prods = dict()
    for head, bodies in glc.producoes.items():
        recursive_bodies = []
        for body in bodies:
            if body[0] == head:
                recursive_bodies.append(body)

        if recursive_bodies:
            new_head = head + "'"
            new_head_bodies = ['&']
            head_bodies = []
            for body in bodies:
                if body in recursive_bodies:
                    new_head_bodies.append(body[1:] + new_head)
                else:
                    head_bodies.append(body + new_head)

            new_prods[head] = head_bodies
            new_prods[new_head] = new_head_bodies

        else:
            new_prods[head] = bodies

    glc.nao_terminais = list(set(new_prods.keys()))
    glc.producoes = new_prods

    return glc

def pegar_primeiro_simbolo(producao, glc):
    simbolos = ''
    indice = 0
    for simbolo in producao:
        simbolos += simbolo
        indice += 1
        if simbolos in glc.nao_terminais or simbolos in glc.terminais:
            return (simbolos, indice)
    return (None,-1)

def verificar_existencia_nao_determinismo_direto(glc, producoes):
    (terminais_producoes,terminais_a_esquerda) = pegar_terminais_a_esquerda(glc, producoes)
    lista_filtrada = filtrar_lista_de_terminais(terminais_a_esquerda, terminais_producoes)
    return (lista_filtrada != [], lista_filtrada)

def resolver_nao_determinismo_direto(glc, nao_terminal, j):
    (existe_nao_determinismo_direto, lista_filtrada) = verificar_existencia_nao_determinismo_direto(glc, glc.producoes[nao_terminal])
    if existe_nao_determinismo_direto:
        mapeamento = mapear_terminais(lista_filtrada)
        for terminal in mapeamento.keys():

            # CRIANDO UM NOVO NAO TERMINAL PARA SUBSTITUIR O RESTO
            novo_nao_terminal = 'X_' + str(j)
            j += 1

            # ADICIONANDO O NOVO NAO TERMINAL
            glc.nao_terminais.append(novo_nao_terminal)
            glc.producoes[novo_nao_terminal] = []

            # REMOVENDO AS PRODUCOES VELHAS
            for producao_alvo in mapeamento[terminal]:
                # PROCURANDO O INDICE DO TERMINAL NA PRODUCAO
                (simbolo, indice) = pegar_primeiro_simbolo(producao_alvo, glc)

                resto = producao_alvo[indice::]

                if resto == '':
                    resto = '&'

                # REMOVENDO A PRODUCs = %s" % novas_producoes)
                glc.producoes[nao_terminal].remove(producao_alvo)

                # SUBSTITUINDO PELA PRODUCAO NOVA
                if (terminal + novo_nao_terminal) not in glc.producoes[nao_terminal]:
                    glc.producoes[nao_terminal].append(terminal + novo_nao_terminal)

                # ADICIONANDO O RESTO DE CADA PRODUCAO VELHA COMO PRODUCAO DO NOVO NAO TERMINAL
                if resto not in glc.producoes[novo_nao_terminal]:
                    glc.producoes[novo_nao_terminal].append(resto)
    return j

def encontrar_nao_determinismo_indireto(glc, nao_terminal):
    producoes_temporarias = []
    relacoes = []
    for producao in glc.producoes[nao_terminal]:
        (primeiro_simbolo,indice) = pegar_primeiro_simbolo(producao, glc)
        if primeiro_simbolo == None:
            continue
        if primeiro_simbolo in glc.terminais and producao not in producoes_temporarias:
            producoes_temporarias.append(producao)
            if primeiro_simbolo not in relacoes:
                relacoes.append((producao, producao))
        if primeiro_simbolo in glc.nao_terminais:
            producoes_primeiro_simbolo = glc.producoes[primeiro_simbolo]
            (producoes_subidas, relacao_entre_producoes) = subir_producoes(producao, producoes_primeiro_simbolo, indice)

            # ADICIONANDO CADA PRODUCAO SUBIDA AS PRODUCOES TEMPORARIAS
            for producao_subida in producoes_subidas:
                if producao_subida not in producoes_temporarias:
                    producoes_temporarias.append(producao_subida)

            # ADICIONANDO A RELACAO ENTRE CADA PRODUCAO NOVA E ANTIGA
            for par in relacao_entre_producoes:
                if par not in relacoes:
                    relacoes.append(par)
    (existe_nao_determinismo_direto, lista_filtrada) = verificar_existencia_nao_determinismo_direto(glc, producoes_temporarias)
    # print(lista_filtrada)
    if existe_nao_determinismo_direto:
        # SUBSTITUINDO AS PRODUCOES ANTIGAS PELAS TEMPORARIAS
        for par in relacoes:
            producao_substituida = par[1]
            if producao_substituida in glc.producoes[nao_terminal]:
                glc.producoes[nao_terminal].remove(producao_substituida)
        for producao in producoes_temporarias:
            glc.producoes[nao_terminal].append(producao)
        return True
    else:
        return False


def subir_producoes(producao_candidata, producoes, indice_primeiro_simbolo):
    novas_producoes = []
    relacao_entre_producoes = []
    for producao in producoes:
        nova_producao = producao + producao_candidata[indice_primeiro_simbolo::]
        par = (nova_producao, producao_candidata)
        if nova_producao not in novas_producoes:
            novas_producoes.append(nova_producao)
        if par not in relacao_entre_producoes:
            relacao_entre_producoes.append(par)
    return (novas_producoes, relacao_entre_producoes)

def pegar_terminais_a_esquerda(glc, producoes):
    terminais_a_esquerda = []
    terminais_producoes = []
    for producao in producoes:
        (simbolo,indice) = pegar_primeiro_simbolo(producao, glc)
        if simbolo == None:
            continue
        if simbolo in glc.terminais:
            par_simbolo_producao = (simbolo,producao)
            par_simbolo_indice = (simbolo, indice)
            terminais_producoes.append(par_simbolo_producao)
            terminais_a_esquerda.append(simbolo)
    return (terminais_producoes,terminais_a_esquerda)

def filtrar_lista_de_terminais(terminais, terminais_producoes):
    lista_filtrada = []
    for par in terminais_producoes:
        if terminais.count(par[0]) > 1 and par not in lista_filtrada:
            lista_filtrada.append(par)
    return lista_filtrada

def mapear_terminais(lista):
    mapeamento = {}
    for par in lista:
        terminal = par[0]
        if terminal not in mapeamento.keys():
            mapeamento[terminal] = []
        indice = par[1]
        mapeamento[terminal].append(indice)
    return mapeamento
