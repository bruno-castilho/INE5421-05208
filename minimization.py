from structures.AF import AF

def minimize(af: AF):

    #ja retira estados inalcansáveis
    #af = determinize(af)    

    #for n pode mudar tamanho ;-;
    
    #stack que da pop por estado visitado em um while
    '''
    visited_states = {a:False for a in af.getStates()}
    #Marca estado como já visitado.
    visited_states[af.initial_state] = True

    stack = af.getStates()

    while (len(stack) != 0):

        state = stack.pop()
    
        for symbol in af.getSymbols():
            #se existir uma transição pelo estado
            if (af.getTransition(state,symbol) is not None):            
                for statesT in af.getTransition(state,symbol):
                    visited_states[statesT] = True
    
    new_states = visited_states.keys()
    #problema com dois inalcansáveis que são ciclos? TEM QUE SER RECURSIVO, DA RUIM SE N FOR

    visited_states2 = {a:False for a in af.getStates()}
    #Marca estado como já visitado.
    visited_states2[af.initial_state] = True

    stack2 = af.getStates()

    #reverse a ordem de stack?

    #

    while (len(stack2) != 0):

        state = stack2.pop()
    
        for symbol in af.getSymbols():
            #se existir uma transição pelo estado
            if (af.getTransition(state,symbol) is not None):            
                for statesT in af.getTransition(state,symbol):
                    visited_states[statesT] = True
    
    new_states = visited_states.keys()


    #remove os estados inalcansáveis
    
    for symbol in af.getSymbols():
        reacheble_states = af.getTransition(af.initial_state,symbol)
    '''
    #coloca um while aqui, adiciona um copy e coloca o copy para entrar no original depois do for 
    # então vai ser iterativo/recursivo
    # para sair do while - if (af.getTransition(state,symbol) is None):
    # aí da um break no while
    
    #while(len(s)), count i, if(i == 1 OR i mod 6 == 1){append(s[i:i+3])} assim pega os estados clean
    newS = {}

    for stateNEW in af.getStates():
        newS[stateNEW] = [stateNEW]

    #print(af.getStates())
    #print(newS)

    reacheble_states = af.initial_state
    stack = af.getStates()

    #print(newS.keys())

    alcan = []

    for state in newS.keys():
    #     print(state)
         for symbol in af.getSymbols():
            alcan.append(af.getTransition(state, symbol))
            

    #print(alcan)

    unal = af.getStates()
    #print(unal)
    
    for alcState in unal:
    #    print(alcState)
        for state in alcan:
    #        print(state)
            if (alcState == state):
    #            print("RARA")
    #            print(state)
    #            print("RARA")
                if (state in unal):
                    unal.remove(state)

    #print("unal")
    #print(unal)
    #print("unal")

    #print("###########")

    newSS = {}

    for stateNEW in af.getStates():
        newSS[stateNEW] = [stateNEW]

    #print(af.getStates())
    #print(newSS)

    reacheble_states = af.initial_state
    

    #print(newS.keys())

    #print(len(af.getStates()))


    alcan2 = [[0 for x in range(2)] for y in range(len(af.getStates()))]
    count = 0

    for stado in af.getStates():
        alcan2[count][0] = stado
        count = count + 1
    
    #print(alcan2)

    alcan2[0][1] = 1
    
    #print(alcan2[0][0])

    iniState = af.getInitialState()

    stack2 = []

    stack2.append(iniState)
    #print("sta")
    #print(stack2[0])
    #print("sta")

    while (len(stack2) != 0):
            
        for symbol in af.getSymbols(): 
            for tran in af.getTransition(stack2[0],symbol):
                count2 = 0
    #            print("stado")
    #            print(stack2[0])
    #            print("stado")
    #            print(tran)
    #            print("///")
                for states in af.getStates():
                    if (alcan2[count2][0] == tran and alcan2[count2][1] != 1):
                        alcan2[count2][1] = 1
                        if(tran != stack[0]):
                            stack2.append(tran)    
                    count2 = count2 + 1

        
        stack2.pop(0)
    

    #estados alcansáveis
    #print(alcan2)



    #print("###########")
    
    #colocar na stack todos os finais, append nos que tem alguma transição para o final
    #fazer isso até que depois da verificação a stack anterior = nova (sem modificações)
    #print("###########")

    stack3 = []

    stateF = af.getFinalStates()

    #print(stateF)

    alcan3 = [[0 for x in range(2)] for y in range(len(af.getStates()))]
    count = 0

    for stado in af.getStates():
        alcan3[count][0] = stado
        count = count + 1
    
    #print(alcan3)
    
    for statesX in stateF:
        stack3.append(statesX)

    #print(stack3)

    countX = 0
    for states in af.getStates():
        for size in stack3:
            if (states == size):
                alcan3[countX][1] = 1
        countX = countX + 1

    stack4 = []

    count3 = 0

    while (stack3 != stack4):
        stack4 = stack3
        for final in stack3:
            #print("final")
            #print(final)
            count3 = 0
            for states in af.getStates():
                #print("state")
                #print(states)
                for symbol in af.getSymbols():
                    for tran in af.getTransition(states, symbol):
                        if (tran == final and states != final and alcan3[count3][1] != 1):
                            stack3.append(states)
                            alcan3[count3][1] = 1
                
                count3 = count3 + 1            

    #print(stack3)

    #print("########### PT2")

    #print("########### PT3")

    stackF = []

    #print(alcan2)
    #print(stack3)

    #stack com alcansáveis e não mortos
    for x in alcan2:
        for y in stack3:
            #print(x[0])
            #print(y)
            if (x[0] == y):
                stackF.append(x[0])

    #print(stackF)

    matr = [[0 for x in range(3)] for y in range(len(stackF)*len(stackF))]
    
    #print(matr)

    countF = 0
    countStd = 0

    while countF < len(matr):
        
        for x in stackF:
            matr[countF][0] = stackF[countStd]
            matr[countF][1] = x
            countF = countF + 1
        countStd = countStd + 1
        
    #print(matr)
    
    #coloca em um while em uma pilha
    finalStates = af.getFinalStates()# onde final states não é morto (está na stackF)
    finalStates2 = []
    tran2 = []
    addSeila = matr
    
    while(finalStates != finalStates2):
        for x in finalStates:
            if (x not in finalStates2):
                finalStates2.append(x)    
        #print("finalStates")
        #print(finalStates)
        #print(finalStates2)
        for x in matr:
            #print("f2")
            #print(finalStates2)
            for symbol in af.getSymbols():
                for y in finalStates:
                    #print("y")
                    #print(y)

#[['q0', 'q0', 1], ['q0', 'q1', 1], ['q0', 'q2', 1], ['q0', 'q3', 1], ['q0', 'q4', 0], 
# ['q0', 'q5', 0], ['q1', 'q0', 0], ['q1', 'q1', 1], ['q1', 'q2', 1], ['q1', 'q3', 1], 
# ['q1', 'q4', 0], ['q1', 'q5', 0], ['q2', 'q0', 0], ['q2', 'q1', 1], ['q2', 'q2', 1],
#  ['q2', 'q3', 0], ['q2', 'q4', 1], ['q2', 'q5', 0], ['q3', 'q0', 0], ['q3', 'q1', 1],
#  ['q3', 'q2', 0], ['q3', 'q3', 1], ['q3', 'q4', 0], ['q3', 'q5', 1], ['q4', 'q0', 0], 
# ['q4', 'q1', 1], ['q4', 'q2', 1], ['q4', 'q3', 1], ['q4', 'q4', 1], ['q4', 'q5', 0], 
# ['q5', 'q0', 0], ['q5', 'q1', 1], ['q5', 'q2', 0], ['q5', 'q3', 1], ['q5', 'q4', 0], 
# ['q5', 'q5', 1]]
                    for tran in af.getTransition(x[0], symbol):
                        if (#TESTE Não final com final
                            (x[1] == tran and tran == y and x[0] != y) #or (x[0] == x[1])
                            # TESTE Final com não final
                            or (x[1] == tran and x[0] == y and x[1] != y)
                            ):
                            x[2] = 1
                        #PRIMEIRA ITERAÇÃO FUNCIONANDO
                            #if (x[0] not in finalStates):
                                #finalStates.append(x[0])
                        #tran2 = [tran]
                        #q0 olha as marações dele, (q2 e q3), q2 tem marcação (q1, q2, q4)
                        
                                    
                                
                        '''for countSTATE in range(len(af.states)):
                            if (x[2] == 0):    
                                for t in tran2:
                                    for tran3 in af.getTransition(t, symbol):
                                        if (x[1] == tran3 and tran3 == y and x[0] != y):
                                            x[2] = 1
                                            if (x[0] not in finalStates):
                                                finalStates.append(x[0])
                                        if (tran3 not in tran2):
                                            tran2.append(tran3)
                        
        #print("finalStates")
        #print(finalStates)
        #print(finalStates2)
        '''
    # trata os valores fara da tabela para a junção(q0 - q2 = 1 logo q2 - q0 = 1) 
    # (olhamos só o triangulo de baixo) (codeninja dfa-minimization)
    
    
    # depois tem que comprara em um while(se for igual ai sai)
    antigaMatr = []

    for statesMatr in matr:
        antigaMatr.append(statesMatr)

    # ta olhando todos                 
    #while (antigaMatr == matr): -- n precisa

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
    #valores ao contario entram na matrix [a][b] = 1 => [b][a] = 1 NÂO SEI SE PRECISA
    for x in matr:
        if (x[2] == 1):
            for y in matr:
                if (x[0] == y[1] and x[1] == y[0]):
                    y[2] = 1
    '''

    #JUNTAR OS ESTADOS se q0 q0 ignora
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

    #print("########### PT3")
    
    # TA ERRADOOOOOOOOOOOOOOOOOOOOO
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