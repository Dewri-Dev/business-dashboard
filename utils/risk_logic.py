def calculate_profit_margin(revenue, expenses):
    if revenue == 0:
        return 0
    return ((revenue - expenses) / revenue) * 100


def generate_risk_alerts(current_revenue, previous_revenue,
                         current_expenses, previous_expenses,
                         inventory_cost):

    alerts = []

    current_margin = calculate_profit_margin(current_revenue, current_expenses)
    previous_margin = calculate_profit_margin(previous_revenue, previous_expenses)

    # Expense spike
    if previous_expenses > 0:
        expense_increase = ((current_expenses - previous_expenses) / previous_expenses) * 100
        if expense_increase > 20:
            alerts.append("⚠ Expenses increased by more than 20% compared to last month.")

    # Margin drop
    if current_margin < previous_margin:
        alerts.append("⚠ Profit margin declined compared to last month.")

    # Low margin
    if current_margin < 10:
        alerts.append("⚠ Profit margin below 10%. Business may be at risk.")

    # Inventory risk
    if inventory_cost > current_revenue * 0.5:
        alerts.append("⚠ Inventory cost is high relative to revenue.")

    if not alerts:
        alerts.append("✅ All metrics look healthy. No active alerts.")

    return alerts