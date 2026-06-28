# Prompt Para Replicar A Arquitetura Backend (DDD & Clean Architecture)

Você é um arquiteto sênior de backend especialista em Node.js e TypeScript. Sua tarefa é criar a estrutura base de uma aplicação escalável utilizando Domain-Driven Design (DDD) e Clean Architecture. O objetivo agora não é focar em qual framework HTTP ou ORM será utilizado, mas sim estabelecer o blueprint conceitual e de domínio da aplicação.

Você deve implementar a fundação do código com um domínio totalmente neutro (use exemplos como **Order**, **Product**, **Customer**, **Tenant**, **Item**), reproduzindo as seguintes estratégias e padrões arquiteturais:

## Filosofia Arquitetural e Camadas
A aplicação deve ser estritamente dividida em camadas, respeitando a Regra de Dependência: o código das camadas internas não pode saber absolutamente nada sobre as camadas externas.

- Domain (Enterprise Layer): O coração da aplicação. Contém as Entidades (Entities), Objetos de Valor (Value Objects) e as regras de negócio puras. Não possui nenhuma dependência externa, bibliotecas de terceiros ou frameworks.

- Application (Use Cases Layer): Orquestra o fluxo de dados. Contém os Casos de Uso (Use Cases) e as interfaces (contratos) dos Repositórios. Importa do Domínio, mas não conhece banco de dados ou rotas web.

- Infrastructure (Adapters & External Layer): A camada mais externa. Implementa os contratos definidos na camada de Application. É aqui que vivem os controladores HTTP, a persistência real no banco de dados, integrações com APIs externas e serviços de mensageria.

## Modelagem de Subdomínios
O design deve prever a divisão do sistema em subdomínios, refletindo os setores do problema de negócio:

- Core Subdomains: O coração do negócio, a lógica principal que traz valor à aplicação.

- Supporting Subdomains: Áreas que dão suporte ao Core, necessárias para o funcionamento, mas que não são o diferencial do sistema.

- Generic Subdomains: Funcionalidades comuns (como envio de e-mail ou autenticação padrão) que poderiam ser terceirizadas ou substituídas por soluções de prateleira.

## Aggregates e Watched Lists
- Aggregates: Modele agrupamentos lógicos de entidades que devem ser tratadas como uma única unidade de consistência transacional. Uma entidade será o Aggregate Root. Operações de persistência só devem acontecer através do Aggregate Root.

- Watched Lists: Para lidar com coleções de entidades filhas dentro de um Aggregate (ex: itens de um pedido, anexos de um documento), implemente o padrão de WatchedList. Essa estrutura deve rastrear quais itens foram adicionados, removidos ou atualizados na lista em memória, permitindo que a camada de infraestrutura saiba exatamente o que persistir no banco de dados sem precisar deletar e recriar todos os registros.

## Tratativa de Erros Funcional (Padrão Either)
É estritamente proibido utilizar throw new Error(), return null ou return undefined para controle de fluxo de regras de negócio ou validações esperadas (como "Recurso não encontrado" ou "Acesso negado").

- Implemente o padrão Result / Either (Left e Right).

- Casos de uso devem sempre retornar um Either.

- Se for sucesso, retorna Right(dados).

- Se for falha, retorna Left(CustomError).

- Crie classes de erro de domínio específicas (ex: ResourceNotFoundError, NotAllowedError).

## Domain Events (Eventos de Domínio)
Para evitar o acoplamento de lógicas secundárias (side-effects) dentro do fluxo principal de um caso de uso, implemente um mecanismo de Eventos de Domínio.

- Quando um Aggregate Root sofre uma alteração importante, ele deve registrar um evento (ex: ItemCreatedEvent).

- O despacho desses eventos só deve ocorrer após a persistência bem-sucedida do Aggregate no banco de dados.

- O sistema deve possuir assinantes (Subscribers) que escutam esses eventos para engatilhar outras ações (como enviar notificações ou atualizar outras tabelas de leitura).

## Estrutura de Diretórios Esperada
Crie a fundação em código baseada nesta estrutura:

```text
src/
  core/
    either.ts                 # Implementação do padrão Left/Right
    entities/
      entity.ts               # Classe base para entidades com geração de ID
      aggregate-root.ts       # Classe base para Aggregates
      unique-entity-id.ts     # Value Object para identificadores
    events/
      domain-event.ts         # Interface para eventos
      domain-events.ts        # Publisher/Subscriber de eventos (Dispatcher)
      event-handler.ts
    logic/
      watched-list.ts         # Classe base para coleções observáveis
  
  domain/
    forum/                    # (Exemplo de Subdomínio Core)
      enterprise/             # Camada de Domínio
        entities/
          question.ts
          answer.ts
        value-objects/
          slug.ts
        events/
          question-best-answer-chosen-event.ts
      
      application/            # Camada de Aplicação
        repositories/
          questions-repository.ts # Apenas a interface
          answers-repository.ts
        use-cases/
          choose-best-answer.ts
          choose-best-answer.spec.ts
          errors/
            resource-not-found-error.ts
            not-allowed-error.ts

  test/
    repositories/
      in-memory-questions-repository.ts # Implementação em memória para testes rápidos
      in-memory-answers-repository.ts
    factories/
      make-question.ts
```
## Regras de Testes
- A camada de Aplicação e Domínio deve ser testada de forma unitária e extremamente rápida, sem depender de banco de dados real.

- Implemente In-Memory Repositories dentro de uma pasta de test/ para simular o comportamento do banco de dados durante os testes dos Casos de Uso.

- Os testes devem validar o retorno do padrão Either (ex: expect(result.isRight()).toBe(true)).

## Convenções Essenciais
- Prefira a composição à herança excessiva.

- Tipagem estrita: evite o uso de any em todo o projeto.

- Classes de domínio (Entities) não devem ter getters/setters públicos para tudo; crie métodos que representem a intenção do negócio (ex: em vez de setStatus('paid'), use pay()).

- Isole a infraestrutura.

# Infraestrutura de Nuvem e Autenticação (Azure Easy Auth)
A aplicação será hospedada em um Azure Web App utilizando o método Easy Auth (App Service Authentication). O banco de dados utilizado será o SQL Server. A LLM deve seguir estritamente as regras abaixo para acomodar esse ambiente:

1. Autenticação (Zero-Trust JWT Local)
É estritamente proibido implementar fluxos de login, registro de senhas, validação de JWT manual, ou utilizar bibliotecas como @fastify/jwt, passport ou bcrypt. A autenticação já foi resolvida pela infraestrutura da nuvem.

Implemente um Hook/Middleware no Fastify (na camada de Infraestrutura) responsável por interceptar as requisições, ler os headers específicos do Azure Easy Auth (como o header X-MS-CLIENT-PRINCIPAL decodificado em Base64) e extrair o contexto do usuário (ex: userId, email, roles).

Esse hook deve popular o objeto request.user do Fastify de forma tipada (usando Declaration Merging do TypeScript).

Os Casos de Uso (Application Layer) nunca devem acessar os headers do Azure. Eles devem receber as informações do usuário (como userId ou tenantId) já limpas através de seus DTOs (Data Transfer Objects) de entrada passados pelos Controllers.

2. Banco de Dados (SQL Server via Prisma)
O schema.prisma deve ser configurado com o provider = "sqlserver".

Respeite as tipagens de banco de dados do SQL Server ao criar os models do Prisma (ex: uso de @db.UniqueIdentifier para UUIDs, se aplicável).

Mantenha o padrão de isolamento absoluto: o Prisma só pode ser acessado dentro das classes concretas de Repositório (src/infra/database/prisma/repositories).

3. Ambiente e Variáveis
O schema do Zod de validação de ambiente (env.ts) deve prever as variáveis de ambiente padrões do Azure App Service, como process.env.WEBSITE_SITE_NAME (opcional, para saber se está em cloud) e garantir que a DATABASE_URL esteja no formato aceito pelo driver do SQL Server.

🧠 Registro de Decisões e Retroalimentação da IA (Living Docs)
Para garantir que novos agentes de contexto ou sub-rotinas MCP entendam o estado da aplicação sem a necessidade de re-ler toda a codebase, o agente DEVE manter um diário técnico de arquitetura ativo no repositório.

Regras de Documentação Ativa:
READMEs Locais por Camada e Subdomínio: Cada subdomínio dentro de src/domain/*, bem como as pastas principais de src/application/* e src/infra/*, deve conter um arquivo README.md minimalista mantido pela IA.

Atualização Compulsória: Sempre que o agente criar um novo Caso de Uso (Use Case), modelar um novo Agregado (Aggregate Root), alterar o schema.prisma, ou expor uma nova rota no Fastify, ele deve atualizar o arquivo correspondente explicando:

O que foi feito: (ex: "Criado o Caso de Uso de Criação de Pedido com suporte a itens múltiplos")

A decisão técnica: (ex: "Utilizado o padrão WatchedList na camada de domínio para gerenciar a adição/remoção dos itens do pedido, otimizando a persistência no Prisma")

Contratos e Domínio: Uma amostra rápida do DTO de entrada/saída esperado, as entidades envolvidas ou os Eventos de Domínio (Domain Events) disparados por essa ação.

Log de Decisões Globais: Na raiz do projeto back-end (ex: apps/api/ ou /), manter um arquivo ARCHITECTURAL_DECISIONS.md no formato compactado de bullet points com as grandes definições estruturais, limites de contexto (Bounded Contexts) e mapeamento de integrações externas realizadas por Sprint.