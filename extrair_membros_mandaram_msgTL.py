import telethon
from telethon import TelegramClient, utils
import asyncio

import json
#dados api telegram
id_app = 20074820
api_hash = '7455c8a34a8033b9bf9f4018206a8e43'

telefone_telegram = '+5565992500472'

#grupo de extração
nome_grupo = 'Grupo Trust-Business'

#pega a entity do grupo pra usar get_messages posteriormente
async def pegaEntityGP(client):
    try:
        async for group in client.iter_dialogs():
            if group.name == nome_grupo:
                return await client.get_entity(group) 
    except(Exception) as e:
        print('ocorreu um erro ao extrait o ENTITY do grupo', nome_grupo, e)
    return


async def extrair_membros_que_mandaram_msg():
    #connecta
    client = TelegramClient(session='session_1', api_id=id_app, api_hash=api_hash)
    await client.start(telefone_telegram) # type: ignore
    #segunda tentativa de conexão
    if not await client.is_user_authorized():
        await client.send_code_request(telefone_telegram)
        codigo = input('digite o codigo recebido')
        await client.sign_in(telefone_telegram, codigo) 
    
    entity_GP = await pegaEntityGP(client) #PEGA entity e armazena
    quemenviou = []
    sett = set()
    caminhoListMembros = './listaMembros.json'
    try:
        if entity_GP:   #itera as mensagens nos chats do grupo e extrai id e access_hash
                    
            async for mensagem in client.iter_messages(entity=entity_GP, limit=3000):
                if mensagem.sender:
                    if mensagem.sender.username:
                        if mensagem.sender.username not in sett:
                            quemenviou.append({'User_id': mensagem.sender.id, 'access_hash': mensagem.sender.access_hash})
                            sett.add(mensagem.sender.username)

            #insere a extração na lista de membros .json                
            with open (caminhoListMembros, 'w', encoding='utf-8') as ListJson:
                json.dump(quemenviou, ListJson, indent=2, ensure_ascii=False)

        else:
            print('NÃO À ENTITYGP')             
    except(Exception) as e:
            print('erro pegando quem enviou mensagem do grupo da entidade: ', entity_GP, 'erro: ', e)
    
        
asyncio.run(extrair_membros_que_mandaram_msg())