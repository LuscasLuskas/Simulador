# Simulador
Simulador TCC

1. Bibliotecas
   - math: Para funções matemáticas como math.exp() (exponencial).
   - matplotlib.pyplot (como plt): Para gerar os gráficos.
   - numpy (como np): Para operações numéricas, especialmente se precisarmos de arrays ou funções matemáticas mais avançadas (aqui, np.inf é usado para representar infinito em um caso extremo).
   - pandas (como pd): Para manipulação e análise de dados, especialmente para criar e exibir o DataFrame com os resultados da simulação.

2. Função Auxiliar: A função auxiliar fará o calculo do valor subjetivo f(x) para um agente, se baseando na Teoria da Prospecção.
 - Paramentros
    - x: A sensação subjetiva de ganho (x > 0) ou perda (x < 0).
    - a: Controla a curvatura da função no domínio das perdas (sensibilidade à perda).
    - b: Controla a curvatura da função no domínio dos ganhos.
    - E: Representa a expectativa do agente, modificando a intensidade da reação a ganhos/perdas.
A função retornará um valor entre -1 (perda máxima percebida) e 1 (ganho máximo percebido).

3. Definição dos Perfis dos Agentes (agent_profiles): Essa parte definirá as caracteristicas dos diferentes tipos de agentes (Compradores e vendedores) e seus subtipos (Hedge, Moderado, Ponzi). Cada agente é representado por um dicionário dentro do diciónario agente_profiles.
 - type: "comprador" ou "vendedor".
 - a, b, E: Parâmetros para a função f_x_function, definindo sua psicologia.
 - lambda_tj: Sensibilidade da demanda/oferta do agente à taxa de juros.
 - fator_impacto_fx: Modula o quão fortemente o sentimento f(x) afeta a quantidade base que o agente deseja transacionar.
 - base_schedule: Um dicionário que representa a curva de demanda/oferta base do agente, mapeando preços a quantidades (ex:{preço1: quantidade1, preço2: quantidade2}).

4. Função Principal da Simulação (run_simulation_advanced_com_seguranca): Essa é a função principal que executará a simulção ciclo a ciclo. Ela vai integrar todos os componentes: agentes, função de sentimento, cálculo de transações, a determinação da taxa de juros e dispositivo de segurança.
 - Inicialização: Configura variáveis iniciais como tj_atual, p_benchmark_atual, consecutive_bad_cycles e o dicionário history para armazenar os dados de cada ciclo.
  - Loop de Ciclos:
    - Cálculo de Demanda/Oferta Agregada: Para cada agente, calcula sua quantidade final desejada de compra/venda. Isso envolve:
     * Determinar x (percepção de ganho/perda) com base no p_benchmark_atual.
     * Calcular f(x) usando os parâmetros do agente.
     * Ajustar a quantidade base pelo f(x) e pelo fator_impacto_fx.
     * Ajustar a quantidade pela taxa de juros (tj_atual) e lambda_tj do agente.
     * As quantidades finais de todos os agentes de mesmo tipo (compradores/vendedores) são somadas para obter as curvas de demanda e oferta agregadas.
  - Apuração do Mercado:
     * Identifica os preços de mercado (P∗) onde há tanto demanda quanto oferta.
     * Calcula o volume de transações (MA) somando o mínimo entre demanda e oferta em cada preço de P∗.
     * Calcula o preço médio das transações do ciclo, que se torna o p_benchmark_atual para o próximo ciclo.
     * Distribui as quantidades transacionadas de volta para os perfis dos agentes para fins de registro.
  - Lógica do Dispositivo de Segurança:
     * Verifica se o MA está abaixo de MA_limiar_baixo E se a tj_atual (que vigorou no ciclo) está acima de TJ_limiar_alto.
     * Se sim, incrementa consecutive_bad_cycles. Senão, zera o contador.
     * Calcula a TJ_proximo_ciclo_calculada normalmente usando a fórmula *TJ=γ/(MA+ε).*
     * Se consecutive_bad_cycles atingir N_ciclos_persistencia, a TJ para o próximo ciclo é forçada para TJ_emergencia, e o contador é zerado. Senão, usa-se a TJ_proximo_ciclo_calculada.
  - Atualização: A tj_atual para o próximo ciclo é definida.
Retorna um DataFrame do Pandas contendo o histórico completo da simulação.

5. Parâmetros de Simulação e Chamada de Função: Nesta parte será definida todos os parâmetros iniciais para a simulação e para o dispositivo de segurança. Bem como, chama-se a função run_simulation_advanced_com_seguranca com esses parâmetros para executar a simulação. O resultado é armazenado na variável simulation_results_df

6. Geração de Gráficos e Impressão de Resultados: Depois da simulação, o codigo vai gerar os gráficos que visualizam os resultados:
 - TJ ao longo dos ciclos, com marcações verticais nos ciclos onde o dispositivo de segurança decidiu intervir.
 - MA ao longos dos ciclos, com uma linha horizontal indicando o MA_limiar_baixo.
 - Comportamento (quantidade transacionada) dos três tipos de compradores.
 - Comportamento (quantidade transacionada) dos três tipos de vendedores.
Os gráficos serão salvos como um arquivo PNG
 - Deve imprimir os últimos 15 ciclos do DataFrame de resultados, sendo eles:
   * ciclo
   * TJ
   * MA
   * Segurança_Ativada
   * Transaction_prices_avg
 - Estatísticas descritivas para TJ, MA e preço médio das transações.
 - O número de vezes que o dispositivo de segurança foi ativado e os detalhes dos ciclos em que a decisão foi tomada.


































