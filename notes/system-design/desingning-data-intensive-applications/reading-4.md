# Chapter 2: Data Models and Query Languages
## Study Notes - Day 3 (Triple-Stores, SPARQL, and Datalog)

> From "Designing Data-Intensive Applications" by Martin Kleppmann
> **Date:** January 15, 2026
> **Topics:** Triple-store model, RDF, Turtle, SPARQL, Datalog

---

## Triple-Stores and SPARQL

### What is the Triple-Store Model?

**Mostly equivalent to property graph model**, just different terminology.

**All information stored as three-part statements:**

```
(subject, predicate, object)
```

### Example Triple

```
(Jim, likes, bananas)
```

- **subject:** Jim (who/what we're talking about)
- **predicate:** likes (the verb/relationship)
- **object:** bananas (the value/thing)

---

## Mapping Triples to Graph Concepts

### Subject = Vertex

The subject of a triple is equivalent to a vertex in a graph.

---

### Object Can Be Two Things

**1. A primitive value (string, number):**

Example: `(lucy, age, 33)`

**In graph terms:** Like a vertex `lucy` with property `{"age": 33}`
- predicate + object = key + value of a property

**2. Another vertex:**

Example: `(lucy, marriedTo, alain)`

**In graph terms:**
- **subject** = tail vertex (lucy)
- **object** = head vertex (alain)
- **predicate** = edge label (marriedTo)
- Creates edge: `lucy --marriedTo--> alain`

---

## Triple-Store vs Cypher (Property Graph)

### Same Data, Different Syntax

**Cypher (Property Graph):**
```cypher
CREATE
  (lucy:Person {name:'Lucy', age:33}),
  (alain:Person {name:'Alain'}),
  (lucy) -[:MARRIED_TO]-> (alain)
```

Properties bundled on vertices, edges connect them.

---

**Triple-Store:**
```
(lucy, a, Person)
(lucy, name, "Lucy")
(lucy, age, 33)
(alain, a, Person)
(alain, name, "Alain")
(lucy, marriedTo, alain)
```

Everything broken into individual statements.

---

### Key Difference

**Cypher:** Properties grouped on vertices/edges
**Triple-Store:** Everything flattened into atomic triples

**But they represent the same graph!**

---

## Industry Usage

**Property Graphs (Cypher/Neo4j):**
- More widely used in practice
- Better tooling and ecosystem
- Used by: LinkedIn, Airbnb, NASA, eBay, Walmart

**Triple-Stores (SPARQL):**
- Less common in industry
- More academic/research use
- Used for: semantic web, knowledge graphs
- Examples: DBpedia, Wikidata

---

## The Turtle Format

### What is Turtle?

**Turtle** = human-readable format for writing triples
- Subset of Notation3 (N3)
- Used for RDF data

---

### Basic Syntax

```turtle
@prefix : <urn:example:>.

_:lucy      a           :Person.
_:lucy      :name       "Lucy".
_:lucy      :bornIn     _:idaho.
_:idaho     a           :Location.
_:idaho     :name       "Idaho".
_:idaho     :type       "state".
_:idaho     :within     _:usa.
_:usa       a           :Location.
_:usa       :name       "United States".
_:usa       :type       "country".
_:usa       :within     _:namerica.
_:namerica  a           :Location.
_:namerica  :name       "North America".
_:namerica  :type       "continent".
```

---

### Understanding the Notation

**The Prefix:**
```turtle
@prefix : <urn:example:>.
```

Defines a namespace shorthand. When you write `:name`, it expands to `<urn:example:name>`.
Just a way to avoid repetition - not critical to understand.

---

**The `_:` Notation (Blank Nodes):**

`_:lucy` = "a blank node named lucy"
- Blank node = anonymous vertex that only exists in this file
- The name is just for referencing within this file
- Like a temporary variable name

**Used for:** Vertices/entities

---

**The `:` Notation (Namespace):**

`:name` or `:Person` = "from the prefix namespace"

Expands to `<urn:example:name>` or `<urn:example:Person>`

**Used for:** Predicates (properties/edges) and types

---

**The `a` Keyword:**

`a` = special keyword meaning "is a type of"

Shorthand for `rdf:type`

```turtle
_:lucy  a  :Person
```
Means: "Lucy is a Person"

No prefix because it's built into Turtle.

---

### Reading Triples

**Each line follows the pattern:**

```turtle
subject    predicate    object.
   ↑           ↑           ↑
  WHO      DOES/HAS     WHAT
```

---

**Examples in plain English:**

```turtle
_:lucy      a           :Person.
```
"Lucy is a Person"

```turtle
_:lucy      :name       "Lucy".
```
"Lucy has name 'Lucy'"

```turtle
_:lucy      :bornIn     _:idaho.
```
"Lucy was born in Idaho"

```turtle
_:idaho     :within     _:usa.
```
"Idaho is within USA"

---

### Objects: Three Types

**The third column (object) can be:**

**1. Type/Class (`:Something`):**
```turtle
_:lucy  a  :Person
```
Person is a type from the namespace.

**2. Literal String (`"Something"`):**
```turtle
_:lucy  :name  "Lucy"
```
"Lucy" is a string value.

**3. Another Vertex (`_:something`):**
```turtle
_:lucy  :bornIn  _:idaho
```
Idaho is another vertex.

---

### Conventions

**Capitalization:**
- `_:lucy` = instance (lowercase) - a specific person
- `:Person` = type/class (capitalized) - the category

Like in programming:
```javascript
const lucy = new Person()
  ↑              ↑
instance       class
```

---

### The Complete Graph

From the Turtle example:

**4 Vertices:**
1. `_:lucy` (Person)
2. `_:idaho` (Location)
3. `_:usa` (Location)
4. `_:namerica` (Location)

**3 Edges:**
- `_:lucy` --bornIn--> `_:idaho`
- `_:idaho` --within--> `_:usa`
- `_:usa` --within--> `_:namerica`

**Properties:**
- lucy: name="Lucy"
- idaho: name="Idaho", type="state"
- usa: name="United States", type="country"
- namerica: name="North America", type="continent"

---

## More Concise Turtle Format

### Using Semicolons

Instead of repeating the subject:
```turtle
_:idaho     a           :Location.
_:idaho     :name       "Idaho".
_:idaho     :type       "state".
_:idaho     :within     _:usa.
```

Use semicolons to compress:
```turtle
_:idaho  a :Location; :name "Idaho"; :type "state"; :within _:usa.
```

**Semicolon `;` means:** "Still talking about the same subject, here's another predicate-object pair"

---

### Example 2-7 (Compressed):

```turtle
@prefix : <urn:example:>.

_:lucy     a :Person;   :name "Lucy";             :bornIn  :idaho.
_:idaho    a :Location; :name "Idaho";            :type "state";    :within _:usa.
_:usa      a :Location; :name "United States";    :type "country";  :within _:namerica.
_:namerica a :Location; :name "North America";    :type "continent".
```

Same data, 4 lines instead of 13!

---

## The Semantic Web

### What Was It?

**The vision (early 2000s):**
- Websites already publish text/pictures for humans
- Why not also publish machine-readable data for computers?
- Create a "web of data" - internet-wide "database of everything"
- Use RDF (Resource Description Framework) for consistent format

**Goal:** Different websites' data could be automatically combined.

---

### What Happened?

**It failed.**
- Overhyped in early 2000s
- Never realized in practice
- Made many people cynical
- Suffered from "dizzying plethora of acronyms, overly complex standards, and hubris"

---

### The Silver Lining

**Author's take:** Look past the failures - there IS good work from the semantic web project.

**Key point:** **Triples can be a good internal data model for applications**, even if you don't care about publishing RDF data.

**Bottom line:** Semantic web failed, but triple concept is still useful.

---

## The RDF Data Model

### What is RDF?

**RDF = Resource Description Framework**

Just a standard way of writing triples.

---

### Formats

**Turtle:** Human-readable (what we've been using)

**RDF/XML:** Same thing but verbose XML format
- Does the same thing "much more verbosely"
- Tools like Apache Jena can convert between formats

---

### Turtle vs RDF/XML Comparison

**Turtle (clean):**
```turtle
_:idaho  a :Location; :name "Idaho"; :type "state"; :within _:usa.
```

**RDF/XML (verbose):**
```xml
<Location rdf:nodeID="idaho">
  <name>Idaho</name>
  <type>state</type>
  <within>
    <Location rdf:nodeID="usa">
      <name>United States</name>
      ...
    </Location>
  </within>
</Location>
```

Way more code for the same data!

---

### RDF Quirks for Internet-Wide Data

**Because RDF designed for combining data from different websites:**

Subjects, predicates, and objects are often **URIs** (web addresses).

**Example predicate:**
Instead of: `:within`
Full form: `<http://my-company.com/namespace#within>`

---

**Why URIs?**

Avoid naming conflicts when combining data from different sources.

Your `within`: `<http://my-company.com/foo#within>`
Their `within`: `<http://other.org/foo#lives_in>`

Different URIs = no conflict.

---

**Important:** The namespace URIs don't need to resolve to actual websites. They're just unique identifiers.

Examples use `urn:example:within` (not real URLs) to make this clear.

---

## The SPARQL Query Language

### What is SPARQL?

**SPARQL** = query language for triple-stores using RDF
- Pronounced "sparkle"
- Acronym: SPARQL Protocol and RDF Query Language
- Predates Cypher (Cypher borrowed pattern matching from SPARQL)

---

### Example 2-9: Find People Who Emigrated

**Goal:** Find people born in US, living in Europe

```sparql
PREFIX : <urn:example:>

SELECT ?personName WHERE {
  ?person :name ?personName.
  ?person :bornIn / :within* / :name "United States".
  ?person :livesIn / :within* / :name "Europe".
}
```

---

### Understanding SPARQL Syntax

**Variables start with `?`:**
- `?person` = variable for any person vertex
- `?personName` = variable for the name value

**The `/` means "follow this edge":**
```sparql
?person :bornIn / :within* / :name "United States"
```

Reading: "person → bornIn → within (0+ times) → name = 'United States'"

**The `*` means "zero or more times":**
- `:within*` = follow within edges 0 or more times
- Handles variable depth: Idaho→USA or Boise→Idaho→USA

---

### SPARQL vs Cypher

**Cypher:**
```cypher
(person) -[:BORN_IN]-> () -[:WITHIN*0..]-> (location)
```

**SPARQL:**
```sparql
?person :bornIn / :within* ?location.
```

**Very similar!** Just different syntax.

---

### Key Difference: No Distinction Between Properties and Edges

**Cypher distinguishes:**
```cypher
(usa {name:'United States'})  # Property syntax
(usa) -[:WITHIN]-> (namerica) # Edge syntax
```

**SPARQL doesn't distinguish:**
```sparql
?usa :name "United States".   # Property
?usa :within ?namerica.       # Edge
```

Both use same predicate syntax because RDF treats properties and edges uniformly.

---

**Example - Matching Property:**

**Cypher:**
```cypher
(usa {name:'United States'})
```

**SPARQL:**
```sparql
?usa :name "United States".
```

---

### Author's Conclusion

> "SPARQL is a nice query language—even if the semantic web never happens, it can be a powerful tool for applications to use internally."

Translation: Semantic web failed, but SPARQL is still useful for graph queries.

---

## Graph Databases vs CODASYL Network Model

### The Question

Remember CODASYL from the 1970s? It also used a network/graph structure.

**Are graph databases just CODASYL 2.0 in disguise?**

---

### Answer: No! Four Key Differences

---

### Difference 1: Schema Flexibility

**CODASYL:**
- Had a schema specifying which record type could nest within which other record type
- Restricted connections

**Graph databases:**
- **No such restriction**
- Any vertex can have an edge to any other vertex
- Much greater flexibility to adapt to changing requirements

---

### Difference 2: How You Access Data

**CODASYL:**
- Only way to reach a record: **traverse one of the access paths to it**
- Had to follow predefined routes like navigating a maze
- Very rigid

**Graph databases:**
- Can **refer directly to any vertex by its unique ID**
- Can use an **index** to find vertices with particular values
- Can **jump directly** to any vertex without traversing from root

**Example:**
```cypher
// Jump directly to Lucy by name
MATCH (person:Person {name: 'Lucy'})
RETURN person
```

No need to start at root and traverse!

---

### Difference 3: Ordering

**CODASYL:**
- Children of a record were an **ordered set**
- Database had to maintain ordering
- Applications had to worry about positions when inserting new records
- Complicated storage and insertion logic

**Graph databases:**
- Vertices and edges are **not ordered**
- Can only sort results when making a query
- Much simpler!

---

### Difference 4: Query Languages

**CODASYL:**
- All queries were **imperative**
- Difficult to write
- Easily broken by schema changes
- Had to manually specify access paths

**Graph databases:**
- Can write imperative traversal code if you want
- But **also support declarative query languages** (Cypher, SPARQL)
- Much easier to write and maintain
- Query optimizer figures out access paths automatically

---

### Summary

**Graph databases learned from CODASYL's mistakes:**
- ✅ Kept: Graph structure for representing relationships
- ❌ Fixed: Rigid access paths → direct access by ID/index
- ❌ Fixed: Imperative queries → declarative query languages
- ❌ Fixed: Ordered children → unordered vertices/edges
- ❌ Fixed: Restrictive schema → any vertex connects to any vertex

---

## The Foundation: Datalog

### What is Datalog?

**Much older language than SPARQL or Cypher** (studied extensively in 1980s)

**Status:**
- Less well known among software engineers
- Important because it provides the **foundation** that later query languages build upon

**In practice:**
- Used in a few systems: Datomic, Cascalog (Hadoop)
- Academic influence on modern query languages

---

### Datalog's Data Model

**Similar to triple-store, but generalized**

Instead of:
```
(subject, predicate, object)
```

Write as:
```
predicate(subject, object)
```

**Predicate comes first!**

---

### Example 2-10: Data in Datalog

```prolog
name(namerica, 'North America').
type(namerica, continent).

name(usa, 'United States').
type(usa, country).
within(usa, namerica).

name(idaho, 'Idaho').
type(idaho, state).
within(idaho, usa).

name(lucy, 'Lucy').
born_in(lucy, idaho).
```

**Reading it:**
- `name(usa, 'United States')` = "USA's name is 'United States'"
- `within(idaho, usa)` = "Idaho is within USA"
- `born_in(lucy, idaho)` = "Lucy was born in Idaho"

---

## Example 2-11: Query in Datalog

**Goal:** Find people who emigrated from US to Europe

```prolog
within_recursive(Location, Name) :- name(Location, Name).     /* Rule 1 */

within_recursive(Location, Name) :- within(Location, Via),    /* Rule 2 */
                                     within_recursive(Via, Name).

migrated(Name, BornIn, LivingIn) :- name(Person, Name),       /* Rule 3 */
                                     born_in(Person, BornLoc),
                                     within_recursive(BornLoc, BornIn),
                                     lives_in(Person, LivingLoc),
                                     within_recursive(LivingLoc, LivingIn).

?- migrated(Who, 'United States', 'Europe').
/* Who = 'Lucy'. */
```

---

### How Datalog Works

**Unlike Cypher/SPARQL (which jump straight to SELECT):**

Datalog takes a small step at a time by **defining rules**.

**Rules define new predicates** derived from data or other rules.

**The `:-` symbol means "IF"** (like ← in logic)

---

### Rule 1: Base Case

```prolog
within_recursive(Location, Name) :- name(Location, Name).
```

**Reading:** "A location is within_recursively its own name"

**Example:**
- Given: `name(usa, 'United States')`
- Therefore: `within_recursive(usa, 'United States')` is true

---

### Rule 2: Recursive Case

```prolog
within_recursive(Location, Name) :- within(Location, Via),
                                     within_recursive(Via, Name).
```

**Reading:** "Location is within_recursively Name IF:
- Location is within some intermediate location Via, AND
- Via is within_recursively Name"

**Example:**
- `within(idaho, usa)` exists (fact)
- `within_recursive(usa, 'United States')` is true (from Rule 1)
- Therefore: `within_recursive(idaho, 'United States')` is true

**This handles chains:**
- Idaho → USA: `within_recursive(idaho, 'United States')`
- Idaho → USA → North America: `within_recursive(idaho, 'North America')`

---

### Rule 3: The Migration Query

```prolog
migrated(Name, BornIn, LivingIn) :- name(Person, Name),
                                     born_in(Person, BornLoc),
                                     within_recursive(BornLoc, BornIn),
                                     lives_in(Person, LivingLoc),
                                     within_recursive(LivingLoc, LivingIn).
```

**Reading:** "A person with Name migrated from BornIn to LivingIn IF:
- Person's name is Name, AND
- Person was born in BornLoc, AND
- BornLoc is within_recursively BornIn, AND
- Person lives in LivingLoc, AND
- LivingLoc is within_recursively LivingIn"

---

### The Query

```prolog
?- migrated(Who, 'United States', 'Europe').
```

**Reading:** "Find Who that migrated from United States to Europe"

**Result:** `Who = 'Lucy'`

---

### Key Insight

**Rules can refer to other rules**, just like functions calling functions.

**Rules can call themselves recursively** (like `within_recursive`).

**Complex queries built up piece by piece:**
1. Define `within_recursive` to handle variable-depth hierarchies
2. Use `within_recursive` in `migrated` rule
3. Query `migrated` to get final answer

---

### Datalog vs SQL/Cypher/SPARQL

**Cypher/SPARQL:**
- Jump straight to pattern matching
- Everything in one query

**Datalog:**
- Define reusable rules step by step
- Compose rules to build complex queries
- More modular approach

**Author's note:** Datalog is "a subset of Prolog" (logic programming language used in computer science).

---

## Key Terminology

| Term | Definition |
|------|------------|
| **Triple** | Three-part statement: (subject, predicate, object) |
| **Triple-Store** | Database that stores data as triples |
| **Subject** | The "who/what" in a triple (equivalent to vertex) |
| **Predicate** | The "relationship/property" in a triple |
| **Object** | The "value/target" in a triple (can be value or another vertex) |
| **RDF** | Resource Description Framework - standard for triples |
| **Turtle** | Human-readable format for writing RDF triples |
| **Notation3 (N3)** | Format that Turtle is a subset of |
| **Blank Node** | Anonymous vertex in RDF (written as `_:name`) |
| **Namespace** | URI prefix to avoid naming conflicts |
| **`a` keyword** | Turtle shorthand for "is a type of" (rdf:type) |
| **SPARQL** | Query language for triple-stores ("sparkle") |
| **Semantic Web** | Failed 2000s vision of machine-readable web data |
| **CODASYL** | 1970s network model database (rigid, failed) |
| **Datalog** | Logic-based query language from 1980s |
| **Rule** | Derived predicate in Datalog defined in terms of other predicates |
| **`:-` operator** | "IF" in Datalog (defines rules) |
| **Prolog** | Logic programming language that Datalog is subset of |

---

## Key Takeaways

### On Triple-Stores
1. **Same as property graphs:** Just different terminology and syntax
2. **Everything is atomic:** Each fact broken into individual (s, p, o) statements
3. **Uniform structure:** Properties and edges both represented as triples
4. **Less popular than property graphs:** But still useful to know

### On RDF and Semantic Web
1. **Semantic web failed:** Overhyped 2000s vision never materialized
2. **RDF still useful:** Triples work well as internal data model
3. **Turtle > XML:** Human-readable format preferred over verbose XML
4. **URIs for namespaces:** Avoid conflicts when combining data from different sources

### On SPARQL
1. **Declarative query language:** Like SQL but for graphs
2. **Similar to Cypher:** Pattern matching borrowed from SPARQL
3. **No property/edge distinction:** Uniform predicate syntax for both
4. **Useful despite semantic web failure:** Good for internal graph queries

### On Graph Databases vs CODASYL
1. **Learned from history:** Fixed all of CODASYL's problems
2. **Direct access:** Can jump to any vertex by ID/index, not just traverse
3. **No ordering requirements:** Vertices/edges unordered
4. **Declarative queries:** Don't have to specify access paths manually
5. **Schema flexibility:** Any vertex can connect to any vertex

### On Datalog
1. **Foundation for modern query languages:** Influenced SQL, SPARQL, Cypher
2. **Rule-based approach:** Build complex queries from simple rules
3. **Recursive rules:** Can define recursive predicates naturally
4. **Modular and composable:** Rules can reference other rules
5. **Less practical today:** But important to understand the concepts

---

## Comparison Table

| Feature | Property Graph (Cypher) | Triple-Store (SPARQL) | Datalog |
|---------|------------------------|----------------------|---------|
| **Data Model** | Vertices with properties, labeled edges | All data as (s, p, o) triples | Predicates: predicate(s, o) |
| **Industry Usage** | High (Neo4j, Neptune) | Low (academic, research) | Very low (Datomic) |
| **Query Style** | Pattern matching | Pattern matching | Rule definition |
| **Learning Curve** | Easy | Moderate | Steep |
| **Recursion** | `*0..` syntax | `*` syntax | Recursive rules |
| **Predates** | No (2010s) | Yes (2000s) | Yes (1980s) |
| **Main Use** | Production apps | Knowledge graphs | Academic/theoretical |

---

## Design Questions to Consider

When choosing a graph data model:
1. Do you need a widely-used, production-ready solution? → Property graphs (Neo4j)
2. Are you working with semantic web/knowledge graphs? → Triple-stores (SPARQL)
3. Do you need to define complex recursive rules? → Datalog
4. Does your team already know SQL? → Property graphs are most similar
5. Is direct vertex access important? → All modern graph DBs support this (unlike CODASYL)

---

## Historical Context

**1960s-70s:** IMS (hierarchical), CODASYL (network) - rigid, imperative
**1970s:** Relational model wins - declarative queries, flexibility
**1980s:** Datalog studied - logic-based queries, recursive rules
**2000s:** Semantic web hype - RDF, triple-stores, failed vision
**2010s:** Modern graph databases - learned from history, declarative queries

**The pattern:** Each generation learns from previous mistakes and improves.

---

## Coming Up (Not Yet Covered)

- More on Datalog queries and rules
- Comparison of all data models (relational, document, graph)
- When to use which model
- Schema evolution strategies

---

## Cross-References

- Day 1: Data models overview, relational vs document
- Day 2: Cypher, graph basics, MapReduce
- Page 36: CODASYL network model details
- Chapter 10: More on Datalog and Cascalog