# Set PARAM_ACTIVATE_CONFIG to False to force using command-line parameters
# Set PARAM_ACTIVATE_CONFIG to True to use the parameters defined in this config.py file
PARAM_ACTIVATE_CONFIG = True

# PARAM_OUTPUT_DIR specifies the directory where the generated training set will be stored
PARAM_OUTPUT_DIR = './output/sample-order-json/'

# PARAM_OUTPUT_MERGE_FILE determines if the output should be merged into a single file
PARAM_OUTPUT_MERGE_FILE = True
# PARAM_OUTPUT_MERGE_FILE_NAME specifies the name of the merged output file
PARAM_OUTPUT_MERGE_FILE_NAME = 'sample.json'

# PARAM_METHOD specifies the data processing method, possible values are:
# 'xmls', 'xml', 'jsons', 'json', 'database'
PARAM_METHOD = 'xmls'

# PARAM_XML_PATH specifies the path to a single XML file to process
PARAM_XML_PATH = './input/sample-order-xml/sample.xml'
# PARAM_XMLS_PATH specifies the directory containing multiple XML files to process
PARAM_XMLS_PATH = './input/sample-order-xml/'

# PARAM_JSON_PATH specifies the path to a single JSON file to process
PARAM_JSON_PATH = './input/sample-order-json/sample.json'
# PARAM_JSONS_PATH specifies the directory containing multiple JSON files to process
PARAM_JSONS_PATH = './input/sample-order-json/'

# Database configuration parameters
# PARAM_DATABASE_HOST specifies the IP address or hostname of the PostgreSQL server
PARAM_DATABASE_HOST = '127.0.0.1'
# PARAM_DATABASE_USER specifies the username to connect to the PostgreSQL server
PARAM_DATABASE_USER = 'username'
# PARAM_DATABASE_DBNAME specifies the name of the database to connect to
PARAM_DATABASE_DBNAME = 'database_name'
# PARAM_DATABASE_DBPASSWORD specifies the password for the PostgreSQL user
PARAM_DATABASE_DBPASSWORD = 'database_password'
# PARAM_DATABASE_PORT specifies the port on which the PostgreSQL server is running
PARAM_DATABASE_PORT = '8080'
