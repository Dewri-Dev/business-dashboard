def calculate_health_score(revenue, expenses, profit):
    """
    Feature 3: Health Scoring
    Calculates a business health score from 0 to 100 based on custom logic.
    """
    # If there's no revenue but there are expenses, score is 0
    if revenue <= 0 and expenses > 0:
        return 0
    elif revenue <= 0:
        return 50  # Neutral starting point for brand new accounts

    score = 50  # Base starting score
    
    # 1. Profitability Factor (Adds up to 30 points)
    margin = (profit / revenue) * 100
    if margin >= 25:
        score += 30
    elif margin >= 15:
        score += 20
    elif margin > 0:
        score += 10
        
    # 2. Expense Management Factor (Adds up to 20 points)
    expense_ratio = (expenses / revenue) * 100
    if expense_ratio <= 40:
        score += 20
    elif expense_ratio <= 70:
        score += 10
        
    # 3. Risk Deductions
    if profit < 0:
        score -= 40  # Massive penalty for operating at a loss
        
    # Ensure the score strictly stays between 0 and 100
    return max(0, min(100, int(score)))


def generate_alerts(revenue, expenses, profit, margin):
    """
    Feature 3: Automated Risk Assessment
    Generates intelligent text alerts based on the financial data.
    """
    alerts = []
    
    # Critical Alerts
    if profit < 0:
        alerts.append(f"🚨 CRITICAL: You are operating at a net loss of ₹{abs(profit):,.2f}.")
    if revenue == 0 and expenses > 0:
        alerts.append("🚨 CRITICAL: You are burning cash with zero incoming revenue.")
        
    # Warnings
    if 0 <= margin < 15 and revenue > 0:
        alerts.append("⚠️ WARNING: Profit margins are very tight (under 15%). Consider reducing expenses.")
    
    expense_ratio = (expenses / revenue) * 100 if revenue > 0 else 0
    if expense_ratio > 75:
        alerts.append(f"⚠️ WARNING: High cash burn. Expenses are consuming {expense_ratio:.1f}% of your revenue.")
        
    return alerts