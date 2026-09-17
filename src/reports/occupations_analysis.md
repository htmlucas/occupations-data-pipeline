
# Occupations Data Analysis

## Dataset

| Métrica | Resultado |
|---|---:|
| Registros no Parquet | 2694 |
| Registros no PostgreSQL | 2695 |
| CBOs distintos | 2695 |

A quantidade de registros é diferente

---

## Qualidade dos dados

### CBOs duplicados

| Métrica | Resultado |
|---|---:|
| Total de registros | 2695 |
| CBOs distintos | 2695 |
| CBOs duplicados | 0 |

Não foram identificados códigos CBO duplicados na tabela do PostgreSQL.

### Ocupações sem nome

| Métrica | Resultado |
|---|---:|
| Registros sem nome | 1 |

Foi identificado 1 registro com nome de ocupação ausente ou vazio.

---

## Características dos nomes das ocupações

### Maior e menor nome

| Tipo | Ocupação | Tamanho |
|---|---|---:|
| Maior | Operador de máquina de fabricação de produtos de higiene e limpeza (sabão, sabonete, detergente, absorvente, fraldas cotonetes e outros) | 136 |
| Menor | Ator | 4 |

O maior nome possui 136 caracteres, enquanto o menor possui 4 caracteres.

---

## Busca por palavra-chave

### Palavra-chave: `engenheiro`

Foram encontradas 10 ocupações relacionadas ao termo `engenheiro`.

Alguns resultados:

| Código CBO | Ocupação |
|---|---|
| 201105 | Bioengenheiro |
| 202105 | Engenheiro mecatrônico |
| 202110 | Engenheiro de controle e automação |
| 212205 | Engenheiro de aplicativos em computação |
| 212210 | Engenheiro de equipamentos em computação |
| 212215 | Engenheiros de sistemas operacionais em computação |
| 214005 | Engenheiro ambiental |
| 214205 | Engenheiro civil |
| 214210 | Engenheiro civil (aeroportos) |
| 214215 | Engenheiro civil (edificações) |


A consulta foi realizada diretamente no PostgreSQL utilizando uma busca por palavra-chave no nome da ocupação.

---

## Amostra de ocupações

As primeiras 20 ocupações, ordenadas alfabeticamente:

| Ocupação |
|---|
| Abatedor |
| Acabador de calçados |
| Acabador de embalagens (flexíveis e cartotécnicas) |
| Acabador de superfícies de concreto |
| Açougueiro |
| Acrobata |
| Adestrador de animais |
| Administrador |
| Administrador de banco de dados |
| Administrador de edifícios |
| Administrador de fundos e carteiras de investimento |
| Administrador de redes |
| Administrador de sistemas operacionais |
| Administrador em segurança da informação |
| Advogado |
| Advogado (áreas especiais) |
| Advogado (direito civil) |
| Advogado (direito do trabalho) |
| Advogado (direito penal) |
| Advogado (direito público) |



---

## Comparação entre Parquet e PostgreSQL

| Métrica | Parquet | PostgreSQL |
|---|---:|---:|
| Registros | 2694 | 2695 |
| Códigos CBO distintos | 2694 | 2695 |

A quantidade de registros presente no arquivo Parquet corresponde à quantidade de registros carregada no PostgreSQL.

---

## Consultas realizadas

As seguintes análises foram executadas:

- `total_occupations.sql`
- `count_unique_cbo.sql`
- `count_null_or_empty_names_cbos.sql`
- `count_max_and_min_names_cbos.sql`
- `search_occupation.sql`
- `sample_occupations.sql`

---

## Conclusão

A análise confirmou que o dataset processado contém 2694 ocupações e que o PostgreSQL possui 2695 de registros.

Também foram analisados:

- unicidade dos códigos CBO;
- registros sem nome;
- tamanho dos nomes das ocupações;
- busca de ocupações por palavra-chave;
- amostra ordenada dos dados;
- comparação entre o arquivo Parquet e os dados carregados no PostgreSQL.

Essas consultas servem como uma primeira camada de validação e exploração dos dados antes das próximas etapas do pipeline.
 
