# from authenticate import authenticate_face

# balance = 5000
# amount = int(input("Enter Amount: "))

# print("Face Authentication Required...")

# if authenticate_face():
#     if amount <= balance:
#         balance -= amount
#         print("Payment Successful")
#         print("Remaining Balance:", balance)
#     else:
#         print("Insufficient Balance")
# else:
#     print("Payment Blocked - Face Not Verified")
from authenticate import authenticate_face
from risk_engine import calculate_risk_score
from user_utils import get_user_data, update_failed_attempts
import json
import random

username = input("Enter Username: ")
user_folder = f"dataset/{username}"

user_data = get_user_data(username)
if not user_data:
    print("❌ User not found")
    exit()

balance = user_data.get("balance", 0)
failed_attempts = user_data.get("failed_attempts", 0)

amount = int(input("Enter Amount: "))

print("🔐 Face Authentication Required...")

# ---------------- FACE AUTH ----------------
if authenticate_face():
    update_failed_attempts(username, True)

    if amount > balance:
        print("❌ Insufficient Balance")
        exit()

    # ---------------- RISK CHECK ----------------
    is_risky, risk_level = calculate_risk_score(
        user_folder,
        amount,
        failed_attempts
    )

    print(f"⚠️ Risk Level: {risk_level}")

    # ---------------- OTP FLOW ----------------
    if is_risky:
        otp = str(random.randint(100000, 999999))
        print(f"[DEBUG OTP]: {otp}")  # Replace with email later

        user_otp = input("Enter OTP: ")

        if user_otp != otp:
            print("❌ Payment Failed: Incorrect OTP")
            exit()

    # ---------------- PAYMENT ----------------
    user_data["balance"] -= amount

    with open(f"{user_folder}/user.json", "w") as f:
        json.dump(user_data, f, indent=4)

    print("✅ Payment Successful")
    print("💰 Remaining Balance:", user_data["balance"])

else:
    update_failed_attempts(username, False)
    print("❌ Payment Blocked - Face Not Verified")
