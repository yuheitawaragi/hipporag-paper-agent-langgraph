from llama_index.core import (
    StorageContext,
    load_index_from_storage,
)


class LlamaIndexLoader:

    @staticmethod
    def load(persist_dir: str):

        storage = StorageContext.from_defaults(
            persist_dir=persist_dir
        )

        return load_index_from_storage(storage)