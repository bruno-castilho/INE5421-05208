from os import system, name
import time
from read import Read
from write import Write
from determination import Determination
from GRtoAFND import GRtoAFND
from AFDtoGR import AFDtoGR

def clear(): 
    if name == 'nt': 
        system('cls') 

    else: 
        system('clear') 


options = '''
Opções:
1  - Conversão de AFND (com e sem ε) para AFD
2  - Conversão de AFND (com e sem ε) para AFD
3  - Conversão de AFND (com e sem ε) para AFD
4  - Conversão de AFND (com e sem ε) para AFD
5  - Conversão de AFND (com e sem ε) para AFD
6  - Conversão de AFND (com e sem ε) para AFD
7  - Conversão de AFND (com e sem ε) para AFD
8  - Conversão de AFND (com e sem ε) para AFD
9  - Conversão de AFND (com e sem ε) para AFD
10 - Exit
    '''



while True:
    clear()
    print(f'{options}', end='\r')
    chosen = input('Escolha uma das opções a cima: ')
    if chosen == '1':
        clear()
        print('Insira o arquivo  do AFND de entrada na pasta ./data e digite o nome do arquivo a baixo(-1 para voltar)')
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
            chosen = input('Escolha uma das opções a cima: ')
            if chosen == '1':
                clear()
                print('Insira o arquivo  do AFND de entrada na pasta ./data e digite o nome do arquivo a baixo(-1 para voltar)')
                filename = input('Nome do arquivo: ')
                if filename != '-1':
                    AF = Read.AF(filename)
                    if AF.getType() == '0':
                        clear()
                        print('############################## AFD de Entrada #############################')
                        AF.print()
                        print()
                        print('############################## GR de Saida #############################')
                        GR = AFDtoGR.generate(AF)
                        GR.print()
                        time.sleep(30)
                        
                    
            elif chosen == '2':
                clear()
                print('Insira o arquivo gramatica de entrada na pasta ./data e digite o nome do arquivo a baixo(-1 para voltar)')
                filename = input('Nome do arquivo: ')
                if filename != '-1':
                    GR = Read.GRR(filename)
                    print('############################## GR de Entrada #############################')
                    GR.print()
                    print()
                    print('############################## AFND de Saida #############################')
                    AFND = GRtoAFND.generate(GR)
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
            elif chosen == '3':
                break
            else:
                clear()
                print('Escolha uma opção valida!')
                time.sleep(2)

    elif chosen == '3':
        break
    elif chosen == '4':     
        break
    elif chosen == '5':
        break
    elif chosen == '6':
        break
    elif chosen == '7':
        break
    elif chosen == '8':
        break
    elif chosen == '9':
        break
    elif chosen == '10':
        break
    else:
        clear()
        print('Escolha uma opção valida!')
        time.sleep(2)
        
    

