def read_csv_from_file(file):
    file_contents_bytes = file.read()
    file_contents = file_contents_bytes.decode("utf-8")
    return file_contents.split('\n')

def transform_file_rows_to_objects(file_contents_array):
    headers = file_contents_array[0].split(',')
    rows = file_contents_array[1:]
    for i in range(len(rows)):
        row_json = {}
        columns = rows[i].split(",")
        for j in range(len(headers)):
            row_json[headers[j]] = columns[j]
        rows[i] = row_json

    return rows