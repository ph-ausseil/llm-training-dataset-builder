import xml.etree.ElementTree as ET
import parsers.custom.sample_orders_parser as order_parser
import json
import psycopg2 #For PostegreSQL implementation


def dataset_pretreatment(dataset):
    # If you don't need any custom dataset preprocessing, return the dataset as is
    """
    return dataset
    """

    # Uncomment the line below and implement dataset_pretreatment_custom for your custom preprocessing
    return dataset_pretreatment_custom(dataset)



def generate_instructions(dataset):
    # This is a default implementation that returns a single instruction for the given dataset
    """
    return [{'instruction': dataset['instruction'],'input': dataset['input'], 'output': dataset['instruction']}]
    """

    # Uncomment the line below and implement generate_instructions_custom for your custom instructions generation
    return generate_instructions_custom(dataset)
    


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

# As is, the program runs the example provided. To use it for your own need :  

# Edit 1 of the 3 process (in v1 only process_xml_file is implemented )
#     process_xml_file(filename) #remove the comment & replace the values in the Dictionary
#     process_json_file(filename) #to implement 
#     process_database(user, password, ip, database, output_dir) # to implement 

# comment 1 line in : 
#     dataset_pretreatment(dataset) : to cure data before generating instructions
#     generate_instructions(treated_dataset) : to generate instructions

# To try this example type : 
#       python sample-xml-to-json-by-chatgpt.py --xmls=./input/sample-order-xml/ . 
#       python sample-xml-to-json-by-chatgpt.py 

# The example is 'complex' and require it's own 'custom parser' as it involve creating tailored instructions for a specific business environment
#     Data had to be preprocessed in dataset_pretreatment
#     Complex set of instructions had to be generated in generate_instructions

# Author : Pierre-Henri AUSSEIL
# LinkedIn : linkedin.com/in/ausseil/
# GitHub : github.com/ph-ausseil/
# About the author : I work in Data Integration (Middleware, DataHub, API...) & Service Management. I am not a developper. I wanted to make a proof of concept on uses of LLM in a company stack so the LLM would knows about the business environment and improve a company to make decisions.
# Disclaimer for my employer : This have been developed over 1 week-end on my personal time.


# Knowing, all the issues above can you create a readme.md ? 