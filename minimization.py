from structures.AF import AF

def minimize(af: AF):

    newS = {}

    
    #estados
    for stateNEW in af.getStates():
        newS[stateNEW] = [stateNEW]

    #pega o estado inicial
    reacheble_states = af.initial_state
    stack = af.getStates()

    alcan = []


    for state in newS.keys():
         for symbol in af.getSymbols():
            alcan.append(af.getTransition(state, symbol))
            
    unal = af.getStates()
    
    #remove os estados alcansáveis
    for alcState in unal:
        for state in alcan:
            if (alcState == state):
                if (state in unal):
                    unal.remove(state)


    newSS = {}

    for stateNEW in af.getStates():
        newSS[stateNEW] = [stateNEW]

    reacheble_states = af.initial_state

    #inicialisa uma matriz que usa marcações
    alcan2 = [[0 for x in range(2)] for y in range(len(af.getStates()))]
    count = 0
    #seta valores iniciais
    for stado in af.getStates():
        alcan2[count][0] = stado
        count = count + 1
    #primeiro estado marcado
    alcan2[0][1] = 1
    
    iniState = af.getInitialState()

    stack2 = []

    stack2.append(iniState)
    #marca estados alcansáveis
    while (len(stack2) != 0):
            
        for symbol in af.getSymbols(): 
            for tran in af.getTransition(stack2[0],symbol):
                count2 = 0
                for states in af.getStates():
                    if (alcan2[count2][0] == tran and alcan2[count2][1] != 1):
                        alcan2[count2][1] = 1
                        if(tran != stack[0]):
                            stack2.append(tran)    
                    count2 = count2 + 1

        
        stack2.pop(0)
    
    stack3 = []

    stateF = af.getFinalStates()

    alcan3 = [[0 for x in range(2)] for y in range(len(af.getStates()))]
    count = 0

    for stado in af.getStates():
        alcan3[count][0] = stado
        count = count + 1

    #coloca na stack os estados finais
    for statesX in stateF:
        stack3.append(statesX)

    #marca os estados
    countX = 0
    for states in af.getStates():
        for size in stack3:
            if (states == size):
                alcan3[countX][1] = 1
        countX = countX + 1

    stack4 = []

    count3 = 0

    #marca os estados não mortos
    while (stack3 != stack4):
        stack4 = stack3
        for final in stack3:
            count3 = 0
            for states in af.getStates():
                for symbol in af.getSymbols():
                    for tran in af.getTransition(states, symbol):
                        if (tran == final and states != final and alcan3[count3][1] != 1):
                            stack3.append(states)
                            alcan3[count3][1] = 1
                
                count3 = count3 + 1            

    stackF = []

    #stackF com alcansáveis e não mortos
    for x in alcan2:
        for y in stack3:
            if (x[0] == y):
                stackF.append(x[0])

    #inicia a matriz de transições zerada
    matr = [[0 for x in range(3)] for y in range(len(stackF)*len(stackF))]

    countF = 0
    countStd = 0

    #coloca as transições na matr
    while countF < len(matr):
        for x in stackF:
            matr[countF][0] = stackF[countStd]
            matr[countF][1] = x
            countF = countF + 1
        countStd = countStd + 1
    
    finalStates = af.getFinalStates()# onde final states não é morto (está na stackF)
    finalStates2 = []
    tran2 = []
    addSeila = matr

    #faz o algoritmo de minimização 
    # https://www.codingninjas.com/codestudio/library/dfa-minimization    
    while(finalStates != finalStates2):
        for x in finalStates:
            if (x not in finalStates2):
                finalStates2.append(x)    
        for x in matr:
            for symbol in af.getSymbols():
                for y in finalStates:
                    for tran in af.getTransition(x[0], symbol):
                        if (#TESTE Não final com final
                            (x[1] == tran and tran == y and x[0] != y) #or (x[0] == x[1])
                            # TESTE Final com não final
                            or (x[1] == tran and x[0] == y and x[1] != y)
                            ):
                            x[2] = 1
                        
    # trata os valores fara da tabela para a junção(q0 - q2 = 1 logo q2 - q0 = 1) 
    # (olhamos só o triangulo de baixo) (codeninja dfa-minimization)
    
    antigaMatr = []

    for statesMatr in matr:
        antigaMatr.append(statesMatr)

    # ta olhando todos                 
    #while (antigaMatr == matr): # n precisa

        for symbol in af.getSymbols():
            for w in matr:
                for tran in af.getTransition(w[0], symbol):
                    for z in matr:
                        for tran2 in af.getTransition(z[0], symbol):
                        #EXISTE UMA TRANSAÇÂO QUE NF CHEGA EM F E OUTRA NF CHEGA EM F OU VICE VERSA  
                        # N MARCA 
                            if (w[2] == 0 and z[0] == w[1] and 
                                (tran  not in af.getFinalStates() and tran2 in af.getFinalStates())):
                                    
                                print("W")
                                print(w)
                                print(tran)
                                print("Z")
                                print(z)
                                print(tran2)
                                w[2] = 1
                            
                            if (w[2] == 0 and z[0] == w[1] and 
                                (tran in af.getFinalStates() and tran2 not in af.getFinalStates())):
                                w[2] = 1 

    '''
    #valores ao contario entram na matrix [a][b] = 1 => [b][a] = 1 NÂO PRECISA (eu acho)
    for x in matr:
        if (x[2] == 1):
            for y in matr:
                if (x[0] == y[1] and x[1] == y[0]):
                    y[2] = 1
    '''

    #JUNTAR OS ESTADOS se x[0] == x[1] ignora
    closures = {}

    newStates = []
    n1States = []
    n2States = []

    for g in stackF:
            closures[g] = [g]

    delClosures = []

    for x in matr:
        for y in closures:
            print("c")
            print(y)
            if (x[0] != x[1] and x[2] == 0 and x[0] not in newStates):
                if (x[0] not in delClosures):
                    delClosures.append(x[0])
    #            newStates.append("'"+x[0]+"', '"+x[1]+"'")
    #            n1States.append(x[0])
    #            n2States.append(x[1])
    for x in delClosures:
        del closures[x]
    
    #Update para estados
    #closures.update({str(delClosures) : for z in delClosures: for x in af.getSymbols: for y in af.getTransition(z,x): y})

    #closures[str(delClosures)] 
    
    #for x in delClosures: 
    #    for z in af.getSymbols: 
    #        af.getTransition(x,symbol)
    #for states in stackF:
    #    if (states not in n1States and states not in n2States):
    #        newStates.append(states)
                            

    print(matr)
    print(af.getFinalStates())
    print(newStates)
    print(stackF)
    print(closures)
    print(delClosures)

    return 0

def main():
    af = AF(states=['q0','q1', 'q2', 'q3'], 
            initial_state='q0', 
            symbols=['a', 'b'], 
            final_states=['q2'],
            transitions= { 
                            'q0': {
                                'a': ['q2','q3'],
                                'b': ['q1']
                                },
                            'q1': {
                                'a': ['q0'],
                                'b': ['q1']
                                },
                            'q2': {
                                'a': ['q2'],
                                'b': []
                                },
                            'q3': {
                                'a': ['q0'],
                                'b': ['q3']
                                }
                            }
            )

    af.print()      
    minimize(af)



main()