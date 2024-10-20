from csv import DictReader

from utils import get_embedding_model


def load_data(file_path):
    embedding_model = get_embedding_model()

    session_data = []
    with open(file_path, "r") as f:
        reader = DictReader(f)
        for row in reader:
            name = row['Session Title']
            start_datetime = f'{row["Date"]} {row["Time Start"]}'
            end_datetime = f'{row["End Date (Optional)"]} {row["Time End (Optional)"]}'
            locations = row["Room/Location"]

            vector_embedding_text = f"{name} starts at {start_datetime} "
            if end_datetime == start_datetime:
                vector_embedding_text += f"and goes all day. "
            else:
                vector_embedding_text += f"and ends at {end_datetime}."

            vector_embedding_text += f"It's located at {locations}. "

            vector_embedding_text += row["Description (Optional)"]

            session_data.append({
                "name": name,
                "session_id": row["Session ID"],
                "context": vector_embedding_text,
                "context_embedding": embedding_model.encode(vector_embedding_text).tolist()
            })

        return session_data
