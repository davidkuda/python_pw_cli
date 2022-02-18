# Get passwords into your clipboard from the terminal.

![Preview of the pw tool](https://github.com/davidkuda/media/blob/main/pw_cli/pw_v0.2.gif)

### Features: 

You can run the script `pw_command.py` to manage your passwords in the command line. See the explanation
for the commands below. Here is what this tool can do:

- Copy secrets such as passwords from a json file into your clipboard
- Generate a random passwords with or without special characters
- Save, update and delete secrets

### Commands:

- `pw <entity>` -> Get the password of `<entity>` from the section main
- `pw -as` -> Print all sections
- `pw -s <section>` -> Print all available entities of `<section>`
- `pw -s <section> <entity>` -> Get the password of `<entity>` from `<section>`
- `pw -r` -> Generate a random password with 42 characters, print it and copy it to the clipboard
- `pw -rn` -> Generate a random password without special characters
- `pw -rl 20` -> Generate a random password with 20 characters
- `pw -rl 20 -rn` -> Generate a random password with 20 characters and without special characters
- `pw -n <name>` -> Add a new randomly created password to the creds.json file for the entity `<name>`  
- `pw -n <entity> -w <website> -u <username>` -> Create a new password with information on the website and the username
- `pw -rm <entity>` -> Remove the password for `<entity>` from the section main
- `pw -rm <entity> -s <section>` -> Remove the password for `<entity>` from `<section>`
- `pw -rms <section>` -> Remove the section `<section>`

### Store your passwords in a json file:

```
"section": {
        "key": {
            "password": "lorem",
            "username": "ipsum",
            "website": "www.website.swiss"
            "additional_info": "..."
        }
    },
"main": {
        "GitHub": {
            "password": "lorem",
            "username": "ipsum",
            "website": "www.GitHub.com"
            "additional_info": "..."
        },
        "netlify": {
            "password": "lorem",
            "username": "ipsum",
            "website": "www.netlify.com"
            "additional_info": "..."
        }
        , ...
    }
```

### A suggestion how to set up the `pw` command:

I create a symlink to the python script `pw_command.py` (command 3). The name of this symlink is just "pw".
The symlink needs execution permissions (command 4). The symlink needs to be in a folder that is listed
in the PATH (command 2). In my case, that's the folder `.bin` which exists in my home directory (command 1).

1. `mkdir ~/.bin/ && cd ~/.bin/` Create the folder `.bin` in your homedir (`$HOME`)
2. `echo "export PATH=\$PATH:\$HOME/xyz" >> $HOME/.zshrc` -> Add the newly created directory to your `$PATH`
3. `ln -s ~/dev/python_pw_cli/src/pw_command.py pw` -> Create the symlink `pw` to the script
4. `chmod 744 pw` -> Change file permissions so that the script becomes executable

Furthermore, you need to assure two things:

1. Update line 1 of `/src/pw_command.py` by specifying your path to Python3 (find out with `which python3`)
2. Create a passwords.json somewhere and pass the path to the variables in `/src/pw/pw_config.py` accordingly

