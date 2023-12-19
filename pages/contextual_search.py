import os
import streamlit as st
import openai
import config as cfg
import qdrant.qdrant_server as qs
import shutil


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
                message = qs.new_collection(collection_name)
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
                qs.delete_collection(collection_name)
                st.success(f"Collection '{collection_name}' deleted successfully.")
            else:
                st.error("Please enter a collection name.")


def main_panel():
    st.markdown(f"### {st.session_state.selected_collection}")
    list_embbedings = qs.list_collection(st.session_state.selected_collection)
    nr_embbedings = len(list_embbedings) if list_embbedings else 0
    st.markdown(f"Number of documents in collection: {nr_embbedings}")

    st.markdown("---")

    uploaded_file = st.file_uploader("Upload a document")
    if uploaded_file is not None:
        # Define the file path
        file_path = os.path.join(
            cfg.CONTEXT_DOCS_PATH / st.session_state.selected_collection / "to_process",
            uploaded_file.name,
        )

        # Save the file to the to_process folder
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"File '{uploaded_file.name}' uploaded successfully.")

    # List the documents in the to_process folder
    list_to_process = os.listdir(
        cfg.CONTEXT_DOCS_PATH / st.session_state.selected_collection / "to_process"
    )
    if list_to_process:
        st.markdown("Documents to process:")
        for file in list_to_process:
            st.markdown(f"{file}")


def main():
    init_session()
    render_sidebar()
    main_panel()


if __name__ == "__main__":
    main()
