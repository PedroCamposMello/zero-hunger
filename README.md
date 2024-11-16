# 1. Problema de negócio

A empresa Fome Zero é um marketplace de restaurantes. Ou seja, seu negócio principal é facilitar o encontro e negociações de clientes e restaurantes. Os restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas e também uma nota de avaliação dos serviços e produtos do restaurante, dentre outras informações.

O CEO Guerra precisa entender melhor o negócio para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a Fome Zero, e para isso, ele precisa que seja feita uma análise nos dados da empresa e que sejam gerados dashboards, a partir dessas análises.

# 2. Premissas assumidas para a análise

1. A base de dados contém as informações mais atuais.
2. Os tipos de culinária de cada registro da base forma simplificados para conter apenas um tipo de culinária.
3. Foi considerado que o primeiro tipo de culinária de cada registro é o mais representativo.
4. Para ranquear os restaurantes com base na avaliação, o critério de  desempate é que o restaurante de menor ID assume a liderança.

# 3. Estratégia da solução

O dashboard foi desenvolvido utilizando as métricas que refletem as 4 principais visões do modelo de negócio da empresa:

1. Visão geral com os restaurantes cadastrados.
    1. Total de restaurantes registrados.
    2. Total de restaurantes com disponibilidade de delivery online.
    3. Total de países diferentes presentes na base de dados.
    4. Total de tipos de culinária presentes na base de dados.
    5. Total de restaurantes com disponibilidade reserva de mesas.
    6. Total de restaurantes com disponibilidade de delivery.
    7. Total de cidade diferentes na base de dados.
    8. Total de avaliações realizadas pelos usuários.
2. Visão focada nas métricas agrupadas por país.
    1. Quantidade total de restaurantes cadastrados por país.
    2. Quantidade de cidades cadastradas por país.
    3. Avaliação média dos restaurantes por país.
    4. Custo médio, para duas pessoas, do restaurante por país.
3. Visão focada nas métricas agrupadas por cidade.
    1. Contagem de restaurantes por cidades.
    2. Cidades com maior e menor média de avaliação dos restaurantes.
    3. Cidades com maior diversidade de culinárias disponíveis.
4. Visão focada nas métricas agrupadas por tipo de culinária.
    1. Os restaurantes mais bem avaliados dos principais tipos de culinária com base na avaliação média.
    2. Os top 10 restaurantes mais bem avaliados.
    3. Os tipos de culinária mais bem avaliados com base na média dos restaurantes.
    4. Os tipos de culinária mais mal avaliados com base na média dos restaurantes.

# 4. Top 3 Insights de dados

1. Índia e Estados Unidos são os países mais presentes na base de dados, juntos eles representam aproximadamente 65% da base de dados.
2. O tipo de culinária mais bem avaliado está classificado com “outros”.
3. Embora represente a maior parte da base de dados, nenhuma cidade indiana está presente no ranque de cidades com maior diversidade de culinária, sugerindo que há pouca diversidade culinária na Índia.

# 5. O produto final do projeto

Painel online, hospedado em um Cloud e disponível para acesso em qualquer dispositivo conectado à internet. 

O painel pode ser acessado através desse link: https://zero-hunger-at6bpu2u9tmxwgtjs8ywaf.streamlit.app/

# 6. Conclusão

O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor forma possível para o CEO.

# 7. Próximo passos

- Converter os custos dos restaurantes para uma única unidade monetária para permitir uma melhor análise baseada em custos.
- Remover a premissa simplificadora que atribui apenas um tipo de culinária por restaurante e verificar o impacto dessa medida no tipo de culinária “outros”.
