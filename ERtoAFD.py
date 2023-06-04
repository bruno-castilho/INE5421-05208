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
    def getTree(er: str, n: list, symbols: str):
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
            # Retorna nó * com filho calculado recursivamente
            return Node("*", left_child=ERtoAFD.getTree(left,n,symbols))

        # Verifica se a expressão é algo entre parenteses
        if er[0] == "(" and er[-1] == ")":
            # Calcula recursivamente a árvore da expressão entre parenteses
            return ERtoAFD.getTree(er[1:-1], n, symbols)

        if er != '&':
            symbols[n[0]] = er
        
        return Node(er, n)  # Nó não possui operadores, então é final

    def transform(ER: ER):
        n = [1]
        sym = {}
        tree = ERtoAFD.getTree(ER.getErAdapted(),n,sym)
        followpos = {}
        for key in sym.keys():
            followpos[key] = []
        
        tree.calculateFollowpos(followpos)
        
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
        
        return AF(0, states, initial_state, symbols, final_states, transitions)