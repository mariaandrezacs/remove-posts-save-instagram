# Remover posts salvos do Instagram

Script em Python que remove automaticamente **todos os posts salvos** da sua conta do Instagram (coleção "All posts"), usando a biblioteca não-oficial [instagrapi](https://github.com/subzeroid/instagrapi).

## Requisitos

- Python 3.10+
- Conta do Instagram (suporta 2FA por app autenticador ou SMS)

## Instalação

```powershell
# Criar ambiente virtual
python -m venv .venv

# Ativar (PowerShell)
.\.venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

## Uso

```powershell
python unsave_all.py
```

O script vai pedir:

1. **Usuário do Instagram** — seu @ ou e-mail/telefone da conta
2. **Senha** — não aparece na tela ao digitar
3. **Código 2FA** — apenas se a conta tiver autenticação em duas etapas (até 3 tentativas)

Depois disso ele lista os posts salvos e remove um por um, com delay aleatório de 2–4 segundos entre cada remoção para evitar bloqueio por abuso de requisições.

Exemplo de saída:

```
Usuário do Instagram: seu_usuario
Senha:
Código 2FA: 123456
12 post(s) salvo(s) encontrados. Removendo...
[1/12] Removido: Dc7CukENAFW
[2/12] Removido: DcJlrsGp6PT
...
Concluído. 12 removidos, 0 falhas.
Deslogado do Instagram.
```

## Comportamento

- Ao finalizar (com sucesso **ou** erro), o script **desloga** da conta e remove qualquer arquivo de sessão.
- Posts que falharem (ex.: já deletados pelo autor) são ignorados e reportados no final.
- Se a conta não tiver posts salvos, o script avisa e encerra.

## Solução de problemas

| Erro | Causa provável | Solução |
|------|----------------|---------|
| `BadPassword` | Instagram rejeitou o contexto de login (IP/dispositivo) após tentativas falhas — não necessariamente senha errada | Aguarde 10–15 min, aprove o aviso "Foi você?" no app, tente de novo |
| `Código recusado` (2FA) | Código expirado (TOTP vale 30s) ou método errado | Use código do app autenticador, não SMS, e digite rápido |
| `ChallengeRequired` | Instagram exige verificação adicional | Resolva a verificação no app oficial e rode o script novamente |
| `PleaseWaitFewMinutes` | Rate limit de login | Aguarde e tente mais tarde |
| `Nenhuma coleção encontrada` | A conta logada não tem posts salvos | Verifique se está na conta certa |

## Avisos

- ⚠️ Usar a API privada do Instagram viola os **Termos de Serviço** da plataforma. O risco de bloqueio temporário existe, embora seja baixo com volumes pequenos e delays — use por sua conta e risco.
- **A remoção é irreversível**: os posts removidos terão que ser salvos manualmente de novo se quiser recuperá-los.
- Nunca compartilhe sua senha ou arquivos de sessão gerados.
