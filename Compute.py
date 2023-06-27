from structures.AF import AF

class Compute():
    
    """
    Uma classe para computar um lexema em um AF
    
    Métodos
    -------

    AFD(AF: AF, lexeme: str) -> boolean:
        Computa uma lexema em um AFD.
    
    AFND(AF: AF, lexeme: str) -> boolean:
        Computa uma lexema em um AFND.
        
    """
    def AFD(AF: AF, lexeme: str):
        #Define o estado atual como estado inicial do autômato.
        current_state = AF.getInitialState()
        #Enquanto o lexema não for totalmente consumido.
        while len(lexeme) > 0:
            #Se o estado atual for diferente de None.
            if current_state != None:
                #Imprime estado atual e lexema.
                print(f'estado atual: {current_state}')
                print(f'lexema: {lexeme}')
                print('/////////////////////')
                #Estado atual igual a transição de estado atual pelo símbolo do cabeçote.
                current_state = AF.getTransition(current_state, lexeme[0])
                #Consome lexema.
                lexeme = lexeme[1:]
            #Se não.
            else:
                #Imprime estado atual e retorna false.
                print(f'estado atual: Morto')
                print(f'lexema: {lexeme}')
                return False
        
        #Imprime estado atual e lexema igual a vazio.
        print(f'estado atual: {current_state}')
        print(f'lexema: Ø')
        
        #Se o estado atual for um estado final, retorna True.
        if current_state in AF.getFinalStates():
            return True
        
        #Se não, retorna False.
        return False
    
    def AFND(AF: AF, lexeme: str):
        #Define estados atuais como uma lista contendo o estado inicial do autômato.
        current_states = [AF.getInitialState()]
        #Enquanto o lexema não for totalmente consumido.
        while len(lexeme) > 0:
            #Imprime estados atuais e lexema.
            print(f'estados atuais: {current_states}')
            print(f'lexema: {lexeme}')
            
            #Se houver estados atuais na lista de estados atuais.
            if len(current_states) > 0:
                print('/////////////////////')

                #Faz a transição de todos os estados da lista de estados atuais pelo símbolo do cabeçote.
                new_current_states = []
                for state in current_states:
                    states = AF.getTransition(state, lexeme[0])
                    if states:
                        new_current_states += states
                
                current_states = new_current_states
                
                #Consome lexema.
                lexeme = lexeme[1:]
                
            #Se não retorna false.
            else:
                return False
            
        #Imprime estados atuais e lexema igual a vazio.
        print(f'estados atuais: {current_states}')
        print(f'lexema: Ø')
        
        #Se na lista de estados atuais contêm um estado final, retorna true.
        for state in current_states:
            if state in AF.getFinalStates():
                return True
            
        #Se não retorna false.
        return False