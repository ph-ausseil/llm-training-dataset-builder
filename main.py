import os           # import the 'os' module for interacting with the operating system
import glob         # import the 'glob' module for searching file patterns in directories
import argparse     # import the 'argparse' module for parsing command line arguments
import parsers.config_parser # import custom module for parsing XML and JSON files
import json         # import the 'json' module for handling JSON data

from config import ( # import the 'config' module for loading configuration parameters
    PARAM_ACTIVATE_CONFIG, PARAM_METHOD, PARAM_XML_PATH, PARAM_XMLS_PATH,
    PARAM_JSON_PATH, PARAM_JSONS_PATH, PARAM_DATABASE_HOST,PARAM_DATABASE_PORT, PARAM_DATABASE_USER,
    PARAM_DATABASE_DBNAME, PARAM_DATABASE_DBPASSWORD, PARAM_OUTPUT_DIR, PARAM_OUTPUT_MERGE_FILE, PARAM_OUTPUT_MERGE_FILE_NAME
)

# This function takes an input directory, file extension, and output directory as arguments,
# searches for all the files with the given extension in the input directory and processes them using the "process_dataset" function.
# It then writes the output to a JSON file in the output directory. If the configuration parameter PARAM_OUTPUT_MERGE_FILE is set to True,
# it merges all the QA pairs from all files into a single JSON file.
def process_dataset_list(input_dir, extension, output_dir):
    if not os.path.exists(input_dir):
        print(f"Warning: Folder '{input_dir}' not found.")
        return

    # Check if PARAM_OUTPUT_MERGE_FILE is True but PARAM_OUTPUT_MERGE_FILE_NAME is empty
    if PARAM_OUTPUT_MERGE_FILE and PARAM_OUTPUT_MERGE_FILE_NAME == '':
        print(f"Warning: PARAM_OUTPUT_MERGE_FILE_NAME empty.")
        return
    
    all_qa_pairs = []
    files_found = False
    for filename in glob.glob(os.path.join(input_dir, f'*.{extension}')):
        files_found = True
        qa_pairs = process_dataset(filename, extension) # process the current file using the 'process_dataset' function
        if qa_pairs:
            # If PARAM_OUTPUT_MERGE_FILE is False, write output to a JSON file with the same name as the input file
            if PARAM_OUTPUT_MERGE_FILE == False :
                output_filename = os.path.join(output_dir, os.path.basename(filename) + '.json')
                with open(output_filename, "w") as f:
                    json.dump(qa_pairs, f)
            else : # Otherwise, add the QA pairs to a list to be merged later
                all_qa_pairs.extend(qa_pairs)

    if not files_found:
        print(f"Warning: No '{extension}' files found in '{input_dir}'.")
        return
    else : 
        write_merged_json( all_qa_pairs, output_dir) # write merged QA pairs to a JSON file

# This function takes a list of QA pairs and writes them to a JSON file with the given name in the output directory.
# If PARAM_OUTPUT_MERGE_FILE_NAME is empty, it returns a warning message.
def write_merged_json(all_qa_pairs, output_dir) :
    if PARAM_OUTPUT_MERGE_FILE_NAME != '' :
        output_filename = os.path.join(output_dir, PARAM_OUTPUT_MERGE_FILE_NAME)
        with open(output_filename, "w") as f:
                json.dump(all_qa_pairs, f)

# This function takes a filename and extension as arguments, and uses the corresponding function in the custom module to process the file.
# It returns the QA pairs as a list.
def process_dataset(filename, extension):
    if not os.path.exists(filename):
        print(f"Warning: File '{filename}' not found.")
        return
    

    # This code block determines how to process the file based on its extension.
    # If the extension is 'xml', call the 'process_xml_file' function from the custom module to extract QA pairs.
    # If the extension is 'json', call the 'process_json_file' function from the custom module to extract QA pairs.
    # If the extension is neither 'xml' nor 'json', raise a ValueError.
    if extension == 'xml':
        qa_pairs = parsers.config_parser.process_xml_file(filename)
    elif extension == 'json':
        qa_pairs = parsers.config_parser.process_json_file(filename)
    else:
        raise ValueError(f"Unsupported file extension: {extension}")

    return qa_pairs

# This code block checks the command line arguments and calls the appropriate function based on the input source.
# If the --xmls argument is used, call 'process_dataset_list' with the XML folder and output directory.
# If the --jsons argument is used, call 'process_dataset_list' with the JSON folder and output directory.
# If the --xml argument is used, call 'process_dataset' with the XML file and output directory.
# If the --json argument is used, call 'process_dataset' with the JSON file and output directory.
# If the --user, --password, --ip, and --database arguments are used, call 'parsers.config_parser.process_database' to extract QA pairs from a database.
# If none of the arguments are used or if the arguments are invalid, print an error message.
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    input_group = parser.add_mutually_exclusive_group(required = not bool(PARAM_ACTIVATE_CONFIG))
    input_group.add_argument('--xmls', type=str, default=PARAM_XMLS_PATH if PARAM_ACTIVATE_CONFIG and PARAM_METHOD.upper() == "xmls".upper() else None, help="Folder of XML files")
    input_group.add_argument('--jsons', type=str, default=PARAM_JSONS_PATH if PARAM_ACTIVATE_CONFIG and PARAM_METHOD.upper() == "jsons".upper() else None, help="Folder of JSON files")
    input_group.add_argument('--xml', type=str, default=PARAM_XML_PATH if PARAM_ACTIVATE_CONFIG and PARAM_METHOD.upper() == "xml".upper() else None, help="Single XML file")
    input_group.add_argument('--json', type=str, default=PARAM_JSON_PATH if PARAM_ACTIVATE_CONFIG and PARAM_METHOD.upper() == "json".upper()  else None, help="Single JSON file")
    parser.add_argument('--outputdir', type=str, default=PARAM_OUTPUT_DIR, help="Output directory")
    parser.add_argument('--user', type=str, default=PARAM_DATABASE_USER if PARAM_ACTIVATE_CONFIG and PARAM_METHOD.upper() == "database".upper() else None, help="Database username")
    parser.add_argument('--password', type=str, default=PARAM_DATABASE_DBPASSWORD if PARAM_ACTIVATE_CONFIG and PARAM_METHOD.upper() == "database".upper() else None, help="Database password")
    parser.add_argument('--ip', type=str, default=PARAM_DATABASE_HOST if PARAM_ACTIVATE_CONFIG and PARAM_METHOD.upper() == "database".upper() else None, help="Database IP address")
    parser.add_argument('--database', type=str, default=PARAM_DATABASE_DBNAME if PARAM_ACTIVATE_CONFIG and PARAM_METHOD.upper() == "database".upper() else None, help="Database name")
    args = parser.parse_args()

    if args.xmls:
        process_dataset_list(args.xmls, 'xml', args.outputdir)
    elif "jsons" and args.jsons:
        process_dataset_list(args.jsons, 'json', args.outputdir)
    elif args.xml:
        write_merged_json(process_dataset(args.xml, 'xml') ,args.outputdir)
    elif args.json:
        write_merged_json(process_dataset(args.json, 'json'), args.outputdir)
    elif args.user and args.password and args.ip and args.database:
        write_merged_json(parsers.config_parser.process_database(args.user, args.password, args.ip, args.database), args.outputdir)
    else:
        print("Invalid input arguments")
