
class ER:
    """
    Uma classe para representar uma expressão regular.
    
    ...

    Atributos
    ---------
    er : str
         expressão regular em forma de string.

    Métodos
    -------
    replaceSymbols() -> Str:
        Troca operações ? e + para seus equivalentes
            a? = (a | &)
            a+ = a.a*
            
    reverseParenthesis(index: list) -> Str or None: 
        Retorna uma sentença.
        
    putConcatenation(er: str) -> Str:
        Retorna er com '.' entre os símbolos.
    
    getErAdapted() -> Str:
        Retorna er com símbolos alterados, '.'  e '#' no final.
        
    print() -> None:
        Imprime a er original.
    """
    
    def __init__(self, er: str):
        self.er = er
        
    def replaceSymbols(self):
        string = ''
        for i in range(len(self.er)):
            symbol = self.er[i]
            if symbol in ['+', '?']:
                esp = self.reverseParenthesis([i - 1])
                if symbol == '+':
                    string = string[:-len(esp)] + esp + esp + '*'
                else:
                    string = string[:-len(esp)] + "(" + esp + '|' + '&' ')'
            else:
                string += symbol
                
        return string

    def reverseParenthesis (self, index: list):
        if self.er[index[0]] != ')':
            return self.er[index[0]]

        string = self.er[index[0]]
        while index[0] > 0:
            index[0] -= 1
            if self.er[index[0]] == ')':
                string = self.parenteseReverse(index) + string
            else:
                string = self.er[index[0]] + string
                if self.er[index[0]] == '(':
                    return string

    def putConcatenation(self, er: str):
        string = ''
        for i in range(len(er) - 1):
            symbol = er[i]
            string += symbol
            if symbol not in ['|', '.', '(']:
                if er[i + 1] not in ['|', '*', '.', ')']:
                    string += '.'

        string += er[-1]

        return string

    def getErAdapted(self):
        er = self.replaceSymbols()
        er = self.putConcatenation(er)
        er += '.#'
        return er

    def print(self):
         print(self.er)