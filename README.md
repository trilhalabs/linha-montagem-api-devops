# 🚀 Laboratório Devops

> O projeto trilhandosaberlabs é uma iniciativa para aprendizado constante, voltado para o modelo hands-on. Este documento tem o grande objetivo de disponibilizar um passo a passo completo para configurar sua máquina local e as integrações, para ter uma referência para o estudo. A sugestão é você criar seu projeto, baseado nos insights obtidos neste laboratório. Vamos colocar a mão na massa! Este laboratório gera custos, mesmo usando a Free Tier da AWS. Lembre-se de ativar os alertasde Budget na sua conta para que os gastos fiquem com maior controle!

- Foco em Python/Django/Django-Restframework, Docker, Pipeline CI/CD, Terraform e AWS

## 🧾 Projeto linha-montagem-api-devops

| Software /Linguagem /Serviços  | Observação  |
| :---------------: |:---------------:|
| Django      | aplicação desenvolvida na linguagem Python através do framework Django |
| Django-RestFramework      | framework Django para desenvolver Rest APIs |
| Gitlab   | repositório privado de fontes e pipeline CI/CD   |
| Github   | repositóriopúblico do projeto  |
| Docker   | gerenciamento de containers  |
| Terraform   | IaaC - Infra as a Code  |
| AWS   | provedor de Cloud Pública  |
| linha-montagem-app-api-proxy   | projeto complementar e necessário para este labortatório  |

- Projeto original

>> ▷ Acesse: <https://github.com/trilhalabs/linha-montagem-api-devops>

## ⚙ Configurações iniciais

> Procedimentos para configuração do terminal local e das ferramentas de integração e cloud pública

### Pré-requisitos

#### Git e Docker

- Criar estrutura local do projeto complementar **linha-montagem-app-api-proxy**
- E gerar a imagem Docker **proxy_lm**
- Este projeto é a camada de arquivos estáticos definido como boa prática para projetos Django (atualmente não possui nenhum arquivo estático para o frontend - fica de desafio 😉)

  ```shell
  git clone git@github.com:trilhalabs/linha-montagem-app-api-proxy.git
  cd linha-montagem-app-api-proxy
  docker build -t proxy_lm .
  ```

- Criar estrutura local do projeto principal **linha-montagem-api-devops**

  ```shell
  git clone git@github.com:trilhalabs/linha-montagem-api-devops.git
  ```

#### Repositórios

- 🔑 É preciso ter a integração das chaves SSH dentro dos repositórios Gitlab e Github. Leia mais em <https://docs.github.com/pt/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key>

- Projetos serão criados nos repositórios Gitlab com ==mirroring== para o Github
- Usaremos o Gitlab para repositório e execução da pipeline, mas com as configurações abaixo, será refletido (mirroring) no Github, para quem prefere manter seus fontes neste repositório. Eu gosto de manter todos no Github!
>>
- **GITHUB**
  - No Github, crie os projetos vazios (sugere-se manter o mesmo nome do projeto)
    - Projeto 1: **linha-montagem-app-api-proxy**
    - Projeto 2: **linha-montagem-api-devops**
  >>
  - Crie token de integração
    - No menu com a foto do seu usuário (lado superior direito), entre no menu Settings
    - Developer Settings / Personal access tokens
    - Crie um token pessoal
    - Este personal token será usado na integração e mirroring do Gitlab para o Github, mantendo atualizado este projeto
  >>
- **GITLAB**
  - Crie os projetos
    - Projeto 1: **linha-montagem-app-api-proxy**
    - Projeto 2: **linha-montagem-api-devops**
  >>
  - Em cada projeto, configure:
    - Menu Settings / Repositories / Expand Mirroring
    - Fazer o link com o github
      - Abaixo, troque os campos correspondentes ao seu usuráio e token do Github
      - Exemplo Projeto 1:
        - <https://"seu-usuario":"coloque-seu-personal-token-github"@github.com/"seu-usuário"/linha-montagem-app-api-proxy.git>
        - Password: Informar novamente o "seu-personal-token-github"

      - Exemplo Projeto 2:
        - <https://"seu-usuario":"coloque-seu-personal-token-github"@github.com/"seu-usuário"/linha-montagem-api-devops.git>
      - Password: Informar novamente o "seu-personal-token-github"
  >>
  - Testando sincronização
    - Máquina Local

      ```shell
      #validar a comunicação local com os repositórios através da chave SSH
      ssh -T git@github.com 
      ssh -T git@gitlab.com
      ```

      - No projeto **linha-montagem-app-api-proxy**

        ```shell
        # inicialização do projeto proxy e teste de push com sincronização
        cd linha-montagem-app-api-proxy
        git init
        git checkout -b develop/setup-proxy
        git add .
        git commit -m "commit inicial proxy - terminal local"
        git remote add gitlab git@gitlab.com:"ssh-do-seu-projeto-no-gitlab".git
        git push gitlab master
        ```

      - No projeto **linha-montagem-api-devops**

        ```shell
        # inicialização do projeto linha de montagem e teste de push com sincronização
        cd linha-montagem-api-devops
        git init
        git checkout -b develop/setup-api
        git add .
        git commit -m "commit inicial api - terminal local"
        git remote add gitlab git@gitlab.com:"ssh-do-seu-projeto-no-gitlab".git
        git push gitlab master
        # 🍀 conferir no Gitlab e Github a subida do projeto com o commit inicial 
        ```

    - Retornando ao Gitlab: configurações finais para versionamento e branches
  
      - No projeto **linha-montagem-app-api-proxy**
        - Menu Repository > Protected Branches
          - Protect a branch: criar "*-release"
          - Selecionar "mantainers"
        - Menu Repository > Protected Tags
          - Protected tag: criar "*-release"
          - Selecionar "mantainers"

      - No projeto **linha-montagem-app-api-devops**
        - Menu Repository > Branches > New Branch
          - name: production
        - Menu Settings > Repository> Expand Protected Branches
          - branch: production
          - Allowed to merge: Mantainers
          - Allowed to push: Mantainers

### Preparando o ambiente local

- **Ambiente virtual**

  ```shell
  cd linha-montagem-api-devops
  python -m venv env
  ls -la
  pwd
  #<caminho-do-projeto>
  source <caminho-do-projeto>/env/Scripts/activate
  ```

- **Django e Django Framework**

  ```shell
  #dentro do diretorio da aplicacao linha-montagem-app-api
  cd env/Scripts/
  python.exe -m pip install --upgrade pip #garantir versão mais atualizada do Pip
  cd ../env/
  pip install django --user #--user é opcional (somente se der erro de permissionamento)
  pip install djangorestframework --user #--user é opcional (somente se der erro de permissionamento)
  django-admin --version
  ```

- **Imagem docker**

  > Documentação <https://docs.docker.com/engine/reference/commandline/build/>

  ```shell
  #dentro do diretorio da aplicacao 
  cd ../linha-montagem-api-devops
  docker-compose build
  ```

- **Tabelas do banco de dados**

  ```shell
  docker-compose run app sh -c "python manage.py makemigrations core"
  #em caso de erro, executar
  #docker-compose run app sh -c "python manage.py migrate"

  docker-compose run app sh -c "python manage.py test && flake8"
  docker-compose run app sh -c "python manage.py createsuperuser"
  # Ex: email: seu-mail@gamil.com
  # Ex: password: senhasecreta

  ```

- **Testando a aplicação**

  ```shell
  #
  # Para os testes, consulte as sessões abaixo "No Container" e "No Browser" para garantir que tudo está 
  # configurado corretamente
  #

  #Teste 1: garantir teste de linha-montagem-api-devops
  docker-compose up --build
  
  #Teste 2: garantir teste de linha-montagem-api-devops através da camada proxy (solução final)
  docker-compose -f docker-compose-proxy.yml up

  # ◉ para validar, veja sessão mais abaixo "No Browser"
  ```

- **No container**

  ```shell
  docker ps
  #sem "entrar" no container da aplicação
  docker exec -it linha-montagem-api-devops_app_1 sh -c "ls -la" 
  #entrando no container no DB
  docker exec -it linha-montagem-api-devops_db_1 bash
  psql -V
  psql -h 127.0.0.1 -U postgres -d app
  \dt #listar tabelas
  \d tabela
  select * from core_user;
  \q #sair
  ```

- **No browser**

  - <http://localhost:8000/>
  - <http://localhost:8000/api/montagem/>
  - <http://localhost:8000/api/user/create/>
  - <http://localhost:8000/api/montagem/tags>
    - haverá falha de autorização: "HTTP 401 Unauthorized"
  - <http://localhost:8000/api/user/token/>
    - Request Headers
      - "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      - ModHeader (Chrome extension)
      Autorization
      token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  - <http://localhost:8000/api/montagem/tags>
  - <http://localhost:8000/api/montagem/atributos/>
  - <http://localhost:8000/api/montagem/montagens/>
  - <http://localhost:8000/api/montagem/montagens/1/upload-image/>
    - <http://localhost:8000/media/uploads/montagem/10206896-e87d-4852-af9c-51762fa8a947.png>
  - <http://localhost:8000/api/montagem/atributos/?assigned_only=2>
    - lista os atributos que aparecem em uma linha de montagem
  - <http://localhost:8000/api/montagem/atributos/?assigned_only=0>
    - lista todos os atributos em linha de montagem
  - <http://localhost:8000/api/montagem/tags/?assigned_only=4>
    - lista as tags que aparecem em uma linha de montagem
  - <http://localhost:8000/api/montagem/tags/?assigned_only=0>
    - lista todos as tags em linha de montagem

## ☁ AWS

> Criação de usuários programáticos para execução do laboratório. Caso você já tenha uma conta com usuários existentes e queira usá-los, sem problema algum. Só atenção ao atachar as Policies mencionadas mais abaixo.

- **AWS Console**
  >>
  - ▻ **IAM**
    - Menu IAM > Policies > Create policy
      - ▻ **Name:** LinhaMontagemAppApi-ProxyCIPushECR
        - Libera os acessos para enviar a imagem docker para repositório ECR
        - Template Json: <https://github.com/trilhalabs/linha-montagem-api-devops/blob/master/templates/user-proxy-iam-policy.json>
        - Procurar no arquivo por "preencha-nome-do-seu-repositorio-proxy-ecr"
        - Substituir pelo valor correspondente do repositório proxy

      - ▻ **Name:** LinhaMontagemAppApi-Devops
        - Template Json: <https://github.com/trilhalabs/linha-montagem-api-devops/blob/master/templates/user-iam-policy.json>
        - Procurar no arquivo por "preencha-nome"
        - Substituir pelos valores correspondentes

    - Menu IAM > Users > Add user
      - ▻ **Name:** useradm
        - Criar um grupo chamado "administradores"
        - Adicionar ao grupo as Policies:
          - (AWS) *AdministratorAccess*
          - (Managed user) Name: *ForceMFA* <https://github.com/trilhalabs/linha-montagem-api-devops/blob/master/templates/user-mfa-policy.json>
        - Este usuário poderá ser usado localmente para testes com o Terraform

      - ▻ **Name:** linha-montagem-app-api-proxy
        - Adicionar a Policy existente **LinhaMontagemAppApi-ProxyCIPushECR**
        - Este usuário será usado no Gitlab para execução do job de Push das imagens no repositório ECR

      - ▻ **Name:** linha-montagem-app-api-devops
        - Adicionar a Policy existente **LinhaMontagemAppApi-Devops**
        - Este usuário será usado no Gitlab para execução a pipeline completa
  >>
  - ▻ **EC2**
    - Crie uma nova Key-pair: **montagem-app-api-devops-bastion**
    - Caso já tenha e queira reusar a sua key-pair, será necessário ajustar a referência no arquivo "deploy/variables.tf", variável "bastion_key_name"
  >>
  - ▻ **S3**
    - Criar Bucket para armazenar os scripts do terraform
    - Name (único global): linha-montagem-app-api-"prefixo-unico"
    - Region: us-east-1
    - Block all public access: true
    - Bucket Versioning: true
  >>
  - ▻ **Elastic Container Repository - ECR**
    - criar um repositório para o código da aplicação **API**
    - name: linha-montagem-app-api-devops
    >>
    - criar um repositório para o código da aplicação **PROXY**
    - name: linha-montagem-app-api-proxy
  >>
  - ▻ **DynamoDB**
    - objetivo é garantir que apenas uma aplicação Terraform esteja rodando ao mesmo tempo
    - name: linha-montagem-app-api-devops-tf-state-lock
      - dica: tf = TerraForm
    - Primary Key: LockID
      - garanta a diferença entre letras maiúsculas e minúsculas

## Gerenciar segredos

> Os acessos locais para utilizar o AWS-CLI são configurados normalmente pelo comando "aws configure". Este comando irá configurar os arquivos "~/.aws/config" e "~/.aws/credentials". O laboratório deverá funcionar normalmente. Porém, abaixo coloquei um método que uso, que entendo gerar mais segurança no gerenciamento das chaves e segredos. O AWS-VAULT irpa gerar o arquivo "~/.aws/config" e terá um controle de sessão sob suas chaves, não gerando um arquivo acessível com as credenciais. No lab, usarei o AWS-VAULT.

### Localmente

- 🔐 Terminal Local: **AWS-Vault**
  - Gerenciador de segredos da AWS para aumentar a segurança no manuseio das chaves em sua máquina local
  - Gera credenciais temporarias na máquina
  - Documentação <https://github.com/99designs/aws-vault>

  ```shell
  aws-vault add <seu-user-iam-com-token>
  #Acces key:
  #Secret key:
  nano ~/.aws/config
  #Completar no conteúdo do arquivo (sem o "#")
  #[profile <user-iam>]
  #region = us-east-1
  #output = json
  #mfa_serial = <ARN-MFA-AWS>

  aws-vault exec <seu-user-iam-com-token> --duration=2h
  #Token
  unset $AWS_VAULT
  unset AWS_VAULT

  #Validar sessão
  aws-vault list
  aws-vault exec <user-iam> -- aws s3 ls
  ```

### Integrações

- **Gitlab**
  - Gerenciar segredos através de variáveis de ambiente.
  - Menu Settings > CI/CD > Variables - Expand
    - **AWS_ACCESS_KEY_ID** ▻ chave de acesso defiida para  usuário iam "linha-montagem-app-api-devops"
    - **AWS_DEFAULT_REGION** ▻ para este lab usamos "us-east-1"
    - **AWS_SECRET_ACCESS_KEY** ▻ chave de segurança do usuário iam "linha-montagem-app-api-devops"
    - **ECR_REPO** ▻ informar URI do repositório ECR
    - **TF_VAR_db_password** ▻ usar valor correspondente do arquivo "/deploy/terraform.tfvars"
    - **TF_VAR_db_username** ▻ usar valor correspondente do arquivo "/deploy/terraform.tfvars"
    - **TF_VAR_django_secret_key** ▻ usar valor correspondente do arquivo "/deploy/terraform.tfvars"
  - Todas "Protected" e "Masked" iguais a "Tue"

## 🛠 Terraform

- **Gitlab**

  >> Esta ação no Gitlab é necessária para "empurrar" (push) a imagem do Proxy para o repositório ECR.Isto é necessário, pois quando a pipeline do projeto principal (API) rodar, ela usará a imagem do proxy no processamento

  - Projeto **linha-montagem-app-api-proxy**
    - Disparando a pipeline
      - Menu Merge Requests
      - Botão New merge request
      - Source branch: develop/setup-proxy (se criou outra branch, informar a mais atual com os commits)
      - Target branch: master
      - Aprove e execute o Merge Request
      - Isso irá disparar o primeiro job **Build**
      - Após sucesso, vá até a console AWS, e confira o repositório linha-montagem-app-api-proxy. Deve haver uma imagem tagueada como "Dev"

      - Faça um novo Merge Request, para gerar a imagem de release
        - Para mais detalhes do que está sendo feito, leia sobre versionamento semântico <https://semver.org/>
      - Menu Repository > Branches > Create: "1.0-release"
        - From master
        - Irá disparar  os jobs **Build** e **Push Dev**

      - Menu Repository > Tags > Create: "1.0.0-release"
        - Create from branch: 1.0-release
        - Irá disparar  os jobs **Build** e **Push Release**

      - Após sucesso, vá até a console AWS, e confira o repositório linha-montagem-app-api-proxy. Deve haver além da imagem tagueada como "Dev", uma outra imagem tagueada como "1.0.0,latest"

>>

- **Testes locais do terraform**

  ```shell
  #garantir diretorio da aplicação
  cd linha-montagem-app-api
  #inicializa arquivos .tf
  docker-compose -f deploy/docker-compose.yml run --rm terraform init
  #lista as workspaces existentes
  docker-compose -f deploy/docker-compose.yml run --rm terraform workspace list
  #cria a workspace dev
  docker-compose -f deploy/docker-compose.yml run --rm terraform workspace new dev
  #garante formatação dos arquivos .tf
  docker-compose -f deploy/docker-compose.yml run --rm terraform fmt
  #valida arquivos .tf
  docker-compose -f deploy/docker-compose.yml run --rm terraform validate
  #planeja a infra-estrutura
  docker-compose -f deploy/docker-compose.yml run --rm terraform plan
  #execupal a infra-estrutura
  docker-compose -f deploy/docker-compose.yml run --rm terraform apply
  
  #Entre na Console da AWS e confira os recursos gerados, como ambiente Dev (referenciado pelo workspace #criado acima) 
  
  # Abra o job Apply no Gitlab e pegue os outputs no final
  # <api_endpoint> - teste no browser
  # <bastion_host> - acesso SSH via terminal 
  # <db_host>

  #remover a infraestrutura
  docker-compose -f deploy/docker-compose.yml run --rm terraform destroy
  ```
>>

- **Rodando pipeline no Gitlab**

  >> Esta ação no Gitlab irpa disparar a pipeline objetivo deste laboratório. Irá gerar a infraestrutura de um ambiente de Staging (homologação) e de Production (produção), que necessitará de paorvação no processo. É importante ter ação, pois esta ação irá gerar custos na sua conta AWS, mas um valor baixo, desde que você não mantenha a infra ativa por muito tempo. DEPOIS DOS TESTES, SEMPRE EXECUTE OS JOBS DESTROY PARA NÃO PAGAR CUSTOS DESNECESSÁRIOS. Lembre-se de ativar os alertas de Budget na sua conta para que os gastos fiquem com maior controle.

  - Projeto **linha-montagem-app-api-devops**
    > Disparando a pipeline para ambiente de homologação (**Staging**)
    - Menu Merge Requests
      - Botão New merge request
      - Source branch: develop/setup-api (se criou outra branch, informar a mais atual com os commits)
      - Target branch: master
      - Aprove e execute o Merge Request
      - Isso irá disparar o primeiro o job **Test and Lint** e seus respecitvos stages **Test and Lint**  e **Validate Terraform**
      >>
    - **Ambiente Staging** na AWS
      - Após sucesso, aprove o Merge na master (botão existente na própria página do Merge Request)
      - Isso irá disparar os jobs
        - Test and lint
          - Test and Lint
          - Validate Terraform
        - Build and push
        - Staging Plan
        - Staging Apply
        - Destroy
          - Staging Destroy
          - Ficará com status "Aprovação Manual"
      >>
      - Abra o job Apply no Gitlab e pegue os outputs no final
      - api.staging.<api_endpoint> - teste no browser
      - EC2<bastion_host> - acesso SSH via terminal
      - <db_host>
      - Após sucesso, vá até a console AWS, e confira os recursos gerados ppara o ambiente "Staging"
      - Caso já queira, execute o job "Destroy" para remover todo o ambiente
      - Sempre é bom dar uma conferida se o fluxo funcionou corretamente e não ficou nada para trás
      >>
      >>
    > Disparando a pipeline para ambiente de homologação (**Production**)
    - Esta pipeline criará o ambiente de Staging (caso ele tenha sido removido) e o de Produção, isto é, ao final do processamento, haverá dois ambientes disponíveis na AWS
    - Menu Merge Requests
      - Botão New merge request
      - Source branch: master
      - Target branch: production
      - Aprove e execute o Merge Request
      - Isso irá disparar o primeiro o job **Test and Lint** e seus respecitvos stages **Test and Lint**  e **Validate Terraform**
      >>
    - **Ambiente Production** na AWS
      - Após sucesso, aprove o Merge na master (botão existente na própria página do Merge Request)
      - Isso irá disparar a pipeline completa com todos os jobs
        - Test and lint
          - Test and Lint
          - Validate Terraform
        - Build and push
        - Staging Plan
        - Staging Apply
        - Production Plan
        - Production Apply
          - Ficará com status "Aprovação Manual"
          - Ao confirmar, a infra do ambiente será criada na AWS
        - Destroy
          - Staging Destroy
          - Production Destroy
          - Ambos, ficarão com status "Aprovação Manual"
      >>
      - Abra o job Apply no Gitlab e pegue os outputs no final
      - api.<api_endpoint> - teste no browser
      - EC2<bastion_host> - acesso SSH via terminal
      - <db_host>
      - Após sucesso, vá até a console AWS, e confira os recursos gerados ppara o ambiente "Staging"
      - Caso jpa queira, execute o job "Destroy" para remover todo o ambiente
      - Sempre é bom dar uma conferida se o fluxo funcionou corretamente e não ficou nada para trás
      >>
      - Para verificar a saida dos endpoints, veja o arquivo "deploy/variables.tf", na viarável "subdomain"

## ✌✌✌ Obrigado por ter realizado este lab... espero que tenha gostado e aproveitado. Até a próxima✌✌✌
