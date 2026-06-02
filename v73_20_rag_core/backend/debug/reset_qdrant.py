from backend.core.qdrant_store import QdrantStore


def main():

    db = QdrantStore()

    try:
        db.client.delete_collection(
            collection_name=db.collection_name
        )

        print(
            f"Deleted collection: "
            f"{db.collection_name}"
        )

    except Exception as e:

        print(
            f"Delete failed: {e}"
        )


if __name__ == "__main__":
    main()