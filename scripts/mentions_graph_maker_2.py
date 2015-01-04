# This script processes a CSV file and creates a gephi graph file.

import gexf
import codecs

def addNode(graph, node_id, user_id, user_name, user_lang):
	node = graph.addNode(node_id, user_name.encode('ascii', 'replace'))
	node.addAttribute(user_id_attr, user_id)
	node.addAttribute(user_name_attr, user_name)
	node.addAttribute(user_lang_attr, user_lang)

def addEdge(graph, edge_id, mentioning_node_id, mentioned_node_id, tweet_id, tweet_timestamp):
	edge = graph.addEdge(edge_id, mentioning_node_id, mentioned_node_id)
	edge.addAttribute(tweet_id_attr, tweet_id)
	edge.addAttribute(tweet_timestamp_attr, tweet_timestamp)

gexf_inst = gexf.Gexf("kluba", "description")
graph = gexf_inst.addGraph("directed", "static", "user_mention graph")

# declaring attributes for graph
## nodes
user_id_attr = graph.addNodeAttribute(title = "user_id", defaultValue = "0", type = "string")
user_name_attr = graph.addNodeAttribute(title = "user_name", defaultValue = "N/A", type = "string")
user_lang_attr = graph.addNodeAttribute(title = "user_lang", defaultValue = "N/A", type = "string")

## edges
tweet_id_attr = graph.addEdgeAttribute(title = "tweet_id", defaultValue = "0", type = "string")
tweet_timestamp_attr = graph.addEdgeAttribute(title = "tweet_timestamp", defaultValue = "0", type = "string")


# TWEET_ID
# TWEET_TIMESTAMP
# ID_MENTIONUJACEGO
# NAME_MENTIONUJACEGO
# LANG_MENTIONUJACEGO
# ID_MENTIONOWANEGO
# NAME_MENTIONOWANEGO
# LANG_MENTIONOWANEGO

user_ids = []
nodes = []
nodeid = 0
edgeid = 0

fileName = 'romabayern2_5h'

mention_file = codecs.open(fileName + '.csv', encoding='utf-8')
for line in mention_file.readlines():
	tokens = line.split(";|")
	if (len(tokens) == 8):
		# if (not int(tokens[2]) in user_ids):
		# 	user_ids.append(int(tokens[2]))
		# 	addNode(graph, nodeid, tokens[2], tokens[3], tokens[4])
		# 	nodeid += 1
		if (not int(tokens[5]) in user_ids):
			user_ids.append(int(tokens[5]))
		# 	addNode(graph, nodeid, tokens[5], tokens[6], tokens[7])
		# 	nodeid += 1
		# addEdge(graph, edgeid, user_ids.index(int(tokens[2])), user_ids.index(int(tokens[5])), tokens[0], tokens[1])
		# edgeid += 1

print "user_ids: ", len(user_ids)

mention_file = codecs.open(fileName + '.csv', encoding='utf-8')
for line in mention_file.readlines():
	tokens = line.split(";|")
	if (len(tokens) == 8):
		if (int(tokens[2]) in user_ids):
			if (int(tokens[5]) in user_ids):
				if (not int(tokens[2]) in nodes):					
					nodes.append(int(tokens[2]))
					addNode(graph, nodeid, tokens[2], tokens[3], tokens[4])
					nodeid += 1
				if (not int(tokens[5]) in nodes):					
					nodes.append(int(tokens[5]))
					addNode(graph, nodeid, tokens[5], tokens[6], tokens[7])
					nodeid += 1					
				addEdge(graph, edgeid, nodes.index(int(tokens[2])), nodes.index(int(tokens[5])), tokens[0], tokens[1])
				edgeid += 1


output_file = open(fileName + '.gexf', "w")
gexf_inst.write(output_file)
