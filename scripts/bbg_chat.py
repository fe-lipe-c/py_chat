from pathlib import Path
import shutil
import pandas as pd
from qdrant_client.http import models
import openai
import config as cfg
import os
import pytesseract
from pdf2image import convert_from_path
from scripts.parse_text import parse_text
import time

DATA_PATH = Path("__file__").parent / "data/bbg_chat"
RAW_DATA_PATH = DATA_PATH / "raw"
TO_PROCESS_PATH = DATA_PATH / "to_process"
PROCESSED_PATH = DATA_PATH / "processed"

# Create folders if they don't exist.
Path.mkdir(RAW_DATA_PATH, parents=True, exist_ok=True)
Path.mkdir(TO_PROCESS_PATH, parents=True, exist_ok=True)
Path.mkdir(PROCESSED_PATH, parents=True, exist_ok=True)


def update_database():
    """"""
    # Initialize DataFrame to be inserted into the database
    df_database = pd.DataFrame(
        columns=[
            "sender",
            "content",
            "collection",
            "embedding",
            "timestamp",
        ]
    )

    for filename in os.listdir(TO_PROCESS_PATH):
        db_name, _ = str(filename).split("_")
        # new_collection(db_name)
        filepath = TO_PROCESS_PATH / filename

        doc = convert_from_path(filepath)

        full_text = ""
        print(f"Processing file: {filename}")
        print(f"Total pages: {len(doc)}")
        start = time.time()
        for page_data in doc:
            text = pytesseract.image_to_string(
                page_data,
                lang="por",
            ).encode("utf-8")
            full_text += str(text, "utf-8")

        print(f"Time taken: {time.time() - start}")

        parsed_messages = parse_text(full_text)
        # Generate the text embedding for each message
        for i in range(len(parsed_messages)):
            embedding = openai.Embedding.create(
                input=[parsed_messages[i]["content"]],
                engine="text-embedding-ada-002",
            )
            parsed_messages[i]["embedding"] = tuple(embedding["data"][0]["embedding"])

        df_messages = pd.DataFrame(parsed_messages)
        df_messages["date"] = df_messages["date"].astype(str)

        # Combine date and time into one string
        df_messages["timestamp"] = (
            df_messages["date"] + " " + df_messages["time"].astype(str)
        )

        # Convert to datetime object
        df_messages["timestamp"] = pd.to_datetime(df_messages["timestamp"])

        # Convert to timestamp
        df_messages["timestamp"] = df_messages["timestamp"].astype(int) / 10**9
        df_messages.drop(columns=["date", "time"], inplace=True)

        df_messages["collection"] = db_name

        df_database = pd.concat([df_database, df_messages]).reset_index(drop=True)

        # df_processed = pd.read_pickle(cfg.PROCESSED_PATH / "df_messages.pkl")
        # df_processed = pd.concat([df_processed, df_messages]).reset_index(drop=True)
        # df_processed.to_pickle(cfg.PROCESSED_PATH / "df_messages.pkl")

        shutil.move(filepath, cfg.RAW_DATA_PATH / filename)

    df_processed = pd.read_pickle(cfg.PROCESSED_PATH / "df_messages.pkl")

    df_database["embedding"] = df_database["embedding"].apply(lambda x: tuple(x))
    df_processed["embedding"] = df_processed["embedding"].apply(lambda x: tuple(x))

    df_merged = df_database.merge(
        df_processed,
        on=["sender", "content", "embedding", "collection", "timestamp"],
        how="outer",
        indicator=True,
    )
    df_unique = df_merged[df_merged["_merge"] == "left_only"]
    df_unique.drop(columns=["_merge"], inplace=True)

    df_unique["embedding"] = df_unique["embedding"].apply(lambda x: list(x))
    if len(df_unique) > 0:
        cfg.client.upsert(
            collection_name="all_chat",
            points=[
                models.PointStruct(
                    id=k,
                    vector={
                        "content": v["embedding"],
                    },
                    payload=v.to_dict(),
                )
                for k, v in df_unique.iterrows()
            ],
        )

    df_processed = pd.concat([df_processed, df_database]).reset_index(drop=True)
    df_processed.drop_duplicates(
        subset=["content", "sender", "collection", "timestamp"], inplace=True
    )
    df_processed.to_pickle(cfg.PROCESSED_PATH / "df_messages.pkl")
