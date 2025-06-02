# Arquivo: configuracao_modelo.py

# Definições dos Perfis dos Agentes
agent_profiles = {
    "comprador_hedge": {
        "type": "comprador", "a": 2.5, "b": 1.0, "E": -0.1, "lambda_tj": 1.5, "fator_impacto_fx": 0.3,
        "base_schedule": {90: 10, 95: 5} # preço: quantidade
    },
    "comprador_moderado": {
        "type": "comprador", "a": 1.5, "b": 1.0, "E": 0.0, "lambda_tj": 1.0, "fator_impacto_fx": 0.5,
        "base_schedule": {95: 20, 100: 15, 105: 10}
    },
    "comprador_ponzi": {
        "type": "comprador", "a": 0.7, "b": 1.0, "E": 0.3, "lambda_tj": 0.4, "fator_impacto_fx": 0.7,
        "base_schedule": {100: 30, 105: 40, 110: 25}
    },
    "vendedor_hedge": {
        "type": "vendedor", "a": 2.5, "b": 1.0, "E": -0.1, "lambda_tj": 0.2, 
        "fator_impacto_fx": 0.3,
        "base_schedule": {110: 10, 105: 5} 
    },
    "vendedor_moderado": {
        "type": "vendedor", "a": 1.5, "b": 1.0, "E": 0.0, "lambda_tj": 0.1,
        "fator_impacto_fx": 0.5,
        "base_schedule": {105: 20, 100: 15, 95: 10}
    },
    "vendedor_ponzi": {
        "type": "vendedor", "a": 0.7, "b": 1.0, "E": 0.3, "lambda_tj": 0.05,
        "fator_impacto_fx": 0.7,
        "base_schedule": {100: 25, 105: 40, 110: 30}
    }
}

# Parâmetros Iniciais e da Simulação
initial_tj_param = 0.05  # Taxa de juros inicial (ex: 5%)
initial_p_benchmark_param = 100.0 # Preço de referência inicial do mercado
gamma_tj_param = 50.0  # Parâmetro da fórmula da TJ (influencia a magnitude da TJ)
epsilon_tj_param = 10.0 # Parâmetro da fórmula da TJ (evita divisão por zero e suaviza a TJ)
num_cycles_param = 50   # Número de ciclos para a simulação

# Parâmetros do dispositivo de segurança
MA_limiar_baixo_param = 110.0  # Se MA < este valor...
TJ_limiar_alto_param = 0.30    # ...E TJ > este valor...
N_ciclos_persistencia_param = 3 # ...por este nº de ciclos consecutivos...
TJ_emergencia_param = 0.10     # ...TJ é forçada para este valor.
