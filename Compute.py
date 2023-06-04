from structures.AF import AF

class Compute():
    
    """
    Uma classe para computar uma sentença em um AF
    
    Métodos
    -------

    AFD(AF: AF, sentence: str) -> boolean:
        Computa uma sentença em um AFD.
    
    AFND(AF: AF, sentence: str) -> boolean:
        Computa uma sentença em um AFND.
        
    """
    def AFD(AF: AF, sentence: str):
        current_state = AF.getInitialState()
        while len(sentence) > 0:
            if current_state:
                print(f'estado atual: {current_state}')
                print(f'sentença: {sentence}')
                print('/////////////////////')
                current_state = AF.getTransition(current_state, sentence[0])
                sentence = sentence[1:]
            else:
                print(f'estado atual: Morto')
                print(f'sentença: {sentence}')
                return False
        
        print(f'estado atual: {current_state}')
        print(f'sentença: Ø')
            
        if current_state in AF.getFinalStates():
            return True

        return False
    
    def AFND(AF: AF, sentence: str):
        current_states = [AF.getInitialState()]
        while len(sentence) > 0:
            print(f'estados atuais: {current_states}')
            print(f'sentença: {sentence}')
            if len(current_states) > 0:
                print('/////////////////////')
                new_current_states = []
                for state in current_states:
                    states = AF.getTransition(state, sentence[0])
                    if states:
                        new_current_states += states
                
                current_states = new_current_states
                sentence = sentence[1:]
            else:
                return False
        
        print(f'estados atuais: {current_states}')
        print(f'sentença: Ø')
        
        for state in current_states:
            if state in AF.getFinalStates():
                return True
        
        return False