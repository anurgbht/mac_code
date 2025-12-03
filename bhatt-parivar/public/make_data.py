# Let's create a JSON file containing the details of a family tree and a basic website template
# to visualize it in a tree-like structure.

import json

# Define the family tree data
family_tree = {
    "name": "John Smith",
    "spouse": "Mary Smith",
    "children": [
        {
            "name": "Michael Smith",
            "spouse": "Anna Smith",
            "children": [
                {
                    "name": "Jake Smith",
                    "spouse": None,
                    "children": []
                },
                {
                    "name": "Ella Smith",
                    "spouse": None,
                    "children": []
                }
            ]
        },
        {
            "name": "Susan Smith",
            "spouse": None,
            "children": [
                {
                    "name": "Laura Smith",
                    "spouse": None,
                    "children": []
                }
            ]
        }
    ]
}

# Create a JSON file
family_tree_path = 'family.json'
with open(family_tree_path, 'w') as json_file:
    json.dump(family_tree, json_file, indent=4)

family_tree_path
