# -*- coding: utf-8 -*-
import telepot
import os
from classes import Funcoes
import buscador

mensagem = "Ola, use os comandos:\n/pdv_uptime : uptime dos pdvs\n/pdv_memoria_livre : memoria livre pdvs\n" \
           "/pdv_limpa_memoria : Limpa Memoria PDV\n/exibe_hora - exibe a hora dos pdvs\n" \
           "/acerta_hora - corrige a hora dos pdvs\n/reinicia_pdv : Reinicia o pdv com base no ultimo octeto (Ex 101,102)\n" \
           "/verifica_cftv : Exibe status CFTV\n/verifica_buscapreco : lista busca precos\n/nivel_toner : nivel toner\n" \
           "/triggers : triggers ativas\n/startvnc\n\n/noticias_tecmundo\n/noticias_tudocelular\n/noticias_olhar_digital\n" \
           "/noticias_uol\n/noticias_techtudo\n/chamados : palavra q informe o assunto - limpa - sem nada para exibir"


def handleCommad(content):
    try:
        chat_id = content['chat']['id']
        try:
            command, param = content['text'].split()
        except:
            command = content['text']
            param = None

        if command == 'Hi':
            mensage = 'Hello, how are you?'
            bot.sendMessage(chat_id, mensage)

        if "pdv_uptime" in command:
            bot.sendMessage(chat_id, f'UPTIME dos PDVs\nAguarde um momento, vou consultar para voce :)')
            os.system('/bin/bash -c "sh comandos.sh uptime"')
            inf = open("envioTelegram.txt")
            bot.sendMessage(chat_id, " " + str(inf.read()))

        if "pdv_memoria_livre" in command:
            bot.sendMessage(chat_id, 'Memoria Livre dos PDVs\nAguarde um momento, vou consultar para voce =)')
            os.system('/bin/bash -c "sh comandos.sh memlivre"')
            inf = open("envioTelegram.txt")
            bot.sendMessage(chat_id, " " + str(inf.read()))

        if "pdv_limpa_memoria" in command:
            bot.sendMessage(chat_id, 'Limpeza memoria Pdv\nAguarde um momento, vou consultar para voce =)')
            os.system('/bin/bash -c "sh comandos.sh limpamem"')
            inf = open("envioTelegram.txt")
            bot.sendMessage(chat_id, " " + str(inf.read()))

        if "exibe_hora" in command:
            bot.sendMessage(chat_id, 'Exibindo a hora dos Pdvs\nAguarde um momento, vou consultar para voce =)')
            os.system('/bin/bash -c "sh comandos.sh exibehora"')
            inf = open("envioTelegram.txt", encoding="ISO-8859-1")
            bot.sendMessage(chat_id, " " + str(inf.read()))

        if "acerta_hora" in command:
            bot.sendMessage(chat_id, 'Corrigindo a hora dos Pdvs\nAguarde um momento, isso pode demorar um pouco =)')
            os.system('/bin/bash -c "sh comandos.sh acertahora"')
            inf = open("envioTelegram.txt", encoding="ISO-8859-1")
            bot.sendMessage(chat_id, " " + str(inf.read()))

        if "reinicia_pdv" in command:
            if str(param):
                os.system('/bin/bash -c "sh comandos.sh reiniciapdv "' + str(param))
                inf = open("envioTelegram.txt")
                bot.sendMessage(chat_id, " " + str(inf.read()))
            else:
                bot.sendMessage(chat_id, "Você nao informou qual o final do IP do PDV")

        if "nivel_toner" in command:
            bot.sendMessage(chat_id, 'Nivel de toner\nAguarde um momento, vou consultar para voce =)')
            os.system('/bin/bash -c "sh comandos.sh toner"')
            inf = open("envioTelegram.txt")
            bot.sendMessage(chat_id, " " + str(inf.read()))

        if "verifica_cftv" in command:
            bot.sendMessage(chat_id, 'Equipamentos de CFTV\nAguarde um momento, vou consultar para voce =)')
            Funcoes.cftv()
            inf = open("envioTelegram.txt")
            bot.sendMessage(chat_id, " " + str(inf.read()))

        if "verifica_buscapreco" in command:
            bot.sendMessage(chat_id, 'Busca Preco online')
            Funcoes.buscapreco()
            inf = open("envioTelegram.txt")
            bot.sendMessage(chat_id, " " + str(inf.read()))

        if "triggers" in command:
            bot.sendMessage(chat_id, 'Triggers Alarmadas')
            Funcoes.verificaTriggers()
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

        if "noticias_pesquisa" in command:
            bot.sendMessage(chat_id, 'Buscando Noticias contendo: ' + str(param))

            # tecmundo
            buscador.retorna_materias(link='https://www.tecmundo.com.br/novidades', tag_bloco='.tec--card',
                                      tag_titulo='.tec--card__title', tag_horario='.z-flex-1', research=param)
            inf = open("resultado.txt", 'r')
            bot.sendMessage(chat_id, " " + str(inf.read()))

            # tudocelular
            buscador.retorna_materias(link='https://www.tudocelular.com/', tag_bloco='.newlist_normal',
                                      tag_titulo='.title_new', tag_horario='em', research=param)
            inf = open("resultado.txt", 'r')
            bot.sendMessage(chat_id, " " + str(inf.read()))

            # olhardigital
            buscador.retorna_materias(link='https://olhardigital.com.br/', tag_bloco='article',
                                      tag_titulo='.title', tag_horario=None, research=param)
            inf = open("resultado.txt", 'r')
            bot.sendMessage(chat_id, " " + str(inf.read()))

            # uol
            buscador.retorna_materias(link='https://noticias.uol.com.br/', tag_bloco='.thumbnails-item',
                                      tag_titulo='.thumb-title', tag_horario=None, research=param)
            inf = open("resultado.txt", 'r')
            bot.sendMessage(chat_id, " " + str(inf.read()))

            # uol
            buscador.retorna_materias(link='https://www.techtudo.com.br/', tag_bloco='.feed-post',
                                      tag_titulo='.feed-post-body', tag_horario=None, research=param)
            inf = open("resultado.txt", 'r')
            bot.sendMessage(chat_id, " " + str(inf.read()))

        if "noticias_tecmundo" in command:
            bot.sendMessage(chat_id, 'Buscando Noticias contendo: ' + str(param))

            # tecmundo
            buscador.retorna_materias(link='https://www.tecmundo.com.br/novidades', tag_bloco='.tec--card',
                                      tag_titulo='.tec--card__title', tag_horario='.z-flex-1', research=param)
            inf = open("resultado.txt", 'r')
            bot.sendMessage(chat_id, " " + str(inf.read()))

        if "noticias_tudocelular" in command:
            # tudocelular
            buscador.retorna_materias(link='https://www.tudocelular.com/', tag_bloco='.newlist_normal',
                                      tag_titulo='.title_new', tag_horario='em', research=param)
            inf = open("resultado.txt", 'r')
            bot.sendMessage(chat_id, " " + str(inf.read()))

        if "noticias_olhar_digital" in command:
            # olhardigital
            buscador.retorna_materias(link='https://olhardigital.com.br/', tag_bloco='article',
                                      tag_titulo='.title', tag_horario=None, research=param)
            inf = open("resultado.txt", 'r')
            bot.sendMessage(chat_id, " " + str(inf.read()))

        if "noticias_uol" in command:
            # uol
            buscador.retorna_materias(link='https://noticias.uol.com.br/', tag_bloco='.thumbnails-item',
                                      tag_titulo='.thumb-title', tag_horario=None, research=param)
            inf = open("resultado.txt", 'r')
            bot.sendMessage(chat_id, " " + str(inf.read()))

        if "noticias_techtudo" in command:
            # techtudo
            buscador.retorna_materias(link='https://www.techtudo.com.br/', tag_bloco='.feed-post',
                                      tag_titulo='.feed-post-body', tag_horario=None, research=param)
            inf = open("resultado.txt", 'r')
            bot.sendMessage(chat_id, " " + str(inf.read()))

        bot.sendMessage(chat_id, mensagem)

    except Exception as e:
        bot.sendMessage(chat_id, f'There was an error!!! {e}')


def sendMessage(chat, mensage):
    bot.sendMessage(chat, mensage)


token_telegram = os.environ["TELEGRAM_TOKEN"]
bot = telepot.Bot(token_telegram)
bot.message_loop(handleCommad)

try:
    print('press CTRL + C to cancel')

    while True:
        pass

except KeyboardInterrupt:
    print('\nBye')
