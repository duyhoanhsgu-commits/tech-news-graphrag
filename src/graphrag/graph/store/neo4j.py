"""Neo4j graph store implementation."""
from __future__ import annotations

from neo4j import AsyncGraphDatabase

from graphrag.core.config import Settings
from graphrag.graph.store.base import BaseGraphStore
from graphrag.schemas.entity import Entity
from graphrag.schemas.relationship import Relationship


class Neo4jGraphStore(BaseGraphStore):
    def __init__(self, settings: Settings) -> None:
        self._driver = AsyncGraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password),
        )
        self._database = settings.neo4j_database

    async def upsert_entities(self, entities: list[Entity]) -> None:
        query = """
        UNWIND $entities AS e
        MERGE (n:Entity {entity_id: e.entity_id})
        SET n.name = e.name,
            n.type = e.type,
            n.description = e.description
        """
        data = [e.model_dump() for e in entities]
        async with self._driver.session(database=self._database) as session:
            await session.run(query, entities=data)

    async def upsert_relationships(self, relationships: list[Relationship]) -> None:
        query = """
        UNWIND $rels AS r
        MATCH (src:Entity {entity_id: r.source_entity_id})
        MATCH (tgt:Entity {entity_id: r.target_entity_id})
        MERGE (src)-[rel:RELATED_TO {relationship_id: r.relationship_id}]->(tgt)
        SET rel.type = r.relationship_type,
            rel.description = r.description
        """
        data = [r.model_dump() for r in relationships]
        async with self._driver.session(database=self._database) as session:
            await session.run(query, rels=data)

    async def get_neighbors(
        self,
        entity_ids: list[str],
        max_hops: int = 1,
    ) -> list[dict]:
        query = f"""
        MATCH (n:Entity)-[r*1..{max_hops}]-(m:Entity)
        WHERE n.entity_id IN $ids
        RETURN n, r, m LIMIT 100
        """
        async with self._driver.session(database=self._database) as session:
            result = await session.run(query, ids=entity_ids)
            return [record.data() async for record in result]

    async def clear(self) -> None:
        async with self._driver.session(database=self._database) as session:
            await session.run("MATCH (n) DETACH DELETE n")

    async def close(self) -> None:
        await self._driver.close()
