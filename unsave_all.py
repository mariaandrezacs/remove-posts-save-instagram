"""
Remove todos os posts salvos no Instagram (coleção "All posts").

Uso:
    python unsave_all.py

- Delay aleatório entre unsaves para evitar bloqueio.
- Ao finalizar (ou em caso de erro), desloga e remove a sessão.
"""

import getpass
import random
import sys
import time
from pathlib import Path

from instagrapi import Client
from instagrapi.exceptions import (
    BadPassword,
    ChallengeRequired,
    PleaseWaitFewMinutes,
    TwoFactorRequired,
)

SESSION_FILE = Path(__file__).with_name("session.json")
MIN_DELAY, MAX_DELAY = 2.0, 4.0


def login(cl: Client, username: str, password: str) -> None:
    try:
        cl.login(username, password)
        return
    except TwoFactorRequired:
        pass
    # 2FA: permite tentar o código mais de uma vez (códigos expiram rápido)
    for tentativa in range(3):
        code = input("Código 2FA (do app autenticador ou SMS): ").strip()
        try:
            cl.login(username, password, verification_code=code)
            return
        except Exception as e:
            if tentativa == 2:
                raise
            print(f"Código recusado ({e}). Tente novamente com um código novo.")


def run(cl: Client) -> None:
    # Localiza a coleção padrão de salvos
    collections = cl.collections()
    if not collections:
        print("Nenhuma coleção encontrada — esta conta não tem posts salvos.")
        return
    saved = next((c for c in collections if c.name.lower() == "all posts"), None)
    if not saved:
        names = [c.name for c in collections]
        print(f"Coleção 'All posts' não encontrada. Coleções existentes: {names}")
        return

    medias = cl.collection_medias(saved.id, amount=500)
    total = len(medias)
    if total == 0:
        print("Nenhum post salvo encontrado.")
        return
    print(f"{total} post(s) salvo(s) encontrados. Removendo...")

    falhas = 0
    for i, media in enumerate(medias, 1):
        try:
            cl.media_unsave(media.pk)
            print(f"[{i}/{total}] Removido: {media.code or media.pk}")
        except Exception as e:
            falhas += 1
            print(f"[{i}/{total}] FALHOU ({media.pk}): {e}")
        if i < total:
            time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))

    print(f"Concluído. {total - falhas} removidos, {falhas} falhas.")


def main() -> None:
    username = input("Usuário do Instagram: ").strip()
    password = getpass.getpass("Senha: ")

    cl = Client()
    try:
        try:
            login(cl, username, password)
        except BadPassword:
            sys.exit(
                "Login recusado pelo Instagram (BadPassword). Isso geralmente é\n"
                "bloqueio temporário após tentativas falhas — aguarde 10-15 min,\n"
                "confira no app se apareceu 'Foi você?' e aprove, depois tente de novo."
            )
        except (ChallengeRequired, PleaseWaitFewMinutes) as e:
            sys.exit(f"Instagram exigiu verificação adicional: {e}\nResolva no app e tente novamente.")
        run(cl)
    finally:
        try:
            cl.logout()
            print("Deslogado do Instagram.")
        except Exception:
            pass
        SESSION_FILE.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
