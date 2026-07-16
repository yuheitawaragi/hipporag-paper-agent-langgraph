import pickle
from pathlib import Path


class GraphSerializer:


    def save(
        self,
        graph,
        path
    ):
        """
        NetworkX graph保存
        """

        path = Path(path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )


        with open(
            path,
            "wb"
        ) as f:

            pickle.dump(
                graph,
                f
            )



    def load(
        self,
        path
    ):
        """
        NetworkX graph読み込み
        """

        with open(
            path,
            "rb"
        ) as f:

            graph = pickle.load(
                f
            )


        return graph