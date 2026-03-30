# Documentação do Projeto Me Conceito

## Visão Geral

O projeto "Me Conceito" é uma aplicação full stack com front-end em React + Vite e back-end em Django + Django REST Framework. O objetivo principal é oferecer uma vitrine interativa de moda, com navegação por categoria, páginas específicas para Loja, Novidades, Feminino e Masculino, e integração com APIs para conteúdo dinâmico.

## Estrutura do Projeto

Raiz do workspace:
- `package.json` - dependências e scripts do front-end.
- `vite.config.js` - configuração básica do Vite.
- `README.md` - template padrão do projeto.
- `src/` - código React do front-end.
- `me_conceito_api/` - código Django do back-end.

### Front-end

Local: `src/`

Arquivos principais:
- `src/main.jsx` - ponto de entrada React, monta `<App />` com `BrowserRouter`.
- `src/App.jsx` - rotas da aplicação e controle de login.
- `src/index.css`, `src/App.css` - estilo global.

Páginas:
- `src/pages/HomePage.jsx` - página inicial / loja. Busca cards do back-end e registra visitas.
- `src/pages/CategoryPage.jsx` - páginas de categoria (`/novidades`, `/feminino`, `/masculino`) e subcategorias.
- `src/pages/LoginPage.jsx` - tela de login e registro de usuário.
- `src/pages/AboutPage.jsx` - página "Sobre" está presente como rota, embora não tenha sido detalhada aqui.

Componentes:
- `src/components/Header.jsx` - barra superior com logo e navegação.
- `src/components/HeroSection.jsx` - seção de destaque que carrega dados de destaque do back-end.
- `src/components/FeaturedSection.jsx` - exibe produto/card em grid com filtro de busca.
- `src/components/Footer.jsx` - rodapé simples.

Assets:
- `src/assets/logo/logo.png` - logo da marca.
- `src/assets/icons/user.png` - ícone de usuário.

### Back-end

Local: `me_conceito_api/`

Arquivos principais:
- `me_conceito_api/backend/settings.py` - configurações Django.
- `me_conceito_api/backend/urls.py` - URLs principais, inclui `api.urls` e `admin`.
- `me_conceito_api/api/models.py` - modelos de dados.
- `me_conceito_api/api/serializers.py` - serializers DRF.
- `me_conceito_api/api/views.py` - APIs REST.
- `me_conceito_api/api/urls.py` - rotas do REST API.
- `me_conceito_api/backend/admin.py` - personalização do painel administrativo.

Tecnologias:
- Django 5.x (presumido pelo código). 
- Django REST Framework.
- SQLite local (`db.sqlite3`).
- `corsheaders` para permitir conexões do front-end rodando em `localhost:5173`.

## Back-end: Modelos de Dados

### Category
Campos:
- `name`, `slug`, `description`
- `hero_title`, `hero_image_url`
- `origem_pagina` (`LOJA`, `NOVIDADES`, `FEMININO`, `MASCULINO`)

Relacionamentos:
- `sections` - `CategorySection` com `related_name='sections'`
- `products` - `Product` com `related_name='products'`

### CategorySection
Campos:
- `category`, `name`, `slug`, `description`, `order`

### Product
Campos principais:
- `name`, `price`, `description`, `image_url`, `button_label`
- `origem_pagina`
- `category`, `section`
- `created_at`

Comportamento:
- `save()` sobrescrito para copiar `origem_pagina` da `category` ao salvar.

Proxy models:
- `LojaProduct`, `NovidadeProduct`, `FemininoProduct`, `MasculinoProduct`

### StoreShowcase
Campos:
- `title`, `subtitle`, `image_url`, `button_label`, `origem_pagina`, `active`

### BannerDestaque
Campos:
- `titulo`, `subtitulo`, `botao_texto`, `imagem_fundo`, `origem_pagina`

Validação:
- `clean()` garante que exista apenas um registro de destaque.

### CardNovidade
Campos:
- `nome`, `preco`, `categoria_tag`, `imagem`, `origem_pagina`

### SiteVisit
Campos:
- `path`, `created_at`

## Back-end: Serializers

- `ProductSerializer` - serializa produtos com `category` e `section` em texto.
- `CategorySectionSerializer` - inclui produtos da seção.
- `CategorySerializer` - inclui seções da categoria.
- `StoreShowcaseSerializer` - mapeia campos para uso no front-end.
- `BannerDestaqueSerializer` - dados do banner de destaque.
- `CardNovidadeSerializer` - converte `CardNovidade` para formato consumido pelo front-end.
- `SiteVisitSerializer` - registra visitas.
- `UserRegistrationSerializer` - registra usuário via email, senha e nome.

## Back-end: Views e Endpoints

Rotas principais configuradas em `me_conceito_api/api/urls.py`:

1. `GET /api/categories/`
   - Lista todas as categorias.

2. `GET /api/categories/<slug>/`
   - Retorna detalhes e seções de uma categoria específica.

3. `GET /api/products/`
   - Lista produtos.
   - Query params suportados:
     - `origem_pagina` para filtrar por categoria de página.
     - `category` para filtrar por `category__slug`.
   - `POST /api/products/` exige autenticação.

4. `GET /api/cards/` e `GET /api/cardnovidade/`
   - Lista `CardNovidade`.
   - Filtra por `origem_pagina`.

5. `GET /api/banner-destaque/`
   - Retorna o banner de destaque para a página.
   - Filtra por `origem_pagina`.

6. `GET /api/store-showcase/`
   - Retorna o showcase de vitrine para a página.
   - Filtra por `origem_pagina`.

7. `POST /api/visits/`
   - Registra o caminho da página acessada.

8. `POST /api/auth/register/`
   - Cria usuário e retorna token.

9. `POST /api/auth/login/`
   - Autentica usuário e retorna token.

Observações de segurança:
- `DEFAULT_PERMISSION_CLASSES` está configurado como `AllowAny`.
- Autenticação usa `TokenAuthentication` e `SessionAuthentication`.

## Rotas do Django

- `path('admin/', admin.urls)`
- `path('api/', include('api.urls'))`

Em modo DEBUG, o Django serve arquivos de mídia via `MEDIA_URL` e `MEDIA_ROOT`.

## Painel Administrativo

O admin foi customizado em `me_conceito_api/backend/admin.py`:

- `CustomAdminSite` altera título e painel inicial.
- `CategoryAdmin` mostra contagem de produtos e usa inline de produtos.
- `ProductAdmin` e proxies organizam produtos por categoria.
- `StoreShowcaseAdmin`, `BannerDestaqueAdmin`, `CardNovidadeAdmin` configuram listagem e filtros.
- `SiteVisit` é registrado para estatísticas de acesso.

## Front-end: Fluxo de Navegação

### Rotas

- `/` e `/loja` → `HomePage` com `pageOrigin='LOJA'`
- `/novidades` → `CategoryPage` com `pageSlug='novidades'`
- `/novidades/:sectionSlug` → mesma página com seção específica
- `/feminino` e `/feminino/:sectionSlug`
- `/masculino` e `/masculino/:sectionSlug`
- `/sobre` → `AboutPage`
- `/login` → `LoginPage`

### Estado global e autenticação

- `App.jsx` mantém `isLoggedIn` baseado em `localStorage.getItem('authToken')`.
- `LoginPage` grava `authToken` em `localStorage` após login ou registro.

### Comportamento das páginas

#### HomePage
- Busca cards via `GET http://127.0.0.1:8000/api/cards/?origem_pagina=${pageOrigin}`.
- Mostra `FeaturedSection` e `HeroSection`.
- Registra visita via `POST /api/visits/`.

#### CategoryPage
- Busca categoria via `GET http://127.0.0.1:8000/api/categories/${pageSlug}/`.
- Monta abas de subcategorias usando `category.sections`.
- Mostra cards do produto para cada seção.
- Também registra visita via `POST /api/visits/`.
- Nota: o código tenta usar `category.uncategorized_products`, mas este campo não é retornado pela API atualmente.

#### HeroSection
- Busca `GET http://127.0.0.1:8000/api/store-showcase/?origem_pagina=${pageOrigin}`.
- Exibe título, descrição, imagem de fundo e botão.

#### FeaturedSection
- Exibe lista de cards recebidos pelo front-end.
- Aplica filtro de busca local via `searchQuery`.

#### LoginPage
- Suporta login e registro.
- URLs de API:
  - `POST /api/auth/login/`
  - `POST /api/auth/register/`
- Em caso de sucesso, salva `authToken` e redireciona para `/`.

### Cabeçalho e navegação

- `Header.jsx` monta links principais e botão de login.
- `navItems` incluem Loja, Novidades, Feminino, Masculino e Sobre.

### Rodapé

- `Footer.jsx` apenas exibe copyright e nome do desenvolvedor.

## Observações Gerais

- O front-end usa URLs hardcoded `http://127.0.0.1:8000`. Em produção, isso deve ser parametrizado.
- A aplicação assume o back-end em execução local na porta 8000.
- A API de cards e categoria usa `origem_pagina` para filtrar conteúdo por página.
- O Django tem `DEBUG=True` por padrão no `settings.py` quando a variável de ambiente não é definida.

## Dependências

### Front-end
- `react`
- `react-dom`
- `react-router-dom`
- `vite`
- `@vitejs/plugin-react`
- `eslint` e plugins relacionados

### Back-end
- `Django`
- `djangorestframework`
- `djangorestframework.authtoken`
- `django-cors-headers`
- `colorfield`
- `admin_interface`

## Recomendação de execução

### Back-end
1. Ativar ambiente virtual.
2. `python manage.py migrate`
3. `python manage.py createsuperuser`
4. `python manage.py runserver`

### Front-end
1. `npm install`
2. `npm run dev`

## Arquivos importantes para revisão

- `src/App.jsx`
- `src/pages/HomePage.jsx`
- `src/pages/CategoryPage.jsx`
- `src/components/HeroSection.jsx`
- `me_conceito_api/api/models.py`
- `me_conceito_api/api/views.py`
- `me_conceito_api/api/urls.py`
- `me_conceito_api/backend/admin.py`

## Observações sobre possíveis melhorias

- Centralizar base URL das APIs em uma constante ou variável de ambiente.
- Ajustar `CategorySerializer` para retornar produtos sem seção, se necessário.
- Melhorar validação de formulários no front-end.
- Adicionar testes automatizados para endpoints e componentes.
