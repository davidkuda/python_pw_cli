entity = 'Name of entity that holds the password.',
all_sections = 'Print all available sections.',
section = '''
Pass a section to print all entities of that section.
The -s flag can be used together with other functions:
Use it with "-add_new_password" to write pw to a specific section:
"pw -n GitHub -s dev" -- Writes a new random password for "GitHub" to the section "dev";
Use it with an argument without a flag to get a password from a specific section:
"pw -s dev GitHub" -- Gets password for "GitHub" from the section "dev"''',
add_new_password = 'Pass an entity as arg and add a new password to the json file.',
generate_random_pw = 'Print a randomly generated password and add it to your clipboard.',
remove = '''
Delete a password from the creds file. Combine together with "-s" 
if the password you want to delete is in an other section than "main".
Example: "pw -d GitHub -s dev" -> Remove the password for GitHub
from the section "dev".''',
set_password = 'Set your own password instead of generating a random password. Use it with "-n".'
