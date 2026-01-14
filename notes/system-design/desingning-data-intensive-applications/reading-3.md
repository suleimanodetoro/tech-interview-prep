# Chapter 2: Data Models and Query Languages
## Study Notes - Day 2 (Declarative Queries, MapReduce, and Graphs)

> From "Designing Data-Intensive Applications" by Martin Kleppmann
> **Date:** January 15, 2026
> **Topics:** Query languages, MapReduce, Graph databases

---

## Declarative vs Imperative Query Languages

### Core Difference

**Imperative (HOW):** Tell computer step-by-step HOW to do it
**Declarative (WHAT):** Tell computer WHAT you want, it figures out HOW

---

### Example: Get All Sharks from Animals List

**Imperative (JavaScript):**
```javascript
function getSharks() {
  var sharks = [];                           // Step 1: Create empty list
  for (var i = 0; i < animals.length; i++) { // Step 2: Loop through
    if (animals[i].family === "Sharks") {    // Step 3: Check each one
      sharks.push(animals[i]);                // Step 4: Add to list
    }
  }
  return sharks;                              // Step 5: Return
}
```

You give explicit instructions: loop, check, add, return.

---

**Declarative (SQL):**
```sql
SELECT * FROM animals WHERE family = 'Sharks';
```

You just say: "Give me animals where family equals Sharks."

Database figures out HOW to do it.

---

### Why Declarative is Better

**1. Simpler and More Concise**
- Less code to write
- Easier to understand

**2. Database Can Optimize**
- Query optimizer chooses best execution strategy
- Can use indexes, parallel execution
- You don't specify HOW, so database is free to improve performance

**3. Flexibility for Database Changes**

**The Ordering Problem:**

With imperative code:
```javascript
for (var i = 0; i < animals.length; i++) {  // Assumes specific order!
  // ...
}
```

If database reorganizes data (to reclaim disk space), your code might break or behave differently.

With declarative SQL:
```sql
SELECT * FROM animals WHERE family = 'Sharks';  -- No order assumed
```

Database can reorganize data freely without breaking your query.

**4. Better Parallelization**
- Declarative queries specify pattern, not algorithm
- Database can parallelize across multiple cores
- Imperative code with loops is hard to parallelize

---

### Declarative Outside Databases: CSS

**Task:** Highlight currently selected navigation item with blue background

**Declarative (CSS):**
```css
li.selected > p {
  background-color: blue;
}
```

"Find all `<p>` elements whose direct parent is `<li>` with class='selected'"

---

**If this were Imperative (JavaScript):**
```javascript
var listItems = document.getElementsByTagName('li');
for (var i = 0; i < listItems.length; i++) {
  if (listItems[i].className === 'selected') {
    var paragraphs = listItems[i].getElementsByTagName('p');
    for (var j = 0; j < paragraphs.length; j++) {
      if (paragraphs[j].parentNode === listItems[i]) {
        paragraphs[j].style.backgroundColor = 'blue';
      }
    }
  }
}
```

Much more complicated!

---

## MapReduce Querying

### What is MapReduce?

**Programming model for processing large amounts of data across many machines**

- Popularized by Google
- Used in MongoDB, CouchDB (limited form)
- Neither fully declarative nor fully imperative - somewhere in between

---

### How MapReduce Works

**Two phases: MAP, then REDUCE**

**MAP:** Transform each document into key-value pairs
**REDUCE:** Combine all values with the same key into single result

---

### Example: Monthly Shark Count Report

**Goal:** Count total sharks observed per month

**Input data:**
```javascript
{
  observationTimestamp: "Mon, 25 Dec 1995 12:34:56 GMT",
  family: "Sharks",
  species: "Great White",
  numAnimals: 3
}
{
  observationTimestamp: "Tue, 12 Dec 1995 16:17:18 GMT",
  family: "Sharks",
  species: "Tiger Shark",
  numAnimals: 4
}
```

---

### The Code

```javascript
db.observations.mapReduce(
  // MAP FUNCTION
  function map() {
    var year = this.observationTimestamp.getFullYear();   // 1995
    var month = this.observationTimestamp.getMonth() + 1; // 12
    emit(year + "-" + month, this.numAnimals);            // emit("1995-12", 3)
  },
  
  // REDUCE FUNCTION
  function reduce(key, values) {
    return Array.sum(values);  // Sum all values for this key
  },
  
  // OPTIONS
  {
    query: { family: "Sharks" },     // Filter before MAP
    out: "monthlySharkReport"        // Output collection
  }
);
```

---

### Step-by-Step Execution

**Step 0: Filter (query)**
```javascript
query: { family: "Sharks" }
```
Only process Sharks documents.

---

**Step 1: MAP Phase**

MAP runs once for each document:

**Document 1:**
- year = 1995, month = 12
- **Emits:** `("1995-12", 3)`

**Document 2:**
- year = 1995, month = 12
- **Emits:** `("1995-12", 4)`

---

**After MAP:** MongoDB groups by key
```
"1995-12" → [3, 4]
```

---

**Step 2: REDUCE Phase**

REDUCE runs once per unique key:

```javascript
reduce("1995-12", [3, 4])
  → Array.sum([3, 4])
  → 7
```

---

**Final Result:**
```javascript
{
  _id: "1995-12",
  value: 7
}
```

Meaning: In December 1995, observed 7 sharks total.

---

### Key Characteristics

**MAP function:**
- Runs for each document
- Must be pure (no side effects, no database queries)
- Extracts/transforms data
- Emits key-value pairs

**REDUCE function:**
- Runs for each unique key
- Must be pure
- Combines values into single result
- Receives all values for that key

**Restrictions:** Pure functions only
- Can't perform database queries
- Can't have side effects
- Can only use data passed as input
- Allows database to run them anywhere, any order, rerun on failure

**Benefits:**
- Can run across many machines in parallel
- Fault-tolerant (can retry on failure)

**Downsides:**
- Two carefully coordinated functions (harder than single query)
- Less optimization opportunities than declarative languages

---

### Modern Alternative: Aggregation Pipeline

MongoDB added declarative query language to address MapReduce complexity:

```javascript
db.observations.aggregate([
  { $match: { family: "Sharks" } },
  { $group: {
      _id: {
        year: { $year: "$observationTimestamp" },
        month: { $month: "$observationTimestamp" }
      },
      totalAnimals: { $sum: "$numAnimals" }
  } }
]);
```

More like SQL, easier to write, better optimization.

---

## Graph-Like Data Models

### When to Use Graphs

**Review:**
- **One-to-many (tree)** → Document model
- **Simple many-to-many** → Relational model
- **Highly interconnected many-to-many** → Graph model

---

### What is a Graph?

**Two components:**

**1. Vertices (Nodes/Entities):**
- The "things" in your data
- Examples: people, places, posts, photos, events

**2. Edges (Relationships/Arcs):**
- The connections between things
- Examples: friend_of, lives_in, works_at, tagged_in

---

### Visual Example

```
[Alice] --friend_of--> [Bob]
   ↑                      ↓
   |                   lives_in
   |                      ↓
lives_in              [New York]
   |
   ↓
[Seattle]
```

**Vertices (the boxes):**
- Alice, Bob, New York, Seattle

**Edges (the arrows):**
- Alice --friend_of--> Bob
- Alice --lives_in--> Seattle
- Bob --lives_in--> New York

---

### Examples of Graph Data

**Social graphs:**
- Vertices: people
- Edges: who knows who

**Web graph:**
- Vertices: web pages
- Edges: links between pages (PageRank!)

**Road networks:**
- Vertices: intersections
- Edges: roads connecting them

---

### Simple vs Highly Interconnected

**Simple Many-to-Many (Relational Works):**

Students ↔ Classes
```sql
students: id, name
classes: id, name
enrollments: student_id, class_id
```

One type of relationship, easy to query with JOINs.

Query: "What classes does Alice take?"
```sql
SELECT c.name 
FROM classes c
JOIN enrollments e ON c.id = e.class_id
WHERE e.student_id = 1;
```

Simple and fast!

---

**Highly Interconnected (Graph Better):**

Social network with:
- People ↔ People (friend_of, married_to, follows)
- People ↔ Posts (created, liked, commented_on)
- People ↔ Photos (uploaded, tagged_in)
- Posts ↔ Photos (contains)
- People ↔ Locations (lives_in, born_in, checked_in_at)
- Locations ↔ Locations (within)
- People ↔ Companies (works_at)
- People ↔ Events (attending, created)
- Events ↔ Locations (at)
- People ↔ Groups (member_of, admin_of)

**Multiple relationship types, multiple entity types, complex path traversals needed.**

---

### Complex Graph Example: Facebook-like Network

**Entities (Vertices):**
- 5 People (Alice, Bob, Carol, Dave, Emma)
- 3 Posts
- 3 Photos
- 3 Events
- 8 Locations (cities, states, countries)
- 3 Companies
- 2 Groups

**Relationships (15+ types):**
- friend_of, married_to, follows
- created, liked, commented_on, shared
- uploaded, tagged_in, contains
- lives_in, born_in, checked_in_at, within
- works_at, worked_at
- member_of, admin_of
- attending, invited_to, maybe_attending
- at, created_by

**Complex queries possible:**
- "Friends of friends who work at same company"
- "Photos of people who attended events in cities where my friends work"
- "Find all paths connecting Alice to Dave"
- "Find people born in Europe who now live in a different continent"

---

### Why Relational Struggles with Graphs

Would need:
- 20+ tables (one per entity type)
- 30+ junction tables (for many-to-many relationships)
- Queries with 10+ JOINs for path-finding
- Recursive CTEs for "friends of friends"
- Very hard to write and very slow to execute

Example query: "Find photos of people who attended events in cities where my friends work"
- Would require 6+ JOINs
- Multiple subqueries
- Recursive traversal for friend relationships
- Complex and slow!

---

### Property Graph Model

**Each vertex consists of:**
- A unique identifier
- A set of outgoing edges
- A set of incoming edges
- A collection of properties (key-value pairs)

**Each edge consists of:**
- A unique identifier
- The vertex at which edge starts (tail vertex)
- The vertex at which edge ends (head vertex)
- A label describing the relationship
- A collection of properties (key-value pairs)

---

### Storing Graphs in SQL (Possible but Not Ideal)

```sql
CREATE TABLE vertices (
    vertex_id integer PRIMARY KEY,
    properties json
);

CREATE TABLE edges (
    edge_id integer PRIMARY KEY,
    tail_vertex integer REFERENCES vertices (vertex_id),
    head_vertex integer REFERENCES vertices (vertex_id),
    label text,
    properties json
);

CREATE INDEX edges_tails ON edges (tail_vertex);
CREATE INDEX edges_heads ON edges (head_vertex);
```

**This shows you CAN represent graphs in relational databases**, but:
- Queries become complex
- Performance suffers for deep traversals
- Not as natural as specialized graph databases

**The author's point:** "Before we talk about graph databases, understand that graphs are just vertices and edges that can be stored in tables."

---

### Graph Terminology

**Tail vertex:** Where arrow starts (non-pointy end)
**Head vertex:** Where arrow points (pointy end)

```
Alice --friend_of--> Bob
  ↑                    ↑
 tail                head
```

In the edges table:
```sql
tail_vertex | head_vertex | label
Alice       | Bob         | "friend_of"
```

Arrow goes FROM tail TO head.

---

### Bidirectional Relationships

**Question:** Are there two-way arrows?

**Answer:** No true two-way edges exist in the data structure.

**For bidirectional relationships, store TWO one-way edges:**
```
Edge 1: Alice --friend_of--> Bob
Edge 2: Bob --friend_of--> Alice
```

This allows efficient traversal in both directions:
- "Who are Alice's friends?" → Follow outgoing friend_of edges from Alice
- "Who is friends with Alice?" → Follow incoming friend_of edges to Alice

---

### Multiple Edges Per Node

**Yes! Nodes can have unlimited incoming and outgoing edges.**

Example - Alice vertex has:

**Outgoing edges:**
- Alice --friend_of--> Bob
- Alice --friend_of--> Carol
- Alice --created--> Post1
- Alice --uploaded--> Photo1
- Alice --lives_in--> NYC
- Alice --works_at--> Google
- Alice --member_of--> TechGroup
- Alice --created--> Event1

**Incoming edges:**
- Emma --follows--> Alice
- Bob --married_to--> Alice

**That's the whole point of graphs** - unrestricted connections between nodes!

---

## The Cypher Query Language

### What is Cypher?

**Declarative query language for property graphs**
- Created for Neo4j graph database
- Named after a character in The Matrix (not cryptography)
- Much simpler than SQL for graph queries

---

### Basic Syntax

**Vertices use parentheses `()`:**
```cypher
(Idaho:Location {name:'Idaho', type:'state'})
```

- `Idaho` = variable name (can be anything you want)
- `Location` = label/type
- `{name:'Idaho', type:'state'}` = properties (key-value pairs)

**Edges use square brackets `[]` and arrows:**
```cypher
(Idaho) -[:WITHIN]-> (USA)
```

- `-[:WITHIN]->` = edge labeled "WITHIN"
- `->` = direction (tail to head)
- Can also be `<-` (reversed) or `-` (undirected match)

---

### Creating Graph Data

```cypher
CREATE
  (NAmerica:Location {name:'North America', type:'continent'}),
  (USA:Location {name:'United States', type:'country'}),
  (Idaho:Location {name:'Idaho', type:'state'}),
  (Lucy:Person {name:'Lucy'}),
  (Idaho) -[:WITHIN]-> (USA) -[:WITHIN]-> (NAmerica),
  (Lucy) -[:BORN_IN]-> (Idaho)
```

**This creates:**
- 4 vertices: NAmerica, USA, Idaho, Lucy
- 3 edges: Idaho→USA, USA→NAmerica, Lucy→Idaho

**All in one CREATE statement!**

---

### Querying Graphs

**Example:** Find people who emigrated from US to Europe

```cypher
MATCH
  (person) -[:BORN_IN]-> () -[:WITHIN*0..]-> (us:Location {name:'United States'}),
  (person) -[:LIVES_IN]-> () -[:WITHIN*0..]-> (eu:Location {name:'Europe'})
RETURN person.name
```

---

### Breaking Down the Query

**Line 1:**
```cypher
(person) -[:BORN_IN]-> () -[:WITHIN*0..]-> (us:Location {name:'United States'})
```

Reading left to right:
1. `(person)` = Find any vertex, call it "person"
2. `-[:BORN_IN]->` = That has an outgoing BORN_IN edge
3. `()` = To some vertex (unnamed placeholder - we don't care what it is)
4. `-[:WITHIN*0..]->` = Follow WITHIN edges, zero or more times
5. `(us:Location {name:'United States'})` = Until reaching USA

---

### The `*0..` Syntax (Variable-Length Paths)

`-[:WITHIN*0..]->` means "follow WITHIN edges **zero or more times**"

- `*` = repeat
- `0..` = from 0 to infinity (no upper limit)

**Why?** Don't know how deep location hierarchy goes:

**0 hops (direct):**
```
person --BORN_IN--> USA
```

**1 hop:**
```
person --BORN_IN--> Idaho --WITHIN--> USA
```

**2 hops:**
```
person --BORN_IN--> Boise --WITHIN--> Idaho --WITHIN--> USA
```

**3 hops:**
```
person --BORN_IN--> Downtown Boise --WITHIN--> Boise --WITHIN--> Idaho --WITHIN--> USA
```

**The query finds all of these!** It says: "Keep following WITHIN edges until you find USA, I don't care how many levels deep."

---

### Other Range Examples

- `*1..3` = 1 to 3 hops (must follow at least once, max 3 times)
- `*2..` = 2 or more hops (must follow at least twice)
- `*..5` = up to 5 hops (0 to 5 times)
- `*0..` = 0 or more hops (what we have - unlimited)

---

### Empty Parentheses `()`

```cypher
(person) -[:BORN_IN]-> () -[:WITHIN*0..]-> (us:...)
```

**The `()` means:** "Some vertex exists here, but I don't care about its details"

**Why use it?**
- You need it as a stepping stone in the pattern
- But you don't need to reference it later
- Don't need to return it or use it in conditions

**If you DID care, you'd name it:**
```cypher
(person) -[:BORN_IN]-> (birthplace) -[:WITHIN*0..]-> (us:...)
RETURN person.name, birthplace.name
```

Now you can use `birthplace` later.

**Think of `()` like `_` in pattern matching** - a wildcard placeholder.

---

### Line 2 of the Query

```cypher
(person) -[:LIVES_IN]-> () -[:WITHIN*0..]-> (eu:Location {name:'Europe'})
```

Same pattern for current residence!

**Note:** Same `(person)` variable - this is the SAME person vertex from line 1.

The query finds people who match BOTH patterns:
- Born somewhere within the US
- Currently live somewhere within Europe

---

### Return Statement

```cypher
RETURN person.name
```

Return the `name` property of matching people.

---

### Cypher vs SQL

**The same query in SQL requires:**
- Recursive Common Table Expressions (CTEs)
- Multiple self-joins on the edges table
- Complex WHERE clauses
- Approximately 30 lines of code
- Much harder to read, write, and maintain

**The same query in Cypher:**
- 3 lines
- Natural pattern matching
- Declarative and easy to understand

**This demonstrates why specialized graph query languages exist** - they make graph queries dramatically simpler.

---

## Key Terminology

| Term | Definition |
|------|------------|
| **Declarative** | Specify WHAT you want, system figures out HOW |
| **Imperative** | Specify step-by-step HOW to do it |
| **Query Optimizer** | Database component that chooses efficient execution strategy |
| **MapReduce** | Programming model for distributed data processing (map + reduce) |
| **Map Function** | Transforms each document into key-value pairs |
| **Reduce Function** | Combines values with same key into single result |
| **Pure Function** | Function with no side effects, only uses input data |
| **Graph** | Data structure with vertices and edges |
| **Vertex (Node)** | Entity in a graph (person, place, thing) |
| **Edge (Relationship)** | Connection between vertices |
| **Property Graph** | Graph where vertices and edges have properties |
| **Tail Vertex** | Where edge starts (non-pointy end of arrow) |
| **Head Vertex** | Where edge ends (pointy end of arrow) |
| **Cypher** | Declarative query language for graphs (Neo4j) |
| **Variable-Length Path** | Pattern matching with 0 or more edge traversals (*0..) |
| **Aggregation Pipeline** | MongoDB's declarative alternative to MapReduce |

---

## Key Takeaways

### On Query Languages
1. **Declarative wins:** Simpler, more optimizable, more flexible than imperative
2. **Database freedom:** Declarative queries allow database to reorganize data and improve performance
3. **Universal pattern:** SQL for databases, CSS for styling, Cypher for graphs - all declarative
4. **Parallel execution:** Declarative queries easier to parallelize across multiple cores

### On MapReduce
1. **Middle ground:** Neither fully declarative nor fully imperative
2. **Two-phase processing:** Map transforms, reduce aggregates
3. **Distributed by design:** Can run across thousands of machines
4. **Pure functions required:** No side effects allows retry and parallelization
5. **Modern alternative:** Aggregation pipelines are more declarative and easier to use

### On Graphs
1. **For interconnection:** Best when data has many types of relationships and entities
2. **Path traversal is natural:** Graph databases optimized for multi-hop queries
3. **Relational can do it:** Can represent graphs in SQL, but queries become complex
4. **Specialized tools matter:** Cypher in 3 lines vs SQL in 30 lines for same query
5. **No true two-way edges:** Bidirectional relationships = two one-way edges

### Design Decisions
1. **Simple many-to-many:** Relational works fine (students ↔ classes)
2. **Highly interconnected:** Graph databases shine (social networks, recommendation engines)
3. **Variable-length paths:** Graph queries handle unknown traversal depth elegantly
4. **Multiple relationships:** Graphs naturally store many relationship types in one structure

---

## Comparison Summary

| Aspect | SQL | MapReduce | Cypher |
|--------|-----|-----------|--------|
| **Style** | Declarative | Middle ground | Declarative |
| **Best for** | Structured data, joins | Large-scale batch processing | Highly connected data |
| **Learning curve** | Moderate | Steep | Easy |
| **Optimization** | Excellent | Limited | Excellent |
| **Parallelization** | Good | Excellent | Good |

---

## Coming Up (Not Yet Covered in Reading)

- SPARQL (another graph query language)
- Datalog (logic-based query language)
- Triple-stores (RDF data model)
- Full comparison of all data models

---

## Cross-References

- Day 1 notes: Data models, relational vs document, schema approaches
- Chapter 10: More on MapReduce and batch processing
- Figure 2-5: Graph structure example (Lucy and Alain)