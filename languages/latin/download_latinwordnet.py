#! /usr/bin/env python

import json
import requests
import sys

# Get the Latin WordNet data from https://latinwordnet.exeter.ac.uk/api/index
# and print it to the console.


def null_to_empty_string(value):
    return value if value is not None else ""


def convert_latinwordnet(data):
    return {
        "extensions": [
            {
                "addsTo": {"pack": "latin", "extensible": "latinWordNet"},
                "data": [
                    [
                        null_to_empty_string(entry["lemma"]),
                        null_to_empty_string(entry["pos"]),
                        null_to_empty_string(entry["morpho"]),
                        null_to_empty_string(entry["uri"]),
                        null_to_empty_string(entry["prosody"]),
                    ]
                    for entry in data
                ],
            }
        ]
    }


def main():
    url = "https://latinwordnet.exeter.ac.uk/api/index"
    results = []
    while url:
        response = requests.get(url)
        data = response.json()
        results.extend(data["results"])
        url = data["next"]
    print(
        """
# This file was automatically generated from data downloaded from the Latin WordNet API, https://latinwordnet.exeter.ac.uk/api/index
# The Latin WordNet database is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
        """
    )
    json.dump(convert_latinwordnet(results), sys.stdout, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
