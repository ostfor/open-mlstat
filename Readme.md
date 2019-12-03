# Example

```python
from open_mlstat.google_docs_stat import GoogleDocsStats
# Create instance
gstat = GoogleDocsStats("<config_path>/config_example.json")

# Add new line to a table
query = {"ID": 0, "Epoch":1}
actions = {}
gstat.add(query, actions)
```

# Create instance

```python
from open_mlstat.google_docs_stat import GoogleDocsStats
gstat = GoogleDocsStats("<config_path>/config_example.json")
```

## Config example
```json
{
  "experiment_name": "unique_name_for_experiment", 
  "credentials": "<path>/drive.json",
  "table_titles": [ 
    "ID", "Date", "Run_Date", "Epoch", "Loss", "Testset", "Checkpoint"
  ]
}
```

### Where
 
 - `experiment_name`: unique_name_for_experiment 
 - `credentials`: `<drive.json>`- google app credentials. See next section.
 - `table_titles`: - Set of titles for table fields

### Credentials

- Create app [here](https://console.cloud.google.com/apis/credentials)
- Enable `Google Drive API` and `Google Sheets API`
- Create and download `service account` key in JSON format

# Adding new line to a table

For adding line `GoogleDocsStats` class has method add

```
gstat.add(query, actions)
```
## Query

Parameter `query` - dict where fields - table fields, values - values for particular field in new line 

### Example
```{'Loss': 0.5, 'Checkpoint': '/tmp/ep1.ckpt', 'Testset': 'test.v1', 'Epoch': 1, 'ID': 0, 'Date': None , 'Run_Date': None}```

## Actions

Parameter `actions` - dict where fields - table fields, values - an action which should be applied. Each action is a
 dict `{"action": <function_name>, "args": <optional args> }`
This dict can be empty or set actions only for particular fields 

### List of available actions

- `upload_file`: upload file from field (optional args `save_path` - path for saving to, `timestemp_prefix` - add
 current timestamp to filename)
- `upload_zip`: zip and upload file/folder from field (optional args same as for previous)
- `timestamp` : current timestamp (no args) 
- `run_timestamp`: timestamp when `GoogleDocsStats` instance has been created (no args)

### Example
```{'Checkpoint': {'args': {'timestemp_prefix': True, 'save_path': 'test.v1/weights/{run_timestamp}'}, 'action': 'upload_zip'}, 'Run_Date': {'action': 'run_timestamp'}, 'Date': {'action': 'timestamp'}}```
