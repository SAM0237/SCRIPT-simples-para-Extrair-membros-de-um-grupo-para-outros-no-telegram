import telethon
from telethon import TelegramClient, utils
import asyncio

import json


async def pegaEntityGP():
    id_app = 1234456
    api_hash = '74xxxxxxxxxxxxxxxxxxx'

    telefone_telegram = '+551234567'

    #grupo de extração
    nome_grupo = 'nomegrupo'


    #connecta
    client = TelegramClient(session='session', api_id=id_app, api_hash=api_hash)
    await client.start(telefone_telegram) # type: ignore
    #segunda tentativa de conexão
    if not await client.is_user_authorized():
        await client.send_code_request(telefone_telegram)
        codigo = input('digite o codigo recebido')
        await client.sign_in(telefone_telegram, codigo)

    try:
        async for group in client.iter_dialogs():
            print(group.name)
                 
    except(Exception) as e:
        print('ocorreu um erro ao extrair ENTITY do grupo', e)
    return
asyncio.run(pegaEntityGP())