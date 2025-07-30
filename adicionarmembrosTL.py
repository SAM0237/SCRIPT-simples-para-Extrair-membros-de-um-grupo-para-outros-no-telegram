import json
import asyncio
from telethon import TelegramClient, utils
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import InputUser

#Id do grupo de destino (não utilizado no codigo)
grupodestinoId = 2773408683

nome_canal = 'screamcorpvazados' #nome do grupo onde os membros serão adicionados

#informações APP telegram
app_id = 20074820
api_hash ='7455c8a34a8033b9bf9f4018206a8e43'
numero_Telegram = '+5565992500472'

#função principal para adicionar membros de forma automatizada
async def adicionar_Membros():

    #passa os dados para conectar ao cliente e tenta conexão
    client = TelegramClient('session2', app_id, api_hash)
    await client.start(numero_Telegram) # type: ignore

    #segunda tentativa caso a primeira n conecte
    if not await client.is_user_authorized():
        await client.send_code_request(numero_Telegram)
        codigo = input('ja sabe man fala o codigo')
        await client.sign_in(codigo)

    caminhoLista = './listaMembros.json'
    with open(caminhoLista, 'r', encoding='utf-8') as ll: #abre a lista .json e le todos os index
        membros = json.load(ll)

    for membro in membros: #itera a lista .json de membros index por index
        try:
            entity_canal = await client.get_entity(nome_canal) 
            input_canal = utils.get_input_channel(entity_canal) #pega inputchannel pro invitetochannelrequest (ele requer esse formato)

            usuario_input = InputUser(user_id=membro['id'], access_hash=membro['access_hash']) #monta o imputuser para o invitechannel também
            #realiza a adição de membro no membro atual da iteração
            await client(InviteToChannelRequest(channel=input_canal, users=[usuario_input])) # type: ignore
            print(f"adicionando membro: {membro['name']}")

            await asyncio.sleep(3.5)

        except Exception as e:
            print('erro ao adicionar usuario: ', e)

    await client.disconnect()         # type: ignore


asyncio.run(adicionar_Membros())