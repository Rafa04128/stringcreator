"""Al tener al menos unas 20gb de txt files vamos a intentar re entrenar el modelo este es el lugar de testeo para,
codificar y decodificar las librerias de texto."""






# create mapping from characters to integers

stoi = {ch:i for i,ch in enumerate(chars) }
itos = { i:ch for i, ch in enumerate(chars) }
encode = lambda s: [stoi[c] for c in s]            # encoder: take a string, output a list of integers
decode = lambda l: ''.join([itos[i] for i in l])   # decoder: take a list of integers utput a string.

print(encode("Hi there"))
print(decode(encode("hi there")))