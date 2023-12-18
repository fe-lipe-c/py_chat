import streamlit as st
import openai
import config as cfg
from scripts.embeddings_db import delete_collection, new_collection
import scripts.bbg_chat as bbg_chat


def init_session():
    # Session state initialization
    if "selected_collection" not in st.session_state:
        st.session_state.selected_collection = None


def render_sidebar():
    with st.sidebar:
        st.markdown("Collections")
        # Retrieve the list of collections from Qdrant
        existing_collections = cfg.QDRANT_DB_CLIENT.get_collections().collections
        collection_names = [col.name for col in existing_collections]
        selected_collection = st.selectbox(
            "Select a collection",
            collection_names,
            index=0,
        )
        st.session_state.selected_collection = selected_collection

    with st.sidebar:
        st.markdown("---")
        st.markdown("Create a new collection")
        # Input box for collection name
        collection_name = st.text_input("Enter a collection name:")

        # Button to check or create collection
        if st.button("Create Collection"):
            if collection_name:
                message = new_collection(collection_name)
                if message[1] == "success":
                    st.success(message[0])
                elif message[1] == "collection_exists":
                    st.warning(message[0])
            else:
                st.error("Please enter a collection name.")

    with st.sidebar:
        st.markdown("---")
        st.markdown("Delete collection")
        # Input box for collection name
        collection_name = st.session_state.selected_collection

        # Button to check or create collection
        if st.button("Delete Collection"):
            if collection_name:
                delete_collection(collection_name)
                st.success(f"Collection '{collection_name}' deleted successfully.")
            else:
                st.error("Please enter a collection name.")


def main_panel():
    st.markdown(f"{st.session_state.selected_collection}")


def main():
    init_session()
    render_sidebar()
    main_panel()


if __name__ == "__main__":
    main()
