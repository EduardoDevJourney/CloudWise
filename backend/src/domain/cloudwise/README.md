# Cloud Wise — Supporting Subdomain

Leitura de custos Azure e dashboard. No MVP, dados gerados pelo seed.

## Modelo

Esquema estrela: `fact_custo` ligada a `dim_data`, `dim_servico` e `dim_assinatura`.
O repositório (`CostsRepository`) filtra e agrega em SQL.

## Entidades

- `CostRecord` — visão achatada de um fato com suas dimensões, usada pela API
