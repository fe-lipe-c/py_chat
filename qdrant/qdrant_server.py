from pathlib import Path
from typing import Optional
from qdrant_client.http.models import VectorParams, Distance
from qdrant_client.http import models
import config as cfg


def new_collection(collection_name: str, vector_size: int = 1536):
    """
    Creates a new collection in the database with the specified name and vector
    size. If the collection already exists, it prints a message and returns
    without creating a new collection.

    Args:
        collection_name (str): The name of the collection to be created.
        vector_size (int, optional): The size of the vectors in the collection.
        Defaults to 1536.

    Returns:
        None. Prints a message if the collection already exists.
    """
    # Check if collection already exists.
    # Get a list of all existing collections in the database
    list_db = []
    for i in cfg.QDRANT_DB_CLIENT.get_collections().collections:
        list_db.append(i.name)
    # If the specified collection is in the list of existing collections, print
    # a message and return
    if collection_name in list_db:
        return (
            f"Collection '{collection_name}' already exists. It contains {cfg.QDRANT_DB_CLIENT.count(collection_name=collection_name).count} vectors.",
            "collection_exists",
        )

    # If the collection doesn't exist, create a new one with the specified name
    # and vector configuration
    else:
        cfg.QDRANT_DB_CLIENT.recreate_collection(
            collection_name=collection_name,
            vectors_config={
                "content": models.VectorParams(
                    distance=models.Distance.COSINE,
                    size=vector_size,
                ),
            },
        )

        # Create a folder for the collection's documents
        collection_path = cfg.CONTEXT_DOCS_PATH / collection_name
        collection_to_process_path = collection_path / "to_process"
        collection_processed_path = collection_path / "processed"

        Path.mkdir(collection_path, parents=True, exist_ok=True)
        Path.mkdir(collection_to_process_path, parents=True, exist_ok=True)
        Path.mkdir(collection_processed_path, parents=True, exist_ok=True)
        return f"Collection '{collection_name}' created successfully.", "success"


def delete_collection(collection_name: str):
    """
    Deletes a collection from the database.

    Args:
        collection_name (str): The name of the collection to be deleted.

    Returns:
        None. Prints a message if the collection doesn't exist.
    """
    # Check if collection exists.
    # Get a list of all existing collections in the database
    list_db = []
    for i in cfg.QDRANT_DB_CLIENT.get_collections().collections:
        list_db.append(i.name)
    # If the specified collection is not in the list of existing collections,
    # print a message and return
    if collection_name not in list_db:
        return print(f"Collection '{collection_name}' does not exist.")

    # If the collection exists, delete it
    cfg.QDRANT_DB_CLIENT.delete_collection(collection_name=collection_name)


def list_collection(collection_name: Optional[str] = None):
    """
    Lists the collections in the database. If a collection name is provided, it
    lists the vectors in that collection. If no collection name is provided, it
    lists all the collections in the database along with their vector counts.

    Args:
        collection_name (Optional[str], optional): The name of the collection
        to list vectors from. If None, lists all collections. Defaults to None.

    Returns:
        list: A list of vectors in the specified collection if a collection
        name is provided and its vectors. Otherwise, returns None and
        prints the vector count for all collections.
    """

    # If no specific collection is specified, list all collections in the database
    if collection_name is None:
        nr_collections = len(cfg.QDRANT_DB_CLIENT.get_collections().collections)
        print(f"There are {nr_collections} collections in the database:\n")
        for collection in cfg.QDRANT_DB_CLIENT.get_collections().collections:
            print(
                f"'{collection.name}': {cfg.QDRANT_DB_CLIENT.count(collection_name=collection.name).count} vectors"
            )

    else:
        # If a specific collection is specified, list the vectors in that collection
        vector_count = cfg.QDRANT_DB_CLIENT.count(collection_name=collection_name).count

        # If the collection contains vectors, get the vectors
        if vector_count > 0:
            db_points = cfg.QDRANT_DB_CLIENT.scroll(
                collection_name=collection_name,
                scroll_filter=models.Filter(),
                with_vectors=True,
                limit=vector_count,
            )
            db_points = db_points[0]
        else:
            db_points = None

        print(f"Collection '{collection_name}' contains {vector_count} vectors.")
        return db_points
