# Validation utilities and quick checks

def validate_env():
    from dotenv import load_dotenv
    import os
    load_dotenv()
    required = ["SERVER", "DATABASE", "TABLE", "MODEL"]
    missing = [k for k in required if not os.getenv(k)]
    return missing

if __name__ == "__main__":
    miss = validate_env()
    if miss:
        print("Missing env:", miss)
    else:
        print("Env appears OK")
