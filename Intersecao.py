from structures.AF import AF
from Determination import Determination

class Intersecao():
    """
    Uma classe para fazer a interseção entre dois AFD.
    
    Métodos
    -------

    transform(AF1: AF, AF2: AF) -> AF
        Retorna AFD
    
    """
    
    def transform(AF1: AF, AF2: AF):        
        #AF1
        AF1.adjust('s')
        af1_states = AF1.getStates()
        af1_initial_state = AF1.getInitialState()
        af1_symbols = AF1.getSymbols()
        af1_final_states = AF1.getFinalStates()
        af1_transitions = AF1.getTransitions()
        
        #AF2
        AF2.adjust('t')
        af2_states = AF2.getStates()
        af2_initial_state = AF2.getInitialState()
        af2_symbols = AF2.getSymbols()
        af2_final_states = AF2.getFinalStates()
        af2_transitions = AF2.getTransitions()
        
        #NOVO AFND
        i = 'i0' #Estado inicial do autômato igual a 'i0'.
        s = [i] + af1_states + af2_states #Lista de estados do automato igual a 'i0' + estados do AF1 + estados do AF2.
        sy = sorted(list(set(af1_symbols) | set(af2_symbols) | set(['&']))) #Lista de símbolos igual a união de símbolos de AF1 e AF2.
        
        
        #Define transições.
        tr = {}
        
        #Para cada estado sem 's'.
        for state in s:
            #Cria-se transições vazias para cada símbolo.
            tr[state] = {}
            for symbol in sy:
                tr[state][symbol] = []
        
        #Define uma transição partindo de 'i0' por '&' para os estados iniciais de AF1 e AF2.
        tr[i]['&'] = [af1_initial_state, af2_initial_state]
        
        #Define transições do novo automato igual a transições de AF1 e AF2.
        for state in af1_states:
            for symbol in af1_symbols:
                if af1_transitions[state][symbol]:
                    tr[state][symbol] = [af1_transitions[state][symbol]]
                else:
                    tr[state][symbol] = []
        
        for state in af2_states:
            for symbol in af2_symbols:
                if af2_transitions[state][symbol]:
                    tr[state][symbol] = [af2_transitions[state][symbol]]
                else:
                    tr[state][symbol] = []
              

        #DETERMINIZA AUTOMATO.
        closures = {}
        
        #Cria &-fecho para cada estado e o inseri no mesmo.
        for state in s:
            closures[state] = [state]
        
        #Se houver transições por &.
        if '&' in sy:
            #Para cada estado.
            for state in closures.keys():
                #Busca estados alcançáveis por &.
                attainable = tr[state]['&']
                
                #Cria dicionário com todos os estados como não visitados.
                visited_states = {a:False for a in s}
                
                #Marca estado como já visitado.
                visited_states[state] = True
                
                #Enquanto houver estados alcançáveis por &.
                while len(attainable) != 0:
                    #Pega um estado.
                    s = attainable.pop()
                    
                    #Se o estado não foi visitado.
                    if not visited_states[s]:
                        #Marca estado como visitado.
                        visited_states[s] = True
                        
                        #Adiciona estado no &-fecho.
                        closures[state].append(s)
                        closures[state] = sorted(closures[state])
                        
                        #Busca estados alcançáveis por & a partir de s e adiciona na lista.
                        attainable += tr[s]['&']
        
            
            #Novo AFD.
            new_initial_state = str(closures[i])
            new_transitions = {}
            new_states = [str(new_initial_state)]
            new_symbols = sy
            if '&' in new_symbols:
                new_symbols.remove('&')
            new_final_states = []
            
            #Lista de estados encontrados.
            states_found = [closures[i]]
            
            #Enquanto a lista de estados encontrados não estiver vazia.
            while len(states_found) != 0:
                #Pega um estado da lista.
                s = states_found.pop(0)
                
                #Cria transições a partir deste estado.
                new_transitions[str(s)] = {}
                for symbol in new_symbols:
                    #Busca todos os estados alcançados por 'symbol' a partir deste estado.
                    states = []
                    for state in s: 
                        states = sorted(list(set(states) | set(tr[state][symbol])))

                    #Une &-fechos de todos os estados e gera um estado único.
                    state = []
                    for t in states:
                        state = sorted(list(set(state) | set(closures[t])))
                    
                    #Adiciona transição a partir de 's' por 'symbol' para 'state'.
                    if len(states) != 0:
                        new_transitions[str(s)][symbol] = str(state)
                    else:
                        new_transitions[str(s)][symbol] = None
                    
                    #Se 'state' for um estado novo em 'new_states'.
                    if str(state) not in new_states and len(states) != 0:
                        #Adiciona na lista de novos estados.
                        new_states.append(str(state))
                        
                        #Adiciona na lista de estados encontrados.
                        states_found.append(state)
                        
            #Para cada novo estado.
            for state in new_states:
                #Converte state de str para list.
                state_with_list = state[1:-1]
                state_with_list = state_with_list.replace(" ", "")
                state_with_list = state_with_list.replace("'", "")
                state_with_list = state_with_list.split(",")
                
                #Se todos os estados finais de AF1 e AF2 estiverem contidos em 'state'.
                if len(set(af1_final_states) & set(state_with_list)) != 0 and len(set(af2_final_states) & set(state_with_list)) != 0:
                    #Adiciona 'state' como um novo estado final.
                    new_final_states.append(state)      
        
        #Retorna autômato resultante.
        return AF(type=0, states=new_states, initial_state=new_initial_state, symbols=new_symbols, final_states=new_final_states, transitions=new_transitions)