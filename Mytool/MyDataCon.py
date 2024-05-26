from pathlib import Path


def convert_dataframe_to_csv(input_dataframe, output_file):
    filepath = Path(output_file)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    print('Output csv path: ', filepath)
    input_dataframe.to_csv(filepath)

