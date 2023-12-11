struct matriz:
    "Matriz 2d simples usando float."
    var linhas: Int
    var colunas: Int
    var total_elementos: Int
    var dados: Pointer[Int]
    
    fn __init__(inout self, valor_padrao: Int, linhas: Int, colunas: Int)->None:
         self.linhas = linhas if linhas > 0 else 1   #caso num de linhas seja menor que 1, ele fica um
         self.colunas = colunas if colunas > 0 else 1  
         self.total_elementos = self.linhas *  self.colunas
         self.dados = Pointer[Int].alloc(self.total_elementos) #aloca memoria para todos os elementos do vetor
         for i in range(self.total_elementos):
             self.dados.store(i, valor_padrao) #guarda os valores padraos na matriz

    #fn __call__ 

    fn __getitem__(borrowed self, linha: Int, coluna: Int)-> Int:
        let posi: Int = (self.colunas * linha) + coluna   #acha a localizacao da memoria do objeto buscado
       
        if posi <= self.total_elementos:
          return self.dados.load(posi)
        else:
            print("tamanho invalido")
            return self.dados.load(0)

    fn __setitem__(inout self, linha: Int, coluna: Int, item: Int )-> Bool:
        let posi: Int = (self.colunas * linha) + coluna   #acha a localizacao da memoria do objeto buscado
       
        if posi <= self.total_elementos:
            self.dados.store(posi,item) #guarda esse elemento na memória
            return True
        else:
            print("tamanho invalido")
            return False

    fn __del__(owned self):
        self.dados.free()

    fn __len__(borrowed self)->Int:
        return  self.total_elementos

    fn __copyinit__(inout self, matriz2:Self )->None: #inicializa uma matrix copiando outra matriz
        self.linhas = matriz2.linhas
        self.colunas = matriz2.colunas
        self.total_elementos = matriz2.total_elementos

        self.dados = Pointer[Int].alloc(self.total_elementos) #aloca memoria para todos os elementos do vetor
        memcpy(self.dados, matriz2.dados, self.total_elementos)

    fn __eq__(borrowed self,  borrowed matriz2: Self)->Bool:
         if self.total_elementos != matriz2.total_elementos:
             return False
         
         for i in range(self.linhas):
             for j in range(self.colunas):
                 let self_valor = self[i,j]
                 let outro_valor = matriz2[i,j]
                 if self_valor != outro_valor:
                    return False
         return True
    fn __ne__ (borrowed self, borrowed matriz2: Self)->Bool:
        return not self == matriz2
    
    # NOTE: in c++ it would be `Matrix operator+ (const Matrix& other) {...}`
    fn __add__ (borrowed self, borrowed matriz2: Self)-> matriz:
          if self.linhas != matriz2.linhas or self.colunas != matriz2.colunas:
            print("erro nao se pode fazer adicao entre matrizes de tamanhos diferentes")
            return matriz(Int(0), self.linhas, self.colunas)
          
          var nova_matriz = matriz(Int(0), self.linhas, self.colunas)
          for i in range(self.linhas):
            for j in range(self.colunas):
                 nova_matriz [i,j] = self[i,j] + matriz2[i,j]
         
         return nova_matriz
    
    fn __sub__ (borrowed self, borrowed matriz2: Self)-> matriz:
          if self.linhas != matriz2.linhas or self.colunas != matriz2.colunas:
            print("erro nao se pode fazer subtracao entre matrizes de tamanhos diferentes")
            return matriz(Int(0), self.linhas, self.colunas)
          
          var nova_matriz = matriz(Int(0), self.linhas, self.colunas)
          for i in range(self.linhas):
            for j in range(self.colunas):
                 nova_matriz [i,j] = self[i,j] - matriz2[i,j]
         
         return nova_matriz

    fn __mul__(borrowed self, borrowed matriz2:Self)->matriz:
        if (self.colunas != matriz2.linhas):
            print("erro: e preciso que a matriz 1 tenha o mesmo numero de colunas que a matriz 2 tem de linhas")
            return matriz(Int(0), self.linhas, self.colunas)
        var nova_matriz = matriz(Int(0), self.linhas, self.colunas)
          
        for i in range (self.linhas):
            for j in range(matriz2.colunas):
                for k in range(self.colunas):
                     nova_matriz[i,j] += self[i,k] * matriz2[k,j]
        
        return nova_matriz

   """Hfn __truediv__ (borrowed self, borrowed matriz2: Self)-> matriz:
          if self.linhas != matriz2.linhas or self.colunas != matriz2.colunas:
            print("erro nao se pode fazer divisao entre matrizes de tamanhos diferentes")
            return matriz(Int(0), self.linhas, self.colunas)
          
          var nova_matriz = matriz(Int(0), self.linhas, self.colunas)
          for i in range(self.linhas):
            for j in range(self.colunas):
                 nova_matriz [i,j] = Int(self[i,j] / matriz2[i,j])
         
         return nova_matriz."""
    
    fn aplicar_funcao[function: fn(Int) -> Int] (borrowed self)->matriz:          
          var nova_matriz = matriz(Int(0), self.linhas, self.colunas)
          for i in range(self.linhas):
            for j in range(self.colunas):
                 nova_matriz [i,j] =  function(self[i,j])
         
         return nova_matriz
    
    fn imprime_matriz(borrowed self)->None:
        print("[")
        for i in range(self.linhas):
            print_no_newline("   [")
            for j in range(self.colunas):
                print_no_newline(self[i,j])
                if j != self.colunas -1:
                    print_no_newline(", ")
            print("], " if  i != self.linhas -1 else "]")
        print("]")


            

        
    
fn main():
    pass