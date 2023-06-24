from os import system, name
import time
from read import Read
from write import Write
from Determination import Determination
from GRtoAFND import GRtoAFND
from AFDtoGR import AFDtoGR
from ERtoAFD import ERtoAFD
from Compute import Compute
from Union import Union
from Intersecao import Intersecao
from Minimization import Minimization
from structures.GLC import fatorar, remover_recursao_esquerda_direta, remover_recursao_esquerda_indireta

def clear(): 
    if name == 'nt': 
        system('cls') 

    else: 
        system('clear') 


options = '''
Opções:
1  - Conversão de AFND (com e sem ε) para AFD
2  - Conversão de AFD para GR e de GR para AFND
3  - Minimização de AFD
4  - União e interseção de AFD
5  - Conversão de ER para AFD
6  - Reconhecimento de sentenças em AF
7  - Reconhecimento de sentenças em AP (via implementação de uma tabela Preditivo LL(1))
8  - Exit
    '''



while True:
    print(f'{options}', end='\r')
    chosen = input('Escolha uma das opções acima: ')
    if chosen == '1':
        clear()
        print('Insira o arquivo  do AFND de entrada na pasta ./data e digite o nome do arquivo abaixo(-1 para voltar)')
        filename = input('Nome do arquivo: ')
        if filename != '-1':
            AF = Read.AF(filename)
            if AF.getType() == '1':
                clear()
                print('############################## AFND de Entrada #############################')
                AF.print()
                print()
                print('############################## AFD de Saida #############################')
                AFD = Determination.determinize(AF)
                AFD.adjust('q')
                AFD.print()
                while True: 
                    answer = input('Deseja salvar o automato?(S/N): ')
                    if answer == 'S' or answer == 's':
                        filename = input('Digite um nome para o arquivo: ')
                        Write.AF(AFD, filename)
                        break
                    elif answer == 'N' or answer == 'n':
                        break
                    else:
                        print('Reposta invalida!')
                        time.sleep(2)
            else:
                clear()
                print('AF invalido!')
                time.sleep(2)
    
    elif chosen == '2':
        while True:
            clear()
            print('''
Opções:
1  - AFD para GR
2  - GR para AFND
3  - Voltar
'''         )   
            chosen = input('Escolha uma das opções acima: ')
            if chosen == '1':
                clear()
                print('Insira o arquivo  do AFD de entrada na pasta ./data e digite o nome do arquivo abaixo(-1 para voltar)')
                filename = input('Nome do arquivo: ')
                if filename != '-1':
                    AF = Read.AF(filename)
                    if AF.getType() == '0':
                        clear()
                        print('############################## AFD de Entrada #############################')
                        AF.print()
                        print()
                        print('############################## GR de Saida #############################')
                        GR = AFDtoGR.transform(AF)
                        GR.print()
                        while True: 
                            answer = input('Deseja salvar a GR ?(S/N): ')
                            if answer == 'S' or answer == 's':
                                filename = input('Digite um nome para o arquivo: ')
                                Write.GR(GR, filename)
                                break
                            elif answer == 'N' or answer == 'n':
                                break
                            else:
                                print('Reposta invalida!')
                                time.sleep(2)
            elif chosen == '2':
                clear()
                print('Insira o arquivo gramatica de entrada na pasta ./data e digite o nome do arquivo abaixo(-1 para voltar)')
                filename = input('Nome do arquivo: ')
                if filename != '-1':
                    GR = Read.GR(filename)
                    print('############################## GR de Entrada #############################')
                    GR.print()
                    print()
                    print('############################## AFND de Saida #############################')
                    AFND = GRtoAFND.transform(GR)
                    AFND.print()
                    while True: 
                        answer = input('Deseja salvar o automato?(S/N): ')
                        if answer == 'S' or answer == 's':
                            filename = input('Digite um nome para o arquivo: ')
                            Write.AF(AFND, filename)
                            break
                        elif answer == 'N' or answer == 'n':
                            break
                        else:
                            print('Reposta invalida!')
                            time.sleep(2)
                            
            elif chosen == '3':
                break
            else:
                clear()
                print('Escolha uma opção valida!')
                time.sleep(2)

    elif chosen == '3':
        clear()
        print('Insira o arquivo  do AFD de entrada na pasta ./data e digite o nome do arquivo abaixo(-1 para voltar)')
        filename = input('Nome do arquivo: ')
        if filename != '-1':
            AFD = Read.AF(filename)
            if AFD.getType() == '0':
                clear()
                print('############################## AFD de Entrada #############################')
                AFD.print()
                print()                
                print('############################## AFD de Saida #############################')
                AFD = Minimization.removeUnobtainables(AFD)
                AFD = Minimization.removeDeadStates(AFD)
                AFD = Minimization.removeEquivalents(AFD)
                AFD.adjust('q')
                AFD.print()
                while True: 
                    answer = input('Deseja salvar o automato?(S/N): ')
                    if answer == 'S' or answer == 's':
                        filename = input('Digite um nome para o arquivo: ')
                        Write.AF(AFD, filename)
                        break
                    elif answer == 'N' or answer == 'n':
                        break
                    else:
                        print('Reposta invalida!')
                        time.sleep(2)
            else:
                clear()
                print('AF invalido!')
                time.sleep(2)
    
    elif chosen == '4':   
        while True:
            clear()
            print('''
Opções:
1  - União
2  - Interseção
3  - Voltar
'''         )   
            chosen = input('Escolha uma das opções acima: ')
            if chosen == '1':
                clear()
                print("Insira os arquivos  dos AFD's de entrada na pasta ./data e digite o nome do arquivo abaixo(-1 para voltar)")
                
                filename1 = input('Nome do arquivo do AF1: ')
                if filename1 == '-1' : pass

             
                filename2 = input('Nome do arquivo do AF2: ')
                
                if filename2 != '-1':
                    AF1 = Read.AF(filename1)
                    AF2 = Read.AF(filename2)
                    
                    if AF1.getType() == '0' and AF2.getType() == '0':
                        clear()
                        print('############################## AFD1 de Entrada #############################')
                        AF1.print()
                        print()
                        print('############################## AFD2 de Entrada #############################')
                        AF2.print()
                        print()
                        print('############################## AFND de Saida #############################')
                        AFND = Union.transform(AF1, AF2)
                        AFND.print()
                        while True: 
                            answer = input('Deseja salvar o AFND ?(S/N): ')
                            if answer == 'S' or answer == 's':
                                filename = input('Digite um nome para o arquivo: ')
                                Write.AF(AFND, filename)
                                break
                            elif answer == 'N' or answer == 'n':
                                break
                            else:
                                print('Reposta invalida!')
                                time.sleep(2)
            elif chosen == '2':
                clear()
                print("Insira os arquivos  dos AFD's de entrada na pasta ./data e digite o nome do arquivo abaixo(-1 para voltar)")
                filename1 = input('Nome do arquivo do AF1: ')
                if filename1 == '-1' : pass
            
                filename2 = input('Nome do arquivo do AF2: ')
                if filename2 != '-1':
                    AF1 = Read.AF(filename1)
                    AF2 = Read.AF(filename2)
                    
                    if AF1.getType() == '0' and AF2.getType() == '0':
                        clear()
                        print('############################## AFD1 de Entrada #############################')
                        AF1.print()
                        print()
                        print('############################## AFD2 de Entrada #############################')
                        AF2.print()
                        print()
                        print('############################## AFD de Saida #############################')
                        AFD = Intersecao.transform(AF1, AF2)
                        AFD.adjust('q')
                        AFD.print()
                        while True: 
                            answer = input('Deseja salvar o AFD ?(S/N): ')
                            if answer == 'S' or answer == 's':
                                filename = input('Digite um nome para o arquivo: ')
                                Write.AF(AFD, filename)
                                break
                            elif answer == 'N' or answer == 'n':
                                break
                            else:
                                print('Reposta invalida!')
                                time.sleep(2)
                            
            elif chosen == '3':
                break
            else:
                clear()
                print('Escolha uma opção valida!')
                time.sleep(2)
            
    elif chosen == '5':
        clear()
        print('Insira o arquivo  da ER de entrada na pasta ./data e digite o nome do arquivo abaixo(-1 para voltar)')
        filename = input('Nome do arquivo: ')
        if filename != '-1':
            print('############################## ER de Entrada #############################')
            ER = Read.ER(filename)
            ER.print()
            print('############################## AFD de Saida #############################')
            AFD = ERtoAFD.transform(ER)
            AFD.print()
            AFD.adjust('q')
            AFD.print()
            while True: 
                    answer = input('Deseja salvar o automato?(S/N): ')
                    if answer == 'S' or answer == 's':
                        filename = input('Digite um nome para o arquivo: ')
                        Write.AF(AFD, filename)
                        break
                    elif answer == 'N' or answer == 'n':
                        break
                    else:
                        print('Reposta invalida!')
                        time.sleep(2)
                        
    elif chosen == '6':
        clear()
        print('Insira o arquivo  do AF de entrada na pasta ./data e digite o nome do arquivo abaixo(-1 para voltar)')
        filename = input('Nome do arquivo: ')
        if filename != '-1':
            AF = Read.AF(filename)
            if AF.getType() == '0':
                clear()
                print('############################## AFD de Entrada #############################')
                AF.print()
                print()
                sentence = input('Digite a sentença que deseja computar: ')
                print('############################## Computando... #############################')
                result = Compute.AFD(AF, sentence)
                if result == True:
                    print('Senteça validada!')
                else:
                    print('Senteça rejeitada!')
                    
                input('Pressione enter para continuar')
    
            elif AF.getType() == '1':
                clear()
                print('############################## AFND de Entrada #############################')
                AF.print()
                print()
                sentence = input('Digite a sentença que deseja computar: ')
                print('############################## Computando... #############################')
                result = Compute.AFND(AF, sentence)
                if result == True:
                    print('Senteça validada!')
                else:
                    print('Senteça rejeitada!')
                    
                input('Pressione enter para continuar')
        
# leitura e edição de uma Gramática Livre de contexto (considerando terminais como um único símbolo minúsculo e não terminais maiúsculos (1pt) 
# algoritmo para verificação de não determinismo e fatoração da gramática (1pt)
# algoritmo para eliminação de recursão a esquerda (1pt)
# Firsts e Follows (1pt)
# construção da tabela do preditivo LL(1) e construção do algoritmo que simula a pilha para o reconhecimento de uma sentença de entrada (1pt)
    elif chosen == '7':
        while True:
            print('''
Opções:
1  - Fatorar
2  - Eliminar recursão a esquerda 
3  - Reconhecimento de sentença
4  - Voltar
'''         )
            chosen = input('Escolha uma das opções acima: ')
            if chosen == '1':
                clear()
                print('Insira o arquivo da GLC na pasta ./data e digite o nome do arquivo abaixo(-1 para voltar)')
                filename = input('Nome do arquivo: ')
                glc = Read.GLC(filename)
                print("Fatoração para a GLC abaixo:")
                glc.display()
                fatorar(glc)
                print("Saída:")
                glc.display()
                answer = input('Deseja salvar a gramatica?(S/N): ')
                if answer == 'S' or answer == 's':
                    filename = input('Digite um nome para o arquivo: ')
                    Write.GLC(glc, filename)
                    break
                elif answer == 'N' or answer == 'n':
                    break

            elif chosen == '2':
                while True:
                    print('''
        Opções:
        1  - Recursão direta
        2  - Recursão indireta
        3  - Voltar
        '''         )
                    chosen2 = input('Escolha uma das opções acima: ')
                    if chosen2 == '1':
                        print('Insira o arquivo da GLC na pasta ./data e digite o nome do arquivo abaixo(-1 para voltar)')
                        filename = input('Nome do arquivo: ')
                        glc = Read.GLC(filename)
                        print("Removendo recursão direta da GLC abaixo:")
                        glc.display()
                        glc = remover_recursao_esquerda_direta(glc)
                        print('Saída:')
                        glc.display()
                        answer = input('Deseja salvar a gramatica?(S/N): ')
                        if answer == 'S' or answer == 's':
                            filename = input('Digite um nome para o arquivo: ')
                            Write.GLC(glc, filename)
                            break
                        elif answer == 'N' or answer == 'n':
                            break
                        break
                    elif chosen2 == '2':
                        print('Insira o arquivo da GLC na pasta ./data e digite o nome do arquivo abaixo(-1 para voltar)')
                        filename = input('Nome do arquivo: ')
                        glc = Read.GLC(filename)
                        print("Removendo recursão indireta da GLC abaixo:")
                        glc.display()
                        glc = remover_recursao_esquerda_indireta(glc)
                        print('Saída:')
                        glc.display()
                        print("Removendo recursão direta da GLC gerada pela remoção de indireta acima:")
                        glc = remover_recursao_esquerda_direta(glc)
                        print('Saída:')
                        glc.display()
                        answer = input('Deseja salvar a gramatica?(S/N): ')
                        if answer == 'S' or answer == 's':
                            filename = input('Digite um nome para o arquivo: ')
                            Write.GLC(glc, filename)
                            break
                        elif answer == 'N' or answer == 'n':
                            break
                        break
                    elif chosen2 == '3':
                        break 
                    else:
                        clear()
                        print('Escolha uma opção valida!')
                        time.sleep(2)

            elif chosen == '3':
                print('Insira o arquivo da GLC na pasta ./data e digite o nome do arquivo abaixo(-1 para voltar)')
                filename = input('Nome do arquivo: ')
                glc = Read.GLC(filename)
                sentenca = input('Sentença que deve ser reconhecida: ')
                print("Reconhecimento de sentença para a GLC abaixo:")
                glc.display()
                print(f'Sentença: {sentenca}\nResultado: {glc.reconhecer(sentenca)}')
                break       
            elif chosen == '4':
                break
            else:
                clear()
                print('Escolha uma opção valida!')
                time.sleep(2)

    elif chosen == '8':
        break
    else:
        clear()
        print('Escolha uma opção valida!')
        time.sleep(2)
        
    

