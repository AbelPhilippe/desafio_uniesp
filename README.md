# UNIESP MBA — SIPRI Arms Transfers Intelligence

Dashboard interativo desenvolvido como parte do desafio do **MBA em Engenharia e Ciência de Dados da UNIESP**, utilizando dados do **SIPRI Arms Transfers Database** para analisar a dinâmica das transferências internacionais de armamentos.

O projeto transforma dados históricos de transferências de armamentos em informações visuais e comparáveis sobre **países exportadores, países importadores, evolução temporal, volume de transferências e comportamento individual por país**.

```text
SIPRI Arms Transfers Database
              ↓
        Data Processing
              ↓
          Analytics
              ↓
     Charts & Indicators
              ↓
       Streamlit Dashboard
```

## Desafio

### Como transformar dados complexos de transferências internacionais de armas em insights claros sobre fornecedores, destinatários e evolução dos fluxos ao longo do tempo?

O desafio consiste em trabalhar com uma extensa base histórica de transferências internacionais de armamentos e transformá-la em uma ferramenta que permita identificar padrões, tendências e mudanças no comportamento dos países.

A aplicação utiliza dados históricos do SIPRI para permitir comparações entre diferentes países e períodos.

## Objetivo

O objetivo do projeto é desenvolver um dashboard interativo capaz de transformar uma grande quantidade de dados históricos em informações claras, comparáveis e visualmente acessíveis.

A aplicação permite analisar:

* Exportações de armamentos;
* Importações de armamentos;
* Evolução das transferências ao longo dos anos;
* Principais países exportadores;
* Principais países importadores;
* Comparação entre diferentes períodos;
* Crescimento e redução das transferências;
* Distribuição das transferências por país;
* Análise individual de países;
* Indicadores baseados no **Trend-Indicator Value (TIV)**.

## Tecnologias

| Responsabilidade     | Tecnologia                    |
| -------------------- | ----------------------------- |
| Linguagem            | Python                        |
| Manipulação de dados | Pandas                        |
| Dashboard            | Streamlit                     |
| Visualização         | Streamlit                     |
| Controle de versão   | Git / GitHub                  |
| Fonte dos dados      | SIPRI Arms Transfers Database |

## Estrutura do projeto

```text
desafio_uniesp/
│
├── app.py
├── read_data.py
├── README.md
├── requirements.txt
│
├── output/
│   ├── Country_exports_by/
│   └── Country_recipient/
│
├── src/
│   ├── analytics.py
│   ├── charts.py
│   ├── config.py
│   ├── data.py
│   └── __pycache__/
│
└── venv/
```

### `app.py`

Arquivo principal da aplicação Streamlit.

Responsável pela construção da interface do dashboard, aplicação dos filtros, apresentação dos indicadores e integração dos módulos de dados, análises e visualizações.

### `read_data.py`

Responsável pela leitura e preparação inicial dos dados utilizados pela aplicação.

### `src/data.py`

Centraliza as operações relacionadas aos dados, incluindo:

* Carregamento dos datasets;
* Preparação dos dados;
* Filtragem por período;
* Seleção de países;
* Organização dos dados utilizados pelo dashboard.

### `src/analytics.py`

Contém as funções responsáveis pelos cálculos analíticos utilizados na aplicação.

Entre as principais operações estão:

* Rankings;
* Totais;
* Crescimento percentual;
* Comparação entre períodos;
* Cálculo de indicadores;
* Análise de exportadores;
* Análise de importadores;
* Análises específicas por país.

### `src/charts.py`

Centraliza a criação das visualizações utilizadas no dashboard.

Os gráficos são utilizados para representar visualmente:

* Evolução temporal;
* Rankings;
* Exportações;
* Importações;
* Comparações entre países;
* Indicadores analíticos.

### `src/config.py`

Centraliza configurações utilizadas pelo projeto, incluindo:

* Diretórios;
* Períodos de análise;
* Países;
* Configurações visuais;
* Cores;
* Parâmetros da aplicação.

### `output/`

Diretório destinado aos arquivos de saída utilizados ou gerados pelo projeto.

```text
output/
├── Country_exports_by/
└── Country_recipient/
```

## Instalação

### Linux / macOS

Clone o repositório:

```bash
git clone https://github.com/AbelPhilippe/desafio_uniesp.git
```

Entre no diretório:

```bash
cd desafio_uniesp
```

Crie um ambiente virtual:

```bash
python3 -m venv venv
```

Ative o ambiente virtual:

```bash
source venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

### Windows

Clone o repositório:

```powershell
git clone https://github.com/AbelPhilippe/desafio_uniesp.git
```

Entre no diretório:

```powershell
cd desafio_uniesp
```

Crie o ambiente virtual:

```powershell
python -m venv venv
```

Ative o ambiente:

```powershell
.\venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

## Executar a aplicação

Com o ambiente virtual ativado:

```bash
python -m streamlit run app.py
```

O Streamlit exibirá no terminal o endereço da aplicação.

Por padrão:

```text
http://localhost:8501
```

Abra o endereço exibido no navegador para acessar o dashboard.

## Dados

Os dados utilizados no projeto são provenientes do **SIPRI Arms Transfers Database**, mantido pelo **Stockholm International Peace Research Institute (SIPRI)**.

A base contém informações históricas sobre transferências internacionais de grandes sistemas de armamentos e permite analisar relações entre países exportadores e importadores.

Fonte oficial:

https://www.sipri.org/databases/armstransfers

Interface oficial para consulta dos dados:

https://armstransfers.sipri.org/

## TIV — Trend-Indicator Value

Uma das principais métricas utilizadas no projeto é o **Trend-Indicator Value (TIV)**.

O TIV é uma medida desenvolvida pelo SIPRI para representar o volume de transferências internacionais de grandes sistemas de armamentos.

> **TIV não representa o preço financeiro ou o valor monetário das armas transferidas.**

O indicador é utilizado principalmente para analisar tendências e comparar volumes de transferências ao longo do tempo.

Portanto, os valores de TIV apresentados no dashboard devem ser interpretados como **indicadores de volume de transferências**, e não como valores financeiros em dólares.

## Análises

### Evolução temporal

Permite observar como o volume de transferências de armamentos varia ao longo dos anos.

### Exportadores

Identifica os principais países fornecedores de armamentos dentro do período selecionado.

### Importadores

Identifica os principais países destinatários de armamentos dentro do período selecionado.

### Comparação entre períodos

Permite comparar os níveis de transferência entre diferentes intervalos de tempo.

### Crescimento percentual

A variação percentual entre dois períodos é calculada utilizando:

```text
Crescimento (%) =
((Valor final - Valor inicial) / Valor inicial) × 100
```

Valores positivos representam crescimento.

Valores negativos representam redução.

### Relação entre exportações e importações

O dashboard permite comparar os volumes relativos de exportações e importações utilizando os indicadores disponíveis no dataset.

## Exemplo de análise

Considerando uma redução do TIV de:

```text
8.793 → 5.404
```

a variação corresponde aproximadamente a:

```text
-38,55%
```

Ou seja, houve uma redução de aproximadamente **38,55%** no indicador.

O valor final corresponde aproximadamente a **61,45% do valor inicial**.

Essa interpretação representa uma variação do indicador TIV e não uma perda financeira equivalente.

## Indicadores e insights

O dashboard pode ser utilizado para identificar padrões como:

* Mudanças na participação de países exportadores;
* Mudanças na participação de países importadores;
* Crescimento ou redução de transferências;
* Alterações no perfil de transferência de determinado país;
* Períodos de maior atividade de exportação ou importação;
* Comparações históricas entre países.

Os resultados dependem do período e dos filtros selecionados pelo usuário.

## Objetivo acadêmico

O projeto foi desenvolvido para aplicar conceitos de **Engenharia de Dados, Ciência de Dados e Visualização de Dados** sobre uma base de dados real.

A aplicação demonstra, de forma prática:

* Manipulação e preparação de dados;
* Organização de datasets;
* Análise exploratória;
* Criação de métricas;
* Cálculo de indicadores;
* Visualização de dados;
* Construção de dashboards interativos;
* Separação entre processamento, análise e visualização;
* Desenvolvimento colaborativo utilizando Git e GitHub.

## Controle de versão

O projeto utiliza **Git** para controle de versão e **GitHub** para colaboração.

Novas funcionalidades podem ser desenvolvidas em branches independentes antes de serem integradas à branch principal.

Exemplo:

```text
main
  ↑
  └── sipri_ui_v13_country-intelligence
```

As alterações podem ser enviadas para o GitHub por meio de commits:

```bash
git add .
git commit -m "Descrição da alteração"
git push
```

Quando uma funcionalidade estiver pronta, ela pode ser integrada à `main` utilizando um **Pull Request**.

## Requisitos

* Python 3.10 ou superior;
* Git;
* pip;
* Ambiente virtual Python recomendado.

As bibliotecas utilizadas pela aplicação estão especificadas no arquivo:

```text
requirements.txt
```

## Execução rápida

Para executar o projeto rapidamente:

```bash
git clone https://github.com/AbelPhilippe/desafio_uniesp.git
cd desafio_uniesp

python3 -m venv venv
source venv/bin/activate

python -m pip install -r requirements.txt

python -m streamlit run app.py
```

No Windows:

```powershell
git clone https://github.com/AbelPhilippe/desafio_uniesp.git
cd desafio_uniesp

python -m venv venv
.\venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt

python -m streamlit run app.py
```

## Fonte e proveniência dos dados

O dataset utilizado neste projeto foi obtido a partir do **SIPRI Arms Transfers Database**, mantido pelo Stockholm International Peace Research Institute.

Os dados são utilizados neste projeto para fins **acadêmicos e educacionais**, permitindo demonstrar técnicas de manipulação, análise e visualização de dados.

Para informações sobre metodologia, cobertura, limitações e definição das métricas, consulte a documentação oficial do SIPRI.

## Considerações sobre os dados

Os resultados apresentados no dashboard devem ser interpretados de acordo com a metodologia utilizada pelo SIPRI.

Em particular:

* TIV não corresponde ao valor financeiro das armas;
* Variações de TIV representam mudanças no indicador de volume de transferências;
* Comparações entre países devem considerar o período selecionado;
* Crescimentos percentuais dependem dos valores inicial e final utilizados;
* Valores de TIV não devem ser interpretados diretamente como dólares ou outra moeda.

## Licença e uso

Este projeto foi desenvolvido para fins **educacionais e acadêmicos** como parte do desafio do **UNIESP MBA em Engenharia e Ciência de Dados**.

Os dados analisados são provenientes do **SIPRI Arms Transfers Database** e estão sujeitos às condições de uso estabelecidas pelo SIPRI.

## Autores

Projeto desenvolvido para:

**UNIESP — MBA em Engenharia e Ciência de Dados**

Repositório:

https://github.com/AbelPhilippe/desafio_uniesp
