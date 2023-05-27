from structures.AF import AF


class Write():
    def AF(AF: AF, filename: str):
        type = AF.getType()
        initial_state = AF.getInitialState()
        final_states = AF.getFinalStates()
        symbols = AF.getSymbols()
        states = AF.getStates()
        transitions = AF.getTransitions()
        
        ref_arquivo = open(f'data/{filename}', "w")
        ref_arquivo.write(str(type) + "\n")
        ref_arquivo.write(str(initial_state) + "\n")
        
        #Escreve estados finais
        for i in range(len(final_states)):
            if i < len(final_states) -1:
                ref_arquivo.write(str(final_states[i]) + ',')
            else:
                ref_arquivo.write(str(final_states[i]) + '\n')
                
        #Escreve simbolos
        for i in range(len(symbols)):
            if i < len(symbols) -1:
                ref_arquivo.write(str(symbols[i]) + ',')
            else:
                ref_arquivo.write(str(symbols[i]) + '\n')
        
        #Escreve estados
        for i in range(len(states)):
            if i < len(states) -1:
                ref_arquivo.write(str(states[i]) + ',')
            else:
                ref_arquivo.write(str(states[i]))
        
        #Escreve transições
        for state in states:
            for symbol in symbols:
                if type == 0:
                    if transitions[state][symbol] != None:
                        ref_arquivo.write( '\n' + f'{state},{symbol},{transitions[state][symbol]}')
                elif type == 1:
                    if len(transitions[state][symbol]) != 0:
                        ref_arquivo.write('\n' + f'{state},{symbol},')
                        for i in range(len(transitions[state][symbol])):
                            if i < len(transitions[state][symbol]) -1:
                                ref_arquivo.write(str(transitions[state][symbol][i]) + '-')
                            else:
                                ref_arquivo.write(str(transitions[state][symbol][i]))
        
        
    