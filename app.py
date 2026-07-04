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
        "Pragmatismo (Peirce)": (1878, 1902, 120, "#FF4400"),
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
        "Idealismo Alemão": (1805, 1862, -200, "#0088EE"),
        "Dialética Hegeliana": (1812, 1858, -300, "#0066EE"),
        "Materialismo Dialético": (1867, 1986, -350, "#0044EE"),
        "Neo-kantismo": (1870, 1955, -50, "#114EF4"),
        "Fenomenologia": (1900, 1941, -200, "#2525FF"),
        "Hermenêutica Filosófica": (1927, 1952, -300, "#2929FA"),
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
    
    philosophers = [
        ("Francis Bacon", "Empirismo", 1620, 0, "static/img/Francis_Bacon.jpg", [
            ("Informações pessoais", "Político, filósofo empirista, cientista e ensaísta inglês."),
            ("Vida e fatos", "Considerado um dos fundadores da Revolução Científica."),
            ("Teorias/Ideias", [
                "O conhecimento verdadeiro só nasce da experiência sensível organizada de forma metódica.",
                "Método Indutivo: consiste nas fases de observação rigorosa, organização racional, formulação de hipóteses e comprovação.",
                "O seu livro Novum Organum funda o programa empirista.",
                "\"Saber é poder.\"",
            ]),
        ]),

        ("Thomas Hobbes", "Empirismo Materialista", 1656, 0, "static/img/Thomas_Hobbes.jpg", [
            ("Informações pessoais", "Filósofo inglês, um dos principais pensadores da filosofia política moderna."),
            ("Vida e fatos", "Popularizou a frase \"O homem é o lobo do homem\". Contemporâneo de Bacon."),
            ("Teorias/Ideias", [
                "Empirismo materialista: reduz toda atividade mental a movimento de matéria.",
                "Teoria causal da percepção: sensações são movimentos internos causados por pressão externa nos órgãos dos sentidos.",
                "Empirismo: todo o conhecimento humano começa nos sentidos.",
            ]),
        ]),

        ("John Locke", "Empirismo Moderado", 1690, 0, "static/img/john_locke.webp", [
            ("Informações pessoais", "Filósofo inglês, expoente do iluminismo e do empirismo moderado."),
            ("Vida e fatos", "Foi um dos principais filósofos contratualistas."),
            ("Teorias/Ideias", [
                "Tábula Rasa: a mente humana ao nascer é uma tábula rasa, e todo conhecimento vem da experiência (sensação e reflexão).",
                "O conhecimento se alimenta da sensação (contato com o mundo) e reflexão (operação da mente).",
                "Ideias abstratas: a mente forma ideias gerais separando características particulares.",
            ]),
        ]),

        ("George Berkeley", "Empirismo", 1713, 0, "static/img/george_berkeley.jpeg", [
            ("Informações pessoais", "Filósofo empirista, teólogo e bispo anglicano irlandês."),
            ("Vida e fatos", "Conhecido por defender o imaterialismo."),
            ("Teorias/Ideias", [
                "Idealismo Imaterialista (Esse est percipi): a matéria não possui existência independente da mente (\"ser é ser percebido\").",
                "Empirismo: todo conhecimento tem origem na experiência sensível, não existem ideias inatas.",
            ]),
        ]),

        ("David Hume", "Empirismo Cético", 1740, 0, "static/img/David_Hume.jpg", [
            ("Informações pessoais", "Filósofo, historiador, ensaísta e diplomata escocês."),
            ("Vida e fatos", "Representante do empirismo cético e radical. Despertou Kant do \"sono dogmático\"."),
            ("Teorias/Ideias", [
                "O problema da indução: não há justificativa lógica para concluir que o futuro será semelhante ao passado.",
                "Empirismo: todo conhecimento tem origem na experiência sensível, não existem ideias inatas.",
                "Empirismo: todo conhecimento deriva da experiência via impressões e ideias.",
            ]),
        ]),

        ("Charles Sanders Peirce", "Pragmatismo (Peirce)", 1878, 0, "static/img/charles_sanders_peirce.jpeg", [
            ("Informações pessoais", "Matemático, lógico, químico e filósofo americano."),
            ("Vida e fatos", "Fundador do pragmatismo."),
            ("Teorias/Ideias", [
                "O problema da indução: não há justificativa lógica para concluir que o futuro será semelhante ao passado.",
                "Empirismo: todo conhecimento tem origem na experiência sensível, não existem ideias inatas.",
                "Empirismo: todo conhecimento deriva da experiência via impressões e ideias.",
            ]),
        ]),

        ("William James", "Pragmatismo (James)", 1909, 0, "static/img/William_James.jpg", [
            ("Informações pessoais", "Filósofo e psicólogo americano."),
            ("Vida e fatos", "Popularizou e expandiu o pragmatismo de Peirce."),
            ("Teorias/Ideias", [
                "Pragmatismo: a verdade é o que \"funciona\" na experiência prática.",
                "Teoria instrumental da verdade: uma teoria é verdadeira quando funciona satisfatoriamente.",
            ]),
        ]),

        ("Paul Feyerabend", "Anarquismo epistemológico", 1982, 0, "static/img/paul-feyerabend.jpeg", [
            ("Informações pessoais", "Filósofo da ciência austríaco."),
            ("Vida e fatos", "Foi um dos principais críticos da ideia de um método científico universal, defendendo uma visão pluralista da ciência e debatendo intensamente com Popper, Kuhn e Lakatos."),
            ("Teorias/Ideias", [
                "Anarquismo epistemológico: não existe um método científico universal capaz de explicar o progresso da ciência.",
                "Pluralismo metodológico: diferentes métodos e teorias podem contribuir para o avanço científico.",
                "Crítica ao cientificismo: a ciência não é a única forma válida de produzir conhecimento.",
            ]),
        ]),
        
        ("Moritz Schlick", "Círculo de Viena", 1946, 0, "static/img/moritz_schlick.jpeg", [
            ("Informações pessoais", "Filósofo alemão."),
            ("Vida e fatos", "Fundador e líder do Círculo de Viena."),
            ("Teorias/Ideias", [
                "Teoria correspondentista da verdade: proposições verdadeiras correspondem a fatos (via sentenças protocolares).",
                "Princípio da verificabilidade: proposição só possui significado se puder ser verificada empiricamente.",
                "Rejeição da metafísica.",
            ]),
        ]),

        ("Otto Neurath", "Círculo de Viena", 1926, 0, "static/img/otto_neurath.jpeg", [
            ("Informações pessoais", "Filósofo austríaco e membro do Círculo de Viena."),
            ("Vida e fatos", "Liderou a \"liberalização do empirismo\" junto com Carnap."),
            ("Teorias/Ideias", [
                "Coerentismo e Antifundacionalismo: a verdade está nas relações entre os enunciados, não na correspondência direta com fatos.",
                "Metáfora do barco de Neurath: a ciência é reconstruída em alto-mar, sem fundações fixas.",
                "Fisicalismo: proposições científicas devem ser expressas em linguagem física.",
            ]),
        ]),

        ("Rudolf Carnap", "Confirmacionismo", 1945, 0, "static/img/Rudolf_Carnap.webp", [
            ("Informações pessoais", "Filósofo e membro do Círculo de Viena."),
            ("Vida e fatos", "Liderou a liberalização do empirismo e orientou o confirmacionismo."),
            ("Teorias/Ideias", [
                "Confirmacionismo: como a verificação completa é impossível, o grau de confirmação a substitui.",
                "Empirismo lógico com linguagem formal rigorosa baseada na lógica.",
            ]),
        ]),

        ("Karl Popper", "Falsificacionismo", 1940, 0, "static/img/Karl_Popper.jpg", [
            ("Informações pessoais", "Filósofo da ciência austríaco-britânico."),
            ("Vida e fatos", "Reagiu ao verificacionismo do Círculo de Viena, do qual nunca foi membro."),
            ("Teorias/Ideias", [
                "Falsificacionismo: uma teoria é científica se puder ser refutada.",
                "Aceita o problema da indução de Hume, mas recusa o ceticismo.",
                "Conjecturas e refutações: a ciência avança tentando sistematicamente refutar hipóteses.",
            ]),
        ]),

        ("Thomas Kuhn", "Historicismo", 1968, 0, "static/img/thomas_kuhn.jpg", [
            ("Informações pessoais", "Físico, historiador e filósofo da ciência estadunidense."),
            ("Vida e fatos", "Foi o grande rival intelectual de Popper ao introduzir o historicismo."),
            ("Teorias/Ideias", [
                "Paradigma e Ciência Normal: a ciência avança resolvendo quebra-cabeças dentro de um paradigma.",
                "Revolução científica: ocorre pela substituição de paradigmas devido a anomalias.",
                "Incomensurabilidade: paradigmas diferentes não podem ser comparados diretamente.",
            ]),
        ]),

        ("Imre Lakatos", "Programas de Pesquisa", 1969, 0, "static/img/Imre_Lakatos.jpg", [
            ("Informações pessoais", "Filósofo da ciência húngaro."),
            ("Vida e fatos", "Tentou refinar o modelo de Popper e responder às críticas de Kuhn."),
            ("Teorias/Ideias", [
                "Programas de pesquisa científica: núcleo firme central e cinturão protetor de hipóteses auxiliares.",
                "Programas podem ser progressivos ou degenerativos.",
            ]),
        ]),

        ("W. V. O. Quine", "Naturalismo Epistemológico", 1960, 60, "static/img/Willard_Van_Orman_Quin.webp", [
            ("Informações pessoais", "Filósofo e lógico estadunidense."),
            ("Vida e fatos", "Destruiu os dogmas do Círculo de Viena com seu naturalismo epistemológico."),
            ("Teorias/Ideias", [
                "Fim da distinção analítico/sintético e do reducionismo empirista.",
                "Holismo confirmacional: teorias são testadas como um sistema inteiro, não isoladamente.",
            ]),
        ]),

        ("René Descartes", "Racionalismo", 1637, 0, "static/img/rene_descartes.jpg", [
            ("Informações pessoais", "Filósofo, matemático e físico francês."),
            ("Vida e fatos", "Fundador do racionalismo moderno."),
            ("Teorias/Ideias", [
                "Racionalismo: o conhecimento verdadeiro tem origem na razão e na ordem das razões.",
                "Dúvida metódica e Cogito (\"Penso, logo existo\").",
            ]),
        ]),

        ("Baruch Spinoza", "Monismo Panteísta", 1678, 0, "static/img/Baruch_Spinoza.jpg", [
            ("Informações pessoais", "Filósofo holandês racionalista."),
            ("Vida e fatos", "Propõe o monismo panteísta."),
            ("Teorias/Ideias", [
                "Substância única infinita: Deus imanente à natureza.",
                "Determinismo: acontecimentos decorrem de leis da natureza.",
            ]),
        ]),

        ("Gottfried Wilhelm Leibniz", "Monadologia", 1714, 0, "static/img/gottfried_willhelm_leibniz.jpg", [
            ("Informações pessoais", "Matemático e filósofo alemão."),
            ("Vida e fatos", "Criou o cálculo e a monadologia."),
            ("Teorias/Ideias", [
                "Monadologia: o mundo é feito de infinitas mônadas.",
                "Princípio da Razão Suficiente.",
            ]),
        ]),

        ("Immanuel Kant", "Criticismo Kantiano", 1784, 0, "static/img/immanuel_kant.jpeg", [
            ("Informações pessoais", "Filósofo alemão."),
            ("Vida e fatos", "Ponto de fusão entre o Racionalismo e o Empirismo (\"revolução copernicana\")."),
            ("Teorias/Ideias", [
                "O conhecimento combina experiência sensível com estruturas \"a priori\" da mente.",
                "A realidade em si (númeno) permanece inacessível.",
            ]),
        ]),

        ("Edmund Gettier", "Problema de Gettier", 1964, 0, "static/img/Edmund-Gettier.png", [
            ("Informações pessoais", "Filósofo americano."),
            ("Vida e fatos", "Demoliu a concepção clássica da epistemologia com um artigo de três páginas."),
            ("Teorias/Ideias", [
                "Problema de Gettier: contraexemplos onde a crença é verdadeira e justificada apenas por acidente/sorte, provando que Crença Verdadeira Justificada (JTB) não garante conhecimento.",
            ]),
        ]),

        ("John Stuart Mill", "Indutivismo Científico", 1844, 0, "static/img/john_stuart_mill.png", [
            ("Informações pessoais", "Filósofo, economista político e funcionário público britânico."),
            ("Vida e fatos", "Operacionalizou o empirismo herdado de Locke."),
            ("Teorias/Ideias", [
                "Indutivismo científico: propôs métodos formais e rigorosos de indução para a investigação científica.",
            ]),
        ]),

        ("Auguste Comte", "Positivismo Clássico", 1842, 0, "static/img/auguste_comte.jpeg", [
            ("Informações pessoais", "Filósofo francês, fundador da Sociologia."),
            ("Vida e fatos", "Criou o Positivismo clássico, radicalizando a tradição empirista."),
            ("Teorias/Ideias", [
                "Lei dos três estados: a humanidade passa pelos estados teológico, metafísico e positivo (científico).",
                "Rejeição total da metafísica em favor da ciência e da observação rigorosa.",
            ]),
        ]),

        ("Ernst Mach", "Empirio-Criticismo", 1885, 0, "static/img/Ernst_Mach.jpg", [
            ("Informações pessoais", "Físico e filósofo austríaco."),
            ("Vida e fatos", "Foi a principal inspiração direta para a formação do Círculo de Viena."),
            ("Teorias/Ideias", [
                "Empirio-criticismo: propôs um critério positivo frente ao ceticismo.",
                "A ciência é, fundamentalmente, uma descrição econômica das sensações e observações.",
            ]),
        ]),

        ("Friedrich Waismann", "Verificacionismo Estrito (Waismann)", 1928, 0, "static/img/Friedrich_Waismann.jpg", [
            ("Informações pessoais", "Matemático e filósofo austríaco."),
            ("Vida e fatos", "Aluno de Schlick, trabalhou diretamente com Wittgenstein nas discussões do Círculo de Viena."),
            ("Teorias/Ideias", [
                "Liderou a \"ala conservadora\" do Círculo junto com Schlick.",
                "Verificacionismo estrito: o sentido de uma proposição é puramente o seu método de verificação empírica.",
            ]),
        ]),

        ("A. J. Ayer", "Verificacionismo Estrito (Ayer)", 1934, 0, "static/img/AJ-Ayer.webp", [
            ("Informações pessoais", "Filósofo britânico."),
            ("Vida e fatos", "Foi o principal responsável por importar e traduzir o positivismo lógico para o mundo anglófono."),
            ("Teorias/Ideias", [
                "Verificacionismo estrito: radicaliza o critério de verificação.",
                "A metafísica, a teologia e a ética são literalmente sem sentido lógico ou cognitivo.",
            ]),
        ]),

        ("Carl Hempel", "Confirmacionismo", 1968, 0, "static/img/Carl_Hempel.jpg", [
            ("Informações pessoais", "Filósofo da ciência alemão e membro da Escola de Berlim (associada ao Círculo de Viena)."),
            ("Vida e fatos", "Juntamente com Carnap, representou a ala que reconheceu a força da crítica humeana à indução."),
            ("Teorias/Ideias", [
                "Confirmacionismo: como a verificação completa (absoluta) de uma teoria é impossível, o \"grau de confirmação\" deve substituir a verificação total.",
            ]),
        ]),

        ("Larry Laudan", "Tradições de Pesquisa", 1977, 0, "static/img/larry_laudan.jpg", [
            ("Informações pessoais", "Filósofo da ciência contemporâneo."),
            ("Vida e fatos", "Participou ativamente do debate sobre demarcação científica no caso McLean v. Arkansas, sobre o ensino do criacionismo."),
            ("Teorias/Ideias", [
                "Tradições de pesquisa: a ciência atua em tradições de pesquisa que progridem resolvendo problemas empíricos e conceituais.",
                "Rejeita a tese da incomensurabilidade radical de Kuhn.",
            ]),
        ]),

        ("John Watkins", "Racionalismo Crítico", 1980, 0, "static/img/John_Watkins.jpg", [
            ("Informações pessoais", "Filósofo popperiano britânico."),
            ("Vida e fatos", "Participante direto do grande debate epistemológico da década de 1960 entre os popperianos e Kuhn."),
            ("Teorias/Ideias", [
                "Crítica à ciência normal: argumentou contra Kuhn dizendo que a ideia de um \"período de pesquisa não-crítica\" (ciência normal) é perigosa para a racionalidade científica.",
            ]),
        ]),

        ("Paul Thagard", "Demarcação Comportamental", 1984, 0, "static/img/paul-thagard.jpeg", [
            ("Informações pessoais", "Filósofo e cientista cognitivo canadense."),
            ("Vida e fatos", "Trouxe uma abordagem computacional e cognitiva para a filosofia da ciência."),
            ("Teorias/Ideias", [
                "Demarcação social: propõe que a pseudociência é caracterizada por uma estagnação progressiva combinada com uma comunidade que não tenta ativamente resolver suas anomalias.",
            ]),
        ]),

        ("Bas van Fraassen", "Empirismo Construtivo", 1980, 0, "static/img/bas-van-fraassen.jpg", [
            ("Informações pessoais", "Filósofo da ciência holandês-americano."),
            ("Vida e fatos", "Um dos principais defensores modernos do antirrealismo científico."),
            ("Teorias/Ideias", [
                "Empirismo construtivo: a ciência busca a \"adequação empírica\" (salvar os fenômenos) e não necessariamente a \"verdade\" literal sobre entidades inobserváveis.",
            ]),
        ]),

        ("David Bloor", "Programa Forte", 1985, 0, "static/img/David-Bloor.jpg", [
            ("Informações pessoais", "Filósofo e sociólogo britânico da ciência."),
            ("Vida e fatos", "Foi um dos criadores da Escola de Edimburgo e do Programa Forte da Sociologia do Conhecimento Científico."),
            ("Teorias/Ideias", [
                "Programa Forte: crenças científicas verdadeiras e falsas devem ser explicadas pelos mesmos tipos de causas sociais.",
                "Princípio da simetria: não há diferença metodológica entre explicar sucessos e erros científicos.",
                "A produção do conhecimento depende do contexto social.",
            ]),
        ]),

        ("Barry Barnes", "Programa Forte", 1976, 0, "static/img/barry_barnes.jpeg", [
            ("Informações pessoais", "Sociólogo e filósofo britânico da ciência."),
            ("Vida e fatos", "Desenvolveu, juntamente com David Bloor, a Escola de Edimburgo e o Programa Forte."),
            ("Teorias/Ideias", [
                "Programa Forte: o conhecimento científico deve ser explicado sociologicamente.",
                "As instituições e práticas sociais moldam o desenvolvimento da ciência.",
                "Defende uma abordagem naturalista para compreender a produção do conhecimento.",
            ]),
        ]),

        ("Christian Wolff", "Wolffianismo", 1730, 0, "static/img/Christian_Wolf.png", [
            ("Informações pessoais", "Filósofo racionalista alemão."),
            ("Vida e fatos", "Atuou como um importante \"nó de transmissão\" de ideias entre Leibniz e Kant."),
            ("Teorias/Ideias", [
                "Wolffianismo: sistematizou rigorosamente a monadologia leibniziana.",
            ]),
        ]),

        ("Johann Gottlieb Fichte", "Idealismo Alemão", 1806, 0, "static/img/Johann_Gottlieb_Fichte.jpeg", [
            ("Informações pessoais", "Filósofo alemão, um dos fundadores do Idealismo Alemão."),
            ("Vida e fatos", "Desenvolveu sua filosofia a partir da obra de Kant, colocando o \"Eu\" como princípio absoluto de todo conhecimento."),
            ("Teorias/Ideias", [
                "Doutrina da Ciência (Wissenschaftslehre): todo conhecimento deriva da atividade do Eu.",
                "O Eu absoluto cria a si mesmo e estabelece o Não-Eu como limite para sua ação.",
                "A liberdade constitui o fundamento da moralidade e da consciência.",
            ]),
        ]),

        ("Friedrich Wilhelm Joseph Schelling", "Idealismo Alemão", 1822, 0, "static/img/Friedrich_Wilhelm_Joseph_Schelling.jpg", [
            ("Informações pessoais", "Filósofo alemão, representante do Idealismo Alemão."),
            ("Vida e fatos", "Procurou superar a separação entre natureza e espírito presente em Fichte."),
            ("Teorias/Ideias", [
                "Filosofia da Natureza: natureza e espírito constituem manifestações de uma mesma realidade absoluta.",
                "Idealismo da identidade: sujeito e objeto possuem uma unidade fundamental.",
                "A arte é o meio privilegiado para compreender o Absoluto.",
            ]),
        ]),

        ("Georg Wilhelm Friedrich Hegel", "Dialética Hegeliana", 1820, 0, "static/img/Georg_Wilhelm_Friedrich_Hegel.webp", [
            ("Informações pessoais", "Filósofo alemão, principal representante do Idealismo Alemão."),
            ("Vida e fatos", "Desenvolveu um sistema filosófico que influenciou profundamente a filosofia, a política e a história."),
            ("Teorias/Ideias", [
                "Dialética: o desenvolvimento da realidade ocorre por meio de contradições e superações sucessivas.",
                "Espírito Absoluto: a história representa o processo de autoconsciência da razão.",
                "A realidade é racional, e a razão manifesta-se historicamente.",
            ]),
        ]),

        ("Hermann Cohen", "Neo-kantismo", 1902, 0, "static/img/Hermann_Cohen.jpeg", [
            ("Informações pessoais", "Filósofo alemão e fundador da Escola de Marburg do Neokantismo."),
            ("Vida e fatos", "Reformulou o kantismo enfatizando a ciência como fundamento da filosofia."),
            ("Teorias/Ideias", [
                "O conhecimento científico constitui o modelo do conhecimento objetivo.",
                "Rejeição da metafísica tradicional em favor da análise crítica da ciência.",
                "Ênfase na razão como processo contínuo de construção do conhecimento.",
            ]),
        ]),

        ("Wilhelm Windelband", "Neo-kantismo", 1891, 0, "static/img/Wilhelm_Windelband.jpeg", [
            ("Informações pessoais", "Filósofo alemão e fundador da Escola de Baden do Neokantismo."),
            ("Vida e fatos", "Introduziu a distinção entre ciências nomotéticas e idiográficas."),
            ("Teorias/Ideias", [
                "Ciências naturais buscam leis gerais (nomotéticas), enquanto ciências históricas estudam eventos singulares (idiográficas).",
                "Defendeu uma teoria dos valores como fundamento das ciências humanas.",
            ]),
        ]),

        ("Ernst Cassirer", "Estruturalismo Epistemológico", 1924, 0, "static/img/ErnstCassirer.jpg", [
            ("Informações pessoais", "Filósofo alemão, principal representante do Neokantismo da Escola de Marburg."),
            ("Vida e fatos", "Expandiu o kantismo para abranger cultura, linguagem, ciência e arte."),
            ("Teorias/Ideias", [
                "Filosofia das Formas Simbólicas: o ser humano compreende o mundo por meio de sistemas simbólicos.",
                "Estruturalismo epistemológico: o conhecimento é construído através de formas culturais e conceituais.",
                "A cultura é a principal expressão da racionalidade humana.",
            ]),
        ]),

        ("Edmund Husserl", "Fenomenologia", 1900, 0, "static/img/edmund_husserl.webp", [
            ("Informações pessoais", "Matemático e filósofo alemão (nascido na Morávia)."),
            ("Vida e fatos", "É o pai fundador da Fenomenologia."),
            ("Teorias/Ideias", [
                "Fenomenologia: estudo das essências da consciência.",
                "Epoché (suspensão do juízo) e a intencionalidade: toda consciência é sempre consciência \"de\" alguma coisa.",
            ]),
        ]),

        ("Gottlob Frege", "Logicismo", 1879, 0, "static/img/gottlob_frege.jpeg", [
            ("Informações pessoais", "Matemático, lógico e filósofo alemão."),
            ("Vida e fatos", "É considerado o fundador da lógica moderna e da filosofia analítica."),
            ("Teorias/Ideias", [
                "Logicismo: a matemática pode ser fundamentada na lógica.",
                "Distinção entre sentido (Sinn) e referência (Bedeutung).",
                "Rejeição do psicologismo na lógica.",
            ]),
        ]),

        ("Bertrand Russell", "Logicismo", 1930, 0, "static/img/bertrand_russel.jpeg", [
            ("Informações pessoais", "Filósofo, lógico e matemático britânico."),
            ("Vida e fatos", "Um dos fundadores da filosofia analítica e vencedor do Nobel de Literatura de 1950."),
            ("Teorias/Ideias", [
                "Teoria das descrições: resolve problemas filosóficos por meio da análise lógica da linguagem.",
                "Logicismo: desenvolveu com Whitehead uma fundamentação lógica da matemática.",
                "Atomismo lógico: o mundo é composto por fatos logicamente independentes.",
            ]),
        ]),

        ("Martin Heidegger", "Fenomenologia", 1930  , 0, "static/img/Martin_Heidegger.jpg", [
            ("Informações pessoais", "Filósofo alemão, principal representante da fenomenologia existencial."),
            ("Vida e fatos", "Foi discípulo de Husserl e revolucionou a ontologia do século XX."),
            ("Teorias/Ideias", [
                "Dasein (ser-aí): o ser humano é definido por sua existência concreta no mundo.",
                "Ser-no-mundo: sujeito e mundo constituem uma unidade inseparável.",
                "A questão do Ser é o problema central da filosofia.",
            ]),
        ]),

        ("Hans-Georg Gadamer", "Hermenêutica Filosófica", 1926, 0, "static/img/hans_georg_gadamer.webp", [
            ("Informações pessoais", "Filósofo alemão e principal representante da hermenêutica filosófica."),
            ("Vida e fatos", "Desenvolveu a hermenêutica a partir da filosofia de Heidegger."),
            ("Teorias/Ideias", [
                "Hermenêutica filosófica: toda compreensão ocorre historicamente por meio da interpretação.",
                "Fusão de horizontes: compreender consiste em integrar perspectivas diferentes.",
                "A linguagem é o meio universal da compreensão humana.",
            ]),
        ]),

        ("Alvin Goldman", "Confiabilismo", 1995, 0, "static/img/Alvin_Goldman.jpeg", [
            ("Informações pessoais", "Filósofo estadunidense."),
            ("Vida e fatos", "Expoente máximo do naturalismo epistemológico contemporâneo."),
            ("Teorias/Ideias", [
                "Confiabilismo: uma crença só se torna conhecimento se for produzida por um processo cognitivo que seja causalmente confiável.",
                "Epistemologia contínua e interligada com a psicologia cognitiva.",
            ]),
        ]),

        ("Ernest Sosa", "Epistemologia de Virtudes", 1991, 0, "static/img/Ernest_Sosa.jpeg", [
            ("Informações pessoais", "Epistemólogo cubano-americano."),
            ("Vida e fatos", "Ramificou as respostas contemporâneas ao problema de Gettier criando uma nova vertente."),
            ("Teorias/Ideias", [
                "Epistemologia de virtudes: o conhecimento não é apenas processo confiável, mas uma crença verdadeira que resulta de uma \"virtude\" ou \"competência\" intelectual exercida de forma apropriada pelo agente.",
            ]),
        ]),

        ("Noam Chomsky", "Racionalismo Contemporâneo", 1957, 0, "static/img/noam-chomsky.jpg", [
            ("Informações pessoais", "Linguista, filósofo, cientista cognitivo e ativista político estadunidense."),
            ("Vida e fatos", "Revolucionou a linguística moderna ao propor a Gramática Gerativa, retomando a tradição racionalista e o inatismo cartesiano em oposição ao behaviorismo."),
            ("Teorias/Ideias", [
                "Gramática Universal: os seres humanos nascem com uma estrutura linguística inata comum a todas as línguas.",
                "Inatismo: a aquisição da linguagem depende de capacidades cognitivas inatas, não apenas da experiência.",
                "Crítica ao behaviorismo: a linguagem não pode ser explicada apenas por estímulo e resposta.",
            ]),
        ]),

        ("Jerry Fodor", "Racionalismo Contemporâneo", 1978, 0, "static/img/Jerry_Fodor.jpg", [
            ("Informações pessoais", "Filósofo e cientista cognitivo estadunidense."),
            ("Vida e fatos", "Foi um dos principais representantes da filosofia da mente e das ciências cognitivas, desenvolvendo teorias inspiradas pelo racionalismo e pela psicologia cognitiva."),
            ("Teorias/Ideias", [
                "Modularidade da mente: a mente possui módulos especializados e relativamente independentes para diferentes funções cognitivas.",
                "Hipótese da Linguagem do Pensamento (Mentalese): o pensamento ocorre por meio de uma linguagem mental interna.",
                "Defesa do inatismo cognitivo para diversos conceitos e capacidades mentais.",
            ]),
        ]),

        ("David Chalmers", "Racionalismo Contemporâneo", 2006, 0, "static/img/David_chalmers.jpg", [
            ("Informações pessoais", "Filósofo australiano especializado em filosofia da mente e consciência."),
            ("Vida e fatos", "Tornou-se um dos filósofos contemporâneos mais influentes ao formular o chamado \"problema difícil da consciência\"."),
            ("Teorias/Ideias", [
                "Problema difícil da consciência: explicar por que processos físicos produzem experiências subjetivas (qualia).",
                "Dualismo de propriedades: a consciência não pode ser completamente reduzida a processos físicos.",
                "Experimento filosófico dos zumbis: utilizado para argumentar contra o fisicalismo estrito.",
            ]),
        ]),
    ]

    works = {
        'Francis Bacon': [('Novum Organum', '1620')],
        'Thomas Hobbes': [('Leviatã', '1651'), ('De Corpore', '1655')],
        'John Locke': [('Ensaio Sobre o Entendimento Humano', '1690')],
        'George Berkeley': [('Tratado sobre os princípios do conhecimento humano', '1710')],
        'David Hume': [('Tratado da Natureza Humana', '1740')],
        'Charles Sanders Peirce': [('Illustrations of the Logic of Science', '1877-78')],
        'William James': [('Pragmatism', '1907')],
        'Moritz Schlick': [('Über das Fundament der Erkenntnis', '1934')],
        'Otto Neurath': [('Physicalism', '1931')],
        'Rudolf Carnap': [('Logical Foundations of Probability', '1950')],
        'Karl Popper': [('A Lógica da Pesquisa Científica', '1934')],
        'Thomas Kuhn': [('A Estrutura das Revoluções Científicas', '1962')],
        'Imre Lakatos': [('Falsification and the Methodology of SRP', '1970')],
        'W. V. O. Quine': [('Two Dogmas of Empiricism', '1951'), ('Ontological Relativity', '1969')],
        'René Descartes': [('Discurso do Método', '1637')],
        'Baruch Spinoza': [('Ética', '1677')],
        'Gottfried Wilhelm Leibniz': [('Monadologia', '1714')],
        'Immanuel Kant': [('Crítica da Razão Pura', '1781')],
        'Edmund Gettier': [('Is Justified True Belief Knowledge?', '1963')],
        'John Stuart Mill': [('A System of Logic', '1843')],
        'Auguste Comte': [('Cours de philosophie positive', '1842')],
        'Ernst Mach': [('Die Mechanik', '1883')],
        'Friedrich Waismann': [('Discussões do Círculo de Viena', '1929-1936')],
        'A. J. Ayer': [('Language, Truth and Logic', '1936')],
        'Carl Hempel': [('Aspects of Scientific Explanation', '1965')],
        'Larry Laudan': [('Progress and Its Problems', '1977'), ('Science at the Bar', '1982')],
        'John Watkins': [('Against Normal Science', '1970')],
        'Paul Thagard': [('Why Astrology Is a Pseudoscience', '1978')],
        'Bas van Fraassen': [('The Scientific Image', '1980')],
        'David Bloor': [('Knowledge and Social Imagery', '1976')],
        'Barry Barnes': [('Scientific Knowledge and Sociological Theory', '1974')],
        'Christian Wolff': [('Philosophia prima sive ontologia', '1730')],
        'Johann Gottlieb Fichte': [('Fundamentos da Doutrina da Ciência', '1794')],
        'Friedrich Wilhelm Joseph Schelling': [('Sistema do Idealismo Transcendental', '1800')],
        'Georg Wilhelm Friedrich Hegel': [('Fenomenologia do Espírito', '1807'), ('Ciência da Lógica', '1812-1816')],
        'Hermann Cohen': [('Logik der reinen Erkenntnis', '1902')],
        'Wilhelm Windelband': [('History and Natural Science', '1894')],
        'Ernst Cassirer': [('Substance and Function', '1910'), ('The Philosophy of Symbolic Forms', '1923-1929')],
        'Edmund Husserl': [('Investigações Lógicas', '1900')],
        'Gottlob Frege': [('Begriffsschrift', '1879'), ('Os Fundamentos da Aritmética', '1884')],
        'Bertrand Russell': [('Principia Mathematica', '1910-1913'), ('The Problems of Philosophy', '1912')],
        'Martin Heidegger': [('Ser e Tempo', '1927')],
        'Hans-Georg Gadamer': [('Verdade e Método', '1960')],
        'Alvin Goldman': [('Epistemology and Cognition', '1986')],
        'Ernest Sosa': [('Knowledge in Perspective', '1991')],
        'Noam Chomsky': [('Syntactic Structures', '1957'), ('Aspects of the Theory of Syntax', '1965')],
        'Jerry Fodor': [('The Modularity of Mind', '1983'), ('The Language of Thought', '1975')],
        'Paul Feyerabend': [('Against Method', '1975'), ('Science in a Free Society', '1978'), ('Farewell to Reason', '1987')],
        'David Chalmers': [('The Conscious Mind', '1996'), ('Reality+: Virtual Worlds and the Problems of Philosophy', '2022')],
    }

    influences = {
        'Francis Bacon': [('Aristóteles', 'Bacon buscou substituir seu método.', 'Discorda')],
        'Thomas Hobbes': [('Francis Bacon', 'Hobbes manteve a base empirista de Bacon, mas a radicalizou no materialismo.', 'Discorda')],
        'John Locke': [('Francis Bacon', 'Locke deu continuidade ao empirismo iniciado por Bacon.', 'Concorda')],
        'George Berkeley': [('John Locke', 'Berkeley partiu do empirismo de Locke, mas radicalizou-o no imaterialismo.', 'Discorda')],
        'David Hume': [('John Locke', 'Hume levou o empirismo de Locke às últimas consequências, radicalizando o ceticismo.', 'Concorda')],
        'Charles Sanders Peirce': [('Immanuel Kant', '-', 'Concorda'), ('David Hume', '-', 'Concorda')],
        'William James': [('Charles Sanders Peirce', 'Herdou e expandiu o pragmatismo peirciano.', 'Concorda')],
        'Moritz Schlick': [('Ernst Mach', 'Precursor do empirismo lógico do Círculo de Viena.', 'Concorda'), ('Auguste Comte', 'Precursor da rejeição da metafísica em favor da ciência.', 'Concorda')],
        'Rudolf Carnap': [('Moritz Schlick', 'Carnap deu continuidade ao projeto do Círculo de Viena liderado por Schlick.', 'Concorda'), ('Otto Neurath', 'Incorporou ideias de Neurath sobre linguagem científica.', 'Concorda')],
        'Karl Popper': [('David Hume', 'Aceitou o problema da indução de Hume, mas recusou o ceticismo, propondo o falsificacionismo.', 'Discorda')],
        'Imre Lakatos': [('Karl Popper', 'Lakatos tentou refinar e defender o falsificacionismo de Popper.', 'Concorda'), ('Thomas Kuhn', 'Buscou responder às críticas históricas levantadas por Kuhn.', 'Discorda')],
        'W. V. O. Quine': [('Rudolf Carnap', 'Quine rompeu com dogmas centrais do empirismo lógico de Carnap.', 'Discorda')],
        'René Descartes': [('Euclides', 'O método geométrico de Euclides inspirou o ideal cartesiano de conhecimento mais geométrico.', 'Concorda')],
        'Baruch Spinoza': [('René Descartes', 'Spinoza partiu do racionalismo cartesiano, radicalizando-o no monismo.', 'Concorda')],
        'Gottfried Wilhelm Leibniz': [('René Descartes', 'Leibniz expandiu o racionalismo cartesiano com a teoria das mônadas.', 'Concorda')],
        'Immanuel Kant': [('David Hume', 'O ceticismo de Hume despertou Kant do "sono dogmático".', 'Discorda'), ('Gottfried Wilhelm Leibniz', 'Kant partiu da tradição racionalista leibniziana antes de reformulá-la criticamente.', 'Discorda')],
        'Edmund Gettier': [('Bertrand Russell', 'A discussão de Russell sobre conhecimento e crença justificada preparou o terreno para o problema de Gettier.', 'Concorda')],
        'John Stuart Mill': [('John Locke', 'Mill operacionalizou o empirismo herdado de Locke.', 'Concorda')],
        'Auguste Comte': [('Empiristas anteriores', 'Radicalizou a tradição empirista em um sistema positivista.', 'Concorda')],
        'Ernst Mach': [('David Hume', 'Retomou o ceticismo humeano em relação a entidades metafísicas não observáveis.', 'Concorda')],
        'Friedrich Waismann': [('Moritz Schlick', 'Trabalhou diretamente sob a liderança de Schlick no Círculo de Viena.', 'Concorda'), ('Ludwig Wittgenstein', 'Incorporou ideias de Wittgenstein às discussões do Círculo.', 'Concorda')],
        'A. J. Ayer': [('Moritz Schlick', 'Importou e traduziu o positivismo lógico do Círculo de Viena.', 'Concorda'), ('Friedrich Waismann', 'Popularizou o verificacionismo estrito de Waismann.', 'Concorda')],
        'Carl Hempel': [('Rudolf Carnap', 'Hempel deu continuidade ao projeto confirmacionista de Carnap.', 'Concorda')],
        'Larry Laudan': [('W. V. O. Quine', 'Incorporou o naturalismo epistemológico quineano à filosofia da ciência.', 'Concorda')],
        'John Watkins': [('Karl Popper', 'Defendeu e desenvolveu o racionalismo crítico popperiano.', 'Concorda')],
        'Paul Thagard': [('Larry Laudan', 'Desenvolveu computacionalmente critérios de progresso científico inspirados em Laudan.', 'Concorda')],
        'Bas van Fraassen': [('W. V. O. Quine', 'Incorporou o naturalismo quineano ao empirismo construtivo.', 'Concorda'), ('Thomas Kuhn', 'Absorveu a crítica kuhniana ao realismo ingênuo sobre teorias científicas.', 'Concorda')],
        'David Bloor': [('Thomas Kuhn', 'Radicalizou sociologicamente a noção kuhniana de paradigma.', 'Concorda')],
        'Barry Barnes': [('Thomas Kuhn', 'Desenvolveu com Bloor a leitura sociológica dos paradigmas kuhnianos.', 'Concorda')],
        'Christian Wolff': [('Gottfried Wilhelm Leibniz', 'Sistematizou rigorosamente a monadologia leibniziana.', 'Concorda')],
        'Johann Gottlieb Fichte': [('Immanuel Kant', 'Desenvolveu sua filosofia a partir da obra de Kant.', 'Concorda')],
        'Friedrich Wilhelm Joseph Schelling': [('Immanuel Kant', 'Partiu da revolução copernicana kantiana.', 'Concorda'), ('Johann Gottlieb Fichte', 'Procurou superar a separação entre natureza e espírito presente em Fichte.', 'Discorda')],
        'Georg Wilhelm Friedrich Hegel': [('Immanuel Kant', 'Desenvolveu seu sistema dialético a partir de problemas deixados pela filosofia crítica de Kant.', 'Concorda')],
        'Hermann Cohen': [('Immanuel Kant', 'Reformulou o kantismo enfatizando a ciência como fundamento da filosofia.', 'Concorda')],
        'Wilhelm Windelband': [('Immanuel Kant', 'Fundou a Escola de Baden do Neokantismo a partir da epistemologia kantiana.', 'Concorda')],
        'Ernst Cassirer': [('Hermann Cohen', 'Formou-se na Escola de Marburg fundada por Cohen.', 'Concorda'), ('Immanuel Kant', 'Expandiu o kantismo para abranger cultura, linguagem, ciência e arte.', 'Concorda')],
        'Edmund Husserl': [('Immanuel Kant', 'A busca por uma fundamentação rigorosa do conhecimento ecoa preocupações kantianas.', 'Concorda'), ('René Descartes', 'A busca por um fundamento apodítico da consciência retoma o projeto cartesiano.', 'Concorda')],
        'Gottlob Frege': [('Gottfried Wilhelm Leibniz', 'Retomou o ideal leibniziano de uma linguagem lógica universal.', 'Concorda')],
        'Bertrand Russell': [('Gottlob Frege', 'Desenvolveu a análise lógica e o logicismo inspirado em Frege.', 'Concorda')],
        'Martin Heidegger': [('Edmund Husserl', 'Foi discípulo de Husserl antes de transformar a fenomenologia em ontologia existencial.', 'Discorda')],
        'Hans-Georg Gadamer': [('Martin Heidegger', 'Desenvolveu a hermenêutica a partir da ontologia de Heidegger.', 'Concorda')],
        'Alvin Goldman': [('W. V. O. Quine', 'Expoente do naturalismo epistemológico quineano.', 'Concorda'), ('Edmund Gettier', 'Desenvolveu o confiabilismo como resposta ao problema de Gettier.', 'Concorda')],
        'Ernest Sosa': [('Edmund Gettier', 'Ramificou as respostas ao problema de Gettier na epistemologia de virtudes.', 'Concorda')],
        'Noam Chomsky': [('René Descartes', 'Retomou o inatismo cartesiano em oposição ao behaviorismo.', 'Concorda')],
        'Jerry Fodor': [('Noam Chomsky', 'Desenvolveu teorias cognitivas inspiradas no inatismo chomskyano.', 'Concorda'), ('René Descartes', 'Defendeu formas de inatismo cognitivo na linhagem cartesiana.', 'Concorda')],
        'David Chalmers': [('René Descartes', 'Retoma o dualismo na discussão contemporânea sobre a consciência.', 'Concorda'), ('Frank Jackson', 'Incorporou argumentos como o do "quarto de Mary" na defesa do dualismo de propriedades.', 'Concorda'), ('Thomas Nagel', 'Baseou-se na pergunta "o que é ser um morcego?" para formular o problema difícil.', 'Concorda')],
    }

    adepts = {
        'Paul Feyerabend': [('Thomas Kuhn', 'Compartilhava a crítica à existência de um método científico único, embora defendesse uma posição menos radical.'), ('David Bloor', 'Incorporou a ideia de que o conhecimento científico deve ser compreendido também em seu contexto social.'), ('Barry Barnes', 'Desenvolveu abordagens sociológicas da ciência inspiradas pela crítica ao objetivismo científico.')],
        'Francis Bacon': [('Thomas Hobbes', 'Adotou o empirismo como base do conhecimento, aplicando-o ao materialismo.'), ('John Locke', 'Desenvolveu o empirismo defendendo que toda ideia deriva da experiência.')],
        'Thomas Hobbes': [('John Locke', 'Manteve a ideia de que todo conhecimento começa na experiência, embora rejeitasse o materialismo de Hobbes.')],
        'John Locke': [('George Berkeley', 'Aceitou que todo conhecimento provém da experiência, embora negasse a existência da matéria.'), ('David Hume', 'Radicalizou o empirismo ao questionar causalidade, substância e indução.')],
        'George Berkeley': [('Arthur Collier', 'Desenvolveu uma forma semelhante de idealismo imaterialista.')],
        'David Hume': [('Ernst Mach', 'Incorporou o empirismo radical e a crítica às entidades metafísicas.')],
        'Charles Sanders Peirce': [('William James', 'Popularizou e ampliou o pragmatismo.')],
        'William James': [('John Dewey', 'Desenvolveu o pragmatismo para educação e democracia.')],
        'Moritz Schlick': [('Friedrich Waismann', 'Desenvolveu o verificacionismo estrito.')],
        'Otto Neurath': [('Rudolf Carnap', 'Incorporou muitas de suas ideias sobre linguagem científica.')],
        'Rudolf Carnap': [('Carl Hempel', 'Desenvolveu o confirmacionismo.')],
        'Karl Popper': [('John Watkins', 'Defendeu o racionalismo crítico.'), ('Imre Lakatos', 'Reformulou o falsificacionismo em programas de pesquisa.')],
        'Thomas Kuhn': [('Paul Feyerabend', 'Radicalizou a crítica ao método científico único.')],
        'Imre Lakatos': [('Elie Zahar', 'Desenvolveu e aplicou a metodologia dos programas de pesquisa.')],
        'W. V. O. Quine': [('Alvin Goldman', 'Desenvolveu uma epistemologia naturalizada inspirada em Quine.')],
        'René Descartes': [('Baruch Spinoza', 'Desenvolveu o racionalismo em um sistema monista.'), ('Gottfried Wilhelm Leibniz', 'Expandiu o racionalismo com a teoria das mônadas.')],
        'Baruch Spinoza': [('Gilles Deleuze', 'Retomou o pensamento spinozano na filosofia contemporânea.')],
        'Gottfried Wilhelm Leibniz': [('Christian Wolff', 'Sistematizou sua filosofia.')],
        'Immanuel Kant': [('Neokantianos', 'Recuperaram criticamente sua epistemologia.')],
        'Edmund Gettier': [('Alvin Goldman', 'Respondeu com o confiabilismo.'), ('Ernest Sosa', 'Respondeu com a epistemologia das virtudes.')],
        'John Stuart Mill': [('Herbert Spencer', 'Desenvolveu o empirismo e o evolucionismo.')],
        'Auguste Comte': [('Émile Durkheim', 'Aplicou o positivismo à sociologia.')],
        'Ernst Mach': [('Moritz Schlick', 'Inspirou o Círculo de Viena.'), ('Rudolf Carnap', 'Desenvolveu o empirismo lógico.')],
        'Friedrich Waismann': [('A. J. Ayer', 'Popularizou o verificacionismo.')],
        'A. J. Ayer': [('Michael Dummett', 'Inicialmente influenciado pela tradição analítica inaugurada por Ayer.')],
        'Carl Hempel': [('Nelson Goodman', 'Desenvolveu problemas ligados à confirmação.')],
        'Larry Laudan': [('Paul Thagard', 'Desenvolveu critérios de progresso científico.')],
        'John Watkins': [('David Miller', 'Desenvolveu o racionalismo crítico popperiano.')],
        'Bas van Fraassen': [('James Ladyman', 'Desenvolveu debates sobre empirismo e realismo científico.')],
        'David Bloor': [('Barry Barnes', 'Desenvolveu conjuntamente o Programa Forte da Sociologia do Conhecimento Científico.')],
        'Barry Barnes': [('David Bloor', 'Desenvolveu em conjunto a abordagem simétrica para explicar o conhecimento científico.')],
        'Christian Wolff': [('Alexander Baumgarten', 'Desenvolveu o sistema wolffiano, especialmente na metafísica e na estética.')],
        'Johann Gottlieb Fichte': [('Friedrich Wilhelm Joseph Schelling', 'Desenvolveu a filosofia de Fichte ampliando-a para incluir a natureza.')],
        'Friedrich Wilhelm Joseph Schelling': [('Românticos alemães', 'Incorporaram sua ideia da unidade entre natureza, espírito e arte.')],
        'Georg Wilhelm Friedrich Hegel': [('Karl Marx', 'Adaptou a dialética hegeliana para uma perspectiva materialista.'), ('Alexandre Kojève', 'Popularizou a interpretação existencial e histórica da dialética hegeliana.')],
        'Hermann Cohen': [('Paul Natorp', 'Expandiu o programa epistemológico da Escola de Marburg.'), ('Ernst Cassirer', 'Estendeu o neokantismo ao estudo da cultura e das formas simbólicas.')],
        'Wilhelm Windelband': [('Heinrich Rickert', 'Desenvolveu a teoria dos valores aplicada às ciências da cultura.')],
        'Ernst Cassirer': [('Jean Piaget', 'Compartilhou a ideia de que o conhecimento é construído por estruturas cognitivas.')],
        'Edmund Husserl': [('Martin Heidegger', 'Transformou a fenomenologia em uma ontologia existencial.'), ('Jean-Paul Sartre', 'Aplicou a fenomenologia ao existencialismo.')],
        'Gottlob Frege': [('Bertrand Russell', 'Desenvolveu o logicismo e a análise lógica inspirados em Frege.'), ('Ludwig Wittgenstein', 'Adotou a lógica fregiana como base de sua filosofia inicial.')],
        'Bertrand Russell': [('A. J. Ayer', 'Desenvolveu a tradição analítica e o empirismo lógico inspirados em Russell.')],
        'Martin Heidegger': [('Hans-Georg Gadamer', 'Desenvolveu a hermenêutica filosófica a partir da ontologia de Heidegger.'), ('Jean-Paul Sartre', 'Adaptou conceitos heideggerianos ao existencialismo.')],
        'Hans-Georg Gadamer': [('Paul Ricoeur', 'Desenvolveu a hermenêutica incorporando análise textual e fenomenologia.')],
        'Alvin Goldman': [('John Greco', 'Desenvolveu versões contemporâneas do confiabilismo e da epistemologia das virtudes.')],
        'Ernest Sosa': [('Linda Zagzebski', 'Expandiu a epistemologia das virtudes para incluir aspectos éticos das virtudes intelectuais.')],
        'Noam Chomsky': [('Steven Pinker', 'Desenvolveu a teoria da linguagem como adaptação biológica baseada na Gramática Universal.'), ('Ray Jackendoff', 'Expandiu a teoria gerativa para integrar sintaxe, semântica e cognição.')],
        'Jerry Fodor': [('Zenon Pylyshyn', 'Desenvolveu modelos computacionais da cognição baseados na arquitetura simbólica proposta por Fodor.')],
        'David Chalmers': [('Galen Strawson', 'Defende formas de panpsiquismo compatíveis com a importância fundamental da consciência.'), ('Philip Goff', 'Desenvolveu o panpsiquismo contemporâneo como resposta ao problema difícil da consciência.')],
    }

    oppositions = {
        'Paul Feyerabend': [('Karl Popper', 'Criticava o abandono de critérios racionais para distinguir ciência de pseudociência.'), ('Imre Lakatos', 'Discordava do anarquismo metodológico e defendia regras racionais para comparar programas de pesquisa.'), ('Larry Laudan', 'Rejeitava seu relativismo metodológico, defendendo critérios objetivos de progresso científico.')],
        'Francis Bacon': [('René Descartes', 'Defendia que a razão e as ideias claras são o fundamento do conhecimento, enquanto Bacon privilegiava a observação e a indução.')],
        'Thomas Hobbes': [('René Descartes', 'Rejeitava a redução da mente à matéria proposta por Hobbes, defendendo o dualismo mente-corpo.')],
        'John Locke': [('René Descartes', 'Criticava a negação das ideias inatas e defendia que certos conhecimentos são anteriores à experiência.')],
        'George Berkeley': [('Thomas Hobbes', 'Defendia uma realidade material independente da mente, incompatível com o imaterialismo de Berkeley.')],
        'David Hume': [('Karl Popper', 'Aceitou o problema da indução de Hume, mas rejeitou a conclusão cética de Hume propondo o falsificacionismo.')],
        'Charles Sanders Peirce': [('William James', 'Divergiu da interpretação subjetivista da verdade adotada por James, defendendo um pragmatismo mais lógico e científico.')],
        'William James': [('Bertrand Russell', 'Criticava a ideia de que a verdade depende apenas de sua utilidade prática.')],
        'Moritz Schlick': [('Otto Neurath', 'Rejeitava a substituição da correspondência aos fatos pelo coerentismo.')],
        'Otto Neurath': [('Moritz Schlick', 'Criticava a existência de fundamentos absolutos para o conhecimento científico.')],
        'Rudolf Carnap': [('W. V. O. Quine', 'Contestou a distinção analítico/sintético e o reducionismo lógico.')],
        'Karl Popper': [('Thomas Kuhn', 'Discordava da ideia de ciência normal e do historicismo dos paradigmas.')],
        'Thomas Kuhn': [('Karl Popper', 'Criticava a ausência de crítica permanente durante a ciência normal.'), ('John Watkins', 'Considerava a ciência normal incompatível com a racionalidade científica.')],
        'Imre Lakatos': [('Paul Feyerabend', 'Considerava excessivamente racional sua metodologia dos programas de pesquisa.')],
        'W. V. O. Quine': [('A. J. Ayer', 'Defendia o positivismo lógico que Quine criticou em "Dois Dogmas do Empirismo".')],
        'René Descartes': [('Francis Bacon', 'Criticava a confiança excessiva na experiência sensível.')],
        'Baruch Spinoza': [('Gottfried Wilhelm Leibniz', 'Discordava do monismo e defendia a pluralidade das mônadas.')],
        'Gottfried Wilhelm Leibniz': [('Baruch Spinoza', 'Rejeitava a ideia de uma única substância.')],
        'Immanuel Kant': [('Idealistas alemães', 'Criticavam a permanência da coisa-em-si inacessível.')],
        'Edmund Gettier': [('Robert Nozick', 'Propôs uma teoria alternativa do conhecimento baseada em rastreamento da verdade.')],
        'John Stuart Mill': [('William Whewell', 'Criticava a redução do método científico à indução.')],
        'Auguste Comte': [('Idealistas alemães', 'Rejeitavam sua eliminação da metafísica.')],
        'Ernst Mach': [('Max Planck', 'Criticou seu fenomenalismo e antirrealismo científico.')],
        'Friedrich Waismann': [('Otto Neurath', 'Criticava o verificacionismo rígido.'), ('Rudolf Carnap', 'Defendia uma versão mais flexível do empirismo lógico.')],
        'A. J. Ayer': [('W. V. O. Quine', 'Rejeitou os pressupostos fundamentais do positivismo lógico.')],
        'Carl Hempel': [('Karl Popper', 'Criticava o confirmacionismo como critério de ciência.')],
        'Larry Laudan': [('Paul Feyerabend', 'Criticava seu relativismo metodológico.'), ('Thomas Kuhn', 'Discordava da incomensurabilidade forte.')],
        'John Watkins': [('Thomas Kuhn', 'Criticava a ciência normal.')],
        'Paul Thagard': [('Paul Feyerabend', 'Discordava do relativismo metodológico.')],
        'Bas van Fraassen': [('Realistas científicos', 'Contestavam sua defesa da adequação empírica em vez da verdade.')],
        'David Bloor': [('Larry Laudan', 'Criticava a redução da ciência a fatores sociológicos, defendendo o papel central da racionalidade e da resolução de problemas.')],
        'Barry Barnes': [('Larry Laudan', 'Rejeitava a explicação puramente sociológica do progresso científico.')],
        'Christian Wolff': [('Christian Thomasius', 'Criticava o excesso de racionalismo sistemático e o uso dedutivo da metafísica.')],
        'Johann Gottlieb Fichte': [('Arthur Schopenhauer', 'Rejeitava o idealismo do Eu absoluto, defendendo a vontade como fundamento da realidade.')],
        'Friedrich Wilhelm Joseph Schelling': [('Materialistas e positivistas', 'Rejeitavam sua concepção metafísica da natureza e do Absoluto.')],
        'Georg Wilhelm Friedrich Hegel': [('Arthur Schopenhauer', 'Criticava o sistema hegeliano por considerá-lo obscuro e excessivamente abstrato.'), ('Karl Popper', 'Acusava Hegel de favorecer o historicismo e justificar formas de autoritarismo.')],
        'Hermann Cohen': [('Idealistas hegelianos', 'Discordavam de sua substituição da metafísica pela análise crítica da ciência.')],
        'Wilhelm Windelband': [('Positivistas', 'Rejeitavam a distinção metodológica entre ciências naturais e humanas.')],
        'Ernst Cassirer': [('Martin Heidegger', 'Criticava a prioridade dada por Cassirer à razão e às formas simbólicas em detrimento da existência concreta.')],
        'Edmund Husserl': [('Positivistas lógicos', 'Rejeitavam a investigação fenomenológica por considerá-la excessivamente descritiva e metafísica.')],
        'Gottlob Frege': [('Intuicionistas', 'Negavam que toda a matemática pudesse ser reduzida à lógica formal.')],
        'Bertrand Russell': [('Idealistas britânicos', 'Discordavam de sua defesa da análise lógica e do realismo.')],
        'Martin Heidegger': [('Rudolf Carnap', 'Considerava sua linguagem metafísica desprovida de significado lógico.')],
        'Hans-Georg Gadamer': [('Positivistas lógicos', 'Rejeitavam a interpretação hermenêutica como método filosófico válido.')],
        'Alvin Goldman': [('Internalistas rigorosos', 'Argumentavam que a justificação depende do acesso consciente às razões da crença, e não apenas da confiabilidade do processo.')],
        'Ernest Sosa': [('Alvin Goldman', 'Considerava insuficiente explicar o conhecimento apenas pela confiabilidade causal, enfatizando as virtudes intelectuais do agente.')],
        'Noam Chomsky': [('B. F. Skinner', 'Defendia que a linguagem é aprendida por condicionamento, rejeitando estruturas linguísticas inatas.'), ('Empiristas contemporâneos', 'Contestavam a hipótese de capacidades cognitivas inatas.')],
        'Jerry Fodor': [('Conexionistas', 'Contestavam a ideia de módulos mentais rígidos, defendendo processamento distribuído.'), ('Behavioristas', 'Negavam estados mentais internos como explicações científicas.'), ('Paul Churchland', 'Criticava a linguagem do pensamento e defendia uma abordagem neurocientífica eliminativista.')],
        'David Chalmers': [('Daniel Dennett', 'Sustenta que o "problema difícil" resulta de uma confusão conceitual e pode ser explicado fisicamente.'), ('Patricia Churchland', 'Defende que os avanços da neurociência tornam desnecessário recorrer ao dualismo de propriedades.')],
    }


    events = [
        (1700, 0, "static/img/bacon.png", "CEO Do Bacon", "O CEO do Bacon Nasceu e Dominou o Mundo Inteiro", "#cc0066"),
        (1710, -33, "static/img/bacon.png", "CEO Do Bacon 2", "O CEO do Bacon Nasceu e Dominou o Mundo Inteiro", "#cc0066"),
        (1720, 0, "static/img/bacon.png", "CEO Do Bacon 3", "O CEO do Bacon Nasceu e Dominou o Mundo Inteiro", "#cc0066"),
        (1730, 33, "static/img/bacon.png", "CEO Do Bacon 4", "O CEO do Bacon Nasceu e Dominou o Mundo Inteiro", "#cc0066"),
        (2026, 0, "static/img/bacon.png", "CEO Do Bacon 5", "O CEO do Bacon Nasceu e Dominou o Mundo Inteiro", "#cc0066"),
    ]
    #(-400, 0, "static/img/bacon.png", "CEO Do Bacon", "O CEO do Bacon Nasceu e Dominou o Mundo Inteiro", "#cc0066")

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