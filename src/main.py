from reader import Reader
from writer import Writer
from processors.apply_processing import apply_processing
from validators.validate_dataset import validate_processed_dataset

def main():
    reader_instance: Reader = Reader()
    writer_instance: Writer = Writer()

    datasets = reader_instance.read_from_folder()

    processed_datasets = []
    verbose = False
    for dataset in datasets:
        processed_dataset = apply_processing(dataset, verbose)
        validate_processed_dataset(processed_dataset)
        processed_datasets.append(processed_dataset)

    writer_instance.write_to_folder(processed_datasets)


if __name__ == '__main__':
    main()