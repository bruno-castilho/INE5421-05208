from structures.NODE import NODE
from structures.AF import AF

def getArvore(er, n, symbols):
    # Procura por operador e retorna parte esquerda e direita.
    def procura_operadores(operador):
        direita, esquerda = '', ''
        parenteses = 0
        for i in range(len(er) - 1, -1, -1):  # Varre ER da direita para esquerda
            # Verifica se encontrou o operador fora de qualquer parenteses
            if er[i] == operador and parenteses == 0:
                esquerda = er[:i]
                return esquerda, direita[::-1]

            # Contagem de parenteses
            if er[i] == ')':
                parenteses += 1
            elif er[i] == '(':
                parenteses -= 1

            direita += er[i]

        return esquerda, direita[::-1]

    esquerda, direita = procura_operadores('|')  # Procura por operador |
    if esquerda != "":
        # Retorna nó | com filhos da esquerda e direita calculados recursivamente
        return NODE("|",left_child=getArvore(esquerda,n,symbols), right_child=getArvore(direita,n,symbols))

    esquerda, direita = procura_operadores('.')  # Procura por operador .
    if esquerda != "":
        # Retorna nó . com filhos da esquerda e direita calculados recursivamente
        return NODE(".",left_child=getArvore(esquerda,n,symbols), right_child=getArvore(direita,n,symbols))

    esquerda, direita = procura_operadores('*')  # Procura por operador *
    if esquerda != "":
        # Retorna nó * com filho calculado recursivamente
        return NODE("*", left_child=getArvore(esquerda,n,symbols))

    # Verifica se a expressão é algo entre parenteses
    if er[0] == "(" and er[-1] == ")":
        # Calcula recursivamente a árvore da expressão entre parenteses
        return getArvore(er[1:-1], n, symbols)

    if er != '&':
        symbols[n[0]] = er
    
    return NODE(er, n)  # Nó não possui operadores, então é final

def erToAFD(er):
    n = [1]
    sym = {}
    tree = getArvore(er,n,sym)
    followpos = {}
    for key in sym.keys():
        followpos[key] = []
    
    tree.calcule_followpos(followpos)
    
    
    transitions = {}
    initial_state = str(tree.getFirstpos())
    symbols = sorted(list(set(sym.values()) & set(sym.values())))
    symbols.remove('#')
    states = [initial_state]
    final_states = []
    #Lista de estados encontrados.
    states_found = [tree.getFirstpos()]
    
    accept_value = None 
    for key in sym.keys():
        if sym[key] == '#':
            accept_value = key
        
    #Enquanto lista de estados encontrados não estiver vazia.
    while len(states_found) != 0:
        s = states_found.pop()
        
        if accept_value in s:
            final_states.append(str(s))
        
        transitions[str(s)] = {}
        for i in symbols:
            t = []
            for j in s:
                if sym[j] == i:
                    t.append(j)
            
            new_state = []
            for k in t:
                new_state = sorted(list(set(new_state) | set(followpos[k])))

            if len(new_state) != 0:
                transitions[str(s)][i] = str(new_state)
            
                if not str(new_state)in states:
                    states_found.append(new_state)
                    states.append(str(new_state))
                    
            else: 
                transitions[str(s)][i] = None
    
    return AF(states, initial_state, symbols, final_states, transitions)

      
        
erToAFD('a.a*.(b.b*.a.a*.b)*.#').print()