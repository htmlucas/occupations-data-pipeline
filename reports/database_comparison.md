# Comparação entre PostgreSQL Local e Amazon RDS

## Objetivo

Comparar os dados armazenados no PostgreSQL local e no PostgreSQL hospedado no Amazon RDS.

A comparação utiliza as mesmas consultas de validação nos dois ambientes.

## Resultados

| Métrica | PostgreSQL Local | Amazon RDS | Resultado |
|---|---:|---:|---|
| Total de registros | 2694 | 2694 | ✅ Igual |
| CBOs distintos | 2694 | 2694 | ✅ Igual |
| CBOs duplicados | 0 | 0 | ✅ Igual |
| Nomes nulos/vazios | 0 | 0 | ✅ Igual |

## Interpretação

A comparação verifica se os dois ambientes possuem o mesmo estado dos dados carregados.

### PostgreSQL Local

- Total de registros: **2694**
- CBOs distintos: **2694**
- CBOs duplicados: **0**
- Nomes nulos/vazios: **0**

### Amazon RDS

- Total de registros: **2694**
- CBOs distintos: **2694**
- CBOs duplicados: **0**
- Nomes nulos/vazios: **0**

## Conclusão

Os dois ambientes apresentaram os mesmos resultados para as validações realizadas.