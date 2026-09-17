(SELECT nome_cbo, LENGTH(nome_cbo) as tamanho, 'Maior' as tipo from occupations order by tamanho DESC LIMIT 1)

UNION ALL

(SELECT nome_cbo, LENGTH(nome_cbo) as tamanho, 'Menor' as tipo from occupations where nome_cbo is not null AND nome_cbo <> '' order by tamanho ASC LIMIT 1)
