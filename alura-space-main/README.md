# Projeto Alura Space

O Alura Space é um projeto desenvolvido com Django, que simula um CRUD para o envio de publicações a respeito de corpos celestes.

| :placard: Vitrine.Dev | Guilherme Henrique  |
| --------------------- | ------------------- |
| :sparkles: Nome       | **Alura-Space**     |
| :label: Tecnologias   | Python, Django, CSS |

### Detalhes do projeto

> - **Fazer login.**
> - **Cadastrar um novo usuário.**
> - **Cadastrar novas imagens para a página inicial.**
> - **Detalhar a imagem, com a opção de alterar ou excluir.**
> - **Administração através do Django Admin**
> - **Filtrar por categoria.**
> - **Pesquisar por nome.**

- `/`: A página inicial do projeto, aonde são listadas as imagens principais da aplicação.

![index](https://github.com/guih1886/alura-space/blob/main/static/assets/imagens/prints/index.png#vitrinedev)

###

- `/login`: Essa rota é responsável por fazer o login na aplicação e redirecionar para a página inicial ou para a página de login, caso o acesso falhe.

  ```python
  def login(request):
    form = LoginForms()

    if request.method == 'POST':
        form = LoginForms(request.POST)

        if form.is_valid():
            nome = form['nome_login'].value()
            senha = form['senha'].value()

            usuario = auth.authenticate(
                request,
                username=nome,
                password=senha
            )

            if usuario:
                auth.login(request, usuario)
                messages.success(request, f"Usuário {nome} logado com sucesso!")
                return redirect('index')
            else:
                messages.error(request, f"Usuário {nome} não encontrado.")
                return redirect('login')

    return render(request, 'usuarios/login.html', {"form": form})
  ```

  ![login](https://github.com/guih1886/alura-space/blob/main/static/assets/imagens/prints/login.png)

####

- `/cadastro`: Essa rota tem a finalidade de cadastrar o novo usuário e recebe através do formulário os campos de `nome`,`email`,`senha` e `confirmação de senha` para o cadastro. Faz a validação da senha e redireciona para a página de login para o acesso.

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

        # busca o usuário no banco de dados
        if User.objects.filter(username=nome).exists():
            messages.error(request, f"Usuário {nome} já cadastrado.")
            return redirect('cadastro')

        usuario = User.objects.create_user(
            username=nome, email=email, password=senha)
        usuario.save()
        messages.success(request, f"Usuário {nome} cadastrado com sucesso.")
        return redirect('login')

    return render(request, 'usuarios/cadastro.html', {'form': form})
  ```

![cadastrar-usuario](https://github.com/guih1886/alura-space/blob/main/static/assets/imagens/prints/cadastrar-usuario.png)

####

- `/nova-imagem`: Essa rota tem a finalidade de cadastrar uma nova imagem para a galeria, sendo necessário preencher os campos de `nome`,`legenda`,`categoria`, `descrição`, `enviar a foto`,`data` e selecionar o `usuario`.

  ```python
  class FotografiaForms(forms.ModelForm):
    class Meta:
        model = Fotografia
        exclude = ['ativo']
        labels = {
            'descricao': 'Descrição',
            'data_fotografia': 'Data de Registro',
            'usuario': 'Usuário',
        }

        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'legenda': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'data_fotografia': forms.DateInput(
                format='%d/%m/%Y',
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'usuario': forms.Select(attrs={'class': 'form-control'}),
        }

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
            messages.error(
                request, "Ocorreu um erro ao cadastrar a fotografia.")

    return render(request, 'galeria/nova_imagem.html', {"form": form})
  ```

![cadastrar](https://github.com/guih1886/alura-space/blob/main/static/assets/imagens/prints/cadastrar.png)

####

- `/imagem/<int:foto_id>`: Essa rota tem a finalidade de detalhar a imagem selecionada, mostrando sua foto, nome, legenda e descrição. Tem os dois botões para editar e excluir a publicação.

  ```python
  def imagem(request, foto_id):
    fotografia = get_object_or_404(Fotografia, pk=foto_id)
    return render(request, 'galeria/imagem.html', {"fotografia": fotografia})
  ```

![imagem](https://github.com/guih1886/alura-space/blob/main/static/assets/imagens/prints/imagem.png)

- Ao clicar para editar a imagem, é carregado o path `/editar-imagem/<int:foto_id>`, onde o formulário de imagem é aberto com os dados carregados da imagem.

```python
  def editar_imagem(request, foto_id):
    fotografia = Fotografia.objects.get(id=foto_id)
    form = FotografiaForms(instance=fotografia)

    if request.method == "POST":
        form = FotografiaForms(
            request.POST, request.FILES, instance=fotografia)
        if form.is_valid():
            form.save()
            messages.success(request, "Fotografia editada com sucesso.")
            return redirect('index')
        else:
            messages.error(
                request, "Ocorreu um erro ao editar a fotografia.")

    return render(request, 'galeria/editar_imagem.html', {'form': form, 'foto_id': foto_id})
```

![editar](https://github.com/guih1886/alura-space/blob/main/static/assets/imagens/prints/editar.png)

####

- `/admin`: Essa rota é o painel de administrador do Django.

![editar](https://github.com/guih1886/alura-space/blob/main/static/assets/imagens/prints/admin.png)

- Através dela, é possível fazer o gerenciamento dos usuários, grupos e também das fotografias, onde podemos cadastrar, alterar e editar todas as fotos além de conseguir-mos buscar-lás e filtrar-lás.

```python
  class ListarFotografias(admin.ModelAdmin):
    list_display = ("id", "ativo", "nome", "legenda")
    list_display_links = ("id", "nome")
    search_fields = ["nome"]
    list_filter = ("categoria",)
    list_editable = ("ativo",)
    list_per_page = 10

admin.site.register(Fotografia, ListarFotografias)
```

![editar](https://github.com/guih1886/alura-space/blob/main/static/assets/imagens/prints/admin2.png)