# Arquivo: visualizacao.py
import matplotlib.pyplot as plt

def plot_taxa_juros(simulation_results_df, TJ_emergencia_param):
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax1 = plt.subplots(figsize=(14, 7))
    color = 'crimson'
    ax1.set_xlabel('Ciclo da Simulação', fontsize=12)
    ax1.set_ylabel('Taxa de Juros (TJ)', color=color, fontsize=12)
    ax1.plot(simulation_results_df["ciclo"], simulation_results_df["tj"], color=color, marker='o', linestyle='-', label='TJ Vigente no Ciclo')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, which='both', linestyle='--', linewidth=0.5)

    ativacoes = simulation_results_df[simulation_results_df["seguranca_ativada"] == 1]
    unique_ativacao_labels_helper = True 
    for ciclo_decisao_ativacao in ativacoes["ciclo"]:
        label_text_vline = ""
        if unique_ativacao_labels_helper: 
            label_text_vline = f'Decisão de Ativar Segurança (TJ={TJ_emergencia_param:.2f} no próx. ciclo)'
            unique_ativacao_labels_helper = False 
        ax1.axvline(x=ciclo_decisao_ativacao, color='blue', linestyle='--', linewidth=1.5, label=label_text_vline)

    plt.title("Taxa de Juros (TJ) e Ativações do Dispositivo de Segurança", fontsize=16)
    handles, labels = ax1.get_legend_handles_labels()
    by_label = dict(zip(labels, handles)) 
    ax1.legend(by_label.values(), by_label.keys(), loc='best')
        
    plt.tight_layout() 
    plt.savefig("plot_taxa_juros_com_seguranca.png") 
    plt.show()

def plot_volume_transacoes(simulation_results_df, MA_limiar_baixo_param):
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.figure(figsize=(12, 6))
    plt.plot(simulation_results_df["ciclo"], simulation_results_df["ma"], marker='s', linestyle='-', color='darkgreen')
    plt.title("Volume de Transações (MA) ao Longo dos Ciclos", fontsize=16)
    plt.xlabel("Ciclo da Simulação", fontsize=12)
    plt.ylabel("Volume de Transações (MA)", fontsize=12)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.axhline(y=MA_limiar_baixo_param, color='red', linestyle=':', linewidth=1.5, label=f'MA Limiar Baixo ({MA_limiar_baixo_param})')
    plt.legend()
    plt.tight_layout()
    plt.savefig("plot_volume_transacoes_com_seguranca.png")
    plt.show()

def plot_comportamento_compradores(simulation_results_df):
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.figure(figsize=(14, 7))
    plt.plot(simulation_results_df["ciclo"], simulation_results_df["comprador_hedge_q_transacted"], label="Comprador Hedge (Transacionado)", marker='^', linestyle=':')
    plt.plot(simulation_results_df["ciclo"], simulation_results_df["comprador_moderado_q_transacted"], label="Comprador Moderado (Transacionado)", marker='o', linestyle='--')
    plt.plot(simulation_results_df["ciclo"], simulation_results_df["comprador_ponzi_q_transacted"], label="Comprador Ponzi (Transacionado)", marker='x', linestyle='-')
    plt.title("Comportamento dos Compradores (Quantidade Transacionada por Ciclo)", fontsize=16)
    plt.xlabel("Ciclo da Simulação", fontsize=12)
    plt.ylabel("Quantidade Total Transacionada", fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig("plot_comportamento_compradores_com_seguranca.png")
    plt.show()

def plot_comportamento_vendedores(simulation_results_df):
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.figure(figsize=(14, 7))
    plt.plot(simulation_results_df["ciclo"], simulation_results_df["vendedor_hedge_q_transacted"], label="Vendedor Hedge (Transacionado)", marker='^', linestyle=':')
    plt.plot(simulation_results_df["ciclo"], simulation_results_df["vendedor_moderado_q_transacted"], label="Vendedor Moderado (Transacionado)", marker='o', linestyle='--')
    plt.plot(simulation_results_df["ciclo"], simulation_results_df["vendedor_ponzi_q_transacted"], label="Vendedor Ponzi (Transacionado)", marker='x', linestyle='-')
    plt.title("Comportamento dos Vendedores (Quantidade Transacionada por Ciclo)", fontsize=16)
    plt.xlabel("Ciclo da Simulação", fontsize=12)
    plt.ylabel("Quantidade Total Transacionada", fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig("plot_comportamento_vendedores_com_seguranca.png")
    plt.show()