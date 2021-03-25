# -*- coding: utf-8 -*-
import telepot
import os
from classes import Funcoes

mensagem = f'\nBOT CT18,\nuse os comandos:\n/pdv_uptime : uptime dos pdvs\n/pdv_memoria_livre : memoria livre pdvs\n' \
           f'/pdv_limpa_memoria : Limpa Memoria PDV\n/exibe_hora - exibe a hora dos pdvs\n' \
           f'/acerta_hora - corrige a hora dos pdvs\n/reinicia_pdv : Reinicia o pdv com base no ultimo octeto (Ex 101,102)\n' \
           f'/verifica_cftv : Exibe status CFTV\n/verifica_buscapreco : lista busca precos\n/nivel_toner : nivel toner\n' \
           f'/triggers : triggers ativas\n/ping : pinga o IP solicitado\n/eda_online : exibe a ultima data que o EDA esteve ON\n\n/chamados : palavra q informe o assunto - limpa - sem nada para exibir'

'''
1035577098 cpd18
1299478866 cpd08
769723764 part
'''


def handleCommad(content):
    try:
        chat_id = content['chat']['id']
        name = content['chat']['first_name']
        print(chat_id, type(chat_id))
        if chat_id == 1035577098 or chat_id == 769723764 or chat_id == 1299478866:
            try:
                command, *param = content['text'].split()
            except:
                command = content['text']
                param = None
            final = ' '
            param = final.join(param)

            if command == 'Hi':
                mensage = 'Hello, how are you?'
                bot.sendMessage(chat_id, mensage)

            if "pdv_uptime" in command:
                bot.sendMessage(chat_id, f'UPTIME dos PDVs\nAguarde um momento {name}, vou consultar para voce :)')
                os.system('/bin/bash -c "sh comandos.sh uptime"')
                inf = open("envioTelegram.txt")
                bot.sendMessage(chat_id, " " + str(inf.read()))

            if "pdv_memoria_livre" in command:
                bot.sendMessage(chat_id,
                                f'Memoria Livre dos PDVs\nAguarde um momento {name}, vou consultar para voce =)')
                os.system('/bin/bash -c "sh comandos.sh memlivre"')
                inf = open("envioTelegram.txt")
                bot.sendMessage(chat_id, " " + str(inf.read()))

            if "pdv_limpa_memoria" in command:
                bot.sendMessage(chat_id, f'Limpeza memoria Pdv\nAguarde um momento {name}, limpando memoria... =)')
                os.system('/bin/bash -c "sh comandos.sh limpamem"')
                inf = open("envioTelegram.txt")
                bot.sendMessage(chat_id, " " + str(inf.read()))

            if "exibe_hora" in command:
                bot.sendMessage(chat_id,
                                f'Exibindo a hora dos Pdvs\nAguarde um momento {name}, vou consultar para voce =)')
                os.system('/bin/bash -c "sh comandos.sh exibehora"')
                inf = open("envioTelegram.txt", encoding="ISO-8859-1")
                bot.sendMessage(chat_id, " " + str(inf.read()))

            if "acerta_hora" in command:
                bot.sendMessage(chat_id,
                                f'Corrigindo a hora dos Pdvs\nAguarde um momento {name}, isso pode demorar um pouco =)')
                os.system('/bin/bash -c "sh comandos.sh acertahora"')
                inf = open("envioTelegram.txt", encoding="ISO-8859-1")
                bot.sendMessage(chat_id, " " + str(inf.read()))

            if "reinicia_pdv" in command:
                bot.sendMessage(chat_id,
                                'Reiniciando o Pdv {param}\nAguarde um momento {name}, isso pode demorar um pouco =)')
                if str(param):
                    os.system('/bin/bash -c "sh comandos.sh reiniciapdv "' + str(param))
                    inf = open("envioTelegram.txt")
                    bot.sendMessage(chat_id, " " + str(inf.read()))
                else:
                    bot.sendMessage(chat_id, "Você nao informou qual o final do IP do PDV")

            if "nivel_toner" in command:
                bot.sendMessage(chat_id, f'Nivel de toner\nAguarde um momento {name}, vou consultar para voce =)')
                os.system('/bin/bash -c "sh comandos.sh toner"')
                inf = open("envioTelegram.txt")
                bot.sendMessage(chat_id, " " + str(inf.read()))

            if "verifica_cftv" in command:
                bot.sendMessage(chat_id, f'Equipamentos de CFTV\nAguarde um momento {name}, vou consultar para voce =)')
                Funcoes.cftv()
                inf = open("envioTelegram.txt")
                bot.sendMessage(chat_id, " " + str(inf.read()))

            if "verifica_buscapreco" in command:
                bot.sendMessage(chat_id, f'Busca Preco online\nAguarde um momento {name}, vou consultar para voce =)')
                Funcoes.buscapreco()
                inf = open("envioTelegram.txt")
                bot.sendMessage(chat_id, " " + str(inf.read()))

            if "ping" in command:
                bot.sendMessage(chat_id, f'Pingando o endereço de IP ' + param)
                Funcoes.ping(param)
                inf = open("envioTelegram.txt")
                bot.sendMessage(chat_id, " " + str(inf.read()))

            if "triggers" in command:
                bot.sendMessage(chat_id, f'Triggers Alarmadas,\nAguarde um momento {name}, vou consultar para voce =)')
                Funcoes.verificaTriggers()
                inf = open("envioTelegram.txt")
                bot.sendMessage(chat_id, " " + str(inf.read()))

            if "eda_online" in command:
                bot.sendMessage(chat_id, f'EDA On-line,\nAguarde um momento {name}, vou consultar para voce =)')
                Funcoes.eda_online()
                inf = open("envioTelegram.txt")
                bot.sendMessage(chat_id, " " + str(inf.read()))

            if "chamado" in command:
                if str(param) == 'limpa':
                    Funcoes.limpachamado()
                    bot.sendMessage(chat_id, "Arquivo de chamados Limpo")
                elif not str(param) == None:
                    Funcoes.chamado(str(param))
                    inf = open("chamados.txt")
                    print(inf)
                    bot.sendMessage(chat_id, " " + str(inf.read()))
                else:
                    inf = open("chamados.txt")
                    bot.sendMessage(chat_id, " " + str(inf.read()))

            bot.sendMessage(chat_id, mensagem)
        else:
            bot.sendMessage(chat_id, f'Desculpe {name}, voce nao possue autorização para utilizar este bot.')
    except Exception as e:
        bot.sendMessage(chat_id, f'There was an error!!! {e}')


def sendMessage(chat, mensage):
    bot.sendMessage(chat, mensage)


token_telegram = os.environ["TELEGRAM_TOKEN"]
bot = telepot.Bot(token_telegram)
bot.message_loop(handleCommad)

try:
    print('bot ct18\npress CTRL + C to cancel')

    while True:
        pass

except KeyboardInterrupt:
    print('\nBye')
