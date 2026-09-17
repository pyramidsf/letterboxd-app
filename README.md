# Letterboxd Insights

API em desenvolvimento para analisar perfis públicos do Letterboxd e gerar estatísticas sobre os filmes assistidos.

## Status

Projeto em andamento. No momento, a API já consegue consultar o feed RSS de um usuário e calcular a média das notas encontradas. A integração com o TMDb, o salvamento completo dos filmes e a geração de estatísticas ainda estão sendo implementados.

## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- SQLite
- httpx
- Beautiful Soup

## Como executar

Clone o repositório e entre na pasta do projeto:

```bash
git clone <url-do-repositorio>
cd letterboxd-app
```

Crie e ative um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install fastapi uvicorn sqlalchemy httpx beautifulsoup4
```

Inicie a API:

```bash
uvicorn main:app --reload
```

Depois, acesse a documentação interativa em [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Endpoints atuais

### Analisar um perfil

```http
POST /analyze/{username}
```

Consulta o RSS público do Letterboxd e retorna os filmes encontrados, a quantidade de filmes e a média das notas do usuário.

Exemplo:

```bash
curl -X POST http://127.0.0.1:8000/analyze/seu_usuario
```

### Consultar estatísticas

```http
GET /stats/{username}
```

Endpoint reservado para as estatísticas do usuário. A implementação ainda está em desenvolvimento.

## Estrutura do projeto

```text
.
├── main.py                  # Aplicação FastAPI e rotas
└── app/
    ├── database/            # Conexão com o SQLite
    ├── models/              # Modelos do banco de dados
    ├── scrapers/            # Coleta de dados do Letterboxd
    ├── services/            # Regras para estatísticas
    └── tmdb/                # Futura integração com o TMDb
```

O arquivo `insights.db` é criado localmente quando a aplicação inicializa e não deve ser versionado.

## Próximos passos

- Integrar a API do TMDb para buscar informações adicionais dos filmes.
- Persistir as análises no banco de dados.
- Implementar as estatísticas do usuário.
- Adicionar testes automatizados e um arquivo de dependências.

## Aviso

Este projeto é experimental e utiliza dados públicos do Letterboxd. Respeite os termos de uso e os limites de acesso do serviço ao executar os scrapers.