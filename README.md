# 🚀 LABORATORIO DEVOPS

> O projeto trilhandosaberlabs é uma iniciativa para aprendizado constante, voltado para o modelo hands-on. Este domento tem o grande objetivo de disponibilizar um passo a passo completo para configurar sua máquina local e as integrações, para poder ter uma referência para o estudo. A sugestão é você criar seu projeto, baseado nos insights obtidos neste laboratório. Vamos clocar a mão namassa!

- Foco em Python/Django/DjangoRestframework, Docker, Pipeline CI/CD e AWS

## Projeto linha-montagem-api-devops

| Software /Linguagem /Serviços  | Observação  |
| :---------------: |:---------------:|
| Django      | aplicação desenvolvida na linguagem Python através do framework Django |
| DjangoRestFramework      | framework Django para desenvolver Rest APIs |
| Gitlab   | repositório privado de fontes e pipeline CI/CD   |
| Github   | repositóriopúblico do projeto  |
| Docker   | gerenciamento de containers  |
| AWS   | provedor de Cloud Pública  |

- Projetos originais
▷ Github **linha-montagem-site-api-devops**: <git@github.com:trilhalabs/linha-montagem-api-devops.git>
▷ Acesse: <https://github.com/trilhalabs/linha-montagem-api-devops>

## Configurações iniciais

### inicialização no git

```shell
git clone git@github.com:trilhalabs/linha-montagem-api-devops.git
cd linha-montagem-api-devops
git init
git add .
git commit -m "commit inicial - terminal local"
```

### integração dos repositórios Github e Gitlab

- criação do projeto nos repositórios Gitlab ==mirroring==>> Github
  - No Github, crie um projeto vazio (sugere-se manter o mesmo nome do projeto)
    - No menu com a foto do seu usuário (lado superior direito), entre no menu Settings
    - Developer Settings / Personal access tokens
    - Crie um token pessoal
  - No Gitlab, menu Settings / Repoitories / Expand Mirroring
    - Fazer o link com o github
      - Exemplo:
        - <https://trilhalabs:"coloque-seu-personal-token-github"@github.com/trilhalabs/linha-montagem-api-devops.git>
        - Token: "coloque-seu-personal-token-github"

### sincronizando repositorios

```shell
git remote add gitlab git@gitlab.com:"ssh-do-seu-projeto-no-gitlab".git
git push gitlab master
```

### preparando o ambiente local

- Gere e execute o ambiente virtual

```shell
#dentro do diretorio da aplicacao recipe-app-api
python -m venv env
ls -la
pwd
#<caminho-do-projeto>
source <caminho-do-projeto>/env/Scripts/activate
```

- Instale o Django e o Django Framework

```shell
#dentro do diretorio da aplicacao recipe-app-api
cd env/Scripts/
python.exe -m pip install --upgrade pip #garantir versão mais atualizada do Pip
cd ../env/
pip install django --user #--user é opcional (somente se der erro de permissionamento)
pip install djangorestframework --user #--user é opcional (somente se der erro de permissionamento)
django-admin --version
```

- Construindo as imagens docker

> Documentação <https://docs.docker.com/engine/reference/commandline/build/>

```shell
#dentro do diretorio da aplicacao 
cd ../linha-montagem-api-devops
docker-compose build
```

- Subindo tabelas do banco de dados

```shell
docker-compose run app sh -c "python manage.py makemigrations core"
#em caso de erro,executar
#docker-compose run app sh -c "python manage.py migrate"
docker-compose run app sh -c "python manage.py test && flake8"
docker-compose run app sh -c "python manage.py createsuperuser"
# Ex: email: seu-mail@gamil.com
# Ex: password: senhasecreta
```

- Testando a aplicação

```shell
docker-compose up
```

- No container

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

- No browser:

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
