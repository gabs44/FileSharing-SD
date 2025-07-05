# Projeto - Sistema de compartilhamento P2P

## Sumário

- [Equipe](#equipe)
- [Descrição da Atividade](#descrição-da-atividade)
- [Linguagem de Programação](#linguagem-de-programação)
- [Estrutura](#estrutura)
- [Executando o projeto](#executando-o-projeto)
- [Comandos no cliente](#comandos-no-cliente)
- [Comunicação entre clientes](#comunicacao-entre-clientes)

## Equipe

- Gabriella Braga Gomes
- Maria Clara Ramalho Medeiros

## Descrição da Atividade

Este projeto, desenvolvido para a disciplina de Sistemas Distriuídos, implementa um sistema simples de compartilhamento de arquivos entre clientes, utilizando sockets em Python, baseado no modelo Napster.

## Linguagem de Programação

A implementação foi feita utilizando **Python 3**, escolhida por sua simplicidade na manipulação de arquivos. 

## Estrutura

- `server.py`: servidor central
- `client.py`: cliente compartilhador
- `run.sh`: script para facilitar execução
- `public/`: pasta com arquivos públicos
- `downloads/`: pasta com arquivos baixados


## Executando o projeto

1. Coloque arquivos na pasta `./public/` para que o cliente compartilhe com a rede.
2. Abra dois terminais.
3. Em um terminal, rode:

```
./run.sh
# Escolha a opção 1 para iniciar o servidor
```

4. Em outro terminal, rode:

```
./run.sh
# Escolha a opção 2 para iniciar o cliente
```


## Comandos no cliente

- `SEARCH <termo>`: busca arquivos com esse nome
- `DELETE <arquivo>`: remove o arquivo da rede (não apaga do disco)
- `LEAVE`: desconecta do servidor e encerra o cliente
- `DOWNLOAD`: baixa arquivo entre clientes

## Comunicação entre clientes

Se um cliente quiser baixar um arquivo listado, deve ser executado o seguinte comando:

```
DOWNLOAD <ip> <arquivo> [inicio] [fim]
```


