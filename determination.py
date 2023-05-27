from structures.AF import AF

class Determination():
    #Calcula &-fechos
    def eClosures(af: AF):
            closures = {}
            
            #Cria &-fecho para cada estado e o inseri no mesmo.
            for state in af.getStates():
                closures[state] = [state]
            
            #Se tiver transições por &.
            if '&' in af.getSymbols():
                #Para cada estado.
                for state in closures.keys():
                    #Busca estados alcaçaveis por &.
                    attainable = af.getTransition(state,'&')
                    
                    #Cria dicionario com todos os estados como não visitados.
                    visited_states = {a:False for a in af.getStates()}
                    
                    #Marca estado como já visitado.
                    visited_states[state] = True
                    
                    #Enquando tiver estados alcaçaveis por &.
                    while len(attainable) != 0:
                        #Pega um estado
                        s = attainable.pop()
                        
                        #Se estado não foi visitado.
                        if not visited_states[s]:
                            #Marca estado como visitado.
                            visited_states[s] = True
                            
                            #Adiciona estado no &-fecho.
                            closures[state].append(s)
                            closures[state] = sorted(closures[state])
                            
                            #Busca estados alcaçaveis por & a partir de s e adiciona na lista.
                            attainable += af.getTransition(s,'&')
                            
            return closures

    #Determiniza automato.
    def determinize(af: AF):
                #Calcula &-fechos
                closures = Determination.eClosures(af)
                
                #Novo automato.
                new_initial_state = str(closures[af.getInitialState()])
                new_transitions = {}
                new_states = [str(new_initial_state)]
                new_symbols = af.getSymbols()
                new_symbols.remove('&')
                new_final_states = []
                
                #Lista de estados encontrados.
                states_found = [closures[af.getInitialState()]]
                
                #Enquanto lista de estados encontrados não estiver vazia.
                while len(states_found) != 0:
                    #Pega um estado da lista.
                    s = states_found.pop(0)
                    
                    #Cria transições a partir deste estado.
                    new_transitions[str(s)] = {}
                    for symbol in new_symbols:
                        #Busca todos os etados alcaçados por 'symbol' a partir deste etado.
                        states = []
                        for state in s: 
                            states = sorted(list(set(states) | set(af.getTransition(state, symbol))))

                        #Une &-fechos de todos os estados e gera um estado unico.
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
                            
                            #Adiciona na lista de estados encontados.
                            states_found.append(state)
                
                
                #Para cada novo estado.
                for state in new_states:
                    #Converte state de str para list.
                    state_with_list = state[1:-1]
                    state_with_list = state_with_list.replace(" ", "")
                    state_with_list = state_with_list.replace("'", "")
                    state_with_list = state_with_list.split(",")
                    #Se algum estado final anterior estiver contido em 'state'.
                    if len(set(af.getFinalStates()) & set(state_with_list)) != 0:
                        #Adiciona 'state' como um novo estado final.
                        new_final_states.append(state)
                        
                return AF(type=0, states=new_states, initial_state=new_initial_state, symbols=new_symbols, final_states=new_final_states, transitions=new_transitions)