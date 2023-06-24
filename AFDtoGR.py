from structures.AF import AF
from structures.GR import GR


class AFDtoGR():
    """
    Uma classe para transformar AFD em GR.
    
    Métodos
    -------
    
    transform(AF: AF) -> GR:
        Retorna GR.
        
    """
    def transform(AF: AF):
        #Autômato inicial.
        states = AF.getStates()
        initial_state = AF.getInitialState()
        symbols = AF.getSymbols()
        final_states = AF.getFinalStates()
        transitions = AF.getTransitions()
        
        #Gera gramática.
        P = {}
        #Para cada estado do autômato.
        for state in states:
            #Cria uma lista de produções produzidas por um não terminal 'state'.
            P[state] = []
            #Para cada símbolo do autômato.
            for symbol in symbols:
                #Se a transição de 'state' por 'symbol' for diferente de None.
                if transitions[state][symbol] != None:
                    #Adiciona uma produção em 'state' com um terminal 'symbol' e um não terminal como o estado alcançado pela transição.
                    P[state].append({'t': symbol, 'n': transitions[state][symbol]})
                    #Se o estado alcançado pela transição for um estado final.
                    if transitions[state][symbol] in final_states:
                        #Adiciona uma produção apenas como o terminal 'symbol'.
                        P[state].append({'t': symbol})
        
        #Se o estado inicial do autômato for um estado final.
        if initial_state in final_states:
            #Adiciona & como uma produção do não terminal 'initial_state'.
            P[initial_state].append({'t':'&'})
        
        
        N = states #Lista de não terminais igual a estados do autômato.
        T = symbols #Lista de terminais igual a símbolos do autômato.
        S = initial_state #Símbolo inicial da gramática igual ao estado inicial do autômato.
        
        #Retorna gramática.
        return GR(N,T,P,S)
    
