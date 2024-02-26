# Calculates Tournament Performance Rating (TPR) and Estimated Performance Rating (EPR) in cases of perfect or zero scores
import math
from scipy.optimize import minimize_scalar

def calculate_win_probability(A, B):
    return 1 / (1 + 10 ** ((B - A) / 400))

def adjust_mn(m, n):
    if not float(m).is_integer():
        m, n = int(m * 2), int(n * 2)
    else:
        m, n = int(m), int(n)
    return m, n

def calculate_score_probability(w, m, n):
    # Ensure m and n are treated as integers for comb function
    m = int(m)
    n = int(n)
    return math.comb(n, m) * w ** m * (1 - w) ** (n - m)

def calculate_score_plus_probability(w, m, n):
    if n < m:
        raise ValueError("n must be greater than or equal to m")

    total_probability = 0
    for k in range(m, n + 1):
        total_probability += math.comb(n, k) * w ** k * (1 - w) ** (n - k)
    return total_probability

def optimize_w(m, n, t):
    def objective(w):
        score_prob = calculate_score_probability(w, m, n)
        if score_prob <= t:
            return -score_prob
        else:
            return float('inf')  # Return a large value if constraint is not met
    
    result = minimize_scalar(objective, bounds=(0, 1), method='bounded')
    return result.x

def optimize_w_plus(m, n, t):
    def objective(w):
        score_plus_prob = calculate_score_plus_probability(w, m, n)
        if score_plus_prob <= t:
            return -score_plus_prob
        else:
            return float('inf')  # Return a large value if constraint is not met

    result = minimize_scalar(objective, bounds=(0, 1), method='bounded')
    return result.x


# def calculate_EPR_old(w_star, B):
#    return 400 * math.log10(-w_star * math.exp((B * math.log(10)) / 400) / (w_star - 1))

def calculate_EPR(w_star, B):
    return B - 400 * math.log10((1 - w_star) / w_star)

def calculate_TPR(m, n, B):
    if m == 0:
        return "TPR cannot be calculated: Player lost all games."
    elif m == n:
        return "TPR cannot be calculated: Player won all games."
    return B - 400 * math.log10((n - m) / m)
