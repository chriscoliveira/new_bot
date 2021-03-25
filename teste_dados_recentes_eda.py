#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv, os, subprocess
from zabbix_api import ZabbixAPI
import json
from datetime import datetime, timedelta
import time


def historico_eda():
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
                                f"\n{host[u'host']} - ultimo UP "
                                f"{datetime.fromtimestamp(int(item[u'lastclock']))}\n")
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
                                txt.write(f'\n{item[u"itemid"]} CT18EDA0{contagem} - MANUTENCAO\n')
                            else:
                                txt.write(f'\n{item[u"itemid"]} CT18EDA0{contagem}\n')
                            for history in historys:
                                if history[u'value'] == '1':
                                    txt.write(
                                        f"\t{host[u'host']} - ultimo UP "
                                        f"{datetime.fromtimestamp(int(history[u'clock']))}\n")
                                    break
            if contagem == 38:
                stop = 1
        if stop == 1:
            break

    txt.close()


if __name__ == '__main__':
    historico_eda()
