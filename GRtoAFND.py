from structures.AF import AF
from structures.GR import GR

class GRtoAFND():
    """
    Uma classe para transformar GR em AFND.
    
    Métodos
    -------
    
    transform(GR: GR) -> AF:
        Retorna AFND.
        
    """
    def transform(GR: GR):
        #GRAMÁTICA INICIAL.
        N = GR.getN()  
        T = GR.getT()
        if '&' in T:
            T.remove('&')
        P = GR.getP()
        S = GR.getS()
        
        #AUTÔMATO RESULTANTE.
        
        #Define transições.
        transitions = {}
        
        #Para cada não terminal da gramática.
        for n in N:
            #Cria transições a partir do não terminal 'n' para todos os terminais 't' como uma lista vazia.
            transitions[n] = {}
            for t in T:
                transitions[n][t] = []
            
            #Para cada produção de 'n'.
            for p in P[n]:
                #Se a produção for diferente de '&'.
                if p['t'] != '&':
                    #Se na produção houver um não terminal.
                    if 'n' in p.keys():
                        #Adiciona uma transição a partir do terminal da produção para o não terminal.
                        transitions[n][p['t']] += [p['n']]
                    #Se não.
                    else:
                        #Adiciona uma transição a partir do terminal da produção para 'X'.
                        transitions[n][p['t']] += ['X']
        
        #Define todas as transições a partir de 'X' para uma lista vazia.
        transitions['X'] = {t: [] for t in T}
        
        states = N + ['X'] #Lista de estados do autômato igual a lista de não terminais da gramática + 'X'.
        initial_state =  S #O estado inicial do autômato é igual ao símbolo inicial da gramática.
        symbols = T #Lista de símbolos do autômato é igual a lista de terminais da gramática.
        final_states = ['X'] #Os estados finais do autômato contém o 'X'.
        
        #Se nas produções do símbolo inicial da gramática conter '&', o estado inicial do autômato é um estado final.
        if '&' in [p['t'] for p in P[S]]:
            final_states.append(S)
            
        #Retorna autômato resultante.
        return AF(1,states, initial_state, symbols, final_states, transitions)
                 
