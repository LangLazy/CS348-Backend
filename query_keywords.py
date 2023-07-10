import mysql.connector
import os
import logging

from db import database

def query_keywords(queryParams: dict[dict[str]]):
    print("hellp")
    # db = database()
    author_params = []
    other_params = []
    for query in queryParams.values():
        if query['field'] == "Author":
            value = query['value'].strip()
            if query['equality'] == "Exact":
                author_params.append(value)
            elif query['equality'] == "Contains":
                author_params.append("%" + value + "%")
        else:
            values = [x.strip(' ') for x in query["value"].split(",")]
            if query['equality'] == "Contains":
                values = ["%" + x + "%" for x in values]
            other_params.extend(values)
    print(author_params)
    print(other_params)
    params = author_params.copy()
    params.extend(other_params)
    print(params)
    query = generate_keyword_query_string(queryParams)
    result = db.execute(query, params)
    output = []
    
    for row in result:
        output.append(row)
    
    return output

def generate_keyword_query_string(queryParams):
    if len(queryParams) == 0:
        return ("SELECT * FROM paper NATURAL JOIN keywords Group by paper_id")
    author_params = ""
    query_params = ""
    for query in queryParams.values():
        if query['value'] == "": continue
        equality = determine_equality(query["equality"], query["boolean"])
        if query["field"] == "Author": 
            if author_params == "": author_params += "a.author_name " + equality + " %s"
            elif query["boolean"] == "NOT": 
                author_params += " AND a.author_name " + equality + " %s"
            elif query["boolean"] != "None": 
                author_params += " " + query["boolean"] + " a.author_name " + equality + " %s"
        else:
            if query["field"] == "Keywords": attribute = "word"
            elif query["field"] == "Title": attribute = "title"
            if query["boolean"] == "AND" or query["boolean"] == "NOT":
                query_params += " AND "
            elif query["boolean"] == "OR":
                query_params += " OR "
            value = [x.strip(' ') for x in query["value"].split(",")]
            formatted_portion = ["t." + attribute + " " + equality + " %s"] * len(value)
            query_params += (" " + query["boolean"] + " ").join(formatted_portion)
    query = ("\
             SELECT * \
             FROM \
                (SELECT * FROM author NATURAL JOIN wrote as a WHERE " + author_params + ") as X\
                NATURAL JOIN \
                (paper NATURAL JOIN keywords  as t WHERE " + query_params  + ") as Y \
            Group by paper_id\
            ")
    print(query)
    return query

def determine_equality(equality, boolean):
    newEquality = "="
    if equality == "Contains": newEquality = "LIKE"
    if boolean == "NOT":
        if equality == "Exact": newEquality = "!" + newEquality
        elif equality == "Contains": newEquality = "NOT " + newEquality
    return newEquality

# field: queryField.KEYWORDS, value: "", boolean: booleanLogic.None

# query_keywords(
#     {
#         "1": {
#             "field": "Keywords",
#             "value": "hello",
#             "equality": "Exact",
#             "boolean": "None"
#         },
#         "2": {
#             "field": "Author",
#             "value": "this",
#             "equality": "Exact",
#             "boolean": "AND"
#         },
#         "3": {
#             "field": "Title",
#             "value": "temp, something, great",
#             "equality": "Contains",
#             "boolean": "AND"
#         },
#         "4": {
#             "field": "Keywords",
#             "value": "cs",
#             "equality": "Exact",
#             "boolean": "NOT"
#         }
#     }
# )