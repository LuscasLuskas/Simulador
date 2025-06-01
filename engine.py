# Arquivo: motor_simulacao.py
import math
import pandas as pd
from funcoes_auxiliares import f_x_function # Importa a função do outro arquivo

def run_simulation_advanced_com_seguranca(
    agent_profiles,
    initial_tj,
    initial_p_benchmark,
    gamma_tj,
    epsilon_tj,
    num_cycles,
    MA_limiar_baixo, 
    TJ_limiar_alto,   
    N_ciclos_persistencia, 
    TJ_emergencia     
):
    tj_atual = initial_tj 
    p_benchmark_atual = initial_p_benchmark 
    consecutive_bad_cycles = 0 

    history = {
        "ciclo": [], "tj": [], "ma": [], "p_benchmark": [],
        "comprador_hedge_q_transacted": [], "comprador_moderado_q_transacted": [], "comprador_ponzi_q_transacted": [],
        "vendedor_hedge_q_transacted": [], "vendedor_moderado_q_transacted": [], "vendedor_ponzi_q_transacted": [],
        "transaction_prices_avg": [],
        "seguranca_ativada": [] 
    }

    all_possible_prices = set()
    for profile in agent_profiles.values():
        all_possible_prices.update(profile["base_schedule"].keys())
    sorted_prices = sorted(list(all_possible_prices))

    for cycle in range(1, num_cycles + 1):
        seguranca_foi_ativada_neste_ciclo = False 
        history["ciclo"].append(cycle)
        
        aggregated_demands_final = {p: 0 for p in sorted_prices}
        aggregated_offers_final = {p: 0 for p in sorted_prices}

        for agent_name, profile in agent_profiles.items():
            for p_agent, q_base in profile["base_schedule"].items():
                x = 0 
                if profile["type"] == "comprador":
                    if p_benchmark_atual == 0: x = 0.1 if p_agent < 100 else -0.1 
                    else: x = (p_benchmark_atual - p_agent) / p_benchmark_atual
                elif profile["type"] == "vendedor":
                    if p_benchmark_atual == 0: x = 0.1 if p_agent > 100 else -0.1
                    else: x = (p_agent - p_benchmark_atual) / p_benchmark_atual

                fx_val = f_x_function(x, profile["a"], profile["b"], profile["E"])
                q_adjusted_sentiment = q_base * (1 + fx_val * profile["fator_impacto_fx"])
                q_adjusted_sentiment = max(0, q_adjusted_sentiment) 
                
                q_final = q_adjusted_sentiment * math.exp(-profile["lambda_tj"] * tj_atual)
                q_final = max(0, q_final) 
                
                if profile["type"] == "comprador":
                    aggregated_demands_final[p_agent] += q_final
                elif profile["type"] == "vendedor":
                    aggregated_offers_final[p_agent] += q_final
        
        ma_total_cycle = 0
        total_transaction_value = 0 
        current_cycle_q_transacted = {agent_name: 0 for agent_name in agent_profiles.keys()}
        p_star = [p for p in sorted_prices if aggregated_demands_final[p] > 0 and aggregated_offers_final[p] > 0]

        for p_market in p_star: 
            demand_at_p = aggregated_demands_final[p_market]
            offer_at_p = aggregated_offers_final[p_market]
            transacted_at_p = min(demand_at_p, offer_at_p) 
            
            ma_total_cycle += transacted_at_p
            total_transaction_value += p_market * transacted_at_p

            if transacted_at_p > 0: 
                for agent_name, profile in agent_profiles.items():
                    q_base_agent_at_p = profile["base_schedule"].get(p_market, 0)
                    if q_base_agent_at_p > 0: 
                        x_agent = 0
                        if profile["type"] == "comprador":
                            if p_benchmark_atual == 0: x_agent = 0.1 if p_market < 100 else -0.1
                            else: x_agent = (p_benchmark_atual - p_market) / p_benchmark_atual
                        else: 
                            if p_benchmark_atual == 0: x_agent = 0.1 if p_market > 100 else -0.1
                            else: x_agent = (p_market - p_benchmark_atual) / p_benchmark_atual
                        
                        fx_val_agent = f_x_function(x_agent, profile["a"], profile["b"], profile["E"])
                        q_adj_sentiment_agent = q_base_agent_at_p * (1 + fx_val_agent * profile["fator_impacto_fx"])
                        q_adj_sentiment_agent = max(0, q_adj_sentiment_agent)
                        q_final_agent_at_p = q_adj_sentiment_agent * math.exp(-profile["lambda_tj"] * tj_atual)
                        q_final_agent_at_p = max(0, q_final_agent_at_p)

                        if profile["type"] == "comprador" and demand_at_p > 0:
                            proportion = q_final_agent_at_p / demand_at_p if demand_at_p > 0 else 0
                            current_cycle_q_transacted[agent_name] += proportion * transacted_at_p
                        elif profile["type"] == "vendedor" and offer_at_p > 0:
                            proportion = q_final_agent_at_p / offer_at_p if offer_at_p > 0 else 0
                            current_cycle_q_transacted[agent_name] += proportion * transacted_at_p
        
        history["ma"].append(ma_total_cycle)
        history["tj"].append(tj_atual) 
        history["p_benchmark"].append(p_benchmark_atual) 
        
        for agent_name_prefix in ["comprador_hedge", "comprador_moderado", "comprador_ponzi",
                                   "vendedor_hedge", "vendedor_moderado", "vendedor_ponzi"]:
            history[f"{agent_name_prefix}_q_transacted"].append(current_cycle_q_transacted[agent_name_prefix])
        
        avg_tx_price_this_cycle = p_benchmark_atual 
        if ma_total_cycle > 0:
            avg_tx_price_this_cycle = total_transaction_value / ma_total_cycle
        history["transaction_prices_avg"].append(avg_tx_price_this_cycle)
        p_benchmark_atual = avg_tx_price_this_cycle

        if ma_total_cycle < MA_limiar_baixo and tj_atual > TJ_limiar_alto:
            consecutive_bad_cycles += 1
        else:
            consecutive_bad_cycles = 0 

        tj_proximo_ciclo_calculada = tj_atual 
        if ma_total_cycle + epsilon_tj <= 0: 
            tj_proximo_ciclo_calculada = gamma_tj / 0.00001 
        else:
            tj_proximo_ciclo_calculada = gamma_tj / (ma_total_cycle + epsilon_tj)
        
        tj_proximo_ciclo_calculada = max(0.0001, min(tj_proximo_ciclo_calculada, 1.0)) 

        if consecutive_bad_cycles >= N_ciclos_persistencia:
            tj_proximo_ciclo_final = TJ_emergencia 
            consecutive_bad_cycles = 0  
            seguranca_foi_ativada_neste_ciclo = True 
            print(f"Ciclo {cycle}: Dispositivo de segurança ATIVADO! TJ para próximo ciclo forçada para {TJ_emergencia:.4f}")
        else:
            tj_proximo_ciclo_final = tj_proximo_ciclo_calculada
        
        history["seguranca_ativada"].append(1 if seguranca_foi_ativada_neste_ciclo else 0)
        tj_atual = tj_proximo_ciclo_final 

    return pd.DataFrame(history)