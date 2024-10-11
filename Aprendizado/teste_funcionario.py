from funcionario import Funcionario

funcionario = Funcionario('Matheus', 'matheus@blabla.com.br')

funcionario.cadastra_hora('Jan', 300)
funcionario.cadastra_hora('Fev', 200)
funcionario.cadastro_salario_hora('Jan', 30)
funcionario.cadastro_salario_hora('Fev', 30)
print(funcionario)
print(funcionario.calcula_salario('Jan'))
print(funcionario.calcula_salario('Fev'))