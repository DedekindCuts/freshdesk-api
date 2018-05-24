# freshdesk-api-weave
A tool for interacting with the Freshdesk API to get and store Weave support data in a MySQL database

## Description

### auto_update_mysql.py
Inserts data from Freshdesk into a MySQL database.

### schema.sql
Can be used to create a MySQL database that is appropriately formatted to be used with `auto_update_mysql.py`, with the table and column names referenced in that file.

## Getting Started

### Prerequisites
To get data from Freshdesk you will need a valid Freshdesk API key and password, and you will need to know your organization's Freshdesk domain.
To use `auto_update_mysql.py` you will also need to have MySQL installed.
These tools all use the Python Requests library and `auto_update_mysql.py` uses the PyMySQL library.
(I recommend installing the package manager [Homebrew](https://brew.sh/) if you haven't already and then using Homebrew to install the latest version of Python.
You can find a walkthrough of this process [here](http://docs.python-guide.org/en/latest/starting/install3/osx/).)

To install MySQL using Homebrew:
```bash
brew install mysql
```

To install Requests and PyMySQL using pip3:
```bash
pip3 install requests
pip3 install pymysql
```

### Usage
First, you will need to edit `config.py` and add your Freshdesk API key, password, and domain.
You will also need to specify the first date for which you would like to retrieve ticket data.
(You don't need to worry about duplicating ticket data, since the database created by `schema.sql` will automatically update existing tickets instead of creating duplicates.)

#### Creating the Freshdesk database in MySQL
You will also need to create a MySQL database named **Freshdesk** that is structured appropriately.
You can easily do this using the included file `schema.sql`.

```bash
mysql -u USERNAME -p < schema.sql
```

Just replace `USERNAME` with your MySQL username, and remember that depending on your current directory, you may need to specify the full path of `schema.sql`.

#### Using `auto_update_mysql.py`
After creating the **Freshdesk** MySQL database, you will need to edit `config.py` to include your MySQL credentials.
(If you used `schema.sql`, you can set `database = "Freshdesk"`.
Also if you are running MySQL locally, then set `host = "localhost"`.)

Running `auto_update_mysql.py` and `manual_update_mysql.py` will update the lists of tickets, companies, and contacts, adding any that are not already in the database.