import os
import glob
import argparse
import parsers.config_parser
import json


from config import (
    PARAM_ACTIVATE_CONFIG, PARAM_METHOD, PARAM_XML_PATH, PARAM_XMLS_PATH,
    PARAM_JSON_PATH, PARAM_JSONS_PATH, PARAM_DATABASE_HOST,PARAM_DATABASE_PORT, PARAM_DATABASE_USER,
    PARAM_DATABASE_DBNAME, PARAM_DATABASE_DBPASSWORD, PARAM_OUTPUT_DIR, PARAM_OUTPUT_MERGE_FILE, PARAM_OUTPUT_MERGE_FILE_NAME
)

def process_dataset_list(input_dir, extension, output_dir):
    if not os.path.exists(input_dir):
        print(f"Warning: Folder '{input_dir}' not found.")
        return

    print (PARAM_OUTPUT_MERGE_FILE)
    if PARAM_OUTPUT_MERGE_FILE and PARAM_OUTPUT_MERGE_FILE_NAME == '':
        print(f"Warning: PARAM_OUTPUT_MERGE_FILE_NAME empty.")
        return
    
    all_qa_pairs = []
    files_found = False
    for filename in glob.glob(os.path.join(input_dir, f'*.{extension}')):
        files_found = True
        qa_pairs = process_dataset(filename, extension)
        if qa_pairs:
            if PARAM_OUTPUT_MERGE_FILE == False :
                output_filename = os.path.join(output_dir, os.path.basename(filename) + '.json')
                with open(output_filename, "w") as f:
                    json.dump(qa_pairs, f)
            else :
                all_qa_pairs.extend(qa_pairs)

    if not files_found:
        print(f"Warning: No '{extension}' files found in '{input_dir}'.")
        return
    else : 
        write_merged_json( all_qa_pairs, output_dir)

def write_merged_json(all_qa_pairs, output_dir) :
    if PARAM_OUTPUT_MERGE_FILE_NAME != '' :
        output_filename = os.path.join(output_dir, PARAM_OUTPUT_MERGE_FILE_NAME)
        with open(output_filename, "w") as f:
                json.dump(all_qa_pairs, f)


def process_dataset(filename, extension):
    if not os.path.exists(filename):
        print(f"Warning: File '{filename}' not found.")
        return

    if extension == 'xml':
        qa_pairs = parsers.config_parser.process_xml_file(filename)
    elif extension == 'json':
        qa_pairs = parsers.config_parser.process_json_file(filename)
    else:
        raise ValueError(f"Unsupported file extension: {extension}")

    return qa_pairs

def generate_qa_pairs(dataset):
    treated_dataset = parsers.dataset_pretreatment(dataset)
    # Generate question-answer pairs
    qa_pairs = parsers.generate_instructions(treated_dataset)
    return qa_pairs


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
