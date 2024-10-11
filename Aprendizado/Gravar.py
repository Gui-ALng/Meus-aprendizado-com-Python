arquivo = open('arqText.txt', 'w')

arquivo.write('Curtos Python \n')
arquivo.write('Aula Pratica')
arquivo.close()

#Leitura do arquivo texto

leitura=open('arqText.txt','r')
print(leitura.read())
leitura.close()