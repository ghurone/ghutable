import warnings


class GhuTable:
    def __init__(self, colunas: list, title: str = None, title_style: str = 'center', table_style: str = 'center'):
        self.__colunas = colunas  # Lista com o nome das colunas
        self.__title = title  # Título da tabela, caso tenha.

        self.__tabela = {}
        self.__tam = {}  # Dicionário com a largura das colunas
        self.__estilo = {}  # Dicionário com o estilo de cada coluna

        self.__rows = []
        self.__n_linhas = 0  # número de itens nas colunas

        for coluna in colunas:
            self.__tabela[coluna] = []
            self.__tam[coluna] = len(coluna)
            self.__estilo[coluna] = 'center'

        self.pad = 1  # Distância da linha vertical

        # Verificando se é um título válido
        self.__largura = self.__att_largura()
        if self.__title and len(self.__title) > self.__largura:
            warnings.warn('Título grande demais', Warning)
            self.__title = None

        # Layout inicial da tabela
        self.can = '+'
        self.ver = '|'
        self.hor = '-'

    def __str__(self):
        # Criando a string do título
        titulo = ''
        if self.__title:
            self.__largura = self.__att_largura()
            titulo = self.can + self.hor * self.__largura + self.can + '\n'
            titulo += self.ver + self.__title.center(self.__largura) + self.ver + '\n'

        # Criando a string do cabeçalho das colunas
        cabeca = self.ver
        div = self.can
        for coluna in self.__colunas:
            tam = self.__tam[coluna] + 2 * self.pad
            div += self.hor * tam + self.can
            cabeca += coluna.center(tam) + self.ver

        div += '\n'
        cabeca += '\n'
        cabeca = div + cabeca + div

        # Criando a string dos elementos de cada coluna
        tabela = ''
        if self.__n_linhas != 0:
            for i in range(self.__n_linhas):
                tabela += self.ver
                for j, key in enumerate(self.__tabela):
                    tam = self.__tam[key] + 2 * self.pad
                    tabela += self.__tabela[key][i].center(tam) + self.ver

                tabela += '\n' + div

        return titulo + cabeca + tabela

    def __repr__(self):
        return str(self)
    
    def __diff(self, coluna):
        for col1 in self.__colunas:
            if col1 in coluna:
                return False

        return True

    def __add__(self, other):
        if isinstance(other, GhuTable):
            if self.__n_linhas == other.__n_linhas and self.__diff(other.__colunas):
                new = GhuTable(self.__colunas + other.__colunas)

                for i in range(self.__n_linhas):
                    new.add_linha(self.__rows[i] + other.__rows[i])

                return new

    def __att_largura(self):
        """Método privado para atulizar o valor da largura da tabela"""
        return sum(self.__tam.values()) + len(self.__colunas) * (2 * self.pad + 1) - 1

    def copia(self):
        new = GhuTable(self.__colunas.copy(), self.__title)
        
        for row in self.__rows:
            new.add_linha(row)

        new.pad = self.pad
        new.ver = self.ver
        new.can = self.can
        new.hor = self.hor

        return new

    def add_linha(self, row: list):
        """Método para adicionar uma nova linha para todas as colunas."""

        if len(row) == len(self.__colunas):

            for i, k in enumerate(self.__tabela):
                item = str(row[i])
                self.__tabela[k].append(item)

                if len(item) > self.__tam[k]:
                    self.__tam[k] = len(item)

            self.__rows.append(row)
            self.__n_linhas += 1

    def mudar_titulo(self, titulo_novo: str) -> None:
        """Método para alterar o título atual."""

        if isinstance(titulo_novo, str):
            self.__att_largura()

            if len(titulo_novo) <= self.__largura:
                self.__title = titulo_novo
            else:
                warnings.warn('Título grande demais. Nada foi alterado.', Warning)
        else:
            raise TypeError('O título precisa ser do tipo `str`.')

    def ordenar_por(self, coluna: str, revert: bool = False) -> object:
        """Ordena a tabela em relação a um coluna (bubblesort)"""

        new_table = self.copia()
        table = new_table.__tabela

        list_ord = table[coluna]
        
        n = len(list_ord)
        for i in range(n-1):
            for j in range(n-1, i, -1):

                if (list_ord[j] < list_ord[j-1] and not revert) or (revert and list_ord[j] > list_ord[j-1]):

                    for v, k in enumerate(table):
                        col = table[k]
                        col[j], col[j-1] = col[j-1], col[j]

        return new_table
        

if __name__ == '__main__':
    # ZONA DE TESTES
    a = GhuTable(['Nome'])
    a.add_linha(['Erick'])

    b = GhuTable(['Idade'])
    b.add_linha([22])
    
    print('Tabela A:')
    print(a)

    print('Tabela B:')
    print(b)

    print('Tabela A + B:')
    print(a+b)