#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os
import subprocess
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

    def ping(ip):
        envio = open('envioTelegram.txt', 'w')
        file = open('listabuscapreco.txt')
        res = subprocess.call(['ping', '-c', '3', ip])
        if res == 0:
            envio.write(f'OK -> {ip}\n')
        elif res == 2:
            envio.write(f'\nOFF-LINE -> {ip}\n\n')
        else:
            envio.write(f'\nOFF-LINE -> {ip}\n\n')
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
                        acionado = datetime.fromtimestamp(
                            float(eventos.get("clock")))
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

    def eda_online():
        zapi = ZabbixAPI(server="http://10.131.0.30/zabbix")
        zapi.login("USUARIO_API", "tenda123")

        txt = open('envioTelegram.txt', 'w')
        grupos = zapi.hostgroup.get({"output": "extend"})

        manutencao = ['CT18EDA005', 'CT18EDA008', 'CT18EDA019', 'CT18EDA027']

        for grupo in grupos:
            # print(f'{grupo}\n')
            GroupId = grupo[u'groupid']
            GroupName = [u'name']
            hosts = zapi.host.get({"output": "extend", "search": "rub", "groupids": 32})

            contagem = 0
            stop = ''
            for host in hosts:
                if 'CT18EDA' in host[u'host']:
                    # txt.write(str(host))
                    itens = zapi.item.get({
                        "hostids": host["hostid"],
                        "output": "extend",
                    })
                    print(contagem)
                    for item in itens:
                        if 'RUB ping' in item[u'name']:
                            if item[u'lastvalue'] == '1':
                                contagem += 1
                                txt.write(
                                    f"\n{host[u'host']} - OK {datetime.fromtimestamp(int(item[u'lastclock']))}\n")
                            else:
                                contagem += 1
                                historys = zapi.history.get({
                                    "output": "extend",
                                    "itemids": item[u'itemid'],
                                    "sortfield": "clock",
                                    "sortorder": "DESC",
                                    "limit": 500
                                })
                                if 'CT18EDA0' + str(contagem).zfill(2) in manutencao:
                                    txt.write(f'\n***CT18EDA0{contagem} - MANUTENCAO\n')
                                else:
                                    txt.write(f'\nCT18EDA0{contagem}\n')
                                for history in historys:
                                    if history[u'value'] == '1':
                                        txt.write(
                                            f"        UP em {datetime.fromtimestamp(int(history[u'clock']))}\n")
                                        break
                if contagem == 38:
                    stop = 1
            if stop == 1:
                break

        txt.close()


if __name__ == "__main__":
    funcao = Funcoes()
    funcao.ping('10.18.2.160')
