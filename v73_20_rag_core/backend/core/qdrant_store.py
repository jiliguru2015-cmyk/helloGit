from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct
)

from backend.config import settings


class QdrantStore:

    def __init__(self):

        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT
        )

        self.collection_name = settings.COLLECTION_NAME

    def ensure(self):

        collections = self.client.get_collections().collections

        names = [
            c.name
            for c in collections
        ]

        if self.collection_name in names:
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=768,
                distance=Distance.COSINE
            )
        )

    def upsert(
        self,
        _id,
        vector,
        payload
    ):

        self.ensure()

        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=_id,
                    vector=vector,
                    payload=payload
                )
            ]
        )

    def search(
        self,
        vector,
        top_k=5
    ):

        self.ensure()

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=vector,
            limit=top_k,
            with_payload=True
        )

        return list(results.points)

    def count(self):

        self.ensure()

        info = self.client.get_collection(
            collection_name=self.collection_name
        )

        return info.points_count

    def reset(self):

        collections = self.client.get_collections().collections

        names = [
            c.name
            for c in collections
        ]

        if self.collection_name in names:

            self.client.delete_collection(
                collection_name=self.collection_name
            )

        self.ensure()