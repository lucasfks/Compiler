# Compiler

Projeto da disciplina de Compiladores.

Vídeo do projeto:
https://youtu.be/FXplTqC437M

Itens que foram entregues no projeto:
- Possui 3 tipos de dados (string, int e float) 	
- Possui a instrução de decisão (if/else)	
- Possui estrutura de repetição	"while"
- Verifica Atribuições com compatibilidade de tipos (semântica) 	
- Possui operações de Entrada e Saída	
- Aceita números decimais (float)
- Verifica declaração de variávies (não usar variáveis que não foram declaradas)	
- Verifica se há variáveis declaradas e não-utilizadas (warning)	
- Geração da linguagem destino C.


## Como executar compilador
Primeiramente, deve-se baixar o repositório e, dentro do diretório onde se encontram os arquivos do repositório, deve-se rodar a instrução: 

`pip install -r requirements.txt`

Tendo feito isso, para executar o compilador deve-se utilizar o seguinte comando:

 Mac/Linux: `python compilador.py <nome_do_arquivo>.isi`
 
 Windows:   `py compilador.py <nome_do_arquivo>.isi`
