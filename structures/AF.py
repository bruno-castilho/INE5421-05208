import pandas as pd

class AF():
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
    
    def getTransition(self, state, symbol):
        return self.transitions[state][symbol]
    
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
                        
    def adjust(self, s):
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
                
                
        
        

                    

                        
                        
                    

            
                  
                    
                

            
    
    