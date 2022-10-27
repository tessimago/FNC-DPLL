

def addvar(variaveis):
    var = input("Variavel a adicionar: ").upper()
    while var in variaveis or len(var) != 1:
        if var in variaveis:
            print("Ja existe essa fariavel")
        if len(var) != 1:
            print("Variavel tem que ter 1 caracter")
        var = input("Variavel a adicionar: ").upper()
    variaveis.append(var)


def showopc():
    print("1: Criar variavel")
    print("2: Analize")
    print("3: Sair")


def verifyPrep(prepositionSplited, simbols, variaveiss):
    for p in prepositionSplited:
        if len(p) != 1 or (p not in simbols and p not in variaveiss):
            print("Erro em: " + p)
            return False
    return True


def changePrepImp(prepositionSplited, i):
    if prepositionSplited[i] == ">":
        prepositionSplited[i] = "v"
        count = 0
        for idx in range(i+1, len(prepositionSplited)):
            if prepositionSplited[idx] == '(':
                count += 1
            elif prepositionSplited[idx] == ')':
                count -= 1
            if count == 0 and prepositionSplited[idx] != "-":
                prepositionSplited.insert(idx+1, ")")
                break
        count = 0
        for idx in range(i-1, -1, -1):
            if prepositionSplited[idx] == ')':
                count += 1
            elif prepositionSplited[idx] == '(':
                count -= 1
            if count == 0 and prepositionSplited[idx-1] != '-':
                prepositionSplited.insert(idx, "-")
                prepositionSplited.insert(idx, "(")
                break
    else:
        prepositionSplited[i] = "v"
        prepositionSplited.insert(i+1, "-")
        count = 0
        for idx in range(i + 1, len(prepositionSplited)):
            if prepositionSplited[idx] == '(':
                count += 1
            elif prepositionSplited[idx] == ')':
                count -= 1
            if count == 0 and prepositionSplited[idx] != "-":
                prepositionSplited.insert(idx + 1, ")")
                break
        count = 0
        for idx in range(i - 1, -1, -1):
            if prepositionSplited[idx] == ')':
                count += 1
            elif prepositionSplited[idx] == '(':
                count -= 1
            if count == 0 and prepositionSplited[idx-1] != "-":
                prepositionSplited.insert(idx, "(")
                break
    count = 0
    idx = 0
    while idx < len(prepositionSplited):
        if prepositionSplited[idx] == "-":
            count += 1
        else:
            count = 0
        if count == 2:
            prepositionSplited.pop(idx)
            prepositionSplited.pop(idx-1)
            idx -= 2
        idx += 1


def transformImp(prepositionSplited):
    done = False
    while not done:
        done = True
        for i in range(len(prepositionSplited)):
            if prepositionSplited[i] == ">" or prepositionSplited[i] == "<":
                done = False
                changePrepImp(prepositionSplited, i)
                print("Implicacao:\t", end="")
                showList(prepositionSplited)
                cleanP(prepositionSplited)
                break


def changePrepEq(prepositionSplited, i):
    # A = B    >>>     (A > B) ^ (B < A)
    prepositionSplited[i] = "^"

    # Get A and B
    count = 0
    A = []
    for idx in range(i - 1, -1, -1):
        if prepositionSplited[idx] == ")":
            count += 1
        elif prepositionSplited[idx] == "(":
            count -= 1
        A.append(prepositionSplited[idx])
        if count == 0 and prepositionSplited[idx - 1] != "-":
            break

    count = 0
    B = []
    for idx in range(i + 1, len(prepositionSplited)):
        if prepositionSplited[idx] == "(":
            count += 1
        elif prepositionSplited[idx] == ")":
            count -= 1
        B.append(prepositionSplited[idx])
        if count == 0 and prepositionSplited[idx] != "-":
            break
    B.reverse()

    prepositionSplited.insert(i+1, "(")

    count = 0
    for idx in range(i + 2, len(prepositionSplited)):
        if prepositionSplited[idx] == '(':
            count += 1
        elif prepositionSplited[idx] == ')':
            count -= 1
        if count == 0 and prepositionSplited[idx] != "-":
            A.append(">")
            A.reverse()
            addList(prepositionSplited, A, idx+1)
            prepositionSplited.insert(idx + 1 + len(A), ")")
            # showList(prepositionSplited)
            break
    count = 0
    prepositionSplited.insert(i, ")")
    for idx in range(i - 1, -1, -1):
        if prepositionSplited[idx] == ')':
            count += 1
        elif prepositionSplited[idx] == '(':
            count -= 1
        if count == 0 and prepositionSplited[idx - 1] != '-':
            B.reverse()
            B.append("<")
            addList(prepositionSplited, B, idx)
            prepositionSplited.insert(idx, "(")
            # showList(prepositionSplited)
            break


def addList(list1, list2, idx):
    list2.reverse()
    for el in list2:
        list1.insert(idx, el)


def transformEq(prepositionSplited):
    done = False
    while not done:
        done = True
        for i in range(len(prepositionSplited)):
            if prepositionSplited[i] == "=":
                done = False
                changePrepEq(prepositionSplited, i)
                print("Equivalencia:\t", end="")
                showList(prepositionSplited)
                cleanP(prepositionSplited)

                break


def cleanP(prepositionSplited):

    # achar 2 ( seguidos abertos, comeca um count normal... se count for 0, sempre que
    # achares um ) ve se tem outro seguido a frente, se tiver BORA, se nao, reseta os 2 ( seguidos
    idx = 0

    openSeguido = False
    count = 0
    idxFirst = -1
    while idx < len(prepositionSplited) - 1:

        if prepositionSplited[idx] == "(" and prepositionSplited[idx + 1] == "(":
            openSeguido = True

            idx += 1
            while prepositionSplited[idx + 1] == "(":
                idx += 1
            idxFirst = idx
            count = 0
            idx += 1
            continue
        elif openSeguido and prepositionSplited[idx] == "(":
            count += 1

        if openSeguido and count == 0 and prepositionSplited[idx] == ")" and prepositionSplited[idx + 1] == ")":
            prepositionSplited.pop(idx)
            prepositionSplited.pop(idxFirst)
            idx = 0
            openSeguido = False
            print("Clean:\t\t\t", end="")
            showList(prepositionSplited)
        elif openSeguido and count == 0 and prepositionSplited[idx] == ")":
            openSeguido = False
        elif openSeguido and count != 0 and prepositionSplited[idx] == ")":
            count -= 1
        idx += 1

    count = 0
    idx = 0
    cleaned = False
    while idx < len(prepositionSplited):
        if prepositionSplited[idx] == "-":
            count += 1
        else:
            count = 0
        if count == 2:
            cleaned = True
            prepositionSplited.pop(idx)
            prepositionSplited.pop(idx - 1)
            idx -= 2
        idx += 1
    if cleaned:
        print("Clean neg:\t", end="")
        showList(prepositionSplited)


def changePrepMorgan(prepositionSplited, i):
    # Mandar o "-" embora
    prepositionSplited.pop(i)
    # Comecar a pesquisa pelo que vem depois do (
    idx = i + 1

    # Meter um "-" la dentro
    prepositionSplited.insert(idx, "-")
    # Exemplos: - ( A v B )    |     - ( ( A v B ) v B )      |   - ( - ( A v B ) v B )
    count = 0

    while idx < len(prepositionSplited):
        if prepositionSplited[idx] == "(":
            count += 1
        elif prepositionSplited[idx] == ")":
            count -= 1

        if count == 0 and prepositionSplited[idx] != "-":
            break
        idx += 1
    idx += 1
    if prepositionSplited[idx] == "^":
        prepositionSplited[idx] = "v"
    elif prepositionSplited[idx] == "v":
        prepositionSplited[idx] = "^"
    prepositionSplited.insert(idx+1, "-")


def transformMorgan(prepositionSplited):
    done = False
    while not done:
        done = True
        for i in range(len(prepositionSplited)):
            if prepositionSplited[i] == "-":
                if prepositionSplited[i+1] == "(":
                    print("Before Leis Morgan:\t", end="")
                    showList(prepositionSplited)
                    done = False
                    changePrepMorgan(prepositionSplited, i)
                    print("Leis Morgan:\t", end="")
                    showList(prepositionSplited)
                    cleanP(prepositionSplited)

                    break


def changePrepDist(prepositionSplited, i, direcao):
    # A v ( B ^ C ) = ( A v B ) ^ ( A v C )
    # |    ( A ^ B ) v C  =  ( A v C ) ^ ( B v C )
    # |    ( A ^ B ) v ( C ^ D ) = ( A v ( C ^ D ) ) ^ ( B v ( C ^ D ) )

    if direcao == "direita":
        idxInicial = i - 1

        # listas de caracteres A, B e C
        A = []

        idx = idxInicial
        count = 0
        while idx >= 0:
            if prepositionSplited[idx] == ")":
                count += 1
            elif prepositionSplited[idx] == "(":
                count -= 1
            A.append(prepositionSplited[idx])
            if count == 0:
                if prepositionSplited[idx - 1] == "-":
                    idx -= 1
                    A.append("-")
                break
            idx -= 1
        idxInicial = idx
        A.reverse()
        # print("A: ", A)
        B = []
        C = []
        idx = i + 2
        count = 0
        while not (count == 0 and prepositionSplited[idx] == "^"):
            if prepositionSplited[idx] == "(":
                count += 1
            elif prepositionSplited[idx] == ")":
                count -= 1
            B.append(prepositionSplited[idx])
            idx += 1
        idx += 1
        while idx < len(prepositionSplited):
            if prepositionSplited[idx] == "(":
                count += 1
            elif prepositionSplited[idx] == ")":
                count -= 1
                if count == -1:
                    break
            C.append(prepositionSplited[idx])
            idx += 1

        idxFinal = idx
        # print("B: ", B)
        # print("C: ", C)
        # Juntar da maneira correta numa nova lista

        rightWay = ["("]
        addList(rightWay, A, len(rightWay))
        rightWay.append("v")
        addList(rightWay, B, len(rightWay))
        rightWay.append(")")
        rightWay.append("^")
        rightWay.append("(")
        A.reverse()
        addList(rightWay, A, len(rightWay))
        rightWay.append("v")
        addList(rightWay, C, len(rightWay))
        rightWay.append(")")
        # print("rightway: ",rightWay)
        # recriar a lista mas quando chegar num certo idxInicial, mete a nova lista, e segue pela idx final

        newList = []
        idx = 0

        while idx < len(prepositionSplited):
            if idx == idxInicial:
                addList(newList, rightWay, idx)
                idx = idxFinal+1
                continue
            newList.append(prepositionSplited[idx])
            idx += 1
        prepositionSplited.clear()
        addList(prepositionSplited, newList, 0)

    elif direcao == "esquerda":
        idxFinal = i + 1

        # listas de caracteres A, B e C
        A = []
        if prepositionSplited[i + 1] == "-":
            idxFinal = i + 2
            A.append("-")

        idx = idxFinal
        count = 0
        while idx < len(prepositionSplited):
            if prepositionSplited[idx] == "(":
                count += 1
            elif prepositionSplited[idx] == ")":
                count -= 1
            A.append(prepositionSplited[idx])
            if count == 0:
                break
            idx += 1
        idxFinal = idx

        # print("A: ", A)
        B = []
        C = []
        idx = i - 2
        count = 0
        while not (count == 0 and prepositionSplited[idx] == "^"):
            if prepositionSplited[idx] == ")":
                count += 1
            elif prepositionSplited[idx] == "(":
                count -= 1
            B.append(prepositionSplited[idx])
            idx -= 1
        # reverse porque a pesquisa foi feita para tras
        B.reverse()
        idx -= 1
        while idx >= 0:
            if prepositionSplited[idx] == ")":
                count += 1
            elif prepositionSplited[idx] == "(":
                count -= 1
                if count == -1:
                    break
            C.append(prepositionSplited[idx])
            idx -= 1
        # reverse porque a pesquisa foi feita para tras
        C.reverse()
        idxInicial = idx
        # print("B: ", B)
        # print("C: ", C)
        # Juntar da maneira correta numa nova lista

        rightWay = ["("]
        addList(rightWay, A, len(rightWay))
        rightWay.append("v")
        addList(rightWay, B, len(rightWay))
        rightWay.append(")")
        rightWay.append("^")
        rightWay.append("(")
        A.reverse()
        addList(rightWay, A, len(rightWay))
        rightWay.append("v")
        addList(rightWay, C, len(rightWay))
        rightWay.append(")")
        # print("rightway: ", rightWay)
        # recriar a lista mas quando chegar num certo idxInicial, mete a nova lista, e segue pela idx final

        newList = []
        idx = 0

        while idx < len(prepositionSplited):
            if idx == idxInicial:
                addList(newList, rightWay, idx)
                idx = idxFinal + 1
                continue
            newList.append(prepositionSplited[idx])
            idx += 1
        prepositionSplited.clear()
        addList(prepositionSplited, newList, 0)
    elif direcao == "both":

        A = []
        B = []
        idx = i - 2
        count = 0
        while not (count == 0 and prepositionSplited[idx] == "^"):
            if prepositionSplited[idx] == ")":
                count += 1
            elif prepositionSplited[idx] == "(":
                count -= 1
            A.append(prepositionSplited[idx])
            idx -= 1
        # reverse porque a pesquisa foi feita para tras
        A.reverse()
        idx -= 1
        while idx >= 0:
            if prepositionSplited[idx] == ")":
                count += 1
            elif prepositionSplited[idx] == "(":
                count -= 1
                if count == -1:
                    break
            B.append(prepositionSplited[idx])
            idx -= 1
        # reverse porque a pesquisa foi feita para tras
        B.reverse()
        idxInicial = idx

        # print("A: ", A)
        # print("B: ", B)

        C = ["("]

        idx = i + 2
        count = 0
        while idx < len(prepositionSplited):
            if prepositionSplited[idx] == "(":
                count += 1
            elif prepositionSplited[idx] == ")":
                count -= 1
            if count == -1:
                break
            C.append(prepositionSplited[idx])
            idx += 1
        C.append(")")
        idx += 1

        # print("C: ", C)

        idxFinal = idx

        # Juntar da maneira correta numa nova lista

        rightWay = ["("]
        addList(rightWay, A, len(rightWay))
        rightWay.append("v")
        addList(rightWay, C, len(rightWay))
        C.reverse()
        rightWay.append(")")
        rightWay.append("^")
        rightWay.append("(")
        addList(rightWay, B, len(rightWay))
        rightWay.append("v")
        addList(rightWay, C, len(rightWay))
        rightWay.append(")")
        # print("Rightway: ", rightWay)
        # recriar a lista mas quando chegar num certo idxInicial, mete a nova lista, e segue pela idx final

        newList = []
        idx = 0

        while idx < len(prepositionSplited):
            if idx == idxInicial:
                addList(newList, rightWay, idx)
                idx = idxFinal
                continue
            newList.append(prepositionSplited[idx])
            idx += 1
        prepositionSplited.clear()
        addList(prepositionSplited, newList, 0)


def verifyAND(prepositionSplited, i, sentido):
    if sentido == "direita":
        idx = i + 2
        count = 0
        while idx < len(prepositionSplited):
            if count == -1:
                break
            if prepositionSplited[idx] == "(":
                count += 1
            elif prepositionSplited[idx] == ")":
                count -= 1
            if count == 0 and prepositionSplited[idx] == "^":
                return True
            idx += 1
        return False
    else:
        idx = i - 2
        count = 0
        while idx > 0:
            if count == -1:
                break
            if prepositionSplited[idx] == ")":
                count += 1
            elif prepositionSplited[idx] == "(":
                count -= 1
            if count == 0 and prepositionSplited[idx] == "^":
                return True
            idx -= 1
        return False


def transformDist(prepositionSplited):
    done = False
    while not done:
        done = True
        for i in range(len(prepositionSplited)):
            if prepositionSplited[i] == "v":
                direita = verifyAND(prepositionSplited, i, "direita")
                esq = verifyAND(prepositionSplited, i, "esquerda")

                if (prepositionSplited[i + 1] == "(" and direita) and (prepositionSplited[i - 1] == ")" and esq):
                    done = False
                    changePrepDist(prepositionSplited, i, "both")
                    #cleanSimplify(prepositionSplited)
                    print("Distributiva both:\t", end="")
                    showList(prepositionSplited)
                    cleanP(prepositionSplited)

                    break
                elif prepositionSplited[i + 1] == "(" and direita:
                    done = False
                    changePrepDist(prepositionSplited, i, "direita")
                    print("Distributiva dire:\t", end="")
                    showList(prepositionSplited)
                    cleanP(prepositionSplited)

                    break
                elif prepositionSplited[i - 1] == ")" and esq:
                    done = False
                    changePrepDist(prepositionSplited, i, "esquerda")
                    print("Distributiva esqu:\t", end="")
                    showList(prepositionSplited)
                    cleanP(prepositionSplited)

                    break


def cleanHack(prepositionSplited):
    tmp = ["("]
    for idxc in range(len(prepositionSplited)):
        c = prepositionSplited[idxc]
        if c == "^":
            tmp.append(")")
            tmp.append("^")
            tmp.append("(")
            continue
        if c != "(" and c != ")":
            tmp.append(c)
    tmp.append(")")
    prepositionSplited.clear()
    addList(prepositionSplited, tmp, 0)


def findVariaveis(prepositionSplited, simbolos):
    variaveis = []
    for c in prepositionSplited:
        if c not in simbolos:
            if c not in variaveis:
                variaveis.append(c)
    return variaveis


def hasComplementar(var, clausula):
    if len(var) == 1:
        for idx in range(len(clausula)):
            if clausula[idx] == var:
                if clausula[idx - 1] == "-":
                    return True
    else:
        for idx in range(len(clausula)):
            if clausula[idx] == var[1] and clausula[idx - 1] != "-":
               return True



def cleanSomeMore(preposicao, variaveis):
    # Clausulas nao duplicadas
    pedacos = []
    pedaco = []
    add = True
    for idx in range(len(preposicao)):
        c = preposicao[idx]
        if c != "^":
            if c in variaveis:
                if preposicao[idx - 1] == "-":
                    if hasComplementar("-"+c,pedaco):
                        #print("-",c," tem complementar em ",pedaco)
                        add = False
                else:
                    if hasComplementar(c,pedaco):
                        #print(c," tem complementar em ",pedaco)
                        add = False

            pedaco.append(c)
        else:
            #print("Adicionar ", pedaco, " ? ",add)
            if pedaco not in pedacos and add and not ("1" in pedaco):
                pedacos.append(pedaco)
            add = True
            pedaco = []
    if pedaco not in pedacos and add and not ("1" in pedaco):
        pedacos.append(pedaco)

    newPrep = []
    for p in pedacos:
        for c in p:
            newPrep.append(c)
        newPrep.append("^")
    if len(newPrep) > 0:
        newPrep.pop(len(newPrep)-1)
    preposicao.clear()
    addList(preposicao, newPrep, 0)


def getParcela(prepositionSplited, idxc, dire):
    parcela = []
    if dire == 0:
        idxInicial = idxc - 1
        i = idxc - 1
        count = 0
        while i >= 0:
            if prepositionSplited[i] == ")":
                count += 1
            elif prepositionSplited[i] == "(":
                count -= 1
            parcela.append(prepositionSplited[i])
            if count == 0:
                if prepositionSplited[i-1] == "-":
                    i -= 1
                    parcela.append("-")
                break
            i -= 1
        idxInicial = i
        parcela.reverse()
        return parcela, idxInicial
    else:
        idxFinal = idxc + 1
        i = idxc + 1
        if prepositionSplited[i] == "-":
            parcela.append("-")
            i += 1

        count = 0
        while i < len(prepositionSplited):
            if prepositionSplited[i] == "(":
                count += 1
            elif prepositionSplited[i] == ")":
                count -= 1
            parcela.append(prepositionSplited[i])
            if count == 0:
                break
            i += 1
        idxFinal = i
        return parcela, idxFinal

def redoList(prepositionSplited,idxInicial,idxFinal,A):
    idx = 0
    tmp = []
    while idx < len(prepositionSplited):
        if idx == idxInicial:
            addList(tmp, A, idx)
            idx = idxFinal + 1
            continue
        tmp.append(prepositionSplited[idx])
        idx += 1
    prepositionSplited.clear()
    addList(prepositionSplited,tmp,0)

def isComplementar(A,B):
    Acopy = A.copy()
    Bcopy = B.copy()
    Acopy.pop(0)
    #print(Acopy)
    #print(Bcopy)
    if Acopy == Bcopy:
        return True
    Acopy = A.copy()
    Bcopy.pop(0)
    #print("----")
    #print(Acopy)
    #print(Bcopy)
    if Acopy == Bcopy:
        return True
    return False

def cleanSimplify(prepositionSplited):
    # A v A = A  |  A v - A = 1  |  A ^ A = A  |  A ^ - A = 0



    idxInicial = 0
    idxFinal = 0
    idxc = 0
    while idxc < len(prepositionSplited):
        c = prepositionSplited[idxc]
        if c == "v":
            A, idxInicial = getParcela(prepositionSplited, idxc, 0)
            B, idxFinal = getParcela(prepositionSplited, idxc, 1)
            #print("A: ", A)
            #print("B: ", B)
            if A == B:
                redoList(prepositionSplited,idxInicial,idxFinal,A)
                idxc = 0
            if isComplementar(A,B):
                redoList(prepositionSplited, idxInicial, idxFinal, ["1"])
                idxc = 0

        idxc += 1

def analize(variaveis):
    simbols = ['(', ')', 'v', '^', '>', '<', '=', '-']
    print("Simbolos aceites: ", simbols)

    preposition = input("Preposicao: ")
    prepositionSplited = preposition.split(" ")

    if len(variaveis) == 0:
        variaveis = findVariaveis(prepositionSplited, simbols)
        print("Variaveis encontradas: ", variaveis)

    print("Inicial:\t", end="")
    showList(prepositionSplited)
    if not verifyPrep(prepositionSplited, simbols, variaveis):
        print("Ocorreu um erro...")
        return


    # transformar = para > e <
    transformEq(prepositionSplited)
    # transformar > e < nas conjuncoes
    transformImp(prepositionSplited)
    before = []
    while before != prepositionSplited:
        before = prepositionSplited.copy()
        # leis de morgan
        transformMorgan(prepositionSplited)
        # Aplicar a distributiva (V sobre ^)
        transformDist(prepositionSplited)

    # tentar tirar alguns parenteses a mais
    cleanP(prepositionSplited)
    #cleanSimplify(prepositionSplited)
    print("Final:\t",  end="")
    showList(prepositionSplited)

    cleanHack(prepositionSplited)
    cleanSomeMore(prepositionSplited, variaveis)
    print("Simplificacao:\t", end="")
    showList(prepositionSplited)

    print("=======================")

    # Depois fazer isto num comando a parte
    if len(prepositionSplited) > 0:
        satisfazivel, var_value = valorDeVerdade(prepositionSplited, variaveis)
        print("Satisfazivel: ", satisfazivel)
        if satisfazivel:
            print(var_value)
    else:
        print("Satisfazivel: Always")


def showList(lista):
    string = ""
    for s in lista:
        if s == "v":
            realS = " ∨ "
        elif s == "^":
            realS = " ∧ "
        elif s == ">":
            realS = " → "
        elif s == "<":
            realS = " ← "
        elif s == "=":
            realS = " ↔ "
        elif s == "-":
            realS = " ¬ "
        else:
            realS = s

        string += realS
    print(string)

def valorDeVerdade(preposicao, variavieis):
    # Clausulas
    pedacos = []
    pedaco = []
    for c in preposicao:
        if c != "^":
            pedaco.append(c)
        else:
            pedacos.append(pedaco)
            pedaco = []
    pedacos.append(pedaco)

    # Verificar veracidade de cada pedaco
    # Criar o dicionario
    var_valor = {}
    for v in variavieis:
        var_valor.setdefault(v, None)  # Acrescentar um undefined / Null como terceiro tipo...?
    return DPLL(pedacos, variavieis, var_valor, variavieis)


def everyClausTrue(pedacos, variaveis_originais, var_valor):
    for p in pedacos:
        valorPedaco = False
        for idxc in range(len(p)):
            if p[idxc] in variaveis_originais:
                if p[idxc - 1] != "-":
                    valorPedaco = valorPedaco or var_valor.get(p[idxc])
                else:
                    valorPedaco = valorPedaco or not var_valor.get(p[idxc])
                if valorPedaco == True:
                    break
        if valorPedaco == False:
            return False
    return True


def find_pure(variaveis, clausulas, var_value):
    accepted = []
    rejected = []
    for p in clausulas:
        for idxc in range(len(p)):
            c = p[idxc]
            if c in variaveis:

                # print("Accpted: ", accepted)
                # print("Rejected: ", rejected)
                # print("Looking for: ", c, " em ", p)

                if var_value.get(c) != None:
                    continue
                if p[idxc-1] == "-":  # Se for negativo
                    if c in accepted:  # Vemos se o positivo ta la nos aceitos
                        accepted.remove(c)
                        rejected.append(c)
                        continue
                    if c not in rejected:
                        tmp = "-"+c
                        if tmp not in accepted:
                            accepted.append(tmp)
                else:
                    tmp = "-" + c
                    if tmp in accepted:
                        accepted.remove(tmp)
                        rejected.append(c)
                        continue
                    if c not in rejected:
                        if c not in accepted:
                            accepted.append(c)
    # print("Accpted: ", accepted)
    # print("Rejected: ", rejected)
    # Se houver... retornar tupla... blablabla
    if len(accepted) > 0:
        if len(accepted[0]) > 1: # ser negativo
            return accepted[0][1], False
        else:
            return accepted[0], True
    else:
        return None, None


def find_unit(variaveis, clausulas, var_value):
    candidates = []
    for p in clausulas:
        varis = []
        for idxc in range(len(p)):
            if p[idxc] in variaveis:
                if p[idxc - 1] == "-":
                    varis.append((p[idxc],False))
                else:
                    varis.append((p[idxc],True))
        if len(varis) == 1:
            candidates.append(varis[0])

    if len(candidates) > 0:
        return candidates[0]
    return None, None


def getNewClausulas(clausulasOrig, var_value, variaveis):
    tmp = []
    for p in clausulasOrig:
        add = True
        for idxc in range(len(p)):
            if p[idxc] in variaveis and var_value.get(p[idxc]) != None:
                if p[idxc - 1] == "-":
                    if not var_value.get(p[idxc]):
                        add = False
                        break
                else:
                    if var_value.get(p[idxc]):
                        add = False
                        break
        if add:
            tmp.append(p)
    return tmp


def DPLL(clausulasOrig, variaveisOrig, var_valueOrig, variaveis_originais):
    var_value = var_valueOrig.copy()
    #print("Para novas clausulas: ", var_value)
    clausulas = getNewClausulas(clausulasOrig, var_value, variaveis_originais)
    #print(var_value)
    variaveis = variaveisOrig.copy()
    if not some_var_value_null(var_value):
        return everyClausTrue(clausulas, variaveis_originais, var_value), var_value
    var, value = find_pure(variaveis, clausulas, var_value)
    if var != None:
        var_value.update({var: value})
        if value:
            print("Puro: ", var)
        else:
            print("Puro: ¬", var)
        variaveis.remove(var)
        return DPLL(clausulas, variaveis, var_value, variaveis_originais)
    var, value = find_unit(variaveis, clausulas, var_value)
    if var != None:
        var_value.update({var: value})
        if value:
            print("Unit: ", var)
        else:
            print("Unit: ¬", var)
        variaveis.remove(var)
        return DPLL(clausulas, variaveis, var_value, variaveis_originais)
    var = variaveis[0]  # Se nao houver variaveis entao todas teem valor, logo acaba la em cima
    variaveis.remove(var)
    var_value.update({var: True})
    print("Split: ", var, " : True", " : ", var_value)

    tmp, tmp_var_value = DPLL(clausulas, variaveis, var_value, variaveis_originais)
    if not tmp:
        var_value.update({var: False})
        print("Split: ", var, " : False", " : ", var_value)
        return DPLL(clausulas, variaveis, var_value, variaveis_originais)

    return tmp, tmp_var_value


def some_var_value_null(var_value):
    for v in var_value.values():
        if v == None:
            return True
    return False


def menu():

    variaveis = []
    while True:
        print("============")
        print("Variaveis: ", variaveis)
        showopc()
        cmd = input(">> ")
        if cmd == "1":
            addvar(variaveis)
        elif cmd == "2":
            analize(variaveis)
        elif cmd == "3":
            break
        else:
            print("Comando invalido.")


menu()
