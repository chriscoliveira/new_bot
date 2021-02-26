#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv, os, subprocess
from zabbix_api import ZabbixAPI
import json
from datetime import datetime, timedelta


class Funcoes:

    def cftv():
        envio = open('envioTelegram.txt', 'w')
        file = open('cftv.txt')
        listas = csv.reader(file, delimiter=",")

        for lista in listas:
            # print(os.system("ping -c 1 %s" % lista[0]))
            res = subprocess.call(['ping', '-c', '1', lista[0]])
            if res == 0:
                envio.write(f'OK -> {lista[1]}\n')
            elif res == 2:
                envio.write(f'\nOFF-LINE -> {lista[0]}\t{lista[1]}\n\n')
            else:
                envio.write(f'\nOFF-LINE -> {lista[0]}\t{lista[1]}\n\n')
        envio.close()
        file.close()

    def buscapreco():
        envio = open('envioTelegram.txt', 'w')
        file = open('listabuscapreco.txt')
        listas = csv.reader(file, delimiter=",")

        for lista in listas:
            # print(os.system("ping -c 1 %s" % lista[0]))
            res = subprocess.call(['ping', '-c', '1', lista[0]])
            if res == 0:
                envio.write(f'OK -> {lista[1]}\n')
            elif res == 2:
                envio.write(f'\nOFF-LINE -> {lista[0]}\t{lista[1]}\n\n')
            else:
                envio.write(f'\nOFF-LINE -> {lista[0]}\t{lista[1]}\n\n')
        envio.close()
        file.close()

    def chamado(assunto):
        envio = open('chamados.txt', 'a')
        envio.write(assunto + '\n')
        envio.close()

    def limpachamado():
        envio = open('chamados.txt', 'w')
        envio.write('')
        envio.close()

    def toner():
        envio = open('envioTelegram.txt', 'w')
        file = open('4impressoras.txt')
        listas = csv.reader(file, delimiter=",")
        for lista in listas:
            print(os.system("ping -c 1 %s" % lista[0]))
            os.system(
                "snmpwalk -v 2c -c public $ip 1.3.6.1.4.1.367.3.2.1.2.24.1.1.5.1 | awk '{print "'$ip' " $4 " % "}' >> /Scripts/envioTelegram.txt")

        envio.close()
        file.close()

    def verificaTriggers():
        try:
            zapi = ZabbixAPI(server="http://10.131.0.30/zabbix")
            zapi.login("USUARIO_API", "tenda123")
            # print('Conectado a API do zabbix versão: {}'.format(zapi.api_version()))
        except Exception as err:
            print('Falha ao conectar na API do Zabbix')
            print('Erro: {}'.format(err))

        texto = open("json_triggers.json", "w")

        triggers = zapi.trigger.get({
            "output": [
                "extend"
            ],
            "active": 1,
            "min_severity": 2,
            "selectHosts": [
                "name"
            ],
            "selectLastEvent": 1,
            "filter": {
                "value": 1
            },
            "sortfield": "description",
            "sortorder": "ASC"
        })
        prioridade = "Nivel: ?"
        # print(triggers)
        try:
            if triggers:
                json.dump(triggers, texto, indent=4, sort_keys=True)

            else:
                texto.write("Nenhuma trigger acionada")
        except Exception as err:
            texto.write('Falha ao listar as triggers \nErro: {}'.format(err))
        texto.close

        zapi.logout()

        """exibe o json"""

        # with open("json_triggers.json","r") as json_file:
        #     dados = json.load(json_file)

        envio = open('envioTelegram.txt', 'w')
        for i in range(len(triggers)):
            valor = triggers[i]
            nome = valor.get('hosts')
            eventos = valor.get('lastEvent')

            vnome = nome[0]
            # print(type(vnome),vnome)
            for hostid, name in vnome.items():

                if 'CT18' in name:
                    if eventos:
                        acionado = datetime.fromtimestamp(float(eventos.get("clock")))
                        acionado = acionado.strftime('%d/%m/%Y %H:%M:%S')
                        severidad = ''
                        severidade = eventos.get("severity")

                        if severidade == '5':
                            severidad = 'Desastre'
                        elif severidade == '4':
                            severidad = 'Alta'
                        elif severidade == '3':
                            severidad = 'Media'
                        elif severidade == '2':
                            severidad = 'Atencao'
                        elif severidade == '1':
                            severidad = 'Informacao'
                        elif severidade == '0':
                            severidad = 'Nao Classificada'

                        envio.write(
                            f'Hora: {acionado}\nHost: {name}\nEvento: {eventos.get("name")}\nSeveridade: {severidad}\n\n')
        envio.close()


if __name__ == "__main__":
    funcao = Funcoes()
    funcao.toner()
