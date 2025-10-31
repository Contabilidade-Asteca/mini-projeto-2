# Mini-Projeto 2 - Sistema Bancário Educativo

Aplicação educacional que demonstra conceitos de Programação Orientada a Objetos na construção de um sistema bancário. Agora o projeto conta com uma interface web moderna desenvolvida com Flask para facilitar a visualização das operações e o gerenciamento dos clientes e contas.

## 🚀 Recursos
- Interface web responsiva para cadastro de clientes, criação de contas, depósitos, saques e consulta de extratos.
- Painel com indicadores do total de clientes, contas e saldo agregado.
- Organização modular com entidades, operações e exceções reutilizáveis.
- Interface de linha de comando original mantida para fins de estudo.

## 🗂️ Estrutura do projeto
```
Mini-Projeto2/
├── app.py                  # Aplicação Flask com a interface web
├── requirements.txt        # Dependências da aplicação web
├── dsa_mini_projeto2.py    # Interface em modo texto (CLI)
├── dsaentidades/
│   ├── cliente.py
│   └── conta.py
├── dsaoperacoes/
│   └── banco.py
├── dsautilitarios/
│   └── exceptions.py
├── templates/              # Páginas HTML da aplicação web
│   ├── base.html
│   └── index.html
└── static/
    └── css/
        └── styles.css
```

## 💻 Executando a interface web
1. Crie e ative um ambiente virtual (opcional, mas recomendado).
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute a aplicação Flask:
   ```bash
   flask --app app run
   ```
4. Acesse `http://127.0.0.1:5000/` no navegador para utilizar o dashboard bancário.

> 💡 Os dados são mantidos em memória durante a execução. Ao reiniciar o servidor, o estado é reiniciado.

## 🧪 Utilizando a versão em linha de comando
Se preferir explorar a versão original em CLI, basta executar:
```bash
python dsa_mini_projeto2.py
```

## 📚 Sobre o projeto
Este mini-projeto faz parte da formação da Data Science Academy e tem como objetivo reforçar conceitos fundamentais de orientação a objetos, encapsulamento e polimorfismo por meio de um caso prático.
