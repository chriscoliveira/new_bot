#!/bin/bash
#
#
# Este script limpa o Cache da Memória RAM sempre que a memória livre estiver abaixo de $MEM_MIN
# No caso deixei pra limpar o cache sempre que a memória livre estiver abaixo de 1GB, adaptar às suas necessidades
# Eu deixo este script no cron do root para executar a cada hora, e ele só vai limpar o cache quando for necessário
#
# Escrito por Fernando B. Giannasi - março/2013
#
# Referências: http://blog.philippklaus.de/2011/02/clear-cached-memory-on-ubuntu/
#              http://www.vivaolinux.com.br/dica/Limpando-a-memoria-cache-no-Linux


# Informações da memória
MEM_LIVRE=`cat /proc/meminfo | grep "^MemFree" | tr -s ' ' | cut -d ' ' -f2` && MEM_LIVRE=`echo "$MEM_LIVRE/1024.0" | bc`
MEM_TOTAL=`cat /proc/meminfo | grep "^MemTotal" | tr -s ' ' | cut -d ' ' -f2` && MEM_TOTAL=`echo "$MEM_TOTAL/1024.0" | bc`

MEM_MIN=`echo 1024`

# Só funciona como root, se não for root precisaremos usar o sudo
SUDO=`which sudo`
if [ "`whoami`" == "root" ]; then ROOT=true; fi
if [ ! "`which sudo`" ] && [ !$ROOT ]; then echo "Não é o superusuário e o SUDO não foi encontrado"; exit 1; fi


# Finalmente limpando o Cache...
if [ "$MEM_LIVRE" -le "$MEM_MIN" ]
then
    echo "Efetuando limpeza do Cache da memória..."
    if [ $ROOT ]; then sync; echo 3 > /proc/sys/vm/drop_caches; else $SUDO sync; echo 3 | $SUDO tee /proc/sys/vm/drop_caches > /dev/null; fi
    MEM_APOS=`cat /proc/meminfo | grep "^MemFree" | tr -s ' ' | cut -d ' ' -f2` && MEM_APOS=`echo "$MEM_APOS/1024.0" | bc`
    echo "Memória total instalada: $MEM_TOTAL MB"
    echo "Memória livre antes: $MEM_LIVRE MB"
    echo "Memória livre após: $MEM_APOS MB"

else
    echo "Não é necessário limpar o Cache da memória"
fi

exit 0
