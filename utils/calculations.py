def calculate_health_score(revenue, expenses, profit):
    """
    Calculates a business health score from 0-100.
    """
    score = 70 # Starting base score
    
    # 1. Profitability Factor
    if profit > 0:
        score += 15
    elif profit < 0:
        score -= 30
        
    # 2. Efficiency Factor (Expense Ratio)
    if revenue > 0:
        expense_ratio = expenses / revenue
        if expense_ratio > 0.8:
            score -= 20
        elif expense_ratio < 0.5:
            score += 10
            
    return max(0, min(score, 100))

def generate_alerts(revenue, expenses, profit, margin):
    """
    Generates human-readable alerts based on business performance.
    """
    alerts = []
    
    if profit < 0:
        alerts.append("CRITICAL: Business is currently operating at a loss.")
    
    if revenue > 0 and (expenses / revenue) > 0.85:
        alerts.append("WARNING: Operating expenses are consuming over 85% of revenue.")
        
    if 0 < margin < 10:
        alerts.append("ADVISORY: Profit margin is thin (< 10%). Consider cost optimization.")
        
    if not alerts:
        alerts.append("STABLE: All financial indicators are within healthy ranges.")
        
    return alerts