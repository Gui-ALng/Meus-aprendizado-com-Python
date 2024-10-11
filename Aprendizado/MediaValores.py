qtd=0
soma=0
media=0
valor = float(input("Digite um valor: "))

while (valor > 0.0):
    soma = soma + valor
    qtd = qtd + 1
    # Entrada de valores
    valor = float(input("digite um valor: "))

#caso digite um valor negativo o laco encerra
media = soma / qtd
print("\n Total da soma: ",soma)
print("\n Quantidade de valores digitados: ",qtd)
print("\n Média dos valores: ",media)