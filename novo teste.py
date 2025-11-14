nome = input("Digite seu Nome: ")
idade = int (input ("Digite a sua idade: "))

if idade >= 18 <= 39:
    print (f" Olá {nome}, você pode dirigir")
elif idade <= 17:
    print (f" Olá {nome}, você NÃO pode dirigir")
else:
    print (f" Olá {nome}, você precisa renovar")