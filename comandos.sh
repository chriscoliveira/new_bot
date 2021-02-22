#!/bin/bash


case $1 in
  'uptime')
    ssh root@10.18.1.7 /Scripts/uptimePDV.sh > /Scripts/envioTelegram.txt
    cat /Scripts/envioTelegram.txt
    ;;

  'memlivre')
    ssh root@10.18.1.7 /Scripts/memfreePDV.sh > /Scripts/envioTelegram.txt
    cat /Scripts/envioTelegram.txt
    ;;
  'limpamem')
    ssh root@10.18.1.7 /Scripts/PDV/limpamemoriapdv.sh > /Scripts/envioTelegram.txt
    cat /Scripts/envioTelegram.txt
    ;;
  'exibehora')
    ssh root@10.18.1.7 /Scripts/exibehora.sh > /Scripts/envioTelegram.txt
    cat /Scripts/envioTelegram.txt
    ;;
  'acertahora')
    ssh root@10.18.1.7 /Scripts/acertahora.sh > /Scripts/envioTelegram.txt
    cat /Scripts/envioTelegram.txt
    ;;
  'reiniciapdv')
    ssh root@10.18.1.7 /Scripts/reiniciaPDV.sh $2 > /Scripts/envioTelegram.txt
    cat /Scripts/envioTelegram.txt
    ;;
  'toner')
    ricoh = "1.3.6.1.4.1.367.3.2.1.2.24.1.1.5.1"
    samsung = ".1.3.6.1.4.1.236.11.5.1.1.3.22.0"
    List=impressoras.txt
    echo "" > /Scripts/envioTelegram.txt
    echo "Data e Horario: `date`" >> /Scripts/envioTelegram.txt
    cat $List | while read ip
    do
      snmpwalk -v 2c -c public $ip 1.3.6.1.4.1.367.3.2.1.2.24.1.1.5.1 | awk '{print "'$ip' " $4 "%"}' >> /Scripts/envioTelegram.txt
    done
    snmpwalk -v 2c -c public 10.18.2.203 .1.3.6.1.4.1.236.11.5.1.1.3.22.0 | awk '{print "'10.18.2.203' " $4 "%"}' >> /Scripts/envioTelegram.txt
    ;;
esac




