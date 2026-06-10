# Visualização de Filosofia da Ciência

Esse projeto tem como objetivo construir uma rede de visualização das principais mentes que circundam o ramo da epistemologia, considerando relações entre elas, suas obras e períodos de tempo em que tiveram mais importância.

## Instalação

...

## Uso

...

## Alteração da Timeline

A modelagem por trás de toda a estrutura visual é um conjunto de grafos. 

- Há um grafo que representa a linha do tempo das correntes filosóficas, onde cada corrente é um vértice, e arestas são ligações entre elas.
- Diversos outros vértices definem filósofos e pensadores importantes abordados, definidos separadamente.
- Também há vértices diferentes que representam marcos históricos e eventos importantes para a ciência.
- Além disso, também definimos outras coisas, como marcações temporais importantes, declarando períodos históricos ou épocas.

Para definir uma instância da timeline, precisamos definir cada um desses componentes no `app.py`.

- **Correntes Filosóficas** - philosophies (`dict - string:tuple`)
    - Corrente (`string`) $\rightarrow$ [ Ano de Início (`int`), Ano Final (`int`), Offset (`int`), Cor (`hex string`) ]

- **Bifurcações** - bifurcations (`list - tuple`)
    - [ Corrente de Origem (`string`), Corrente Derivada (`string`) ]

- **Épocas** - epochs (`list - tuple`)
    - [ ano (`int`), nome da época (`string`) ]

- **Filósofos** - philosophers (`list - tuple`)
    - [ nome (`string`), ano (`int`), offset (`int`), imagem (`src string`), resumo (`string`) ]

- **Obras** - works (`dict - string:(list - tuple)`)
    - Filósofo (`string`) $\rightarrow$ Obras (`list`)
        - (nome da obra 1 (`string`), descrição da obra 1 (`string`) )
        - (nome da obra 2 (`string`), descrição da obra 2 (`string`) )
        - ...

- **Influências** - influences (`dict - string:(list - tuple)`)
    - Filósofo (`string`) $\rightarrow$ Influências (`list`)
        - (nome da influência (`string`), descrição/motivo (`string`), status (`string`, "Concorda" ou "Discorda"))

- **Adeptos** - adepts (`dict - string:(list - tuple)`)
    - Filósofo (`string`) $\rightarrow$ Adeptos (`list`)
        - (nome do adepto (`string`), descrição/motivo (`string`))

- **Oposições** - oppositions (`dict - string:(list - tuple)`)
    - Filósofo (`string`) $\rightarrow$ Opositores (`list`)
        - (nome do opositor (`string`), descrição/motivo (`string`))

- **Eventos Importantes** - events (`list - tuple`)
    - [ ano (`int`), offset (`int`), imagem (`src string`), nome (`string`), descrição (`string`), cor (`hex string`) ]