from telethon import TelegramClient, utils
#from telethon.tl.functions.channels import GetParticipantsRequest
#from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import ChannelParticipantsSearch
#from telethon.tl.functions.messages import GetDialogsRequest

#import time
import asyncio

import json
#informações da aplicação telegram
app_id = 20074820
api_hash ='7455c8a34a8033b9bf9f4018206a8e43'
numeroTelegram = '+5565992500472'

#nome do canal a ser extraido
nomedocanal = 'screamcorporation'

#Função principal para extração de membros
async def extrairmembros():
    #implementando dados necessarios pro cliente se conectar
    client = TelegramClient('sessao1', app_id, api_hash)

    #conectando o cliente, e caso não conecte automaticamente realiza outro login forçado
    await client.start(numeroTelegram)  # type: ignore
    if not await client.is_user_authorized(): #Segunda tentativa de login caso a primeira não funcione
        await client.send_code_request(numeroTelegram)
        codigo = input('digite o codigo recebido no telegram: ')
        await client.sign_in(numeroTelegram, codigo)

    #pega a entity do canal, para pegar o inputchannel (o get participants requer nesse formato)
    entitycanal = await client.get_entity(nomedocanal)
    print(entitycanal)
    inputcanal = utils.get_input_channel(entitycanal)
    
    membros = []
    membros = await client.get_participants(inputcanal, aggressive=True) #pega todos os dados brutos em relação aos participantes
    count = int(0)
    arraymembros = []
    for membro in membros: #itera os dados e filtra (username, first name e last name) e armazena em variaveis para adicionar no array
        if membro.username:
            username = membro.username
        else:
            username = ''
        if membro.first_name:
            first_name = membro.first_name
        else:
            first_name = ''
        if membro.last_name:
            last_name = membro.last_name    
        else:
            last_name = ''
        name = (first_name + '' + last_name).strip()
        
        #Adiciona no array os dados necessarios e importantes em formato .JSON
        arraymembros.append({'username': username, 'name': name, 'id': membro.id, 'access_hash': membro.access_hash})
    #print (arraymembros)
    
    pathlista = './listaMembros.json' #caminho da lista json
    with open(pathlista, 'w', encoding='utf-8') as listaM: #escreve tudo na lista
        json.dump(arraymembros, listaM, indent=3, ensure_ascii=False)
          

asyncio.run(extrairmembros())
    
    