import warnings


class GhuTable:
    def __init__(self, colunas: list, title: str = None, title_style: str = 'center', table_style: str = 'center'):
        self.__colunas = colunas  # Lista com o nome das colunas
        self.__title = title  # Título da tabela, caso tenha.

        self.__tabela = {}
        self.__tam = {}  # Dicionário com a largura das colunas
        self.__estilo = {}  # Dicionário com o estilo de cada coluna

        self.__n_linhas = 0  # número de itens nas colunas

        # ESTILOS
        self.__title_style = title_style if title_style in ('center', 'left', 'right') else 'center'
        self.__estilo_padrao = table_style if table_style in ('center', 'left', 'right') else 'center'

        for coluna in colunas:
            self.__tabela[coluna] = []
            self.__tam[coluna] = len(coluna)
            self.__estilo[coluna] = self.__estilo_padrao

        self.pad = 1  # Distância da linha vertical

        # Verificando se é um título válido
        self.__largura = self.__att_largura()
        if len(self.__title) > self.__largura:
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
                tabela = self.ver
                for j, key in enumerate(self.__tabela):
                    tam = self.__tam[key] + 2 * self.pad
                    tabela += self.__tabela[key][i].center(tam) + self.ver

                tabela += '\n' + div

        return titulo + cabeca + tabela

    def __repr__(self):
        return str(self)

    def __att_largura(self):
        """Método privado para atulizar o valor da largura da tabela"""
        return sum(self.__tam.values()) + len(self.__colunas) * (2 * self.pad + 1) - 1

    def add_linha(self, row: list):
        """Método para adicionar uma nova linha para todas as colunas."""

        if len(row) == len(self.__colunas):

            for i, k in enumerate(self.__tabela):
                item = str(row[i])
                self.__tabela[k].append(item)

                if len(item) > self.__tam[k]:
                    self.__tam[k] = len(item)

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
