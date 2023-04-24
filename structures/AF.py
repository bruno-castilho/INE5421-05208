import pandas as pd

class AF():
    def __init__(self, states: list, initial_state: str, symbols: list, final_states: list, transitions: dict):
        self.states = states
        self.initial_state = initial_state
        self.symbols = symbols
        self.final_states = final_states
        self.transitions = transitions
        
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
                        
    
                    
                        
                    

                        
                        
                    

            
                  
                    
                

            
    
    