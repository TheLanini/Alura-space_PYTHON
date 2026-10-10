# README de rotas, funções e APIs do projeto Alura Space

Este documento explica, de forma detalhada, como a aplicação funciona, quais rotas existem, quais funções processam cada página e como os dados são manipulados.

## 1. Visão geral

O projeto Alura Space é uma aplicação web desenvolvida com Django para gerenciar uma galeria de fotografias de corpos celestes.

A aplicação trabalha com:
- autenticação de usuários
- cadastro de usuários
- upload de imagens
- listagem de fotos
- busca por nome
- filtro por categoria
- edição e exclusão de registros
- painel administrativo do Django

Observação importante:
- não existe uma API REST em JSON nesta aplicação;
- as rotas são páginas server-side renderizadas pelo Django, usando views e templates HTML.
- o que é chamado aqui de "API" é, na prática, a camada de rotas/views da aplicação web.

---

## 2. Estrutura principal

```text
alura-space-main/
├── apps/
│   ├── galeria/
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── migrations/
│   └── usuarios/
│       ├── forms.py
│       ├── urls.py
│       ├── views.py
│       └── migrations/
├── setup/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── README.md
├── README-rotas-e-funcoes.md
└── requirements.txt
```

---

## 3. Rotas da aplicação

As rotas principais estão distribuídas em dois módulos:
- `apps.galeria.urls`
- `apps.usuarios.urls`
- e também o `setup/urls.py`, que inclui as rotas dos apps no projeto principal.

### 3.1 Arquivo principal de rotas

Arquivo: `setup/urls.py`

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.galeria.urls')),
    path('', include('apps.usuarios.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Descrição:
- `admin/` → painel administrativo do Django
- `''` → inclui as rotas da galeria
- `''` → inclui as rotas de usuários
- `static(...)` → habilita acesso às imagens enviadas via upload

---

## 4. Rotas da galeria (`apps/galeria/urls.py`)

Arquivo: `apps/galeria/urls.py`

```python
from django.urls import path
from apps.galeria.views import index, imagem, buscar, nova_imagem, editar_imagem, deletar_imagem, filtro

urlpatterns = [
    path('', index, name="index"),
    path('imagem/<int:foto_id>', imagem, name="imagem"),
    path('buscar', buscar, name="buscar"),
    path('nova-imagem', nova_imagem, name="nova_imagem"),
    path('editar-imagem/<int:foto_id>', editar_imagem, name="editar_imagem"),
    path('deletar-imagem/<int:foto_id>', deletar_imagem, name="deletar_imagem"),
    path('filtro/<str:categoria>', filtro, name="filtro")
]
```

### Tabela de rotas da galeria

| Rota | Método | Função | Descrição |
|------|--------|---------|-----------|
| `/` | GET | `index` | Página inicial da galeria |
| `/imagem/<foto_id>` | GET | `imagem` | Detalhes de uma foto |
| `/buscar` | GET | `buscar` | Pesquisa por nome |
| `/nova-imagem` | GET/POST | `nova_imagem` | Cadastro de nova foto |
| `/editar-imagem/<foto_id>` | GET/POST | `editar_imagem` | Edição de foto |
| `/deletar-imagem/<foto_id>` | GET | `deletar_imagem` | Exclusão de foto |
| `/filtro/<categoria>` | GET | `filtro` | Listagem filtrada por categoria |

---

## 5. Rotas de usuários (`apps/usuarios/urls.py`)

Arquivo: `apps/usuarios/urls.py`

```python
from django.urls import path
from apps.usuarios.views import login, cadastro, logout

urlpatterns = [
    path('login', login, name='login'),
    path('cadastro', cadastro, name='cadastro'),
    path('logout', logout, name='logout'),
]
```

### Tabela de rotas de usuários

| Rota | Método | Função | Descrição |
|------|--------|---------|-----------|
| `/login` | GET/POST | `login` | Autenticação do usuário |
| `/cadastro` | GET/POST | `cadastro` | Cadastro de novo usuário |
| `/logout` | GET | `logout` | Encerramento da sessão |

---

## 6. Modelos e entidades do sistema

### 6.1 Modelo `Fotografia`

Arquivo: `apps/galeria/models.py`

```python
class Fotografia(models.Model):
    OPCOES_CATEGORIA = [
        ("NEBULOSA", "Nebulosa"),
        ("ESTRELA", "Estrela"),
        ("GALAXIA", "Galáxia"),
        ("PLANETA", "Planeta")
    ]

    nome = models.CharField(max_length=100, null=False, blank=False)
    legenda = models.CharField(max_length=200, null=False, blank=False)
    categoria = models.CharField(max_length=150, choices=OPCOES_CATEGORIA, default="")
    descricao = models.TextField(null=False, blank=False)
    foto = models.ImageField(upload_to="fotos/%Y/%m/%d/", blank=True)
    ativo = models.BooleanField(default=True)
    data_fotografia = models.DateField(default=timezone.now, blank=False)
    usuario = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='user'
    )
```

Campos principais:
- `nome`: nome da foto/publicação
- `legenda`: texto curto da imagem
- `categoria`: enum da categoria
- `descricao`: detalhamento da imagem
- `foto`: imagem enviada
- `ativo`: indica se está ativa
- `data_fotografia`: data da foto
- `usuario`: usuário que criou a imagem

---

## 7. Formulários usados

### 7.1 `LoginForms`

Arquivo: `apps/usuarios/forms.py`

```python
class LoginForms(forms.Form):
    nome_login = forms.CharField(...)
    senha = forms.CharField(widget=forms.PasswordInput(...))
```

Função:
- recebe nome de usuário e senha
- valida autenticação na view `login`

### 7.2 `CadastroForms`

```python
class CadastroForms(forms.Form):
    nome_cadastro = forms.CharField(...)
    email = forms.EmailField(...)
    senha1 = forms.CharField(...)
    senha2 = forms.CharField(...)
```

Função:
- recebe dados do usuário
- valida senha e confirmação
- cria o usuário com `User.objects.create_user(...)`

### 7.3 `FotografiaForms`

Arquivo: `apps/galeria/forms.py`

```python
class FotografiaForms(forms.ModelForm):
    class Meta:
        model = Fotografia
        exclude = ['ativo']
```

Função:
- formulário para criar e editar fotos
- inclui campos como nome, legenda, categoria, descrição, foto, data e usuário

---

## 8. Funções da aplicação e comportamento

### 8.1 Funções da galeria

#### `index(request)`

Arquivo: `apps/galeria/views.py`

```python
def index(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado.")
        return redirect('login')

    fotos = Fotografia.objects.order_by("data_fotografia").filter(ativo=True)
    return render(request, 'galeria/index.html', {"cards": fotos})
```

Responsabilidades:
- exige autenticação
- busca fotos ativas
- ordena por data da fotografia
- renderiza a página inicial

#### `imagem(request, foto_id)`

```python
def imagem(request, foto_id):
    fotografia = get_object_or_404(Fotografia, pk=foto_id)
    return render(request, 'galeria/imagem.html', {"fotografia": fotografia})
```

Responsabilidades:
- busca uma foto pelo ID
- exibe a página de detalhe da fotografia

#### `buscar(request)`

```python
def buscar(request):
    fotos = Fotografia.objects.order_by("data_fotografia").filter(ativo=True)

    if "busca" in request.GET:
        palavra_a_buscar = request.GET["busca"]
        if palavra_a_buscar:
            fotos = fotos.filter(nome__icontains=palavra_a_buscar)
        else:
            return redirect('index')
    return render(request, 'galeria/index.html', {"cards": fotos})
```

Responsabilidades:
- lê o parâmetro `busca` da query string
- filtra registros pelo campo `nome`
- usa busca case-insensitive (`icontains`)

#### `nova_imagem(request)`

```python
def nova_imagem(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado.")
        return redirect('login')

    form = FotografiaForms
    if request.method == "POST":
        form = FotografiaForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Nova fotografia cadastrada.")
            return redirect('index')
        else:
            messages.error(request, "Ocorreu um erro ao cadastrar a fotografia.")

    return render(request, 'galeria/nova_imagem.html', {"form": form})
```

Responsabilidades:
- bloqueia acesso sem login
- recebe formulário com imagem e dados
- valida o formulário
- salva a foto no banco
- redireciona para a página inicial

#### `editar_imagem(request, foto_id)`

```python
def editar_imagem(request, foto_id):
    fotografia = Fotografia.objects.get(id=foto_id)
    form = FotografiaForms(instance=fotografia)

    if request.method == "POST":
        form = FotografiaForms(request.POST, request.FILES, instance=fotografia)
        if form.is_valid():
            form.save()
            messages.success(request, "Fotografia editada com sucesso.")
            return redirect('index')
        else:
            messages.error(request, "Ocorreu um erro ao editar a fotografia.")

    return render(request, 'galeria/editar_imagem.html', {'form': form, 'foto_id': foto_id})
```

Responsabilidades:
- carrega a fotografia pelo ID
- preenche o formulário com os dados existentes
- salva alterações quando o usuário envia o formulário

#### `deletar_imagem(request, foto_id)`

```python
def deletar_imagem(request, foto_id):
    fotografia = Fotografia.objects.get(id=foto_id)
    if fotografia:
        fotografia.delete()
        messages.success(request, "Fotografia excluida com sucesso.")
        return redirect('index')
    else:
        messages.error(request, "Ocorreu um erro ao excluir a fotografia.")
```

Responsabilidades:
- remove a foto do banco
- redireciona para a página inicial

#### `filtro(request, categoria)`

```python
def filtro(request, categoria):
    fotos = Fotografia.objects.order_by("data_fotografia").filter(ativo=True, categoria=categoria)
    return render(request, 'galeria/index.html', {"cards": fotos})
```

Responsabilidades:
- filtra fotos pela categoria recebida na URL
- exibe apenas os registros ativos daquela categoria

---

### 8.2 Funções de usuário

#### `login(request)`

```python
def login(request):
    form = LoginForms()

    if request.method == 'POST':
        form = LoginForms(request.POST)

        if form.is_valid():
            nome = form['nome_login'].value()
            senha = form['senha'].value()

            usuario = auth.authenticate(request, username=nome, password=senha)

            if usuario:
                auth.login(request, usuario)
                messages.success(request, f"Usuário {nome} logado com sucesso!")
                return redirect('index')
            else:
                messages.error(request, f"Usuário {nome} não encontrado.")
                return redirect('login')

    return render(request, 'usuarios/login.html', {"form": form})
```

Responsabilidades:
- exibe o formulário de login
- valida usuário e senha
- autentica o usuário com `auth.authenticate`
- faz login com `auth.login`
- redireciona para a página inicial em caso de sucesso

#### `cadastro(request)`

```python
def cadastro(request):
    form = CadastroForms()

    if request.method == "POST":
        form = CadastroForms(request.POST)

    if form.is_valid():
        if form['senha1'].value() != form['senha2'].value():
            messages.error(request, "Senhas não conferem.")
            return redirect('cadastro')

        nome = form['nome_cadastro'].value()
        email = form['email'].value()
        senha = form['senha1'].value()

        if User.objects.filter(username=nome).exists():
            messages.error(request, f"Usuário {nome} já cadastrado.")
            return redirect('cadastro')

        usuario = User.objects.create_user(username=nome, email=email, password=senha)
        usuario.save()
        messages.success(request, f"Usuário {nome} cadastrado com sucesso.")
        return redirect('login')

    return render(request, 'usuarios/cadastro.html', {'form': form})
```

Responsabilidades:
- valida confirmação da senha
- impede usuário duplicado
- cria o usuário com `create_user`
- redireciona para o login

#### `logout(request)`

```python
def logout(request):
    auth.logout(request)
    messages.success(request, "Logout realizado com sucesso.")
    return redirect('login')
```

Responsabilidades:
- encerra a sessão atual
- redireciona para a tela de login

---

## 9. Fluxo geral da aplicação

### Fluxo de autenticação
1. usuário acessa `/login`
2. informa nome e senha
3. `login` valida as credenciais
4. se válido, `auth.login()` inicia a sessão
5. redireciona para `/`

### Fluxo de cadastro
1. usuário acessa `/cadastro`
2. informa nome, e-mail e senha
3. `cadastro` valida campos e senhas
4. salva o usuário no banco
5. redireciona para `/login`

### Fluxo de galeria
1. usuário autenticado acessa `/`
2. `index` lista fotos ativas em ordem de data
3. pode navegar para `/imagem/<id>` para detalhes
4. pode buscar em `/buscar`
5. pode filtrar por categoria em `/filtro/<categoria>`
6. pode criar, editar ou excluir imagens

---

## 10. Resumo prático das APIs/web endpoints

Mesmo sem uma API REST em JSON, a aplicação possui os seguintes endpoints web:

- `GET /` → página inicial da galeria
- `GET /login` / `POST /login` → login
- `GET /cadastro` / `POST /cadastro` → cadastro
- `GET /logout` → logout
- `GET /buscar?busca=nome` → busca por nome
- `GET /imagem/<foto_id>` → detalhe da foto
- `GET /nova-imagem` / `POST /nova-imagem` → novo cadastro de imagem
- `GET /editar-imagem/<foto_id>` / `POST /editar-imagem/<foto_id>` → editar imagem
- `GET /deletar-imagem/<foto_id>` → excluir imagem
- `GET /filtro/<categoria>` → filtro por categoria
- `GET /admin/` → painel administrativo do Django

---

## 11. Conclusão

A aplicação Alura Space é um sistema web em Django orientado a páginas e templates, não uma API REST tradicional. O núcleo da lógica está em:
- `apps.galeria.views`
- `apps.usuarios.views`
- modelos em `apps.galeria.models`
- formulários em `apps.galeria.forms` e `apps.usuarios.forms`
- roteamento em `setup/urls.py`, `apps.galeria.urls` e `apps.usuarios.urls`

Esses elementos juntos permitem autenticação, cadastro, upload, listagem, busca, filtro e gerenciamento de imagens em uma galeria de astronomia.
