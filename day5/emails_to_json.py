import sys
sys.path.append('../resources/util/')
from email_util import EmailWalker
from mrjob.protocol import JSONValueProtocol
import os

def root_to_json(root_dir, output_file):
    walker = EmailWalker(root_dir)
    output = open(output_file, "w")

    for email in walker:
        email['date'] = str(email['date'])
        line = JSONValueProtocol.write(None, email) + '\n'
        output.write(line)

    output.close()

def all_folders(root_container, output_dir):
    for file in os.listdir(root_container):
        path = os.path.join(root_container, file)
        if os.path.isdir(path):
            output = os.path.join(output_dir, file+".json")
            root_to_json(path, output)
            
if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "one_root":
        root_to_json(sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 4 and sys.argv[1] == "many_roots":
        all_folders(sys.argv[2], sys.argv[3])
    else:
        print "one_root walks a single email root folder and emits a json file for it"
        print "many_roots walks all of the email roots in a directory and outputs a json file for each one"
        print "Arguments: [one_root|many_roots] [path_to_root|path_to_root_container] [output_file|output_directory"
    
