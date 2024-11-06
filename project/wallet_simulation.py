from Crypto.PublicKey import RSA

def generate_wallet():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    print(f"Private Key:\n{private_key.decode('utf-8')}")
    print(f"Public Key:\n{public_key.decode('utf-8')}")

if __name__ == "__main__":
    generate_wallet()
