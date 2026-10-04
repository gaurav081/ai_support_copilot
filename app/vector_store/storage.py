import json


def save_documents(
    documents: list[dict],
    file_path: str
) -> None:

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            documents,
            file,
            ensure_ascii=False,
            indent=2
        )


def load_documents(
    file_path: str
) -> list[dict]:

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)