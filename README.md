# config_builder

A small tool to generate config files from variable/secret stores using templates

## Problem statement

We often have to create config files for applications containg the same data and/or secrets.
For example, you might have two applications that connect to the same database server. Both of those applications might have configuration files like this:

```properties
# application-1.properties
database.host=my-host.example.com
database.user=my-user
database.password=my-password
database.database=application_1
```

```json
# application-2.json
{
  "database": {
    "url": "my-host.example.com",
    "username": "my-user",
    "password": "my-password",
    "database_name": "application_2"
  }
}
```

Note that the database properties for _host_, _username_ and _password_ are duplicated across both files. This means that if the credentials change you'll have to update the configuration in both files.

Furthermore, these credentials might already be stored in some secret or variable store such as a local KeePassXC database. You might not want to permanently store these credentials in a readable text file. Furthermore, this database might be shared with the rest of your team, meaning the credentials could change at any time.

## Provided solution

This tool provides a solution for both problems in the form of **template files** and **variable containers**.

The main idea is that you keep your secrets in your secret stores and dynamically generate your configuration files by using template files.
I might create the following template files for the examples above:

```properties
# application-1.properties.template
database.host=${keepass://databases/my-host/@url}
database.user=${keepass://databases/my-host/@username}
database.password=${keepass://databases/my-host/@password}
database.database=application_1
```

```json
# application-2.json.template
{
  "database": {
    "url": "${keepass://databases/my-host/@url}",
    "username": "${keepass://database/my-host/@username}",
    "password": "${keepass://databases/my-host/@password}",
    "database_name": "application_2"
  }
}
```

Here, variables are denoted as `${container://path}` where `container` is a configurable name linked to some secret store (in this case a KeePassXC database file) and `path` denotes a path to the actual variable in that secret store.
In this case `${keepass://database/my-host/@url}` is going to fetch the property `url` of the entry `database/my-host` from the KeePassXC database configured as `keepass`.

To configure containers you can provide a config.py file, which can look something like this:

```python
VARIABLE_CONTAINERS = {
  'keepass': {
    'class': KeePassContainer,
    'config': {
      'db_path': '/Users/enver/Secrets/secrets.kdbx',
    }
  }
}
```

Using this configuration you can then generate the configuration files from the templates using the following two commands:

```bash
$ python -m config_builder -t templates/application-1.properties.template > output/application-1.properties
$ python -m config_builder -t templates/application-2.json.template > output/application-2.json
```

If all of your templates are contained in a single folder, then you could very easily write a script which periodically compiles the templates and symlinks those configuration files to each application configuration folder.

