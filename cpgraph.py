import json
import uuid
import flask
import networkx as nx

# Basic ETL process

# Extract the data

with open("cp.txt", "r", encoding="utf-8") as f:
    elements = []

    root_node = {
        "uuid": str(uuid.uuid4()),
        "name": "Root",
        "type": "ROOT",
        "lines": [],
        "parent": ""
    }

    elements.append(root_node)
    last_id = root_node["uuid"]

    number_of_lines = -1
    charsum = 0
    for line in f.read().splitlines():
        charsum += len(line)
        if line.startswith(("LIBRO", "TÍTULO", "CAPÍTULO", "Sección", "Artículo", "Disposición")):
            elem = {"uuid": str(uuid.uuid4()), "name": line, "type": line.split(" ")[0][0], "lines": [], "parent": ""}
            last_id = elem["uuid"]
            elements.append(elem)
        else:
            if line != "":
                # If the line is not a header line then we assume the element is the description of the previous element
                finds = [x for x in elements if x["uuid"] == last_id][0]
                finds["lines"].append(line)
        number_of_lines += 1


# Transform the data: setting parent UUIDs

ids = {
    "ROOT": root_node["uuid"],
    "L": "",
    "T": "",
    "C": "",
    "S": "",
    "A": "",
    "D": ""
}

index = 0
while index < len(elements):
    elem = elements[index]
    type = elem["type"]

    ids[type] = elem["uuid"]

    if type == "ROOT":
        # The root element is added, and it will always be the same, so there is nothing else to do
        pass
    elif type == "L":
        # The "Libro" element is always linked to root
        elem["parent"] = ids["ROOT"]
    elif type == "T":
        # The "Titulo" element can be under root or under a book, but this is an exceptional case
        elem["parent"] = ids["L"] if ids["L"] != "" else ids["ROOT"]
    elif type == "C":
        # The "Capitulo" element can be under a title or not
        elem["parent"] = ids["T"]
    elif type == "S":
        # The "Seccion" element can be under a chapter or not
        elem["parent"] = ids["C"]
    elif type == "A":
        # The "Articulo" element can be under a title, a chapter or a section, it depends on the previous element
        reverse_index = index
        while elem["parent"] == "":
            if elements[reverse_index]["type"] != type:
                elem["parent"] = elements[reverse_index]["uuid"]
            reverse_index -= 1
    elif type == "D":
        # The "Disposicion" element is always linked to root
        elem["parent"] = ids["ROOT"]
    else:
        # There are no other elements, so if we get this case we just ignore it
        pass

    index += 1

# Checks to ensure integrity of the document

character_sum = 0
for elem in elements:
    character_sum += (len(elem["name"]) if elem["type"] != "ROOT" else 0) + sum([len(l) for l in elem["lines"]])

print(f"Original number of characters: {charsum + number_of_lines}")
print(f"Number of characters after transformation: {character_sum + number_of_lines}")
assert character_sum == charsum

# Load the data (in this case we just dump it)

# Dump to file

with open("elements.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(elements))

# Graph construction

G = nx.DiGraph()

for x in elements:
    G.add_node(x["uuid"], type=x["type"][0], message=x["name"], size=10)
    G.add_edge(x["uuid"], x["parent"])

d = nx.json_graph.node_link_data(G)
json.dump(d, open('./graph/graph.json', 'w+'))

print("Graph dumped")

# Server side

app = flask.Flask(__name__, static_folder="./graph")
app.config["CACHE_TYPE"] = "null"


@app.route('/')
def static_proxy():
    return app.send_static_file('index.html')


print("Running app...")

app.run(port=8000)
