
"""Bank account management module with safer coding practices."""

import hashlib
import json
import secrets
from pathlib import Path

account_data = {}


def create_account(acc_id, name, initial_deposit=0):
    """Create a bank account with an initial deposit."""
    if acc_id in account_data or initial_deposit < 0:
        return False

    account_data[acc_id] = {
        "name": name,
        "balance": initial_deposit,
        "transactions": [
            f"Account created with initial balance {initial_deposit}"
        ],
    }
    return True


def deposit(acc_id, amount):
    """Deposit a positive amount into an existing account."""
    if acc_id not in account_data or amount <= 0:
        return False

    account = account_data[acc_id]
    account["balance"] += amount
    account["transactions"].append(f"Deposited {amount}")
    return True


def withdraw(acc_id, amount):
    """Withdraw a positive amount if sufficient funds are available."""
    if acc_id not in account_data or amount <= 0:
        return False

    account = account_data[acc_id]
    if account["balance"] < amount:
        return False

    account["balance"] -= amount
    account["transactions"].append(f"Withdrew {amount}")
    return True


def compute_bonus(acc_id, rate=0.05):
    """Calculate a bonus using a numeric rate, not an expression."""
    if acc_id not in account_data:
        raise ValueError("Account does not exist.")
    if not isinstance(rate, (int, float)) or isinstance(rate, bool):
        raise ValueError("Rate must be numeric.")
    if not 0 <= rate <= 1:
        raise ValueError("Rate must be between 0 and 1.")

    balance = account_data[acc_id]["balance"]
    return balance * rate


def get_hash(pin):
    """Hash a PIN using PBKDF2-HMAC-SHA256 with a random salt."""
    if not isinstance(pin, str) or not pin.isdigit():
        raise ValueError("PIN must contain digits only.")

    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", pin.encode("utf-8"), salt, 600_000
    )
    return f"{salt.hex()}:{digest.hex()}"


def generate_temp_pin():
    """Generate a cryptographically secure four-digit temporary PIN."""
    return f"{secrets.randbelow(9000) + 1000:04d}"


def backup_data(filename="backup.json"):
    """Save account data to a JSON backup file."""
    backup_path = Path(filename)
    with backup_path.open("w", encoding="utf-8") as backup_file:
        json.dump(account_data, backup_file, indent=4)
    print(f"Backup saved to {backup_path}")


def main():
    """Run a demonstration of the bank account operations."""
    create_account("A01", "Alice", 1000)
    deposit("A01", 500)
    withdraw("A01", 200)

    print("Bonus:", compute_bonus("A01"))
    print("PIN Hash:", get_hash("1234"))
    print("Temporary PIN:", generate_temp_pin())
    backup_data()


if __name__ == "__main__":
    main()
