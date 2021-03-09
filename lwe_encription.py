import random
import math
import binascii

# -------------------------------- Parâmetros -------------------------------- #
# Este será o tamanho dos vetores criptográficos
nvals = 20

B = []
e = []
# Valor secreto s
s = 20
# Parâmetro q (matrizes e vetores serão mod q)
q = 97

# ------------------------------ Função cifragem ----------------------------- #

def encrypt(public_key, message):
    # Nossa chave pública é composta de dois vetores
    A = public_key[0]
    B = public_key[1]

    # Multiplicando por 7 pois cada caracter ascii é 7 bits, 
    # e (u,v) cifra apenas um bit
    
    u = [0] * len(message)
    v = [0] * len(message)
    
    for i in range(len(message)):
        u[i] = [0]* 7
        v[i] = [0]* 7
            
    for i in range(len(message)):
        for j in range(7):
            # Recolhendo amostras de valores aleatórios para usar como índice
            # Para cada bit da mensagem, devemos realizar a amostragem    
            sample = random.sample(range(nvals-1), nvals//4)

            
            for x in range(0,len(sample)):
                u[i][j] = u[i][j] + A[sample[x]]
                v[i][j] = v[i][j] + B[sample[x]]

            v[i][j] = v[i][j] + math.floor(q/2) * int(message[i][j])
            v[i][j] = v[i][j] % q
            u[i][j] = u[i][j] % q
        
    # (u,v) é o nosso texto cifrado
    return u,v


# ----------------------------- Função Decifragem ---------------------------- #

def decrypt(secret_key, ciphertext):
    u = ciphertext[0]
    v = ciphertext[1]
    
    dec = [0] * len(u)
    ret = [0] * len(u)
    
    for i in range(len(u)):
        dec[i] = [0] * 7
        ret[i] = [0] * 7

    for i in range(len(u)):
        for j in range(7):
            dec[i][j] = (v[i][j] - s*u[i][j]) % q
            if (dec[i][j] > q/2):
                ret[i][j] = '1'
            else:
                ret[i][j] = '0'
        ret[i] = ''.join(ret[i])

    ret = '0b'+ ''.join(ret)
    return ret
    # return int(ret, 2)

A = random.sample(range(q), nvals)

for x in range(0,len(A)):
	e.append(random.randint(1,4))
	B.append((A[x]*s+e[x])%q)


# ----------------------------- Input de usuário ----------------------------- #

public_key = (A,B)

text_bin = []
text = str(input("Digite a mensagem a ser cifrada: "))
text_bytes = text.encode('ascii')

for i in range(len(text_bytes)):
    a = bin(text_bytes[i])
    text_bin.append(a[2:])

# --------------------------- Cifragem / Decifragem -------------------------- #

ciphertext = encrypt(public_key, text_bin)
response = decrypt(s, ciphertext)

# ---------------------------------- Prints ---------------------------------- #

print(f'''Chave pública A:
{A}

Vetor de erros e:
{e}

Chave secreta:
{s}

Chave pública B:
{B}

Texto cifrado:
u: {ciphertext[0]}
v: {ciphertext[1]}

Texto decifrado (binário): {response[2:]}
''')
