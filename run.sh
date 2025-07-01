#!/bin/bash

echo "=== Compilador e Executor P2P ==="
echo "1 - Iniciar servidor"
echo "2 - Iniciar cliente"
echo "3 - Sair"
read -p "Escolha uma opção: " option

if [ "$option" == "1" ]; then
    echo "Iniciando servidor..."
    python3 server.py
elif [ "$option" == "2" ]; then
    echo "Iniciando cliente..."
    python3 client.py
else
    echo "Saindo..."
fi