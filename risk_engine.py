# import json
# import os

# def calculate_risk_score(sender_folder, amount):
#     """
#     Analyzes transaction risk using historical averages.
#     Returns: (is_anomaly, risk_level)
#     """
#     user_file = f"{sender_folder}/user.json"
    
#     if not os.path.exists(user_file):
#         return False, "Low"

#     with open(user_file, 'r') as f:
#         data = json.load(f)

#     # Get transaction history (if any)
#     history = data.get("transactions", [])
    
#     if len(history) < 3:
#         # Not enough data: use a fixed threshold (e.g., ₹5000)
#         if amount > 5000:
#             return True, "Medium (New Account High Value)"
#         return False, "Low"

#     # Calculate Mean of past transactions
#     amounts = [t['amount'] for t in history]
#     avg_spend = sum(amounts) / len(amounts)
    
#     # Logic: If current amount is > 3x the average, it's an anomaly
#     if amount > (avg_spend * 3):
#         return True, "High (Value Deviation)"
import json
import os

def calculate_risk_score(sender_folder, amount, failed_attempts):
    """
    Returns: (is_risky, risk_level)
    """

    user_file = f"{sender_folder}/user.json"
    
    if not os.path.exists(user_file):
        return False, "Low"

    with open(user_file, 'r') as f:
        data = json.load(f)

    history = data.get("transactions", [])

    # 🚨 Rule 1: Failed attempts
    if failed_attempts >= 3:
        return True, "High (Multiple Failed Attempts)"

    # 🚨 Rule 2: New account + high value
    if len(history) < 3:
        if amount > 5000:
            return True, "Medium (New Account High Value)"
        return False, "Low"

    # 🚨 Rule 3: Deviation from average
    amounts = [t['amount'] for t in history]
    avg_spend = sum(amounts) / len(amounts)

    if amount > (avg_spend * 3):
        return True, "High (Value Deviation)"

    return False, "Low"
    
#     return False, "Low"
