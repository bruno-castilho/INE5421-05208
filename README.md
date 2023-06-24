# INE5421-Linguagens-Formais-e-Compiladores

### Trabalho: Manipulação de Linguagens Regulares e Linguagens Livres de Contexto
1. Objetivo do Trabalho:
O objetivo deste trabalho é a implementação dos algoritmos relacionados à manipulação
de Linguagens Regulares e Livres de Contexto. Tais algoritmos são úteis na implementação de Geradores de Analisadores Léxicos e Sintáticos ou na implementação dos próprios
analisadores, servindo de arcabouço para o desenvolvimento de Compiladores.

2. Definição do Trabalho:\
Implementar algoritmos para manipular Autômatos Finitos, Gramáticas Regulares, Expressões Regulares, Gramáticas Livres de Contexto e Autômatos de Pilha.\
Os seguintes algoritmos devem ser implementados:\
(a) Conversão de AFND (com e sem ε) para AFD (0,5pt)\
(b) Conversão de AFD para GR e de GR para AFND (0,5pt)\
(c) Minimização de AFD (1,0pt)\
(d) União e interseção de AFD (1,0pt)\
(e) Conversão de ER para AFD (usando o algoritmo baseado em árvore sintática - Livro\
Aho - seção 3.9) (1,5pt)\
(f) Reconhecimento de sentenças em AF (0,5pt)\
(g) Reconhecimento de sentenças em AP (via implementação de uma tabela Preditivo\
LL(1)) - Além dos algoritmos relacionados a análise da sentença de entrada, devem\
ser implementados os algoritmos para cálculo dos conjuntos First e Follow, Fatoração e Eliminação de Recursão à esquerda (5pt)


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



