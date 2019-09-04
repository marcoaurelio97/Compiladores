import json 

# variáveis globais
tokens, erros = [], []
linha, indice, global_indice = 1, 0, 0

def analisadorLexico(programa):
    # TODO: implementar essa funcao
    global linha, indice, global_indice

    # lista de tokens lógicos
    logicos = {
        "Sim": "logico",
        "Nao": "logico"
    }

    # lista de tokens reservados
    reservados = {
        "se": "reservado",
        "se nao": "reservado",
        "se nao se": "reservado",
        "enquanto": "reservado",
        "retorna": "reservado"
    }

    # lista de tokens de erro
    op_erros = {
        "@": "desconhecido"
    }

    # lista de tokens simples
    op_simples = {
        ",": "virgula",
        "(": "abre-parenteses",
        ")": "fecha-parenteses",
        "{": "abre-chaves",
        "}": "fecha-chaves",
        "=": "operador-igual",
        "<": "operador-menor",
        ">": "operador-maior",
        "+": "operador-mais"
    }

    # lista de tokens duplos
    op_duplos = {
        "::": "atribuicao",
        "--": "comentario"
    }

    # lista de tokens extras
    op_extras = {
        "\n": "quebra-linha",
        ":": "dois-pontos",
        "!=": "operador-diferente"
    }

    token_text = ""
    comentario, text, number = False, False, False # variáveis de controle do tipo do texto
    flag_indice = 0

    for c in programa: # iteração em cada caractere do programa
        if c == "-" and programa[global_indice + 1] == "-": # caso o caractere for um traço e o próximo também
            comentario = True # então um comentário é iniciado
            flag_indice = indice # o índice de início do comentário é salvo
            token_text += c + programa[global_indice + 1] # os caracteres são atribuídos ao texto analisado

        elif c == "\n": # caso o caractere for um quebra de linha
            if comentario: # e for um comentário
                comentario = False # o comentário foi finalizado
                addToken(op_duplos["--"], token_text, linha, flag_indice) # e o token do comentário é adicionado
                token_text = ""
            
            if text: # se for um texto
                text = False # o texto foi finalizado
                if token_text in logicos: # se o token obtido estiver na lista de lógicos
                    addToken(logicos[token_text], token_text, linha, flag_indice) # é adicionado um token lógico
                    token_text = ""
                else: # caso não esteja na lista de lógicos
                    token_text = token_text.split() # o token é um texto de retorno de função
                    addToken(reservados[token_text[0]], token_text[0], linha, flag_indice) # o "retorna" é um token reservado
                    addToken("identificador", token_text[1], linha, flag_indice + len(token_text[0]) + 1) # a variável retornada é um identificador
                    token_text = ""

            addToken(op_extras["\n"], c, linha, indice) # o caractere "\n" é adicionado

            linha += 1 # a linha é incrementada
            indice = 0 # o índice da linha é zerado
            global_indice += 1 # o índice global é incrementado
            continue

        elif c == ":": # caso o caractere for dois pontos
            if text: # e for um texto
                if not token_text.istitle(): # e não começar com a primeira letra maiúscula
                    addToken("identificador", token_text, linha, flag_indice) # o texto é um token identificador
                else: #se começar com a primeira letra maiúscula
                    addToken("reservado", token_text, linha, flag_indice) # o texto é um token reservado

                text = False
                token_text = ""
                
            if programa[global_indice + 1] == ":": # se o próximo caractere for dois pontos também
                addToken(op_duplos["::"], "::", linha, indice) # o texto é um token de atribuição
            elif programa[global_indice - 1] != ":": # se o caractere anterior não for dois pontos
                addToken(op_extras[":"], ":", linha, indice) # o texto é um token de dois pontos
            
            indice += 1 # o índice da linha é incrementado
            global_indice += 1 # o índice global é incrementado
            continue # é continuado para o próximo caractere
        
        elif c == "'": # caso o caractere for uma aspas simples
            if token_text and token_text.count("#", len(token_text) - 2, len(token_text)) % 2 == 0: # caso a quantidade de # nos 2 últimos caracteres for par
                text = False
                token_text += c # o caractere é atribuído ao texto analisado
                addToken("texto", token_text, linha, flag_indice) # o token é um texto
                token_text = ""
            else:
                if not text: # se não for um texto
                    text = True
                    flag_indice = indice # é salvo o índice do início do texto
                
                token_text += c # o caractere é atribuído ao texto analisado

            indice += 1 # o índice da linha é incrementado
            global_indice += 1 # o índice global é incrementado
            continue # é continuado para o próximo caractere

        elif c.isnumeric(): # se o caractere for numérico
            if not programa[global_indice + 1].isnumeric(): # e o próximo caractere não for numérico
                if not token_text:
                    flag_indice = indice # é salvo o índice de início do número

                token_text += c # o caractere é atribuído ao texto analisado
                addToken("numero", token_text, linha, flag_indice) # o texto é um token de número
                token_text = ""
                number = False

            else:
                token_text += c # o caractere é atribuído ao texto analisado
                if not number:
                    number = True # um número foi encontrado
                    flag_indice = indice # é salvo o índice de início do número

            indice += 1 # o índice da linha é incrementado
            global_indice += 1 # o índice global é incrementado
            continue # é continuado para o próximo caractere

        elif c in op_simples: # se o caractere estiver na lista de tokens simples
            if text: # se for um texto
                text = False
                if token_text in reservados: # se estiver na lista de reservado
                    addToken(reservados[token_text], token_text, linha, flag_indice) # o texto é um token reservado
                elif token_text + c in op_extras: # se estiver na lista de tokens extras
                    token_text += c # o caractere é atribuído ao texto analisado
                    addToken(op_extras[token_text], token_text, linha, flag_indice) # o texto é um token extra
                    token_text = ""

                    indice += 1 # o índice da linha é incrementado
                    global_indice += 1 # o índice global é incrementado
                    continue # é continuado para o próximo caractere
                elif not token_text.istitle(): # se o texto não começar com a primeira letra maiúscula
                    addToken("identificador", token_text.strip(), linha, flag_indice) # o token é um token identificador
                else: #se começar com a primeira letra maiúscula
                    addToken("reservado", token_text, linha, flag_indice) # o texto é um token reservado

                token_text = ""
            
            addToken(op_simples[c], c, linha, indice)

            indice += 1 # o índice da linha é incrementado
            global_indice += 1 # o índice global é incrementado
            continue # é continuado para o próximo caractere
        
        elif c in op_erros: # se o caractere estiver na lista de erros
            text = False
            token_text = token_text[:-1] # um espaço desnecessário é removido
            addToken(reservados[token_text], token_text, linha, flag_indice) # o texto é um token reservado
            addToken(op_erros[c], c, linha, indice) # o caractere de erro é adicionado aos tokens
            addErro(f"simbolo, {c}, desconhecido", linha, indice) # e adicionado a lista de erros
            token_text = ""

        elif c != "-": # se o caractere for diferente de traço
            if not comentario: # e não for um comentário
                if not text: # e não for um texto
                    text = True # então é um texto
                    flag_indice = indice # e o índice de início do texto é salvo

            if c == " " and token_text == "": # se o caractere for um espaço e o texto analisado estiver vazio
                text = False # não é um texto
                indice += 1 # o índice da linha é incrementado
                global_indice += 1 # o índice global é incrementado
                continue # é continuado para o próximo caractere
            else:
                token_text += c # o caractere é atribuído ao texto analisado

        indice += 1 # o índice da linha é incrementado
        global_indice += 1 # o índice global é incrementado

    return {"tokens":tokens,"erros":erros} # é retornado todos os tokens e erros encontrados


def addToken(grupo, texto, linha, indice): # função que adiciona um token à lista de tokens
    tokens.append({
        "grupo": grupo,
        "texto": texto,
        "local": {"linha":linha,"indice":indice}
    })


def addErro(texto, linha, indice): # função que adiciona um erro à lista de erros
    erros.append({
        "texto": texto,
        "local": {"linha":linha,"indice":indice}
    })

# ALERTA: Nao modificar o codigo fonte apos esse aviso

def testaAnalisadorLexico(programa, teste):
    # Caso o resultado nao seja igual ao teste
    # ambos sao mostrados e a execucao termina  
    resultado = json.dumps(analisadorLexico(programa), indent=2)
    teste = json.dumps(teste, indent=2)
    if resultado != teste:
        # Mostra o teste e o resultado lado a lado  
        resultadoLinhas = resultado.split('\n')
        testeLinhas = teste.split('\n')
        if len(resultadoLinhas) > len(testeLinhas):
            testeLinhas.extend(
                [' '] * (len(resultadoLinhas)-len(testeLinhas))
            )
        elif len(resultadoLinhas) < len(testeLinhas):
            resultadoLinhas.extend(
                [' '] * (len(testeLinhas)-len(resultadoLinhas))
            )
        linhasEmPares = enumerate(zip(testeLinhas, resultadoLinhas))
        maiorTextoNaLista = str(len(max(testeLinhas, key=len)))
        maiorIndice = str(len(str(len(testeLinhas))))
        titule = '{:<'+maiorIndice+'} + {:<'+maiorTextoNaLista+'} + {}'
        objeto = '{:<'+maiorIndice+'} | {:<'+maiorTextoNaLista+'} | {}'
        print(titule.format('', 'teste', 'resultado'))
        print(objeto.format('', '', ''))
        for indice, (esquerda, direita) in linhasEmPares:
            print(objeto.format(indice, esquerda, direita))
        # Termina a execucao
        print("\n): falha :(")
        quit()

# Programa que passdo para a funcao analisadorLexico
programa = """-- funcao inicial

inicio:Funcao(valor:Logica,item:Texto):Numero::{
}

tiposDeVariaveis:Funcao::{
  textoVar:Texto::'#'exemplo##'
  numeroVar:Numero::1234
  logicoVar:Logico::Sim
}

tiposDeFluxoDeControle:Funcao:Logico::{
  resultado:Logico::Nao

  se(1 = 2){
    resultado::Nao
  } se nao se('a' != 'a'){
    resultado::Nao
  } se nao @ {
    resultado::Sim
  }

  contador:Numero::0
  enquanto(contador < 10){
    contador::contador + 'a'
  }

  retorna resultado
}"""

# Resultado esperado da execucao da funcao analisadorLexico
# passando paea ela o programa anterior
teste = {
    "tokens":[
        # Comentario    
        {
            "grupo":"comentario", "texto": "-- funcao inicial", 
            "local":{"linha":1,"indice":0}
        },
        {
            "grupo":"quebra-linha", "texto": "\n", 
            "local":{"linha":1,"indice":17}
        },
        {
            "grupo":"quebra-linha", "texto": "\n", 
            "local":{"linha":2,"indice":0}
        },
        # Funcao inicio
        {
            "grupo":"identificador", "texto": "inicio", 
            "local":{"linha":3,"indice":0}
        },
        {
            "grupo":"dois-pontos", "texto": ":", 
            "local":{"linha":3,"indice":6}
        },
        {
            "grupo":"reservado", "texto": "Funcao", 
            "local":{"linha":3,"indice":7}
        },
        {
            "grupo":"abre-parenteses", "texto": "(", 
            "local":{"linha":3,"indice":13}
        },
        {
            "grupo":"identificador", "texto": "valor", 
            "local":{"linha":3,"indice":14}
        },
        {
            "grupo":"dois-pontos", "texto": ":", 
            "local":{"linha":3,"indice":19}
        },
        {
            "grupo":"reservado", "texto": "Logica", 
            "local":{"linha":3,"indice":20}
        },
        {
            "grupo":"virgula", "texto": ",", 
            "local":{"linha":3,"indice":26}
        },
        {
            "grupo":"identificador", "texto": "item", 
            "local":{"linha":3,"indice":27}
        },
        {
            "grupo":"dois-pontos", "texto": ":", 
            "local":{"linha":3,"indice":31}
        },
        {
            "grupo":"reservado", "texto": "Texto", 
            "local":{"linha":3,"indice":32}
        },
        {
            "grupo":"fecha-parenteses", "texto": ")", 
            "local":{"linha":3,"indice":37}
        },
        {
            "grupo":"dois-pontos", "texto": ":", 
            "local":{"linha":3,"indice":38}
        },
        {
            "grupo":"reservado", "texto": "Numero", 
            "local":{"linha":3,"indice":39}
        },
        {
            "grupo":"atribuicao", "texto": "::", 
            "local":{"linha":3,"indice":45}
        },
        {
            "grupo":"abre-chaves", "texto": "{", 
            "local":{"linha":3,"indice":47}
        },
        {
            "grupo":"quebra-linha", "texto": "\n", 
            "local":{"linha":3,"indice":48}
        },
        {
            "grupo":"fecha-chaves", "texto": "}", 
            "local":{"linha":4,"indice":0}
        },
        {
            "grupo":"quebra-linha", "texto": "\n", 
            "local":{"linha":4,"indice":1}
        },
        {
            "grupo":"quebra-linha", "texto": "\n", 
            "local":{"linha":5,"indice":0}
        },
        # Funcao tiposDeVariaveis
        {
            "grupo":"identificador", "texto": "tiposDeVariaveis", 
            "local":{"linha":6,"indice":0}
        },
        {
            "grupo":"dois-pontos", "texto": ":", 
            "local":{"linha":6,"indice":16}
        },
        {
            "grupo":"reservado", "texto": "Funcao", 
            "local":{"linha":6,"indice":17}
        },
        {
            "grupo":"atribuicao", "texto": "::", 
            "local":{"linha":6,"indice":23}
        },
        {
            "grupo":"abre-chaves", "texto": "{", 
            "local":{"linha":6,"indice":25}
        },
        {
            "grupo":"quebra-linha", "texto": "\n", 
            "local":{"linha":6,"indice":26}
        },
        # textoVar:Texto::'#'exemplo##'
        {
            "grupo":"identificador", "texto": "textoVar", 
            "local":{"linha":7,"indice":2}
        },
        {
            "grupo":"dois-pontos", "texto": ":", 
            "local":{"linha":7,"indice":10}
        },
        {
            "grupo":"reservado", "texto": "Texto", 
            "local":{"linha":7,"indice":11}
        },
        {
            "grupo":"atribuicao", "texto": "::", 
            "local":{"linha":7,"indice":16}
        },
        {
            "grupo":"texto", "texto": "'#'exemplo##'", 
            "local":{"linha":7,"indice":18}
        },
        {
            "grupo":"quebra-linha", "texto": "\n", 
            "local":{"linha":7,"indice":31}
        },
        # numeroVar:Numero::1234
        {
            "grupo":"identificador", "texto": "numeroVar", 
            "local":{"linha":8,"indice":2}
        },
        {
            "grupo":"dois-pontos", "texto": ":", 
            "local":{"linha":8,"indice":11}
        },
        {
            "grupo":"reservado", "texto": "Numero", 
            "local":{"linha":8,"indice":12}
        },
        {
            "grupo":"atribuicao", "texto": "::", 
            "local":{"linha":8,"indice":18}
        },
        {
            "grupo":"numero", "texto": "1234", 
            "local":{"linha":8,"indice":20}
        },
        {
            "grupo":"quebra-linha", "texto": "\n", 
            "local":{"linha":8,"indice":24}
        },
        # logicoVar:Logico::Sim
        {
            "grupo":"identificador", "texto": "logicoVar", 
            "local":{"linha":9,"indice":2}
        },
        {
            "grupo":"dois-pontos", "texto": ":", 
            "local":{"linha":9,"indice":11}
        },
        {
            "grupo":"reservado", "texto": "Logico", 
            "local":{"linha":9,"indice":12}
        },
        {
            "grupo":"atribuicao", "texto": "::", 
            "local":{"linha":9,"indice":18}
        },
        {
            "grupo":"logico", "texto": "Sim", 
            "local":{"linha":9,"indice":20}
        },
        {
            "grupo":"quebra-linha", "texto": "\n", 
            "local":{"linha":9,"indice":23}
        },
        # Fecha Funcao
        {
            "grupo":"fecha-chaves", "texto": "}", 
            "local":{"linha":10,"indice":0}
        },
        {
            "grupo":"quebra-linha", "texto": "\n", 
            "local":{"linha":10,"indice":1}
        },
        {
            "grupo":"quebra-linha", "texto": "\n", 
            "local":{"linha":11,"indice":0}
        },
        # Funcao tiposDeFluxoDeControle
        {
            "grupo":"identificador", "texto": "tiposDeFluxoDeControle", 
            "local":{"linha":12,"indice":0}
        },
        {
            "grupo":"dois-pontos", "texto": ":", 
            "local":{"linha":12,"indice":22}
        },
        {
            "grupo":"reservado", "texto": "Funcao", 
            "local":{"linha":12,"indice":23}
        },
        {
            "grupo":"dois-pontos", "texto": ":", 
            "local":{"linha":12,"indice":29}
        },
        {
            "grupo":"reservado", "texto": "Logico", 
            "local":{"linha":12,"indice":30}
        },
        {
            "grupo":"atribuicao", "texto": "::", 
            "local":{"linha":12,"indice":36}
        },
        {
            "grupo":"abre-chaves", "texto": "{", 
            "local":{"linha":12,"indice":38}
        },
        {
            "grupo":"quebra-linha", "texto": "\n", 
            "local":{"linha":12,"indice":39}
        },
        # resultado:Logico::Nao
        {
            "grupo":"identificador", "texto": "resultado", 
            "local":{"linha":13,"indice":2}
        },
        {
            "grupo":"dois-pontos", "texto": ":", 
            "local":{"linha":13,"indice":11}
        },
        {
            "grupo":"reservado", "texto": "Logico", 
            "local":{"linha":13,"indice":12}
        },
        {
            "grupo":"atribuicao", "texto": "::", 
            "local":{"linha":13,"indice":18}
        },
        {
            "grupo":"logico", "texto": "Nao", 
            "local":{"linha":13,"indice":20}
        },
        {
            "grupo":"quebra-linha", "texto": "\n", 
            "local":{"linha":13,"indice":23}
        },
        {
            "grupo":"quebra-linha", "texto": "\n", 
            "local":{"linha":14,"indice":0}
        },
        # se(1 = 2){
        {
            "grupo":"reservado", "texto": "se", 
            "local":{"linha":15,"indice":2}
        },
        {
            "grupo":"abre-parenteses", "texto": "(", 
            "local":{"linha":15,"indice":4}
        },
        {
            "grupo":"numero", "texto": "1", 
            "local":{"linha":15,"indice":5}
        },
        {
            "grupo":"operador-igual", "texto": "=", 
            "local":{"linha":15,"indice":7}
        },
        {
            "grupo":"numero", "texto": "2", 
            "local":{"linha":15,"indice":9}
        },
        {
            "grupo":"fecha-parenteses", "texto": ")", 
            "local":{"linha":15,"indice":10}
        },
        {
            "grupo":"abre-chaves", "texto": "{",
            "local":{"linha":15,"indice":11}
        },
        {
            "grupo":"quebra-linha", "texto": "\n", 
            "local":{"linha":15,"indice":12}
        },
        {
            "grupo":"identificador", "texto": "resultado", 
            "local":{"linha":16,"indice":4}
        },
        {
            "grupo":"atribuicao", "texto": "::", 
            "local":{"linha":16,"indice":13}
        },
        {
            "grupo":"logico", "texto": "Nao", 
            "local":{"linha":16,"indice":15}
        },
        {
            "grupo":"quebra-linha", "texto": "\n", 
            "local":{"linha":16,"indice":18}
        },
        # } se nao se('a' != 'a'){
        {
            "grupo":"fecha-chaves", "texto": "}",
            "local":{"linha":17,"indice":2}
        },
        {
            "grupo":"reservado", "texto": "se nao se", 
            "local":{"linha":17,"indice":4}
        },
        {
            "grupo":"abre-parenteses", "texto": "(", 
            "local":{"linha":17,"indice":13}
        },
        {
            "grupo":"texto", "texto": "'a'", 
            "local":{"linha":17,"indice":14}
        },
        {
            "grupo":"operador-diferente", "texto": "!=", 
            "local":{"linha":17,"indice":18}
        },
        {
            "grupo":"texto", "texto": "'a'", 
            "local":{"linha":17,"indice":21}
        },
        {
            "grupo":"fecha-parenteses", "texto": ")", 
            "local":{"linha":17,"indice":24}
        },
        {
            "grupo":"abre-chaves", "texto": "{",
            "local":{"linha":17,"indice":25}
        },
        {
            "grupo":"quebra-linha", "texto": "\n", 
            "local":{"linha":17,"indice":26}
        },
        {
            "grupo":"identificador", "texto": "resultado", 
            "local":{"linha":18,"indice":4}
        },
        {
            "grupo":"atribuicao", "texto": "::", 
            "local":{"linha":18,"indice":13}
        },
        {
            "grupo":"logico", "texto": "Nao", 
            "local":{"linha":18,"indice":15}
        },
        {
            "grupo":"quebra-linha", "texto": "\n", 
            "local":{"linha":18,"indice":18}
        },
        # } se nao @ {
        {
            "grupo":"fecha-chaves", "texto": "}",
            "local":{"linha":19,"indice":2}
        },
        {
            "grupo":"reservado", "texto": "se nao", 
            "local":{"linha":19,"indice":4}
        },
        {
            "grupo":"desconhecido", "texto": "@", 
            "local":{"linha":19,"indice":11}
        },
        {
            "grupo":"abre-chaves", "texto": "{",
            "local":{"linha":19,"indice":13}
        },
        {
            "grupo":"quebra-linha", "texto": "\n", 
            "local":{"linha":19,"indice":14}
        },
        {
            "grupo":"identificador", "texto": "resultado", 
            "local":{"linha":20,"indice":4}
        },
        {
            "grupo":"atribuicao", "texto": "::", 
            "local":{"linha":20,"indice":13}
        },
        {
            "grupo":"logico", "texto": "Sim", 
            "local":{"linha":20,"indice":15}
        },
        {
            "grupo":"quebra-linha", "texto": "\n", 
            "local":{"linha":20,"indice":18}
        },
        {
            "grupo":"fecha-chaves", "texto": "}", 
            "local":{"linha":21,"indice":2}
        },
        {
            "grupo":"quebra-linha", "texto": "\n", 
            "local":{"linha":21,"indice":3}
        },
        {
            "grupo":"quebra-linha", "texto": "\n", 
            "local":{"linha":22,"indice":0}
        },
        # contador:Numero::0
        {
            "grupo":"identificador", "texto": "contador", 
            "local":{"linha":23,"indice":2}
        },
        {
            "grupo":"dois-pontos", "texto": ":", 
            "local":{"linha":23,"indice":10}
        },
        {
            "grupo":"reservado", "texto": "Numero", 
            "local":{"linha":23,"indice":11}
        },
        {
            "grupo":"atribuicao", "texto": "::", 
            "local":{"linha":23,"indice":17}
        },
        {
            "grupo":"numero", "texto": "0", 
            "local":{"linha":23,"indice":19}
        },
        {
            "grupo":"quebra-linha", "texto": "\n", 
            "local":{"linha":23,"indice":20}
        },
        # enquanto(contador < 10){
        {
            "grupo":"reservado", "texto": "enquanto", 
            "local":{"linha":24,"indice":2}
        },
        {
            "grupo":"abre-parenteses", "texto": "(", 
            "local":{"linha":24,"indice":10}
        },
        {
            "grupo":"identificador", "texto": "contador", 
            "local":{"linha":24,"indice":11}
        },
        {
            "grupo":"operador-menor", "texto": "<", 
            "local":{"linha":24,"indice":20}
        },
        {
            "grupo":"numero", "texto": "10", 
            "local":{"linha":24,"indice":22}
        },
        {
            "grupo":"fecha-parenteses", "texto": ")", 
            "local":{"linha":24,"indice":24}
        },
        {
            "grupo":"abre-chaves", "texto": "{",
            "local":{"linha":24,"indice":25}
        },
        {
            "grupo":"quebra-linha", "texto": "\n", 
            "local":{"linha":24,"indice":26}
        },
        {
            "grupo":"identificador", "texto": "contador", 
            "local":{"linha":25,"indice":4}
        },
        {
            "grupo":"atribuicao", "texto": "::", 
            "local":{"linha":25,"indice":12}
        },
        {
            "grupo":"identificador", "texto": "contador", 
            "local":{"linha":25,"indice":14}
        },
        {
            "grupo":"operador-mais", "texto": "+", 
            "local":{"linha":25,"indice":23}
        },
        {
            "grupo":"texto", "texto": "'a'", 
            "local":{"linha":25,"indice":25}
        },
        {
            "grupo":"quebra-linha", "texto": "\n", 
            "local":{"linha":25,"indice":28}
        },
        {
            "grupo":"fecha-chaves", "texto": "}", 
            "local":{"linha":26,"indice":2}
        },
        {
            "grupo":"quebra-linha", "texto": "\n", 
            "local":{"linha":26,"indice":3}
        },
        {
            "grupo":"quebra-linha", "texto": "\n", 
            "local":{"linha":27,"indice":0}
        },
        # Fecha Funcao
        {
            "grupo":"reservado", "texto": "retorna", 
            "local":{"linha":28,"indice":2}
        },    
        {
            "grupo":"identificador", "texto": "resultado", 
            "local":{"linha":28,"indice":10}
        },
        {
            "grupo":"quebra-linha", "texto": "\n", 
            "local":{"linha":28,"indice":19}
        },
        {
            "grupo":"fecha-chaves", "texto": "}", 
            "local":{"linha":29,"indice":0}
        }
    ], "erros":[
        {
            "texto":"simbolo, @, desconhecido",
            "local":{"linha":19,"indice":11}
        }
    ]
}

# Execucao do teste que valida a funcao analisadorLexico
testaAnalisadorLexico(programa, teste)

print("(: sucesso :)")