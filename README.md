<p align="center">
<img align="center" src="https://portalpadrao.ufma.br/ineof/imagens/logo-ufsc.png/@@images/84622670-9bb9-4fee-9460-dcfd76b7e33f.png" alt="UFSC logo" width="200" height="250">
</p>

<h1 align="center">
UNIVERSIDADE FEDERAL DE SANTA CATARINA<br />
CENTRO TECNOLÓGICO<br />
CURSO DE GRADUAÇÃO EM CIÊNCIAS DA COMPUTAÇÃO
</h1>
</br>
</br>
</br>
<h3 align="center">
  Gabriel Dutra, Bruno da Silva Castilho e Rafael Begnini de Castilhos
</h3>


</br>

# Trabalho: Manipulação de Linguagens Regulares e Linguagens Livres de Contexto
1. Objetivo do Trabalho:
O objetivo deste trabalho é a implementação dos algoritmos relacionados à manipulação
de Linguagens Regulares e Livres de Contexto. Tais algoritmos são úteis na implementação de Geradores de Analisadores Léxicos e Sintáticos ou na implementação dos próprios
analisadores, servindo de arcabouço para o desenvolvimento de Compiladores.

2. Definição do Trabalho:\
Implementar algoritmos para manipular Autômatos Finitos, Gramáticas Regulares, Expressões Regulares, Gramáticas Livres de Contexto e Autômatos de Pilha.

Os seguintes algoritmos devem ser implementados:
  - Conversão de AFND (com e sem ε) para AFD
  - Conversão de AFD para GR e de GR para AFND
  - Minimização de AFD
  - União e interseção de AFD
  - Conversão de ER para AFD (usando o algoritmo baseado em árvore sintática - Livro
  Aho - seção 3.9)
  - Reconhecimento de sentenças em AF
  - Reconhecimento de sentenças em AP (via implementação de uma tabela Preditivo
  LL(1)) - Além dos algoritmos relacionados a análise da sentença de entrada, devem
  ser implementados os algoritmos para cálculo dos conjuntos First e Follow, Fatoração e Eliminação de Recursão à esquerda 


Observações:
- As entradas podem ser feitas via arquivo ou interface, a critério do grupo;
- Os resultados intermediários devem poder ser salvos. Exemplo: um AFND convertido para AFD deve poder ser unido com outro AFD, ou ainda poder ser minimizado;
- Para épsilon use a notação &;
- Este trabalho é justamente para aprender a lidar com Expressões Regulares.
Logo, não deve-se fazer uso de bibliotecas de Regex.
- AFs podem ser apresentados na forma de tabelas de transição e ou diagramas de
transição, a escolha do grupo;
- Todos os AFs (intermediários ou resultantes) devem ser reutilizáveis (passíveis de
Edição)


## Dependências
  - Projeto desenvolvido na linguagem de programação python, para a instalação do interpretador execute o seguinte comando:
    ```
    apt-get install python3
    ```
  - Neste projeto foi utilizado a biblioteca pandas, para instalação siga os passos abaixo:
    1. Instale o gerenciador de pacotes do python.
       ```
       apt-get install python3-pip
       ```
    2. Instale a biblioteca pandas.
        ```
        pip3 install pandas
        ```

## Tipos de arquivos de entrada
  - Gramáticas Regulares
    - Descreva a GR em um arquivo `.txt`, da seguinte forma:
      1. Linha-1 - símbolos não terminais separados por `,`, exemplo: `A,B,C`
      2. Linha-2 - símbolos terminais separados por `,`, exemplo: `a,b,c`
      3. Linha-3 - símbolo inicial da gramática, exemplo `A`
      4. Linha-4aN - Descreva as produções da seguinte forma `{cabeça de produção}-> prod1 | prod2`, exemplo: `A-> aA | bB | cC| a`
    - Exemplo de arquivo:
      ```txt
      A,B,C
      a,b,c
      A
      A-> aA | bB | cC| a 
      B-> bB | cC | b 
      C-> cC | c
      ```
  - Autômatos Finito
    - Descreva o autômato em um arquivo `.txt`, da seguinte forma:
      1. Linha-1 - Tipo do autômato, `0 para AFD e 1 para AFND`
      2. Linha-2 - Estado inicial do autômato, exemplo: `q0`
      3. Linha-3 - Todos os estados de aceitação do autômato separados por `,`, exemplo: `q1,q2`
      4. Linha-4 - Todos o simbolos reconhecidos pelo autômato separados por `,`, exemplo: `a,b,c`
      5. Linha-5 - Todos os estados do autômato separados por `,`, exemplo: `q0,q1,q2`
      6. Linha-6aN - Transições do autômato, exemplo: `q0,a,q1` ou `q0,a,q1-q2`
    - Exemplos de arquivo:
      ```txt
      0
      q0
      q1,q2
      a,b,c
      q0,q1,q2
      q0,a,q1
      q0,b,q2
      q1,a,q1
      q1,b,q0
      q2,a,q0
      q2,b,q2
      ```
      ```txt
      1
      q0
      q1,q2
      a,b,c
      q0,q1,q2
      q0,a,q1-q2
      q0,b,q1-q2
      q1,a,q1
      q1,b,q0
      q2,a,q0
      q2,b,q2
      ```
- Expressões Regulares
  - Escreva a ER em um arquivo ```.txt```, com os seguintes critérios.
    1. A Expressão deve conter apenas os operadores `*,+,|,?`
    2. A Expressão deve estar contida na primeira linha do arquivo.
  - Exemplo de arquivo:
    ```txt
    (a|b)*(ab)?(ab)(&|a)+
    ```

- Gramáticas Livre de Contexto
    - Descreva a GR em um arquivo `.txt`, da seguinte forma:        
      1. Linha-1 - Definição da gramática, `*GLC`
      2. Linha-2 - Definição de não terminais: `*NaoTerminais`
      3. Linha-3 - Todos os não terminais separados por ` ` (espaço em branco), exemplo: `P K V`
      4. Linha-4 - Definição de terminais: `*Terminais`
      5. Linha-5 - Todos os terminais separados por ` ` (espaço em branco), exemplo: `c v f`
      6. Linha-6 - Definição de simbolo inicial: `*SimboloInicial`
      7. Linha-7 - Simbolo inicial, exemplo: `P`
      8. Linha-8 - Definição de produções: `*Producoes`
      9. Linha-9aN - Todas as produções, uma por linha: `P->KVC`
    - Exemplos de arquivo:
      ```txt
        *GLC
        *NaoTerminais
        P K V F C
        *Terminais
        c v f ; b e d
        *SimboloInicial
        P
        *Producoes
        P->KVC
        K->cK
        K->&
        V->vV
        V->F
        F->fP;F
        F->&
        C->bVCe
        C->d;C
        C->&
      ```
## Execução
  - Inputs
    - Os arquivos de entrada devem estar contidos no diretório `./data`.
  
  - Outputs
    - Os arquivos de saída irão ser alocados no diretório `./data`.
   
  - Run
    - Para iniciar a aplicação execute um dos comandos abaixo, e siga as instruções que aparecerão.
      ```
      python3 main.py
      ```
      ou
      ```
      python main.py
      ```
