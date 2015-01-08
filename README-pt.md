Este repositório contém um novo *scraper* para extrair os dados do banco do CAGR para serem usados pelo CAPIM e
derivados. Ele vem com um *pipeline* para MongoDB e um para arquivo JSON como um exemplo do que pode ser feito com um
*framework* de *scraping* flexível como o Scrapy.

O **moita-scrapy** primeiro faz login com as credenciais providenciadas em [moita/settings.py](moita/settings.py), e
então procede para a tabela de dados para coletar os dados necessários para o *scraping*. O *crawler* é muito simples,
com menos de 150 linhas e em grande parte só são necessárias porque o CAGR é excessivamente complexo e mal feito.

Para usar o seu próprio pipeline (por exemplo, se você quer salvar os dados extraídos para um formato específio ou banco
de dados diferente), leia a documentação do Scrapy. Links para páginas relevantes da documentação estão incluídos no
topo de cada arquivo.

Para mudar o formato do resultado dos dados coletados, por favor leia a função ***parse*** dentro de ***CagrSpider*** em 
[moita/spiders/cagr.py](moita/spiders/cagr.py). Atualmente, os dados são coletados como:

Campus:
- id do campus (int), ex: 1 para FLO
- nome do campus (str), ex: FLO para Florianópolis
- disciplinas do campus (list):
  - id da disciplina (str), ex: INE5401
  - nome da disciplina (str), ex: Introdução à Computação
  - carga horária (int), ex: 36
  - turmas (list):
    - id da turma (str), ex: 01208A
    - vagas totais (int), ex: 50
    - vagas ocupadas (int), ex: 35
    - vagas especiais (int), ex: 5
    - horários (list):
      - dia (int), ex: 2 para segunda-feira
      - sala (str), ex: AUX-ALOCAR
      - hora (list), ex: ['1010', '1100'] se a aula começa em 10:10 e dura 2 aulas
    - professores(list), ex: ['Rafael Luiz Cancian', 'José Luis Güntzel']

Embora pareça complexo, é muito fácil para atravessar e fazer operações de busca, assumindo que você divida em diversas
classes. O JSON resultante para EaD (maior arquivo) tem em torno de 1.7MB e pode ser comprimido para cerca de 219KB com
gzip. O arquivo pode ser ainda mais reduzido se você manter o formato original de tempo (ex: `2.0820-2 / AUX-ALOCAR`) ou
removendo dados padrão (ex: quando as vagas são 0) mas isso reduz a expressividade dos dados e não ajuda tanto depois da
compressão gzip.

Este *crawler* foi inspirado pelo original feito por [Ramiro Polla](@ramiropolla) que pode ser encontrado em 
[ramiropolla/matrufsc_dbs](https://github.com/ramiropolla/matrufsc_dbs), tentando fazer os dados serem mais úteis e
mantendo o código limpo e legível, tanto quanto *web scraping* e XPath me permitiram.

**Observação**: este software foi feito enquanto meu provedor de internet havia bloqueado o GitHub por algum motivo
obscuro desconhecido. É por isso que depois de algum tempo eu desisti de fazer versionamento git e decidi apenas lançar
quando estivesse pronto. Eu devo voltar ao versionamento normal agora que cancelei o serviço.

Este trabalho está duplamente licenciado pela [MIT License](https://tldrlegal.com/license/mit-license) e pela
[Beerware License](https://tldrlegal.com/license/beerware-license).