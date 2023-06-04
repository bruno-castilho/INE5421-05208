import pandas as pd

class AF():
    """
    Uma classe para representar um autômato finito.
    
    ...

    Atributos
    ---------
    type: Int
        Tipo do automato.
            0: AFD
            1: AFND
            
        states: list
            Lista de todos os estados.
            
        initial_state: str
            Estado inicial.
            
        symbols: list
           Lista de todos os símbolos.
           
        final_states: list
            Lista de estados finais.
            
        transitions: dict
            Transições do autômato.
            
    Métodos
    -------
    getType() -> Int:
        Retorna tipo do autômato.
            0: AFD
            1: AFND
            
    getStates() -> List:
        Retorna lista de estados.
        
    getInitialState() -> Str:
        Retorna estado inicial.
        
    getSymbols() -> List:
        Retorna lista de simbolos.
        
    getFinalStates() -> List:
        Retorna lista de estados finais.
        
    getTransitions() -> Dict:
        Retorna dicionário com todas as transições.
        
    getTransition(state: str, symbol: str) -> Str:
        Retorna um estado.
        
    print() -> None:
        Imprime autômato em forma de tabela.
        
    adjust(s: str) -> None:
        Ajusta nome dos estados do autômato como 's''numero'.
    """
    
    def __init__(self, type: int, states: list, initial_state: str, symbols: list, final_states: list, transitions: dict):
        self.type = type
        self.states = states
        self.initial_state = initial_state
        self.symbols = symbols
        self.final_states = final_states
        self.transitions = transitions
    
    def getType(self):
        return self.type
    
    def getStates(self):
        return self.states
    
    def getInitialState(self):
        return self.initial_state
    
    def getSymbols(self):
        return self.symbols
    
    def getFinalStates(self):
        return self.final_states
    
    def getTransitions(self):
        return self.transitions
    
    def getTransition(self, state: str, symbol: str):
        try:
            return self.transitions[state][symbol]
        except:
            return
    
    def print(self):
        data = {}
        
        #Formata tabela:
        for state in self.transitions:
            str_state = state
            #Se 'state' é um estado final adiciona '*'
            if state in self.final_states:
                str_state = '*' + str_state
            
            
            #Se 'state' é um estado inicial adiciona '->'
            if state == self.initial_state:
                str_state = '->' + str_state
            
            
            data[str_state] = self.transitions[state]
        
        pd.set_option('colheader_justify', 'center')
        data = pd.DataFrame(data)
        data = data.transpose()
        
        print(data)
                        
    def adjust(self, s: str):
        map_states = {self.states[i]:f'{s}{i}' for i in range(len(self.states))}   
        states = [state for state in map_states.values()]  
        initial_state =  map_states[self.initial_state]
        final_states = [map_states[state] for state in self.final_states] 
        transitions = {}
        
        for state in self.states:
            transitions[map_states[state]] = {}
            for symbol in self.symbols:
                if self.transitions[state][symbol]:
                    transitions[map_states[state]][symbol] = map_states[self.transitions[state][symbol]]
                else:
                    transitions[map_states[state]][symbol] = None

        
        self.states = states
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = transitions
                
                
        
        

                    

                        
                        
                    

            
                  
                    
                

            
    
    