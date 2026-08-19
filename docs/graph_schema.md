# Graph Schema

## Nodes

### Article
| Property | Type | Description |
|---|---|---|
| `article_id` | String | Primary key |
| `title` | String | Article headline |
| `url` | String | Source URL |
| `published_at` | DateTime | Publication date |

### Chunk
| Property | Type | Description |
|---|---|---|
| `chunk_id` | String | Primary key (MD5) |
| `article_id` | String | Parent article |
| `chunk_index` | Int | Position in article |

### Entity
| Property | Type | Description |
|---|---|---|
| `entity_id` | String | UUID |
| `name` | String | Canonical name |
| `type` | String | Person / Org / Location / … |
| `description` | String | Short description |

## Relationships

| Type | From → To | Description |
|---|---|---|
| `PART_OF` | Chunk → Article | Chunk belongs to article |
| `MENTIONS` | Chunk → Entity | Chunk mentions entity |
| `RELATED_TO` | Entity → Entity | Generic semantic relation |
| `WORKS_FOR` | Entity(Person) → Entity(Org) | Employment |
| `LOCATED_IN` | Entity → Entity(Location) | Location membership |
| `CO_OCCURS_WITH` | Entity → Entity | Co-mentioned in same chunk |

## Cypher Index Queries

```cypher
CREATE INDEX entity_name FOR (e:Entity) ON (e.name);
CREATE INDEX entity_type FOR (e:Entity) ON (e.type);
CREATE INDEX article_id FOR (a:Article) ON (a.article_id);
```
