import neo4j
from neo4j import GraphDatabase
from langchain import PromptTemplate
from llm import openai_llm
from datetime import datetime

from config import URL, USER, PASSWORD

def knowledge_graph_neo4j(summarized_transcript):
    cypher_generation_prompt = PromptTemplate(
    input_variable = ["summarized_transcript"],
    template = """
    
    You are a Cypher query generation expert trained in graph-based criminal intelligence modeling.

    You are given a structured summary of a surveillance transcript, which has been formatted using a predefined schema. Your task is to convert this structured summary into Cypher queries for ingestion into a Neo4j database.

    Please follow the rules and be precise:

    In the below example cypher queries I might have given round brackets instead of curly brackets for preventing discrepancies with the input mechanism of prompt_template method in langchain

---

### GRAPH SCHEMA

**Node Types:**
- :Person (name, alias, age, sex)
- :Operation (name)
- :Location (name, location_type)
- :SpecialEvent (name)
- :Item (name)

**Relationship Types:**
- (Person)-[:task (timestamp)]->(Operation)
- (Person)-[:was_at (timestamp, meeting_reason)]->(Location)
- (Person)-[:operates]->(Operation)
- (Item)-[:task (timestamp, description)]->(Person)

---

### INSTRUCTIONS

1. **Use `CREATE` exclusively** when instantiating nodes. Do **not** use `MERGE`.  
2. **Terminate every Cypher statement with a semicolon (`;`)** so each `CREATE`, `MATCH`, or `CREATE` stands as its own executable command.  
3. **Anonymous node creation**: in each `CREATE (:Label {{ }});` statement do **not** assign a variable.  
4. Always include **all known properties** on creation—e.g. `age`, `alias`, and `sex` for `:Person` nodes when those values are available.  
5. After node creation, for each relationship:
   - Use `MATCH` to locate the existing nodes (by their unique properties).
   - Then use `CREATE` to form the relationship, with its properties.
   - End each `MATCH … CREATE` block with a semicolon.
6. Use **consistent timestamp format**: `"YYYY‑MM‑DDThh:mm"`.  
7. Only generate relationships allowed by the schema.  
8. Do **not** fabricate or guess any values not explicitly provided in the summary.  
9. Review all Cypher before finalizing; only output when you’re confident it’s logically and syntactically correct.  
10. Output your Cypher statements in a single code block, with each line ending in `;`.

---

### INPUT: Structured Summary

{summarized_transcript}

---

### OUTPUT: Cypher Query Block


    """
)

    cypher_generation_chain = ( cypher_generation_prompt | openai_llm)
    response = cypher_generation_chain.invoke({"summarized_transcript": summarized_transcript})
    cypher_query = response.content

    clean_cypher_query = "\n".join(
    line for line in cypher_query.splitlines()
    if not (line.startswith("```") or line.startswith("```cypher"))
    )

    file_timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S-%f")[:-3]
    with open("generated_cypher"+str(file_timestamp)+".txt", "w", encoding="utf-8") as f:
        f.write(clean_cypher_query)

    driver = GraphDatabase.driver(URL, auth=(USER, PASSWORD))

    cypher_stmts_list = [s.strip() for s in clean_cypher_query.split(";") if s.strip()]

    with driver.session() as session:
        with session.begin_transaction() as tx:
            for cypher_stmt in cypher_stmts_list:
                tx.run(cypher_stmt)
            tx.commit()

    driver.close()

