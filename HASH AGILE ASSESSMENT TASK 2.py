import requests
import pandas as pd

# Define the Solr URL and collection names
SOLR_URL = 'http://localhost:8983/solr'  # Update this to your Solr URL
NAME_COLLECTION = 'Hash_JAGASURYA_H'
PHONE_COLLECTION = 'Hash_8108'

# Function to create a collection (core)
def create_collection(collection_name):
    response = requests.get(f"{SOLR_URL}/admin/cores?action=CREATE&core={collection_name}")
    if response.status_code == 200:
        print(f"Collection '{collection_name}' created successfully.")
    else:
        print(f"Error creating collection '{collection_name}': {response.json()}")

# Function to index data into Solr
def index_data(collection_name, exclude_column):
    df = pd.read_csv('C:\\Users\\jagas\\Downloads\\employee.csv', encoding='ISO-8859-1')
    df = df.drop(columns=[exclude_column], errors='ignore')

    for index, row in df.iterrows():
        document = row.to_dict()
        response = requests.post(f"{SOLR_URL}/{collection_name}/update/json/docs", json=document)
        if response.status_code == 200:
            print(f"Document {index} indexed successfully.")
        else:
            print(f"Error indexing document {index}: {response.text}")

# Function to get employee count
def get_emp_count(collection_name):
    response = requests.get(f"{SOLR_URL}/{collection_name}/select?q=*:*&rows=0")
    if response.status_code == 200:
        count = response.json()['response']['numFound']
        print(f"Employee count in '{collection_name}': {count}")
        return count
    else:
        print(f"Error getting employee count from '{collection_name}': {response.text}")
        return None

# Function to delete employee by ID
def del_emp_by_id(collection_name, employee_id):
    response = requests.post(f"{SOLR_URL}/{collection_name}/update?commit=true", json={"delete": {"id": employee_id}})
    if response.status_code == 200:
        print(f"Employee with ID '{employee_id}' deleted successfully.")
    else:
        print(f"Error deleting employee with ID '{employee_id}': {response.text}")

# Function to search by column
def search_by_column(collection_name, column_name, column_value):
    response = requests.get(f"{SOLR_URL}/{collection_name}/select?q={column_name}:{column_value}")
    if response.status_code == 200:
        results = response.json()['response']['docs']
        print(f"Search results for '{column_name}'='{column_value}': {results}")
        return results
    else:
        print(f"Error searching in '{collection_name}': {response.text}")
        return None

# Function to get department facet
def get_dep_facet(collection_name):
    response = requests.get(f"{SOLR_URL}/{collection_name}/facet?q=*:*&facet.field=Department&facet.mincount=1")
    if response.status_code == 200:
        facets = response.json()['facet_counts']['facet_fields']
        print(f"Department facets for '{collection_name}': {facets}")
        return facets
    else:
        print(f"Error getting department facets from '{collection_name}': {response.text}")
        return None

# Execute the functions in order
create_collection(NAME_COLLECTION)
create_collection(PHONE_COLLECTION)
get_emp_count(NAME_COLLECTION)
index_data(NAME_COLLECTION, 'Department')
index_data(PHONE_COLLECTION, 'Gender')
del_emp_by_id(NAME_COLLECTION, 'E02003')
get_emp_count(NAME_COLLECTION)
search_by_column(NAME_COLLECTION, 'Department', 'IT')
search_by_column(NAME_COLLECTION, 'Gender', 'Male')
search_by_column(PHONE_COLLECTION, 'Department', 'IT')
get_dep_facet(NAME_COLLECTION)
get_dep_facet(PHONE_COLLECTION)  
