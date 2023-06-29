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
        Dicionário que mapeia as produções.

    tabela_analise : Multi List
        Tabela criada para análise da gramática.
    
    Métodos
    -------
    get_nao_terminais() -> List

    get_terminais() -> List

    get_simbolo_inicial() -> Str

    get_producoes() -> List

    _arrumar_producoes()
    
    display()

    reconhecer() -> Bool

    criar_tabela_de_analise() -> Dict

    isLL1() -> List

    init_analysis_table() -> Dict

    map_productions() -> Dict

    calculate_firsts() -> Set

    split_into_symbols() -> List

    get_first_symbol() -> String

    calculate_follows() -> Set

    first_of_sequence() -> Set

    fatorar()

    remover_recursao_esquerda_indireta() -> GLC

    remover_recursao_esquerda_direta() -> GLC

    pegar_primeiro_simbolo() -> Tuple

    verificar_existencia_nao_determinismo_direto() -> Tuple

    resolver_nao_determinismo_direto()

    encontrar_nao_determinismo_indireto() -> Bool

    subir_producoes() -> Tuple

    pegar_terminais_a_esquerda() -> Tuple

    filtrar_lista_de_terminais() -> List

    mapear_terminais() -> Dict
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

        sentenca += '$'
        sentenca = split_into_symbols(sentenca,self.terminais + ['$'],self.nao_terminais)
        stack = []
        stack.append('$')
        stack.append(self.simbolo_inicial)

        # Índice para avaliar a sentença
        cabecote = 0
        while(True):
            print(stack)
            topo = stack[len(stack)-1]
            if topo == sentenca[cabecote]:
                # Aceite
                if topo == '$':
                    return True
                # Topo == cabeçote != $
                if topo in self.terminais:
                    # Desempilha o topo
                    antigo_topo = stack.pop()
                    # Avança a entrada
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
                    # Retira o topo da pilha
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

    # Preenche tabela de análise
    # Analisar se já não existe uma entrada definida quando for colocar algo
    # Se existir, indique que houve conflito
    for non_terminal in analysis_table.keys():
        for production in glc.producoes[non_terminal]:
            number = map[non_terminal+'->'+production]
            symbols_alfa = split_into_symbols(production, glc.get_terminais(), glc.get_nao_terminais())
            first_alfa = first_of_sequence(production, firsts, symbols_alfa)
            for a in (first_alfa - set('&')):
                if analysis_table[non_terminal][a] == -1:
                    analysis_table[non_terminal][a] = number
                else:
                    # Conflito
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
    # Calcula o first para cada símbolo  
    #{X : FIRST(X) for X} in (N U T)
    first = {s: set((s,)) for s in glc.terminais + ['&']}
    for X in glc.nao_terminais:
        first[X] = set()

    nova_added = True
    while nova_added:
        nova_added = False
        for cabeca, corpos in glc.producoes.items():
            for corpo in corpos:
                symbol = get_first_symbol(corpo, glc.terminais, glc.nao_terminais)

                if symbol in glc.terminais + ['&']:
                    nova_first = first[cabeca].union(first[symbol])

                elif symbol in glc.nao_terminais:
                    f = first[symbol]
                    nova_first = first[cabeca].union(f - set('&'))

                    while '&' in f:
                        # Pega o corpo da produção sem o primeiro símbolo
                        corpo = corpo[len(symbol):]
                        if corpo == '':
                            nova_first = nova_first.union('&')
                            break

                        symbol = get_first_symbol(corpo, glc.terminais, glc.nao_terminais)
                        f = first[symbol]
                        nova_first = nova_first.union(f - set('&'))

                else:
                    raise Exception(f'Symbol {symbol} not in GLC (N U T)')

                if nova_first != first[cabeca]:
                    nova_added = True
                    first[cabeca] = nova_first

    return first

def split_into_symbols(corpo, T, N):
    symbols = []  # Lista vazia para armazenar os símbolos

    while len(corpo) > 0: # Enquanto o comprimento do corpo for maior que zero
        symbol = get_first_symbol(corpo, T, N) # Obtém o primeiro símbolo do corpo usando a função get_first_symbol, passando corpo, T e N como argumentos
        symbols.append(symbol) # Adiciona o símbolo obtido à lista de símbolos
        corpo = corpo[len(symbol):] # Atualiza o corpo, removendo o símbolo obtido

    return symbols

def get_first_symbol(corpo, T, N):
    # Obtêm o primeiro símbolo do corpo de uma produção
    # Corresponde a um símbolo em T U N
    symbols = T + N
    symbols.append('&')
    for i, _ in enumerate(corpo):
        if corpo[: i + 1] in symbols:
            return corpo[: i + 1]

    return corpo


def calculate_follows(glc, firsts=None):
    # Calcula o follow para cada símbolo   
    # {X : FOLLOW(X) for X} in (N U T)

    # Deve calcular o first se ainda não existe
    if firsts is None:
        firsts = calculate_firsts(glc)

    follows = {s: set(()) for s in glc.nao_terminais}
    follows[glc.simbolo_inicial] = set('$')

    # Dicionário para guardar os casos: FOLLOW(A) em FOLLOW(B)
    # Será armazenado dessa forma: inside[A] = [B]
    inside = {n: set(()) for n in glc.nao_terminais}

    nova_added = True
    while(nova_added):
        nova_added = False
        for cabeca, corpos in glc.producoes.items():
            for corpo in corpos:
                symbols = split_into_symbols(corpo, glc.terminais, glc.nao_terminais)
                for i in range(len(symbols)):
                    # caso 1: produção X -> aBC ou X -> ABC
                    if symbols[i] in glc.nao_terminais:
                        target = symbols[i]
                        # verifica se houve mudanças
                        old = follows[target]

                        beta = ''.join(symbols[i+1:])
                        # caso 1.1: BETA é diferente da sentença vazia
                        # ação: FIRST(BETA)/{&} em FOLLOW(TARGET)
                        if beta != '':
                            symbols_beta = split_into_symbols(beta, glc.terminais, glc.nao_terminais)
                            first_beta = first_of_sequence(beta, firsts, symbols_beta)

                            # FIRST(BETA)\{&} em FOLLOW(TARGET)
                            follows[target].update((first_beta - set('&')))
                            if '&' in first_beta:
                                # FOLLOW(cabeca) em FOLLOW(TARGET)
                                if cabeca != target:
                                    inside[cabeca].add(target)
                        # caso 1.2: BETA é igual a sentença vazia (X->alfaB)
                        # ação: FOLLOW(cabeca) em FOLLOW(TARGET)
                        else:
                            if cabeca != target:
                                inside[cabeca].add(target)
                        if old != follows[target]:
                            nova_added = True

    nova_added = True
    while(nova_added):
        nova_added = False
        for non_terminal in inside.keys():
            for dependent in inside[non_terminal]:
                old = follows[dependent]
                follows[dependent].update(follows[non_terminal])
                if old != follows[dependent]:
                    nova_added = True
    return follows

# Se A→αBβ, então tudo em first(β) exceto & está em follow(B).
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
    # Resolve o primeiro não determinismo direto
    for nao_terminal in glc.nao_terminais:
        j = resolver_nao_determinismo_direto(glc, nao_terminal, j)
    # Se encontrar um não determinismo indireto, resolva
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
    novas_producoes = dict()  # Dicionário vazio para armazenar as novas produções

    for cabeca, corpos in glc.producoes.items():
        recursiva_corpos = []  # Lista vazia para armazenar corpos recursivos

        for corpo in corpos:
            if corpo[0] == cabeca:  # Verifica se o corpo começa com a mesma cabeça
                recursiva_corpos.append(corpo)  # Adiciona o corpo à lista de corpos recursivos

        if recursiva_corpos:
            nova_cabeca = cabeca + "'"  # Cria uma nova cabeça para as produções recursivas
            nova_cabeca_corpos = ['&']  # Lista com um corpo vazio '&' para a nova cabeça
            cabeca_corpos = []  # Lista para armazenar as produções modificadas

            for corpo in corpos:
                if corpo in recursiva_corpos:
                    nova_cabeca_corpos.append(corpo[1:] + nova_cabeca)
                    # Adiciona o corpo sem o primeiro símbolo e com a nova cabeça
                else:
                    cabeca_corpos.append(corpo + nova_cabeca)
                    # Adiciona o corpo original com a nova cabeça

            novas_producoes[cabeca] = cabeca_corpos  # Atualiza as produções da cabeça original
            novas_producoes[nova_cabeca] = nova_cabeca_corpos  # Adiciona as novas produções com a nova cabeça

        else:
            novas_producoes[cabeca] = corpos  # Mantém as produções da cabeça original

    glc.nao_terminais = list(set(novas_producoes.keys()))
    # Atualiza a lista de não-terminais da gramática com as chaves do dicionário de novas produções
    glc.producoes = novas_producoes  # Atualiza as produções da gramática com as novas produções

    return glc

def pegar_primeiro_simbolo(producao, glc):
    simbolos = ''  # Variável para armazenar os símbolos percorridos
    indice = 0  # Variável para armazenar o índice do primeiro símbolo
    
    for simbolo in producao:
        simbolos += simbolo  # Concatena o símbolo atual à sequência de símbolos percorridos
        indice += 1  # Incrementa o índice
        
        if simbolos in glc.nao_terminais or simbolos in glc.terminais:
            # Verifica se a sequência de símbolos é um não-terminal ou um terminal da gramática
            return (simbolos, indice)  # Retorna uma tupla com a sequência de símbolos e o índice
        
    return (None, -1)  # Caso nenhum símbolo seja encontrado, retorna uma tupla com None e -1

def verificar_existencia_nao_determinismo_direto(glc, producoes):
    # Chama a função pegar_terminais_a_esquerda, passando glc e producoes como argumentos e atribui os resultados às variáveis terminais_producoes e terminais_a_esquerda
    (terminais_producoes,terminais_a_esquerda) = pegar_terminais_a_esquerda(glc, producoes)

    # Chama a função filtrar_lista_de_terminais, passando terminais_a_esquerda e terminais_producoes como argumentos e atribui o resultado à variável lista_filtrada
    lista_filtrada = filtrar_lista_de_terminais(terminais_a_esquerda, terminais_producoes)

    # Retorna uma tupla com dois elementos: o primeiro elemento é uma expressão booleana que verifica se a lista_filtrada não está vazia,
    # e o segundo elemento é a própria lista_filtrada
    return (lista_filtrada != [], lista_filtrada)

def resolver_nao_determinismo_direto(glc, nao_terminal, j):
    (existe_nao_determinismo_direto, lista_filtrada) = verificar_existencia_nao_determinismo_direto(glc, glc.producoes[nao_terminal])
    if existe_nao_determinismo_direto:
        mapeamento = mapear_terminais(lista_filtrada)
        for terminal in mapeamento.keys():

            # Cria um novo não terminal para substituir
            novo_nao_terminal = 'X_' + str(j)
            j += 1

            # Adiciona novo não terminal
            glc.nao_terminais.append(novo_nao_terminal)
            glc.producoes[novo_nao_terminal] = []

            # Remove produções velhas
            for producao_alvo in mapeamento[terminal]:
                # Procura o índice do terminal na produção
                (simbolo, indice) = pegar_primeiro_simbolo(producao_alvo, glc)

                resto = producao_alvo[indice::]

                if resto == '':
                    resto = '&'

                glc.producoes[nao_terminal].remove(producao_alvo)

                # Substituindo pela nova produção
                if (terminal + novo_nao_terminal) not in glc.producoes[nao_terminal]:
                    glc.producoes[nao_terminal].append(terminal + novo_nao_terminal)

                # Adicionando o resto de cada produção velha como produção do novo não terminal
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

            # Adiciona cada produção subida para as produções temporais
            for producao_subida in producoes_subidas:
                if producao_subida not in producoes_temporarias:
                    producoes_temporarias.append(producao_subida)

            # Adiciona a relação entre cada produção nova e antiga
            for par in relacao_entre_producoes:
                if par not in relacoes:
                    relacoes.append(par)
    (existe_nao_determinismo_direto, lista_filtrada) = verificar_existencia_nao_determinismo_direto(glc, producoes_temporarias)
    # print(lista_filtrada)
    if existe_nao_determinismo_direto:
        # Substitui produções antigas pelas temporarias
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
    novas_producoes = []  # Lista vazia para armazenar as novas produções
    relacao_entre_producoes = []  # Lista vazia para armazenar pares de produções

    for producao in producoes:
        nova_producao = producao + producao_candidata[indice_primeiro_simbolo::]
        # Cria uma nova produção adicionando a parte restante da produção candidata após o primeiro símbolo
        par = (nova_producao, producao_candidata)  # Cria um par (nova_producao, producao_candidata)
        
        if nova_producao not in novas_producoes:  # Verifica se a nova produção já está presente na lista de novas produções
            novas_producoes.append(nova_producao)  # Adiciona a nova produção à lista de novas produções
        
        if par not in relacao_entre_producoes:  # Verifica se o par (nova_producao, producao_candidata) já está presente na lista de relações de produções
            relacao_entre_producoes.append(par)  # Adiciona o par à lista de relações de produções

    return (novas_producoes, relacao_entre_producoes)

def pegar_terminais_a_esquerda(glc, producoes):
    terminais_a_esquerda = []  # Lista vazia para armazenar os terminais à esquerda
    terminais_producoes = []  # Lista vazia para armazenar pares (terminal, produção)
    
    for producao in producoes:
        (simbolo, indice) = pegar_primeiro_simbolo(producao, glc)  # Obtém o primeiro símbolo da produção e seu índice
        if simbolo == None:  # Se o símbolo for None, pula para a próxima iteração do loop
            continue
        if simbolo in glc.terminais:  # Verifica se o símbolo é um terminal da gramática
            par_simbolo_producao = (simbolo, producao)  # Cria um par (terminal, produção)
            par_simbolo_indice = (simbolo, indice)  # Cria um par (terminal, índice)
            terminais_producoes.append(par_simbolo_producao)  # Adiciona o par (terminal, produção) à lista
            terminais_a_esquerda.append(simbolo)  # Adiciona o terminal à lista de terminais à esquerda
    
    return (terminais_producoes,terminais_a_esquerda)

def filtrar_lista_de_terminais(terminais, terminais_producoes):
    lista_filtrada = []  # Lista vazia para armazenar os pares filtrados
    for par in terminais_producoes:
        if terminais.count(par[0]) > 1 and par not in lista_filtrada:
            # Verifica se o terminal do par ocorre mais de uma vez na lista de terminais
            # e se o par ainda não está presente na lista filtrada
            lista_filtrada.append(par)  # Adiciona o par à lista filtrada
    return lista_filtrada

def mapear_terminais(lista):
    mapeamento = {}  # Dicionário para armazenar o mapeamento de terminais
    for par in lista:
        terminal = par[0]  # Obtém o primeiro elemento do par como o terminal
        if terminal not in mapeamento.keys():  # Verifica se o terminal já existe no mapeamento
            mapeamento[terminal] = []  # Se não existir, cria uma lista vazia para o terminal
        indice = par[1]  # Obtém o segundo elemento do par como o índice
        mapeamento[terminal].append(indice)  # Adiciona o índice à lista do terminal no mapeamento
    return mapeamento
