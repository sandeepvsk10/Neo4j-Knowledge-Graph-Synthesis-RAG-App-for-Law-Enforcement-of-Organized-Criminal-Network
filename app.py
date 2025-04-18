from load_transcript import load_transcripts
from generate_summary import generate_transcript_summary
from knowledge_graph import knowledge_graph_neo4j
from graph_rag import graph_retreiver, rag_llm_response

# load_transcript.py

transcript = load_transcripts('transcript_id_',1,2)

# summary.py
generated_summary = generate_transcript_summary(transcript)

# user_query
user_query = input("Enter your user query")

knowledge_graph_neo4j(generated_summary)

cypher_query_result = graph_retreiver(user_query)

reasoned_user_response = rag_llm_response(user_query,cypher_query_result)

print(reasoned_user_response)

