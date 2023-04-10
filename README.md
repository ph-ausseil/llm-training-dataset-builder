# Llama-lora-fine-tuner

Works for all with llama-lora & alpaca-lora to finetune llama-based LLM.

This project processes sample orders in various formats (XML, JSON, and PostgreSQL database) and generates question-answer pairs based on the orders' information 😊

The code is designed to be **modular** and easily **customizable**, allowing for various pretreatment methods and instruction generation.

## Features

- Supports processing of XML, JSON, and PostgreSQL database input formats.
- Customizable dataset preprocessing and instruction generation.
- Option to merge output files into a single file.
- Configurable parameters via `config.py` or command-line arguments.

## Files and Functions

### main.py
This is the main entry point for the program. It handles command-line arguments, processes the input files or database, and generates the output files.

### config.py
This file contains configuration parameters that are used throughout the project.
- **PARAM_ACTIVATE_CONFIG**: Whether to use config.py parameters or command-line arguments (True/False).
- **PARAM_OUTPUT_DIR**: The directory where the training set is created.
- **PARAM_OUTPUT_MERGE_FILE**: Whether to merge output files (True/False).
- **PARAM_OUTPUT_MERGE_FILE_NAME**: The name of the merged output file.
- **PARAM_METHOD**: The processing method (values: xmls, xml, jsons, json, database).
- **PARAM_XML_PATH, PARAM_XMLS_PATH, PARAM_JSON_PATH, PARAM_JSONS_PATH**: Input file/directory paths for XML and JSON files.
- **PARAM_DATABASE_HOST, PARAM_DATABASE_USER, PARAM_DATABASE_DBNAME, PARAM_DATABASE_DBPASSWORD, PARAM_DATABASE_PORT**: PostgreSQL database connection parameters.

### config_parser.py
This file contains functions to process XML, JSON, and PostgreSQL database inputs and generate question-answer pairs based on the dataset.
- **dataset_pretreatment(dataset)**: Preprocesses the dataset. Can be customized.
- **generate_instructions(dataset)**: Generates question-answer pairs based on the dataset. Can be customized.
- **process_xml_file(filename)**: Processes an XML file and generates question-answer pairs.
- **process_json_file(filename)**: Processes a JSON file and generates question-answer pairs.
- **process_database(user, password, host, port, database)**: Fetches data from a PostgreSQL database, processes it, and generates question-answer pairs.

### sample_orders_parser.py
This file contains custom functions to pretreat datasets and generate question-answer pairs.
- **remove_duplicates(items_node)**: Removes duplicate items from the items_node based on their description.
- **update_sku_price(item_node, sku_dict, price_dict)**: Updates the SKU and price of the item_node based on the description.
- **apply_inflation(order_date, price, quantity)**: Applies inflation based on the order_date to the price and quantity.
- **calculate_total_price(items_node)**: Calculates the total price of all items in the items_node.
- **update_items_with_inflation(items, order_date)**: Updates the items with inflated prices and quantities based on the order_date.
- **generate_general_instructions(dataset)**: Generates general instructions based on the dataset.
- **generate_item_instructions(item_node)**: Generates item-specific instructions based on the item_node.
- **dataset_pretreatment_custom(dataset)**: Custom function to preprocess the dataset.
- **generate_instructions_custom(dataset)**: Custom function to generate question-answer pairs based on the dataset.

## Getting Started

1. Choose one of the three processing methods to implement:
   - process_xml_file(filename): Processing XML files (already implemented in the example)
   - process_json_file(filename): Processing JSON files (now implemented)
   - process_database(user, password, ip, database, output_dir): Processing records from a database (now implemented)
2. Modify the **dataset_pretreatment(dataset)** function to preprocess the data before generating instructions.
3. Modify the **generate_instructions(treated_dataset)** function to generate the desired instructions.
4. To test the example provided, run one of the following commands:

```sh
python main.py --xmls=./input/sample-order-xml/
```
or
```sh
python main.py --xml=./input/sample-order-xml/sample-file.xml
```
For JSON files:
```sh
python main.py --jsons=./input/sample-order-json/
```
or
```sh
python main.py --json=./input/sample-order-json/sample-file.json
```
For PostgreSQL database:
```sh
python main.py --user=<db_user> --password=<db_password> --ip=<db_host> --database=<db_name>
```

## Author

**Pierre-Henri AUSSEIL**

LinkedIn: [linkedin.com/in/ausseil/](https://linkedin.com/in/ausseil/)
GitHub: [github.com/ph-ausseil/](https://github.com/ph-ausseil/)

## About the author

I work in Data Integration (Middleware, DataHub, API...) & Service Management. I am not a developer. I wanted to make a proof of concept on the uses of LLM in a company stack so the LLM would know about the business environment and improve a company's decision-making.

## Disclaimer for my employer

This has been developed over one weekend on my personal time.

The example included in this program is relatively complex, as it requires a custom parser for a specific business environment. Data preprocessing is performed in the dataset_pretreatment function. The complex set of instructions is generated in the generate_instructions function. By following these steps and referring to the code samples provided, you can adapt this program to process various input formats and generate custom instructions based on your specific requirements.
