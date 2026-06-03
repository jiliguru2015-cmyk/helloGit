from backend.core.doc_store import DocStore


def main():

    store = DocStore()

    docs = store.load_all()

    print("\n====================")
    print("DOC STORE TEST")
    print("====================")

    print(
        f"Loaded Chunks: {len(docs)}"
    )

    for i, doc in enumerate(
        docs[:10]
    ):

        print(
            f"\n[{i}] "
            f"{doc.get('source')}"
        )

        print(
            doc.get(
                "text",
                ""
            )[:120]
        )

    print("\nDONE\n")


if __name__ == "__main__":
    main()