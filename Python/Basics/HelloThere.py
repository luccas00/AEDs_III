
# Hello There.py
# This script demonstrates the basic syntax in Python.
# Author: Luccas Carneiro
# Date: 15/10/2025
# Version: 1.0

print("Hello there!")
print("General Kenobi!")    

text = "You are a bold one."
msg: str = "Kill him!"
is_alt = False

print(text)
print(msg)
print(is_alt)

number = 42
idade: int = 30
peso: float = 70.5

PI: float = 3.141592653589793
MAX: int = 100
NOME: str = "Luccas"

FLAG: bool = True
is_active: bool = False

print(number)
print(idade)
print(peso)
print(PI)
print(MAX)
print(NOME)
print(FLAG)
print(is_active)

print(type(text))
print(type(number))
print(type(peso))
print(type(FLAG))
print(type(NOME))
print(type(is_active))
print(type(idade))
print(type(msg))
print(type(is_alt))
print(type(PI))
print(type(MAX))

print("Nome: {nome} Idade: {idade} Peso: {peso}".format(nome=NOME, idade=idade, peso=peso))
print(f"Nome: {NOME} Idade: {idade} Peso: {peso}")
print("Nome: %s Idade: %d Peso: %.2f" % (NOME, idade, peso))
print("Nome:", NOME, "Idade:", idade, "Peso:", peso)

meuNome = input("Qual o seu nome? ")
print(f"Olá, {meuNome}!")

minhaIdade: int = int(input("Qual a sua idade? "))
print(f"Você tem {minhaIdade} anos.")

meuPeso: float = float(input("Qual o seu peso? "))
print(f"Você pesa {meuPeso} kg.")

soma = minhaIdade + idade
subtracao = idade - minhaIdade
multiplicacao = idade * minhaIdade
divisao = idade / minhaIdade
divisao_inteira = idade // minhaIdade
modulo = idade % minhaIdade
exponenciacao = idade ** minhaIdade

print(f"Soma: {soma}")
print(f"Subtração: {subtracao}")
print(f"Multiplicação: {multiplicacao}")
print(f"Divisão: {divisao}")
print(f"Divisão Inteira: {divisao_inteira}")
print(f"Módulo: {modulo}")
print(f"Exponenciação: {exponenciacao}")

idade += 1
print(f"Idade após incremento: {idade}")

idade -= 1
print(f"Idade após decremento: {idade}")

result = (idade > minhaIdade) and (peso < meuPeso)
print(f"Resultado da comparação: {result}")

if idade > minhaIdade:
    print("Você é mais velho que eu.")
elif idade < minhaIdade:
    print("Você é mais novo que eu.")
else:
    print("Temos a mesma idade.")
    
result2 = (peso > meuPeso) or (idade < minhaIdade)
print(f"Resultado da segunda comparação: {result2}")

print(idade is minhaIdade)
print(idade is not minhaIdade)

flag3 = True
print(flag3)
print(not flag3)

curso = "Python"
frutas = ["maçã", "banana", "laranja", "uva"]
saques = (100, 200, 300, 400)
keys = [1, 2, 3, 4]
values = ['um', 'dois', 'três', 'quatro']

print(curso)
print(frutas)
print(saques)
print(keys)
print(values)

print(type(curso))
print(type(frutas))
print(type(saques))
print(type(keys))
print(type(values))

print(curso[0])
print(frutas[1])
print(saques[2])
print(keys[3])
print(values[0])

print(curso[0:3])
print(frutas[1:3])
print(saques[0:2])
print(keys[2:])
print(values[:2])

print(len(curso))
print(len(frutas))
print(len(saques))
print(len(keys))
print(len(values))

print("banana" in frutas)
frutas.append("manga")
print(frutas)

print(keys)
print(1 in keys)
print(10 in keys)
print(5 not in keys)
keys.append(5)
print(keys)

print("Fim do programa.")

