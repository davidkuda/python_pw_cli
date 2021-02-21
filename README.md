# Get passwords into your clipboard from the terminal.

### Features: 

- Copy data into clipboard

### Commands:

- `pw <name>` -> Get the password of <name> from the section main
- `pw <name> <section>` -> Get the password of <name> from the section <section>
- `pw sections` -> Print all available sections
- `pw section <section>` -> Print all available keys of <section>

### Todo:

- Generate a random password with a length of 42 characters
- Add user_name to the json (see example below)
- Encrypt / Decrypt creds file
- copy username and pw into clipboard
- crud operations:
    - Add new password 
    - Update existing password
    - Remove pw


Storing information on passwords:

```
"section": {
        "key": {
            "password": "lorem",
            "user_name": "ipsum",
            "website": "www.website.swiss"
            "additional_info": "..."
        }
    }
```
