# Arquivo: main.py
import pandas as pd 

# Importa componentes dos outros arquivos do projeto
from model_config import (
    agent_profiles, 
    initial_tj_param, 
    initial_p_benchmark_param,
    gamma_tj_param, 
    epsilon_tj_param, 
    num_cycles_param,
    MA_limiar_baixo_param, 
    TJ_limiar_alto_param, 
    N_ciclos_persistencia_param,
    TJ_emergencia_param
)
from engine import run_simulation_advanced_com_seguranca
from visualization import (
    plot_taxa_juros, 
    plot_volume_transacoes, 
    plot_comportamento_compradores,
    plot_comportamento_vendedores
)

def main():
    print("Iniciando a simulação de mercado...")

    # Simulação
    simulation_results_df = run_simulation_advanced_com_seguranca(
        agent_profiles,
        initial_tj_param,
        initial_p_benchmark_param,
        gamma_tj_param,
        epsilon_tj_param,
        num_cycles_param,
        MA_limiar_baixo_param,
        TJ_limiar_alto_param,
        N_ciclos_persistencia_param,
        TJ_emergencia_param
    )

    print("Simulação concluída. Gerando gráficos e resultados...")

    # Gráficos
    plot_taxa_juros(simulation_results_df, TJ_emergencia_param)
    plot_volume_transacoes(simulation_results_df, MA_limiar_baixo_param)
    plot_comportamento_compradores(simulation_results_df)
    plot_comportamento_vendedores(simulation_results_df)

    # --- Impressão dos Resultados
    print("\n--- Resultados da Simulação com Dispositivo de Segurança (Últimos 15 ciclos) ---")
    print(simulation_results_df[["ciclo", "tj", "ma", "seguranca_ativada", "transaction_prices_avg"]].tail(15).to_markdown(index=False))

    print("\n--- Estatísticas Descritivas Gerais (TJ, MA, Preço Médio Transação) ---")
    print(simulation_results_df[["tj", "ma", "transaction_prices_avg"]].describe().to_markdown())

    print("\n--- Informações sobre Ativações do Dispositivo de Segurança ---")
    total_ativacoes = simulation_results_df['seguranca_ativada'].sum()
    print(f"Total de vezes que o dispositivo de segurança foi ativado (decisão tomada): {total_ativacoes}")
    if total_ativacoes > 0:
        print("Ciclos em que a decisão de ativar o dispositivo foi tomada (TJ de emergência no ciclo seguinte):")
        print(simulation_results_df[simulation_results_df['seguranca_ativada'] == 1][["ciclo", "tj", "ma"]].to_markdown(index=False))
    
    print("\nExecução finalizada. Verifique os gráficos salvos e o output do console.")

if __name__ == "__main__":
    main()
