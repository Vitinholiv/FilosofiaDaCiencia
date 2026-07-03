from flask import Flask, render_template, jsonify
from render import build_timeline_elements

app = Flask(__name__)

def visualization_data():
    philosophies = {
        "Raízes de Euclides": (1550, 1625, 0, "#00FF44"),

        "Empirismo": (1640, 1734, 220, "#88FF00"),
        "Empirismo Materialista": (1651, 1701, 170, "#AAFF00"),
        "Empirismo Moderado": (1670, 1838, 370, "#CCFF00"),
        "Idealismo Empírico": (1710, 1760, 320, "#EEFF00"),
        "Empirismo Cético": (1739, 1878, 270, "#FFFF00"),
        "Indutivismo Científico": (1843, 1890, 320, "#FFDD00"),
        "Positivismo Clássico": (1842, 1890, 420, "#FFBB00"),
        "Ceticismo Radical": (1750, 1800, 220, "#FFD500"),
        "Positivismo Científico": (1895, 1917, 350, "#FF9900"),
        "Empirio-Criticismo": (1883, 1917, 200, "#FF7700"),
        "Pragmatismo (Peirce)": (1878, 1902, 150, "#FF4400"),
        "Pragmatismo (James)": (1907, 1957, 50, "#FF3300"),
        "Círculo de Viena": (1922, 1950, 250, "#FF2200"),
        "Verificacionismo Estrito (Waismann)": (1929, 1964, 150, "#FF1100"),
        "Verificacionismo Estrito (Ayer)": (1936, 1966, 100, "#FF0000"),
        "Coerentismo": (1931, 1971, 400, "#DD0022"),
        "Fundacionalismo": (1928, 1984, 450, "#BB0044"),
        "Confirmacionismo": (1945, 1969, 350, "#C10E47"),
        "Falsificacionismo": (1934, 1973, 200, "#C1003A"),
        "Naturalismo Epistemológico": (1951, 1975, 300, "#DB081D"),
        "Tradições de Pesquisa": (1977, 2027, 200, "#D7032A"),
        "Programa Forte": (1976, 2026, 50, "#E80A49"),
        "Racionalismo Crítico": (1980, 2020, 350, "#D80229"),
        "Programas de Pesquisa": (1970, 2020, 100, "#C00C4E"),
        "Historicismo": (1968, 2012, 250, "#FF2453"),
        "Anarquismo Epistemológico": (1982, 2025, 300, "#FF0026"),
        "Demarcação Comportamental": (1978, 2028, 150, "#FF2121"),
        "Empirismo Construtivo": (1980, 2030, 400, "#FF0048"),

        "Racionalismo": (1630, 1709, -220, "#00FFDD"),
        "Monismo Panteísta": (1677, 1727, -270, "#00EECC"),
        "Ocasionalismo": (1674, 1724, -320, "#00DDCC"),
        "Monadologia": (1714, 1764, -170, "#00CCBB"),
        "Wolffianismo": (1730, 1776, 0, "#00BBAA"),
        "Criticismo Kantiano": (1781, 1895, -100, "#00AAEE"),
        "Idealismo Alemão": (1805, 1862, -150, "#0088EE"),
        "Dialética Hegeliana": (1812, 1858, -200, "#0066EE"),
        "Materialismo Dialético": (1867, 1986, -300, "#0044EE"),
        "Neo-kantismo": (1870, 1955, -50, "#114EF4"),
        "Fenomenologia": (1900, 1941, -200, "#2525FF"),
        "Hermenêutica Filosófica": (1927, 1952, -250, "#2929FA"),
        "Existencialismo": (1946, 1993, -150, "#540BCA"),
        "Logicismo": (1879, 1958, 0, "#6418FC"),
        "Estruturalismo Epistemológico": (1923, 1973, -100, "#711EF7"),
        "Racionalismo Contemporâneo": (1957, 2007, -200, "#7B0ECF"),
        "Problema de Gettier": (1963, 2013, -50, "#801EDC"),
        "Confiabilismo": (1986, 2036, -100, "#7E1BE1"),
        "Epistemologia de Virtudes": (1991, 2041, -250, "#7A0CB9"),
    }

    bifurcations = [
        ("Raízes de Euclides", "Racionalismo"),
        ("Racionalismo", "Empirismo"),
        ("Empirismo", "Empirismo Materialista"),

        ("Empirismo", "Empirismo Moderado"),
        ("Empirismo", "Idealismo Empírico"),
        ("Empirismo", "Empirismo Cético"),
        ("Empirismo Moderado", "Indutivismo Científico"),
        ("Empirismo Moderado", "Positivismo Clássico"),
        ("Empirismo Cético", "Ceticismo Radical"),
        ("Empirismo Cético", "Empirio-Criticismo"),
        ("Empirismo Cético", "Pragmatismo (Peirce)"),
        ("Indutivismo Científico", "Positivismo Científico"),
        ("Positivismo Clássico", "Positivismo Científico"),
        ("Pragmatismo (Peirce)", "Pragmatismo (James)"),
        ("Empirio-Criticismo", "Círculo de Viena"),
        ("Positivismo Científico", "Círculo de Viena"),
        ("Círculo de Viena", "Fundacionalismo"),
        ("Círculo de Viena", "Coerentismo"),
        ("Círculo de Viena", "Falsificacionismo"),
        ("Coerentismo", "Confirmacionismo"),
        ("Círculo de Viena", "Verificacionismo Estrito (Waismann)"),
        ("Verificacionismo Estrito (Waismann)", "Verificacionismo Estrito (Ayer)"),
        ("Confirmacionismo", "Naturalismo Epistemológico"),
        ("Falsificacionismo", "Programas de Pesquisa"),
        ("Falsificacionismo", "Historicismo"),
        ("Historicismo", "Anarquismo Epistemológico"),
        ("Historicismo", "Tradições de Pesquisa"),
        ("Historicismo", "Racionalismo Crítico"),
        ("Tradições de Pesquisa", "Demarcação Comportamental"),
        ("Racionalismo", "Monismo Panteísta"),
        ("Racionalismo", "Ocasionalismo"),
        ("Racionalismo", "Monadologia"),
        ("Monadologia", "Wolffianismo"),
        ("Wolffianismo", "Criticismo Kantiano"),
        ("Criticismo Kantiano", "Idealismo Alemão"),
        ("Criticismo Kantiano", "Neo-kantismo"),
        ("Criticismo Kantiano", "Fenomenologia"),
        ("Idealismo Alemão", "Dialética Hegeliana"),
        ("Idealismo Alemão", "Materialismo Dialético"),
        ("Neo-kantismo", "Logicismo"),
        ("Neo-kantismo", "Estruturalismo Epistemológico"),
        ("Fenomenologia", "Hermenêutica Filosófica"),
        ("Fenomenologia", "Existencialismo"),
        ("Logicismo", "Problema de Gettier"),
        ("Naturalismo Epistemológico", "Empirismo Construtivo"),
        ("Programas de Pesquisa", "Programa Forte"),
        ("Problema de Gettier", "Confiabilismo"),
        ("Materialismo Dialético", "Epistemologia de Virtudes"),
        ("Hermenêutica Filosófica", "Racionalismo Contemporâneo")
    ]

    epochs = [
        (-600, "Período Pré-Socrático"),
        (-400, "Grécia Clássica"),
        (1,    "Início da Era Comum"),
        (500,  "Alta Idade Média"),
        (1200, "Baixa Idade Média"),
        (1500, "Idade Moderna"),
        (1800, "Idade Contemporânea"),
        (2000, "Globalização")
    ]
    '''("Francis Bacon", "Bacon", -240, 0, "static/img/bacon.png", 'Barriga de porco defumada'),
        ("Francis Calabresa", "Calabresa", -297, 0, "static/img/calabresa.png", 'Embutido feito com carne carne carne carne carne carne carne carne carne carne carne carne carne carne carne carne carne carne carne carne carne carne carne carne '),
        ("Francis Pepino", "Salada", -180, 0, "static/img/pepino.png", 'Vegetal'),
        ("Francis Alface", "Salada", -590, 0, "static/img/alface.png", 'Outro vegetal'),
        ("Francis Alcatra", "Carne", 450, 0, "static/img/alcatra.png", 'Bovinae'),
        ("Francis Variedades", "Carne", 800, 0, "static/img/variedades.png", 'Cortes de vários animais')'''
    
    philosophers = [
        ("Francis Bacon", "Programa Forte", 1900, 0, "static/img/bacon.png", 'Barriga de porco defumada'),
    ]

    works = {
        
    }
    '''"Francis Bacon": [
            ('Rubrica',    'Ano 1 - Falava sobre a Rubrica'),
            ('Kopesh',     'Ano 2 - Falava sobre um machado'),
            ('Fogueteiro', 'Ano 3 - Falava sobre um foguete')
        ],
        "Francis Calabresa": [
            ('Defumados', 'Ano 1 - Tratado sobre defumação')
        ],
        "Francis Pepino": [
            ('Verde Vivo', 'Ano 1 - Manifesto vegetal')
        ],
        "Francis Alcatra": [
            ('Cortes Nobres', 'Ano 1 - Guia de cortes bovinos')
        ],
        "Francis Variedades": [
            ('Pluralidade', 'Ano 1 - Sobre a diversidade animal')
        ]'''

    influences = {
        
    }
    '''"Francis Bacon": [
            ("Pepino", "Pepino é bom demais!", "Concorda"),
            ("Alface", "Alface é ruim demais!", "Discorda")
        ],
        "Francis Calabresa": [
            ("Carne", "Compartilhamos a origem animal.", "Concorda"),
            ("Salada", "Vegetais não têm sabor.", "Discorda")
        ],
        "Francis Pepino": [
            ("Alface", "Partilhamos a leveza.", "Concorda"),
            ("Calabresa", "Embutidos são nocivos.", "Discorda")
        ],
        "Francis Alface": [
            ("Pepino", "Somos ambos refrescantes.", "Concorda"),
            ("Bacon", "Gordura em excesso é ruim.", "Discorda")
        ],
        "Francis Alcatra": [
            ("Carne", "Mesma família, mesmo propósito.", "Concorda"),
            ("Pepino", "Vegetais são insuficientes.", "Discorda")
        ],
        "Francis Variedades": [
            ("Calabresa", "Diversidade é riqueza.", "Concorda")
        ]'''

    adepts = {
        
    }
    '''"Francis Bacon": [
            ("Variedades", "Variedades é o futuro!")
        ],
        "Francis Calabresa": [
            ("Carne", "Carne é nossa origem!")
        ],
        "Francis Pepino": [
            ("Alface", "Juntos somos mais verdes!")
        ],
        "Francis Alface": [
            ("Pepino", "Unidos pelo verde!")
        ],
        "Francis Alcatra": [
            ("Calabresa", "Ambos somos proteína!")
        ],
        "Francis Variedades": [
            ("Bacon", "Bacon abraça a variedade!")
        ]'''

    oppositions = {
        
    }
    '''"Francis Bacon": [
            ("Calabresa", "Calabresa tem muito sal!"),
            ("Salada", "Salada é muito ruim!")
        ],
        "Francis Calabresa": [
            ("Bacon", "Bacon é gorduroso demais!")
        ],
        "Francis Pepino": [
            ("Bacon", "Carne é desnecessária!")
        ],
        "Francis Alface": [
            ("Calabresa", "Processados são o mal!")
        ],
        "Francis Alcatra": [
            ("Salada", "Salada não sustenta!")
        ]'''

    events = [
        
    ]
    #(-400, 0, "static/img/bacon.png", "CEO Do Bacon", "O CEO do Bacon Nasceu e Dominou o Mundo Inteiro", "#cc0066")

    return {
        "philosophies": philosophies,
        "bifurcations": bifurcations,
        "epochs": epochs,
        "philosophers": philosophers,
        "works": works,
        "influences": influences,
        "adepts": adepts,
        "oppositions": oppositions,
        "events": events
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/timeline')
def timeline_api():
    data = visualization_data()
    resultado = build_timeline_elements(data)
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)