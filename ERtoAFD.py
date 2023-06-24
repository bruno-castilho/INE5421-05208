from structures.Node import Node
from structures.AF import AF
from structures.ER import ER

class ERtoAFD():
    """
    Uma classe para transformar ER em AFD.
    
    Métodos
    -------
    getTree(er: str, n: list, symbols: str) -> Node:
        Retorna nó raiz da árvore sintática.
    
    transform(ER: ER) -> AF:
        Retorna AFD.
        
    """
    def getTree(er: str, n: list, symbols: dict):
        # Procura por operador e retorna parte esquerda e direita.
        def searchOperators(operator):
            left, right = '', ''
            parentheses = 0
            for i in range(len(er) - 1, -1, -1):  # Varre ER da direita para esquerda
                # Verifica se encontrou o operador fora de qualquer parenteses
                if er[i] == operator and parentheses == 0:
                    left = er[:i]
                    return left, right[::-1]

                # Contagem de parenteses
                if er[i] == ')':
                    parentheses += 1
                elif er[i] == '(':
                    parentheses -= 1

                right += er[i]

            return left, right[::-1]

        left, right = searchOperators('|')  # Procura por operador |
        if left != "":
            # Retorna nó | com filhos da esquerda e direita calculados recursivamente
            return Node("|",left_child=ERtoAFD.getTree(left,n,symbols), right_child=ERtoAFD.getTree(right,n,symbols))

        left, right = searchOperators('.')  # Procura por operador .
        if left != "":
            # Retorna nó . com filhos da esquerda e direita calculados recursivamente
            return Node(".",left_child=ERtoAFD.getTree(left,n,symbols), right_child=ERtoAFD.getTree(right,n,symbols))

        left, right = searchOperators('*')  # Procura por operador *
        if left != "":
            #Retorna nó * com filho calculado recursivamente
            return Node("*", left_child=ERtoAFD.getTree(left,n,symbols))

        # Verifica se a expressão é algo entre parenteses
        if er[0] == "(" and er[-1] == ")":
            # Calcula recursivamente a árvore da expressão entre parenteses
            return ERtoAFD.getTree(er[1:-1], n, symbols)

        if er != '&':
            symbols[n[0]] = er
        
        return Node(er, n)  # Nó não possui operadores, então é final

    def transform(ER: ER):
        n = [1] #Contador de nós folhas(definido em uma lista para ser usada como ponteiro).
        sym = {}#Dicionário para mapear números para cada símbolo.
        tree = ERtoAFD.getTree(ER.getErAdapted(),n,sym) #Gera árvore sintática.
        followpos = {} #Tabela de followpos
        
        #Para cada número em 'sym'.
        for key in sym.keys():
            #Cria uma lista vazia.
            followpos[key] = []
        
        #Calcula followpos.
        tree.calculateFollowpos(followpos)
        
        #AUTÔMATO RESULTANTE.
        initial_state = str(tree.getFirstpos()) #Define o estado inicial do autômato como firtpost do nó raiz da árvore sintática.
        
        #Define símbolos do autômato como símbolos da er.
        symbols = sorted(list(set(sym.values()) & set(sym.values()))) 
        symbols.remove('#') 
        
        
        
        states = [initial_state] #Define lista de estados com o estado inicial contido.
        final_states = [] #Define a lista de estados finais como vazia.
        
        #Lista de estados encontrados.
        states_found = [tree.getFirstpos()]
        
        #Define qual valor de n que deverá estar contido no estado para ser estado de aceitação.
        accept_value = None 
        for key in sym.keys():
            if sym[key] == '#':
                accept_value = key
            
        transitions = {}
        
        #Enquanto a lista de estados encontrados não estiver vazia.
        while len(states_found) != 0:
            
            #Pega um estado da lista de estados encontrados.
            s = states_found.pop()
            
            #Se accept_value estiver contido em 's', 's' é um estado de aceitação.
            if accept_value in s:
                final_states.append(str(s))
            
            
            #Define transições a partir de 's'.
            transitions[str(s)] = {}
            
            #Para cada símbolo em 'symbols'.
            for i in symbols:
                #Busca valores em 's' que representam o símbolo 'i'.
                t = []
                for j in s:
                    if sym[j] == i:
                        t.append(j)
                
               #Define estado alcançável a partir de 's' por 'i'.
                new_state = []
                
                #Faz união de todos os followpos dos valores em 't' e coloca new_state.
                for k in t:
                    new_state = sorted(list(set(new_state) | set(followpos[k])))

                #Se new_state diferente de vazio.
                if len(new_state) != 0:
                    #Coloca na tabela de transição o estado alcançavel a partir de 's' por 'i'.
                    transitions[str(s)][i] = str(new_state)

                    #Se o estado não estiver na lista de estados do autômato.
                    if not str(new_state)in states:
                        #Coloca na lista de estados encontrados.
                        states_found.append(new_state)
                        #Coloca na lista de estados.
                        states.append(str(new_state))
                #Se não.  
                else: 
                    #Coloca na tabela de transição None como estado alcançável a partir de 's' por 'i'.
                    transitions[str(s)][i] = None
                    
        #Retorna autômato resultante.
        return AF(0, states, initial_state, symbols, final_states, transitions)