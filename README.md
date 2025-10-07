# ⚡ Analisador de Dados Elétricos

Bem-vindo ao **Analisador de Dados Elétricos**, um aplicativo web interativo desenvolvido com **Streamlit** que permite carregar, visualizar e analisar arquivos CSV de analisadores do tipo **MAR722** da Megabras.

---

## 📝 Funcionalidades

- Carregar múltiplos arquivos CSV de analisadores MAR722  
- Visualizar gráficos interativos de **tensão (VRMS)**, **corrente (IRMS)** e **potência ativa (P kW)**  
- Consultar estatísticas resumidas (média, mínimo, máximo, desvio padrão, etc.)  
- Exportar gráficos gerados como imagens  
- Rodapé estilizado com informações do desenvolvedor  

---

## 📂 Estrutura do Projeto

analisador_dados_eletricos/
│
├─ Home.py # Página principal (introdução)
├─ pages/
│ ├─ 1_Upload de Arquivos.py # Página de upload de arquivos
│ └─ 2_Resultados.py # Página de visualização de resultados
├─ assets/
│ └─ cartoon_me.png # Imagem do desenvolvedor para rodapé
├─ main_functions.py # Funções auxiliares para processamento de arquivos e gráficos
├─ requirements.txt # Dependências do projeto
└─ README.md # Este arquivo


---

## 🚀 Como Executar

1. Clone o repositório:

```bash
git clone https://github.com/seuusuario/AnalisadorApp.git
cd AnalisadorApp
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Rode o applicativo
```bash
streamlit run Home.py
```

## 👤 Desenvolvedor

**José ALVES** - [Site pessoal](https://jeduapf.github.io)
