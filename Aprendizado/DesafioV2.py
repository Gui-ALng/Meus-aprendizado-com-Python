import pandas as pd
import numpy as np
import tensorflow as tf


# Função para criar o DataFrame com os dados fornecidos
def criar_dataframe():
    data = {
        'Aparelho': [
            'ABRIDOR/AFIADOR', 'AFIADOR DE FACAS', 'APARELHO DE SOM 3 EM 1', 'APARELHO DE SOM PEQUENO',
            'AQUECEDOR DE AMBIENTE', 'AQUECEDOR DE MAMADEIRA', 'AR-CONDICIONADO 7.500 BTU',
            'AR-CONDICIONADO 10.000 BTU', 'AR-CONDICIONADO 12.000 BTU', 'AR-CONDICIONADO 15.000 BTU',
            'AR-CONDICIONADO 18.000 BTU', 'ASPIRADOR DE PÓ', 'BARBEADOR/DEPILADOR/MASSAGEADOR', 'BATEDEIRA',
            'CHUVEIRO ELÉTRICO', 'COMPUTADOR/IMPRESSORA/ESTABILIZADOR', 'FERRO ELÉTRICO AUTOMÁTICO',
            'FORNO MICROONDAS', 'FREEZER VERTICAL/HORIZONTAL', 'GELADEIRA 1 PORTA', 'GELADEIRA 2 PORTAS',
            'LÂMPADA FLUORESCENTE COMPACTA - 15 W', 'LAVADORA DE ROUPAS', 'LIQUIDIFICADOR', 'SECADOR DE CABELO GRANDE',
            'TV EM CORES - 29"', 'VENTILADOR DE TETO'
        ],
        'Potencia': [
            135, 20, 80, 20, 1550, 100, 1000, 1350, 1450, 2000, 2100, 100, 10, 120, 3500, 180, 1000, 1200, 130, 90,
            130, 15, 500, 300, 1400, 110, 120
        ],
        'Dias_Uso': [
            10, 5, 20, 30, 15, 30, 30, 30, 30, 30, 30, 30, 30, 8, 30, 30, 12, 30, 30, 30, 30, 30, 12, 15, 30, 30, 30
        ],
        'Tempo_Uso': [
            5 / 60, 30 / 60, 3, 4, 8, 15 / 60, 8, 8, 8, 8, 8, 20 / 60, 30 / 60, 30 / 60, 40 / 60, 3, 1, 20 / 60, 24, 24,
            24, 5, 1,
            15 / 60, 10 / 60, 5, 8
        ],
        'Consumo_Mensal': [
            0.11, 0.05, 4.8, 2.4, 186.0, 0.75, 120, 162, 174, 240, 252, 10.0, 0.15, 0.48, 70.0, 16.2, 12.0, 12.0, 50,
            30, 55, 2.2, 6.0, 1.1, 7.0, 16.5, 28.8
        ]
    }
    return pd.DataFrame(data)


# Função para perguntar quais aparelhos o usuário possui
def selecionar_aparelhos(df):
    print("Selecione os aparelhos que você possui (digite os números separados por vírgula):")
    for i, aparelho in enumerate(df['Aparelho']):
        print(f"{i + 1}. {aparelho}")

    indices = input("Digite os números: ")
    indices = [int(i) - 1 for i in indices.split(',')]
    return df.iloc[indices]


# Função para aplicar o questionário
def aplicar_questionario(df):
    respostas = {}
    for _, row in df.iterrows():
        tempo_uso = float(
            input(f"Tempo médio de uso diário de {row['Aparelho']} (em horas, padrão: {row['Tempo_Uso']}): ") or row[
                'Tempo_Uso'])
        respostas[row['Aparelho']] = tempo_uso

    valor_kwh = float(input("Valor do kWh cobrado pela concessionária de energia: "))
    return respostas, valor_kwh


# Função para calcular o consumo médio
def calcular_consumo_medio(df, respostas, valor_kwh):
    consumo_total = 0
    for _, row in df.iterrows():
        consumo = row['Potencia'] * respostas[row['Aparelho']] * row['Dias_Uso'] / 1000
        consumo_total += consumo

    custo_total = consumo_total * valor_kwh
    return consumo_total, custo_total


# Função para definir a meta de consumo
def definir_meta_consumo(consumo_atual):
    percentual_str = input("Digite o percentual de redução desejado (ex: 10 para 10%): ")
    percentual = float(percentual_str.replace('%', ''))
    return consumo_atual * (1 - percentual / 100)


# Função para criar e treinar a rede neural
def criar_rede_neural(df, respostas, meta_consumo):
    X = np.array([[row['Potencia'], respostas[row['Aparelho']], row['Dias_Uso']] for _, row in df.iterrows()])
    y = np.array([respostas[row['Aparelho']] for _, row in df.iterrows()])

    X_norm = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
    y_norm = (y - y.min()) / (y.max() - y.min())

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(3,)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='mse')
    model.fit(X_norm, y_norm, epochs=100, verbose=0)

    return model, X_norm


# Função para otimizar o consumo
def otimizar_consumo(model, X_norm, df, respostas, meta_consumo):
    novos_tempos = model.predict(X_norm).flatten()

    y_min, y_max = min(respostas.values()), max(respostas.values())
    novos_tempos = novos_tempos * (y_max - y_min) + y_min

    for i, (_, row) in enumerate(df.iterrows()):
        if row['Aparelho'] in ['FREEZER VERTICAL/HORIZONTAL', 'GELADEIRA 1 PORTA', 'GELADEIRA 2 PORTAS']:
            novos_tempos[i] = 24  # Equipamentos essenciais ficam ligados 24h
        elif row['Aparelho'] == 'CHUVEIRO ELÉTRICO':
            novos_tempos[i] = max(novos_tempos[i], 20 / 60)  # Mínimo de 20 minutos por pessoa

    return dict(zip(df['Aparelho'], novos_tempos))


# Função principal
def main():
    df = criar_dataframe()
    df_selecionado = selecionar_aparelhos(df)
    respostas, valor_kwh = aplicar_questionario(df_selecionado)
    consumo_atual, custo_atual = calcular_consumo_medio(df_selecionado, respostas, valor_kwh)

    print(f"\nConsumo atual: {consumo_atual:.2f} kWh")
    print(f"Custo atual: R$ {custo_atual:.2f}")

    meta_consumo = definir_meta_consumo(consumo_atual)
    model, X_norm = criar_rede_neural(df_selecionado, respostas, meta_consumo)
    novos_tempos = otimizar_consumo(model, X_norm, df_selecionado, respostas, meta_consumo)

    novo_consumo, novo_custo = calcular_consumo_medio(df_selecionado, novos_tempos, valor_kwh)

    print("\nSugestões de otimização:")
    for aparelho, tempo in novos_tempos.items():
        print(f"{aparelho}: {tempo:.2f} horas por dia")

    print(f"\nNovo consumo estimado: {novo_consumo:.2f} kWh")
    print(f"Novo custo estimado: R$ {novo_custo:.2f}")
    print(f"Economia estimada: R$ {custo_atual - novo_custo:.2f}")


if __name__ == "__main__":
    main()