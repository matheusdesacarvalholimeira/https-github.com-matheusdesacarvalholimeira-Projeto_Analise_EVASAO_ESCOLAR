import os
import pyotp
from dotenv import load_dotenv

# Carrega o .env só uma vez
load_dotenv()

# Carrega o segredo MFA do .env
TOTP_SECRET = os.getenv('MFA_SECRET')

if TOTP_SECRET is None:
    print("❌ Erro: A variável MFA_SECRET não está definida no .env!")
    exit(1)

totp = pyotp.TOTP(TOTP_SECRET)

codigo_usuario = input("🔐 Digite o código MFA (Microsoft Authenticator ou similar): ")

if not totp.verify(codigo_usuario):
    print("❌ MFA inválido! Encerrando a execução por segurança.")
    exit(1)
else:
    print("✅ MFA verificado com sucesso. Continuando execução...")
