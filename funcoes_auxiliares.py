# Arquivo: funcoes_auxiliares.py
import math
import numpy as np

def f_x_function(x, a, b, E):
    """Calcula o valor subjetivo f(x) com base em uma fórmula similar à Teoria do Prospecto."""
    term1_denominator = 1 + math.exp(-a * (1 + E) * x)
    term2_denominator = 1 + math.exp(b * (1 + E) * x)
    
    if term1_denominator == 0: 
        term1 = np.inf if -a*(1+E)*x < 0 else 0
    else: 
        term1 = 1 / term1_denominator

    if term2_denominator == 0: 
        term2 = np.inf if b*(1+E)*x > 0 else 0
    else: 
        term2 = 1 / term2_denominator
        
    return term1 - term2