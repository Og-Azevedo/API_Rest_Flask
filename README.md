# Desafio Mesha

## Acesso
Esse sistema se encontra em um container Docker no seguinte endereço:
IMPORTANTE: Faça o login no sistema como administrador. Use  o login: "admin" e senha: "admin". 
se precisar de ajuda para isso basta [clicar aqui para ir para documentação referente a esse processo.](https://documenter.getpostman.com/view/19989248/UVyytsdH#97319513-5c24-4f2b-91a7-caa4cbaa03bb) 

    docker push ogazevedo/desafio-mesha:tagname



## Documentação
Para saber mais informações sobre os ENDPOINTS desse gerenciador de recursos acesse:
[Link para documentação](https://documenter.getpostman.com/view/19989248/UVyytsdH#9c877bbb-7869-415e-82ac-dc04c9a571e5)

## Objetivo
Desenvolver um sistema gerenciador de recursos que cumprisse os seguintes requisitos:

 - Ter 2 tipos de usuários: Administradores e Usuários "simples";
 - Possuir um modelo de recurso com seus respectivos atributos;
 - Um CRUD para usuários comuns;
 - Um CRUD para os recursos;

**Os administradores do gerenciador deve ter:**

 - Registrar novos recursos no sistema;
 -  Atualizar Recursos no sistema; 
 -  Deletar Recursos do sistema;   
 -  Deletar usuários;

**Os usuários simples devem poder:**

 - Listar os recursos disponíveis no sistema;
-   Alocar recursos por um determinado tempo.


# Solução

Desenvolvi um sistema baseado em uma rede de hotéis. Toda estrutura é basicamente composta por 3 tipos de elementos: Hotel, Usuário simples, Administradores. Em seguida você encontra mais detalhes sobre cada um deles:
### Hotel
Cada recurso do sistema seria correspondente a uma unidades de cada hotel da rede. O recurso de hotel possui os seguintes atributos:

 - Id do hotel;
 - Nome;
 - Estrelas;
 - Preço da diária;
 - Cidade;
 - Checkin / Checkout
 - Hospede;
 
 Abaixo segue um exemplo:
 
    {
      "hotel_id": "branco",
      "nome": "Branco Hotel",
      "estrelas": 3.3,
      "diaria": 550.2,
      "cidade": "Maceió",
      "checkin": "2055-11-01",
      "checkout": "2023-02-01",
      "hospede": "user11"
    }

### Usuário simples
Esse tipo de usuário representa um hóspede, logo seu poder de manipular as informações no sistema é bem restrito. Basicamente ele consegue visualizar os hotéis disponíveis e reservar um intervalo de data em seu nome. Por mais que ele não tenha acesso a mais ações, os usuários do tipo administrador consegue executar as seguintes ações com esse tipo de usuário: Ler, Criar, Editar, Deletar. Segue abaixo seus atributos: 

 - Id do usuário;
 - Login;
 - Senha;
 - Tipo;
 
 Abaixo segue um exemplo:
 
    
    {
      "user_id": 2,
      "login": "user2",
      "senha": "123456",
      "tipo": "usuario_simples"
    }

### Usuário Administrador
Esse tipo de usuário é capaz de fazer todos os tipos de manipulações com qualquer recurso dentro do sistema, seja ele hotel, usuário simples, administradores. Para ficar mais clara a amplitude das ações disponíveis para esse tipo de usuário, vou listar abaixo:

##### Hotéis
- Acessar lista de hotéis
- Acessar informações de hotel
- Criar novo hotel
- Editar informações de hotel
- Deletar hotel
- Reservar hotel

##### Usuários Simples
- Acessar lista de usuários
- Acessar informações de usuário
- Editar informações de usuário
- Deletar usuário
- Logar usuário
- Deslogar usuário
- Cadastrar novo usuário

##### Administradores
- Acessar lista de admins
- Acessar informação de admin
- Deletar admin
- Logar admin
- Deslogar admin
- Cadastrar novo admin


Segue abaixo seus atributos: 

 - Id do usuário;
 - Login;
 - Senha;
 - Tipo;
 
 Abaixo segue um exemplo:
 
    
    {
      "admin_id": 2,
      "login": "admin",
      "senha": "123456",
      "tipo": "usuario_admin"
    }

