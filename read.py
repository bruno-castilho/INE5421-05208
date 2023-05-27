from structures.AF import AF


class Read():
    def AFND(filename):
        ref_arquivo = open(f'data/{filename}', "r")
        type = ref_arquivo.readline().rstrip('\n')
        
        if type == '1':
            initial_state = ref_arquivo.readline().rstrip('\n')
            final_states = ref_arquivo.readline().rstrip('\n').split(',')
            symbols = ref_arquivo.readline().rstrip('\n').split(',')
            states = ref_arquivo.readline().rstrip('\n').split(',')        
            transitions = {}
            
            for state in states:
                transitions[state] = {}
                for symbol in symbols:
                    transitions[state][symbol] = []
            
            for value in ref_arquivo:
                value = value.rstrip('\n').split(',')
                transitions[value[0]][value[1]] = value[2].split('-')
            
            return AF(1, states, initial_state, symbols, final_states, transitions)
        
        ref_arquivo.close()
    
    def GRR(filename):
        ref_arquivo = open(f'data/{filename}', "r")
        l = ref_arquivo.readline().rstrip('\n')        
        l = l.replace(' ', '')
        print(l.split('->'))
        
        

