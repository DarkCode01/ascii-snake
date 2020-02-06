import shutil

def setup():
    # get dimensions of screen
    columns, rows = shutil.get_terminal_size()
    columns, rows = (columns - 8) // 3, rows - 20

    # Verify hardcode mode
    hardcode_mode = input("Hardcode Mode (yes/no) > ")
    hardcode_mode = True if hardcode_mode.lower() == 'yes' else False

    return {
        'hardcode_mode': hardcode_mode,
        'dimensions': {
            'rows': rows,
            'columns': columns
        }
    }