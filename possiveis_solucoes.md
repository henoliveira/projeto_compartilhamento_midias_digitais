# Estrutura dos nós
Todos os nós armazenam:
- X arquivos.
- Y vizinhos.

Todos os nós devem ser capaz de se comunicar por meio dos vizinhos.

```mermaid
flowchart LR
    1((1)) --> 2((2)) --> 3((3)) --> 5((5))
    3 -->  4((4)) --> 2
    5 --> 1 --> 4 --> 7((7))
    6((6)) --> 5
    1 --> 6
    7 --> 6
```

# Solução 1 - Varredura com id de objetivo
Nessa solução, levamos em consideração que na empresa existem dois sistemas. 
Um para compartilhamento de arquivos, que seria o que estamos desenvolvendo.
E outro sistema para comunicação, como Email, Slack, etc.

Nesse caso, o sistema de compartilhamento de arquivos não precisaria ter acesso
à lista global de arquivos do sistema, seja ela por um servidor centralizado, ou
por uma varredura periódica na rede toda em busca da lista atualizada de arquivos.

# Solução 2 - Varredura total
Essa outra solução consiste em fazer uma varredura total dos nós assim que o 
usuário abrir o sistema, buscando em cada um dos nós a lista de arquivos salvos, 
e passando por cada um dos vizinhos armazenados em cada nó, e como no algoritmo de 
dijkstra deveremos fazer uma espécie de conta para não passar no mesmo nó mais de 
uma vez. 

E então, após passar por todos os nós, devemos retornar para o nó que foi
iniciado a lista de todos os arquivos existentes na rede e seus respectivos donos,
e a partir disso o usuário pode solicitar o arquivo que quiser.

# Solução 3 - Servidor de indexação
Nesta solução teríamos um servidor onde seria armazenado a lista de todos os
arquivos existentes na nossa rede e seus respectivos donos.
