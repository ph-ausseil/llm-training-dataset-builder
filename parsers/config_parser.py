import xml.etree.ElementTree as ET
import parsers.custom.sample_orders_parser as order_parser
import json
#import psycopg2 #For PostegreSQL implementation


def generate_qa_pairs(dataset):
    treated_dataset = dataset_pretreatment(dataset)
    # Generate question-answer pairs
    qa_pairs = generate_instructions(treated_dataset)
    return qa_pairs

def dataset_pretreatment(dataset):
    # If you don't need any custom dataset preprocessing, return the dataset as is
    """
    return dataset
    """

    # Uncomment the line below and implement dataset_pretreatment_custom for your custom preprocessing
    return order_parser.dataset_pretreatment_custom(dataset)



def generate_instructions(dataset):
    # This is a default implementation that returns a single instruction for the given dataset
    """
    return [{'instruction': dataset['instruction'],'input': dataset['input'], 'output': dataset['instruction']}]
    """

    # Uncomment the line below and implement generate_instructions_custom for your custom instructions generation
    return order_parser.generate_instructions_custom(dataset)
    


#example of process_xml_file implementation
def process_xml_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    # Uncomment this block and replace the values in the Dictionary to create a custom dataset from the XML
    """
    dataset = {
        'instruction': root.attrib['instruction'],
        'input': root.attrib['input'],
        'output': root.attrib['instruction']
    }
    """

    #This is an example of dataset this comment to get a template of work
    dataset = {
        'order_id': root.attrib['id'],
        'order_date': root.attrib['date'],
        'items': list(root.find("Items")),
        'seller': root.find('Seller').attrib['firstname'] + ' ' + root.find('Seller').attrib['lastname'],
        'customer_email': root.find('Customer').attrib['email'],
        'customer_id': root.find('Customer').attrib['id']
    }
    # Generate question-answer pairs
    qa_pairs = generate_qa_pairs(dataset)

    return qa_pairs

def process_json_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)

    dataset = {
        'instruction': data['instruction'],
        'input': data['input'],
        'output': data['output']
    }

    qa_pairs = generate_qa_pairs(dataset)
    return qa_pairs

def process_database(user, password, host, port, database):
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(
        user= PARAM_DATABASE_USER,
        password= PARAM_DATABASE_DBPASSWORD,
        host= PARAM_DATABASE_HOST,
        port= PARAM_DATABASE_PORT,
        database=PARAM_DATABASE_DBNAME
    )

    # Fetch data from the database
    cursor = connection.cursor()
    cursor.execute("SELECT instruction, input, output FROM your_table_name;")
    data = cursor.fetchall()

    # Close the database connection
    cursor.close()
    connection.close()

    # Process the data and generate question-answer pairs
    qa_pairs = []
    for row in data:
        dataset = {
            'instruction': row[0],
            'input': row[1],
            'output': row[2]
        }
        qa_pairs.extend(generate_qa_pairs(dataset))

    return qa_pairs
