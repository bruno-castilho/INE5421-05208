from structures.AF import AF
from structures.GR import GR
from structures.ER import ER
from structures.GLC import GLC

class Read():
    """
    Uma classe para fazer leitura de arquivos.
    
    Métodos
    -------
    AF(filename: str) -> AF:
        Retorna AF.
    
    GR(filename: str) -> GR:
        Retorna GR.
    
    ER(filename: str) -> ER:
        Retorna ER.
    """
    def AF(filename: str):
        ref_arquivo = open(f'data/{filename}', "r")
        type = ref_arquivo.readline().rstrip('\n').strip()
        initial_state = ref_arquivo.readline().rstrip('\n').strip()
        final_states = ref_arquivo.readline().rstrip('\n').strip().split(',')
        symbols = ref_arquivo.readline().rstrip('\n').strip().split(',')
        states = ref_arquivo.readline().rstrip('\n').strip().split(',')        
        transitions = {}
            
        for state in states:
            transitions[state] = {}
            for symbol in symbols:
                if type == '0':
                    transitions[state][symbol] = None
                if type == '1':
                    transitions[state][symbol] = []
        
        for value in ref_arquivo:
            value = value.rstrip('\n').strip().split(',')
            if type == '0':
                transitions[value[0]][value[1]] = value[2]
            if type == '1':
                transitions[value[0]][value[1]] = value[2].split('-')
        
        ref_arquivo.close()
        
        return AF(type, states, initial_state, symbols, final_states, transitions)
        
    def GR(filename: str):
        ref_arquivo = open(f'data/{filename}', "r")
        N = ref_arquivo.readline().rstrip('\n').strip().split(',')
        T = ref_arquivo.readline().rstrip('\n').strip().split(',')
        S = ref_arquivo.readline().rstrip('\n').strip()
        P = {}
        
        for value in ref_arquivo:
            string = value.rstrip('\n')
            string = string.replace(' ', '')
            list = string.split('->')
            H = list[0]
            P[H] = []
            for p in list[1].split('|'):
                for t in T:
                    if t in p:
                        data = {'t':t}
                        p = p.replace(t,'')
                        if len(p) > 0:
                            data['n'] = p
                            
                        P[H].append(data)
                        break
                    
        ref_arquivo.close()
        return GR(N=N,T=T,S=S,P=P)

    def ER(filename: str):
        ref_arquivo = open(f'data/{filename}', "r")
        er = ref_arquivo.readline().rstrip('\n') 
        er = er.replace(' ','')
        ref_arquivo.close()
        
        return ER(er)

    def GLC(filename: str):
        texto = None
        try:
            arquivo = open(f'data/{filename}', "r")
            texto = arquivo.read().split('\n')
            arquivo.close()
        except OSError:
            arquivo.close()
        nao_terminais = pegar_nao_terminais(texto)
        terminais = pegar_terminais(texto)
        producoes = pegar_producoes(texto)
        simbolo_inicial = pegar_simbolo_inicial(texto)
    
        return GLC(nao_terminais, terminais, producoes, simbolo_inicial)

def pegar_nao_terminais(texto):
    indice = texto.index('*NaoTerminais')
    return texto[indice+1].split()

def pegar_terminais(texto):
    indice = texto.index('*Terminais')
    return texto[indice+1].split()

def pegar_simbolo_inicial(texto):
    indice = texto.index('*SimboloInicial')
    return texto[indice+1]

def pegar_producoes(texto):
    indice = texto.index('*Producoes')
    return texto[indice+1:-1]