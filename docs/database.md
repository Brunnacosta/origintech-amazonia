# Banco de Dados - OriginTech Amazônia

## Fluxo Principal

Usuário
↓
Produtor
↓
Fazenda
↓
Talhão
↓
Lote

---

# Relacionamentos

Usuário (1) → (1) Produtor

Produtor (1) → (N) Fazendas

Fazenda (1) → (N) Talhões

Talhão (1) → (N) Lotes

---

# Entidades

## Usuário

- id
- nome
- email
- senha_hash
- tipo
- ativo
- criado_em

---

## Produtor

- id
- usuario_id
- cpf_cnpj
- telefone
- data_nascimento
- municipio
- estado
- bio
- foto

---

## Fazenda

- id
- produtor_id
- nome
- area_total
- municipio
- estado
- latitude
- longitude

---

## Talhão

- id
- fazenda_id
- nome
- area
- tipo_cultivo

---

## Lote

- id
- talhao_id
- codigo
- safra
- data_colheita
- fermentacao
- secagem
- peso
- status