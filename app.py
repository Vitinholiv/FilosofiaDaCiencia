from flask import Flask, render_template, jsonify
from render import build_timeline_elements

app = Flask(__name__)

def visualization_data():
    philosophies = {
        "Raízes de Euclides": (1580, 1605, 0, "#00FF44"),

        "Empirismo": (1620, 1734, 220, "#88FF00"),
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
        "Fundacionalismo": (1928, 2026, 450, "#BB0044"),
        "Confirmacionismo": (1945, 1969, 350, "#C10E47"),
        "Falsificacionismo": (1934, 1973, 200, "#C1003A"),
        "Naturalismo Epistemológico": (1951, 1975, 300, "#DB081D"),
        "Tradições de Pesquisa": (1977, 2026, 200, "#D7032A"),
        "Programa Forte": (1976, 2026, 50, "#E80A49"),
        "Racionalismo Crítico": (1980, 2026, 350, "#D80229"),
        "Programas de Pesquisa": (1970, 2026, 100, "#C00C4E"),
        "Historicismo": (1968, 2026, 250, "#FF2453"),
        "Anarquismo Epistemológico": (1982, 2026, 300, "#FF0026"),
        "Demarcação Comportamental": (1978, 2026, 150, "#FF2121"),
        "Empirismo Construtivo": (1980, 2026, 400, "#FF0048"),

        "Racionalismo": (1610, 1709, -220, "#00FFDD"),
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
        "Existencialismo": (1946, 2026, -150, "#540BCA"),
        "Logicismo": (1879, 1958, 0, "#6418FC"),
        "Estruturalismo Epistemológico": (1923, 1973, -100, "#711EF7"),
        "Racionalismo Contemporâneo": (1957, 2026, -200, "#7B0ECF"),
        "Problema de Gettier": (1963, 2026, -50, "#801EDC"),
        "Confiabilismo": (1986, 2026, -100, "#7E1BE1"),
        "Epistemologia de Virtudes": (1991, 2026, -250, "#7A0CB9"),

        "Futuro": (2031, 2046, 25, "#AA0AB9")
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
        ("Hermenêutica Filosófica", "Racionalismo Contemporâneo"),
        ("Epistemologia de Virtudes","Futuro"),
        ("Racionalismo Contemporâneo","Futuro"),
        ("Existencialismo","Futuro"),
        ("Confiabilismo","Futuro"),
        ("Problema de Gettier","Futuro"),
        ("Programa Forte","Futuro"),
        ("Programas de Pesquisa","Futuro"),
        ("Demarcação Comportamental","Futuro"),
        ("Tradições de Pesquisa","Futuro"),
        ("Historicismo","Futuro"),
        ("Anarquismo Epistemológico","Futuro"),
        ("Racionalismo Crítico","Futuro"),
        ("Empirismo Construtivo","Futuro"),
        ("Fundacionalismo","Futuro"),
    ]

    epochs = [
        (1600, "1600"), (1620, "1620"), (1640, "1640"), (1660, "1660"), (1680, "1680"),
        (1700, "1700"), (1720, "1720"), (1740, "1740"), (1760, "1760"), (1780, "1780"),
        (1800, "1800"), (1820, "1820"), (1840, "1840"), (1860, "1860"), (1880, "1880"),
        (1900, "1900"), (1920, "1920"), (1940, "1940"), (1960, "1960"), (1980, "1980"),
        (2000, "2000"), (2026, "2026")
    ]
    '''("Francis Bacon", "Bacon", -240, 0, "static/img/bacon.jpg", 'Barriga de porco defumada'),
        ("Francis Calabresa", "Calabresa", -297, 0, "static/img/calabresa.jpg", 'Embutido feito com carne carne carne carne carne carne carne carne carne carne carne carne carne carne carne carne carne carne carne carne carne carne carne carne '),
        ("Francis Pepino", "Salada", -180, 0, "static/img/pepino.jpg", 'Vegetal'),
        ("Francis Alface", "Salada", -590, 0, "static/img/alface.jpg", 'Outro vegetal'),
        ("Francis Alcatra", "Carne", 450, 0, "static/img/alcatra.jpg", 'Bovinae'),
        ("Francis Variedades", "Carne", 800, 0, "static/img/variedades.jpg", 'Cortes de vários animais')'''
    
    philosophers = [
        ("Francis Bacon", "Empirismo", 1620, 0, "static/img/Francis_bacon.jpg", [
            ("Informações pessoais", "Político, filósofo empirista, cientista e ensaísta inglês."),
            ("Vida e fatos", "Considerado um dos fundadores da Revolução Científica."),
            ("Teorias/Ideias", [
                "O conhecimento verdadeiro só nasce da experiência sensível organizada de forma metódica.",
                "Método Indutivo: consiste nas fases de observação rigorosa, organização racional, formulação de hipóteses e comprovação.",
                "O seu livro Novum Organum funda o programa empirista.",
                "\"Saber é poder.\"",
            ]),
        ]),
        
        ("Thomas Hobbes", "Empirismo Materialista", 1653, 0, "static/img/Thomas_Hobbes.jpg", [
            ("Informações pessoais", "Filósofo inglês, um dos principais pensadores da filosofia política moderna."),
            ("Vida e fatos", "Popularizou a frase “O homem é o lobo do homem”. Contemporâneo de Bacon."),
            ("Teorias/Ideias", [
                "Empirismo materialista: reduz toda atividade mental a movimento de matéria.",
                "Teoria causal da percepção: sensações são movimentos internos causados por pressão externa nos órgãos dos sentidos.",
                "Empirismo: todo o conhecimento humano começa nos sentidos.",
            ]),
        ]),
    ]

    works = {
        'Francis Bacon': [('Novum Organum', '1920')]
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

    LOREM_IPSUM = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since 1966, when designers at Letraset and James Mosley, the librarian at St Bride Printing Library in London, took a 1914 Cicero translation and scrambled it to make dummy text for Letraset's Body Type sheets. It has survived not only many decades, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised thanks to these sheets and more recently with desktop publishing software like Aldus PageMaker and Microsoft Word including versions of Lorem Ipsum."

    influences = {
        'Francis Bacon': [('Aristóteles', '-', 'Discorda'), ('Gustas', LOREM_IPSUM, 'Dircorda'), ('Erique', '-', 'Concorda')],
        'Thomas Hobbes': [('Aristóteles', '-', 'Discorda'), ('Gustas', LOREM_IPSUM, 'Dircorda'), ('Erique', '-', 'Concorda')]
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
        'Francis Bacon': [('Thomas Hobbes', '-'), ('John Locke', '-')]
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
        'Francis Bacon': [('René Descartes', '-')]
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
        (1600, -34, "static/img/events/18.jpeg", "Execução de Giordano Bruno", "A execução de Giordano Bruno em 1600 expôs o conflito crescente entre a nova ciência e a autoridade religiosa.", "#88FF00"),
        (1605, 0, "static/img/events/19.jpg", "Leis Planetárias de Kepler", "As leis planetárias formuladas por Kepler em 1609 consolidaram a astronomia matemática, influenciando Descartes e mais tarde Kant.", "#00FFDD"),
        (1609, 34, "static/img/events/20.webp", "Galileu aperfeiçoa o telescópio", "Galileu aperfeiçoou o telescópio em 1609, provocando uma revolução na observação científica que impactaria Bacon, Descartes, Popper e Kuhn.", "#88FF00"),
        (1610, -34, "static/img/events/21.jpeg", "Sidereus Nuncius", "Em 1610, Galileu publicou Sidereus Nuncius, apresentando evidências observacionais decisivas em favor do modelo heliocêntrico do universo.", "#88FF00"),
        (1618, 0, "static/img/events/22.jpeg", "Guerra dos Trinta Anos", "A Guerra dos Trinta Anos, de 1618 a 1648, formou o contexto político turbulento da filosofia moderna de Hobbes.", "#AAFF00"),
        (1620, 34, "static/img/events/23.jpg", "Bacon publica Novum Organum", "Francis Bacon publicou Novum Organum em 1620, fundando o empirismo moderno que influenciaria Hobbes, Locke, Berkeley, Hume, Mill e Comte.", "#88FF00"),
        (1632, 34, "static/img/events/24.jpg", "Galileu publica o Diálogo", "Galileu publicou o Diálogo Sobre os Dois Máximos Sistemas do Mundo em 1632, defendendo publicamente o heliocentrismo.", "#88FF00"),
        (1633, 0, "static/img/events/25.jpg", "Julgamento de Galileu", "O julgamento de Galileu em 1633 tornou-se um marco histórico do conflito entre a ciência e a autoridade religiosa.", "#88FF00"),
        (1637, 34, "static/img/events/26.jpg", "Descartes publica Discurso do Método", "Descartes publicou o Discurso do Método em 1637, fundando o racionalismo moderno que influenciaria Spinoza, Leibniz e Kant.", "#00FFDD"),
        (1642, -34, "static/img/events/27.jpg", "Guerra Civil Inglesa", "A Guerra Civil Inglesa, entre 1642 e 1651, influenciou profundamente o pensamento político de Hobbes e Locke.", "#AAFF00"),
        (1642, -34, "static/img/events/28.jpg", "Morte de Galileu e nascimento de Newton", "A coincidência entre a morte de Galileu e o nascimento de Newton em 1642 simboliza a transição da Revolução Científica.", "#CCFF00"),
        (1660, 0, "static/img/events/29.jpg", "Fundação da Royal Society", "A fundação da Royal Society em 1660 institucionalizou a ciência experimental, influenciando diretamente Bacon, Locke e Hume.", "#88FF00"),
        (1665, 34, "static/img/events/30.jpg", "Hooke publica Micrographia", "Robert Hooke publicou Micrographia em 1665, popularizando a microscopia e reforçando o método observacional defendido por Bacon.", "#88FF00"),
        (1665, -34, "static/img/events/31.jpeg", "Fundação do Philosophical Transactions", "A fundação do Philosophical Transactions em 1665 criou o primeiro periódico científico, moldando toda a filosofia moderna.", "#00FF44"),
        (1687, 0, "static/img/events/32.png", "Newton publica Principia", "Isaac Newton publicou os Principia em 1687, consolidando a mecânica clássica e influenciando Locke, Berkeley, Hume e Kant.", "#CCFF00"),
        (1688, 34, "static/img/events/33.webp", "Revolução Gloriosa", "A Revolução Gloriosa de 1688 estabeleceu o contexto político do liberalismo inglês que moldaria as ideias de Locke.", "#CCFF00"),
        (1690, -34, "static/img/events/34.jpg", "Locke publica Ensaio sobre o Entendimento Humano", "John Locke publicou o Ensaio sobre o Entendimento Humano em 1690, consolidando o empirismo clássico que inspiraria Berkeley e Hume.", "#CCFF00"),
        (1704, 0, "static/img/events/35.jpeg", "Newton publica Opticks", "Newton publicou Opticks em 1704, fortalecendo o método experimental e influenciando diretamente as reflexões de Hume e Kant.", "#FFFF00"),
        (1715, -34, "static/img/events/36.webp", "Iluminismo", "O Iluminismo, entre 1715 e 1789, consolidou a razão e a ciência como fundamentos sociais, moldando Locke, Hume e Kant.", "#CCFF00"),
        (1739, 0, "static/img/events/37.jpg", "Hume publica Tratado da Natureza Humana", "David Hume publicou o Tratado da Natureza Humana em 1739, formulando o problema da indução que despertaria Kant do sono dogmático.", "#FFFF00"),
        (1751, 0, "static/img/events/38.jpeg", "Início da Enciclopédia", "O início da publicação da Enciclopédia em 1751 popularizou o conhecimento científico entre os pensadores iluministas europeus.", "#00AAEE"),
        (1776, 34, "static/img/events/39.jpg", "Independência dos EUA", "A Independência dos Estados Unidos em 1776 representou a aplicação prática dos ideais políticos iluministas defendidos por Locke.", "#CCFF00"),
        (1781, -34, "static/img/events/40.jpg", "Kant publica Crítica da Razão Pura", "Immanuel Kant publicou a Crítica da Razão Pura em 1781, sintetizando racionalismo e empirismo e inspirando os Idealistas Alemães.", "#00AAEE"),
        (1789, 34, "static/img/events/41.jpg", "Revolução Francesa", "A Revolução Francesa de 1789 consolidou politicamente o racionalismo iluminista, influenciando Comte e o desenvolvimento posterior do idealismo hegeliano.", "#FFBB00"),
        (1807, 34, "static/img/events/42.jpg", "Hegel publica Fenomenologia do Espírito", "Hegel publicou a Fenomenologia do Espírito em 1807, marco fundador do idealismo alemão que influenciaria Heidegger e Gadamer.", "#0066EE"),
        (1830, -34, "static/img/events/43.webp", "Comte publica Curso de Filosofia Positiva", "Auguste Comte publicou o Curso de Filosofia Positiva entre 1830 e 1842, fundando o positivismo que inspiraria Mach, Schlick e Carnap.", "#FFBB00"),
        (1831, 34, "static/img/events/44.webp", "Faraday descobre a indução eletromagnética", "Michael Faraday descobriu a indução eletromagnética em 1831, consolidando a física experimental valorizada mais tarde por Mach.", "#FF7700"),
        (1859, 0, "static/img/events/45.webp", "Darwin publica A Origem das Espécies", "Charles Darwin publicou A Origem das Espécies em 1859, revolucionando a biologia e influenciando Mill, Comte, Mach e Popper.", "#FFDD00"),
        (1865, 0, "static/img/events/46.jpeg", "Maxwell formula o eletromagnetismo", "James Clerk Maxwell formulou as equações do eletromagnetismo em 1865, unificando a física clássica e influenciando Mach e Popper.", "#FF7700"),
        (1870, -34, "static/img/events/47.jpeg", "Segunda Revolução Industrial", "A Segunda Revolução Industrial, entre 1870 e 1914, tornou a ciência base do desenvolvimento tecnológico valorizado por Comte e Mach.", "#FFBB00"),
        (1879, 34, "static/img/events/48.png", "Frege publica Begriffsschrift", "Gottlob Frege publicou o Begriffsschrift em 1879, fundando a lógica moderna que influenciaria Russell, Carnap e Quine.", "#6418FC"),
        (1887, 0, "static/img/events/49.png", "Experimento de Michelson-Morley", "O experimento de Michelson-Morley em 1887 questionou a existência do éter luminífero, abrindo caminho para Einstein e Popper.", "#FF7700"),
        (1895, 0, "static/img/events/50.jpg", "Descoberta dos raios X", "A descoberta dos raios X em 1895 provocou uma revolução experimental que reforçou o positivismo científico de Mach.", "#FF7700"),
        (1896, 34, "static/img/events/51.jpeg", "Descoberta da radioatividade", "A descoberta da radioatividade em 1896 marcou o início da física nuclear, ampliando o debate positivista de Mach.", "#FF7700"),
        (1897, -34, "static/img/events/52.jpg", "Descoberta do elétron", "A descoberta do elétron em 1897 iniciou a física subatômica, um avanço central para as reflexões científicas de Mach.", "#FF7700"),
        (1900, -34, "static/img/events/53.jpeg", "Planck propõe a teoria quântica", "Max Planck propôs a teoria quântica em 1900, iniciando a mecânica quântica que influenciaria Schlick, Carnap, Popper e Kuhn.", "#FF2200"),
        (1905, 0, "static/img/events/54.jpg", "Einstein publica a Relatividade Especial", "Albert Einstein publicou a Teoria da Relatividade Especial em 1905, provocando uma revolução conceitual estudada por Schlick e Carnap.", "#FF2200"),
        (1911, 34, "static/img/events/55.webp", "Modelo de Rutherford", "Ernest Rutherford propôs seu modelo atômico em 1911, oferecendo uma nova estrutura da matéria discutida pelo Círculo de Viena.", "#FF2200"),
        (1914, 0, "static/img/events/56.jpeg", "Primeira Guerra Mundial", "A Primeira Guerra Mundial, entre 1914 e 1918, gerou uma crise de confiança no progresso científico sentida por Wittgenstein e Schlick.", "#FF2200"),
        (1915, -34, "static/img/events/57.jpg", "Relatividade Geral", "Einstein publicou a Teoria da Relatividade Geral em 1915, propondo uma nova teoria da gravitação discutida por Schlick e Popper.", "#FF2200"),
        (1917, 34, "static/img/events/58.jpg", "Revolução Russa", "A Revolução Russa de 1917 influenciou intensamente os debates de Neurath sobre a relação entre ciência e sociedade.", "#FF2200"),
        (1925, -34, "static/img/events/59.jpg", "Formulação da Mecânica Quântica", "A formulação da mecânica quântica entre 1925 e 1927 colocou em crise o determinismo clássico, tema caro a Popper e Kuhn.", "#C1003A"),
        (1927, 34, "static/img/events/60.jpeg", "Quinta Conferência Solvay", "A Quinta Conferência Solvay de 1927 marcou o célebre debate entre Bohr e Einstein, tema recorrente em Popper e Kuhn.", "#C1003A"),
        (1927, 0, "static/img/events/61.jpg", "Heidegger publica Ser e Tempo", "Martin Heidegger publicou Ser e Tempo em 1927, marco fundador da fenomenologia existencial que influenciaria diretamente Gadamer.", "#2525FF"),
        (1927, 34, "static/img/events/62.jpg", "Manifesto do Círculo de Viena", "O Manifesto do Círculo de Viena, publicado em 1929, consolidou o positivismo lógico reunindo Schlick, Carnap, Neurath, Waismann e Ayer.", "#FF2200"),
        (1929, -34, "static/img/events/63.jpg", "Grande Depressão", "A Grande Depressão de 1929 intensificou os debates de Neurath sobre racionalidade econômica e planejamento científico da sociedade.", "#FF2200"),
        (1931, 0, "static/img/events/64.webp", "Teoremas da Incompletude de Gödel", "Kurt Gödel publicou seus Teoremas da Incompletude em 1931, revelando limites da lógica formal que impactaram Carnap, Quine e Popper.", "#FF2200"),
        (1933, 34, "static/img/events/65.jpeg", "Ascensão de Hitler ao poder", "A ascensão de Hitler ao poder em 1933 forçou o exílio do Círculo de Viena, transformando profundamente a filosofia da ciência.", "#FF2200"),
        (1934, -34, "static/img/events/66.jpg", "Popper publica A Lógica da Pesquisa Científica", "Karl Popper publicou A Lógica da Pesquisa Científica em 1934, fundando o falsificacionismo que influenciaria Lakatos, Watkins e Kuhn.", "#C1003A"),
        (1938, 0, "static/img/events/67.jpg", "Descoberta da fissão nuclear", "A descoberta da fissão nuclear em 1938 deu início à era nuclear, tema que Popper discutiria em termos de responsabilidade científica.", "#C1003A"),
        (1939, 34, "static/img/events/68.webp", "Segunda Guerra Mundial", "A Segunda Guerra Mundial, entre 1939 e 1945, tornou a ciência fortemente financiada pelos Estados, tema discutido por Popper e Kuhn.", "#C1003A"),
        (1945, 0, "static/img/events/69.jpeg", "Bombas atômicas", "O lançamento das bombas atômicas em 1945 tornou a ética e a responsabilidade científica temas centrais para Popper e Kuhn.", "#C1003A"),
        (1947, -34, "static/img/events/70.jpg", "Guerra Fria", "A Guerra Fria, entre 1947 e 1991, provocou uma grande expansão da pesquisa científica estudada por Kuhn, Lakatos e Laudan.", "#FF2453"),
        (1953, 34, "static/img/events/71.jpg", "Descoberta da estrutura do DNA", "A descoberta da estrutura do DNA em 1953 fundou a biologia molecular, um avanço científico analisado por Karl Popper.", "#C1003A"),
        (1957, -34, "static/img/events/72.jpeg", "Sputnik", "O lançamento do Sputnik em 1957 deu início à corrida espacial, um evento que marcaria as reflexões históricas de Kuhn.", "#FF2453"),
        (1962, 34, "static/img/events/73.jpeg", "Kuhn publica A Estrutura das Revoluções Científicas", "Thomas Kuhn publicou A Estrutura das Revoluções Científicas em 1962, introduzindo paradigmas que influenciariam Lakatos, Feyerabend e Laudan.", "#FF2453"),
        (1963, 0, "static/img/events/74.png", "Artigo de Gettier", "O artigo de Edmund Gettier, publicado em 1963, provocou uma crise na definição clássica de conhecimento, influenciando Goldman e Sosa.", "#7E1BE1"),
        (1969, -34, "static/img/events/75.jpeg", "Chegada do homem à Lua", "A chegada do homem à Lua em 1969 tornou-se símbolo do sucesso científico do século vinte, tema comentado por Kuhn.", "#FF2453"),
        (1970, 0, "static/img/events/76.jpg", "Lakatos publica os Programas de Pesquisa", "Imre Lakatos publicou sua metodologia dos Programas de Pesquisa em 1970, sintetizando as ideias de Popper e Kuhn.", "#C00C4E"),
        (1977, 34, "static/img/events/77.jpg", "Laudan publica Progress and Its Problems", "Larry Laudan publicou Progress and Its Problems em 1977, propondo a ciência como um processo de resolução de problemas.", "#D7032A"),
        (1980, -34, "static/img/events/78.jpg", "Van Fraassen publica The Scientific Image", "Bas van Fraassen publicou The Scientific Image em 1980, consolidando o empirismo construtivo em diálogo com Quine e Kuhn.", "#FF0048"),
        (1986, 0, "static/img/events/79.jpeg", "Acidente de Chernobyl", "O acidente de Chernobyl em 1986 intensificou o debate filosófico sobre risco tecnológico analisado por Larry Laudan.", "#D7032A"),
        (1989, 34, "static/img/events/80.jpg", "Queda do Muro de Berlim", "A Queda do Muro de Berlim em 1989 trouxe uma nova organização da pesquisa científica mundial discutida por Laudan.", "#D7032A"),
        (1989, -34, "static/img/events/81.jpg", "Criação da World Wide Web", "A criação da World Wide Web em 1989 revolucionou a comunicação científica global, tema relevante para a epistemologia de Goldman.", "#7E1BE1"),
        (1991, 0, "static/img/events/82.jpg", "Fim da União Soviética", "O fim da União Soviética em 1991 provocou uma reestruturação profunda da ciência mundial analisada por Larry Laudan.", "#D7032A"),
        (2001, -34, "static/img/events/83.webp", "Atentados de 11 de setembro", "Os atentados de 11 de setembro de 2001 expandiram a pesquisa em segurança e tecnologia, tema abordado por Chalmers.", "#D80229"),
        (2003, 34, "static/img/events/84.jpg", "Projeto Genoma Humano", "A conclusão do Projeto Genoma Humano em 2003 marcou um avanço decisivo da genética moderna, discutido por Alvin Goldman.", "#7E1BE1"),
        (2012, 34, "static/img/events/85.jpg", "Descoberta do bóson de Higgs", "A descoberta do bóson de Higgs em 2012 confirmou o Modelo Padrão da física, tema debatido por Van Fraassen e Chalmers.", "#FF0048"),
        (2015, -34, "static/img/events/86.jpg", "Primeira detecção de ondas gravitacionais", "A primeira detecção de ondas gravitacionais em 2015 confirmou experimentalmente a Relatividade Geral, reforçando o empirismo construtivo de Van Fraassen.", "#FF0048"),
        (2020, 0, "static/img/events/87.jpeg", "Pandemia de COVID-19", "A pandemia de COVID-19, iniciada em 2020, evidenciou debates sobre evidência científica, modelos, negacionismo e confiança na ciência, temas caros a Laudan.", "#D7032A"),
    ]

    events_band_color = "#34003d" 
    events_band_height = 100
    events_band_opacity = 0.55
    events_band_border_opacity = 0.00
    events_band_text_color = "#be41d4"
    events_band_font = "monospace"
    events_band_staff = True
    events_band_staff_lines = 2
    events_band_staff_opacity = 0.55
    events_band_staff_color = "#630c72"

    return {
        "philosophies": philosophies,
        "bifurcations": bifurcations,
        "epochs": epochs,
        "philosophers": philosophers,
        "works": works,
        "influences": influences,
        "adepts": adepts,
        "oppositions": oppositions,
        "events": events,
        "events_band_color": events_band_color,
        "events_band_height": events_band_height,
        "events_band_opacity": events_band_opacity,
        "events_band_border_opacity": events_band_border_opacity,
        "events_band_text_color": events_band_text_color,
        "events_band_font": events_band_font,
        "events_band_staff": events_band_staff,
        "events_band_staff_lines": events_band_staff_lines,
        "events_band_staff_opacity": events_band_staff_opacity,
        "events_band_staff_color": events_band_staff_color
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