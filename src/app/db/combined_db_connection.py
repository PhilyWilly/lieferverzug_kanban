from kanban_db_connection import get_interesting_produktionslinien
from internal_db_connection import get_every_lieferverzug

def combined_database_data():
    kanban_data = get_interesting_produktionslinien()
    lieferverzug_data = get_every_lieferverzug()

    # Create a dictionary for quick lookup of lieferverzug data by vorgangsnummer
    lieferverzug_dict = {lv['vorgangsnummer']: lv for lv in lieferverzug_data}

    combined_data = []
    for kanban_row in kanban_data:
        vorgangsnummer = kanban_row['vorgangsnummer']
        lieferverzug_info = lieferverzug_dict.get(vorgangsnummer, None)

        combined_row = {
            **kanban_row,
            "lieferverzugs_grund": lieferverzug_info['lieferverzugs_grund'] if lieferverzug_info else None,
            "neue_kw": lieferverzug_info['neue_kw'] if lieferverzug_info else None
        }
        combined_data.append(combined_row)

    return combined_data

if __name__ == "__main__":
    combined_data = combined_database_data()
    for row in combined_data:
        print(row)