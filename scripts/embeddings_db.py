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
