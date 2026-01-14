# Chapter 2 Continued: Data Models and Query Languages
## Study Notes - Data Models, Relational vs Document Databases

> From "Designing Data-Intensive Applications" by Martin Kleppmann

---

## Response Time vs Latency (Recap from Yesterday Revision)

### Key Distinction

**Response Time:**
- **Total** time from client's perspective
- Includes everything: network delays + queueing + processing + return network delays
- What the user actually experiences

**Latency:**
- **Waiting/delay** time before processing starts
- Component of response time
- Duration request is idle, not being worked on

**Formula:**
```
Response Time = Network delay (send) + Queueing delay + Service time + Network delay (return)
                ↑_____________________________________________↑
                            Latency is part of this
```

### Real-World Analogy

**Restaurant Order:**
- **Latency:** Time waiting in line before chef starts cooking
- **Response Time:** Total time from placing order until food arrives at your table
  - Includes: waiting in line + cooking time + delivery to table

### Why It Matters

- High response time could be from high latency (too much queueing) OR slow processing
- Understanding which helps you optimize:
  - High latency → need more capacity to reduce queue
  - Slow processing → need better algorithms or hardware

---

## Distributing Systems (Recap from Yesterday)

### Stateless vs Stateful Systems

**Stateless Services (Easy to Distribute):**
- Web servers, API servers
- Don't store data themselves
- Can spin up 10 copies, load balance between them
- Example: 
  ```
  Request → [Server 1, Server 2, Server 3, ...] → Response
  Any server can handle any request
  ```

**Stateful Systems (Hard to Distribute):**
- Databases, caches
- Store data, so distribution introduces complexity:
  - How to keep data consistent across nodes?
  - How to handle node failures?
  - How to coordinate writes?
  - How to partition data?

### The Strategy

**"Scale up before you scale out"**

1. **Start simple:** One database server (vertical scaling)
   - Buy bigger machine with more RAM/CPU
   - Avoid distributed complexity

2. **Only distribute when forced to:**
   - Single machine becomes too expensive
   - Need high availability (redundancy)
   - Data too large for one machine

**Why:** Distributed databases are much harder to build and maintain

---

## Operations Teams (Recap from Yesterday)

### What Ops Teams Do

**Day-to-day responsibilities:**
- **Monitor systems:** Watch dashboards for errors, performance issues
- **Respond to incidents:** Get paged when systems fail, diagnose and fix
- **Deploy updates:** Roll out new code to production
- **Manage infrastructure:** Provision servers, configure networks, manage databases
- **Handle scaling:** Add resources when traffic spikes
- **Backup and recovery:** Ensure data is backed up, restore when needed
- **Security patches:** Keep systems updated
- **Troubleshoot:** Investigate customer-reported issues
- **Capacity planning:** Predict when you'll need more resources

### Operability

**Definition:** Making it easy for operations teams to keep the system running smoothly

**Good operability features:**
- Clear, helpful logs and error messages
- Automated deployments
- Self-healing systems
- Monitoring dashboards
- Easy rollback capabilities

**Bad operability:**
- Cryptic errors
- Manual deployment steps requiring deep expertise
- Systems that mysteriously fail and need 3am debugging sessions

---

## Data Models and Layers (Recap from Yesterday)

### What is a Data Model?

**Definition:** How you choose to represent and organize information

### The Layers

**Each layer hides complexity from the layer above:**

```
Layer 1: Application Code (Objects/Data Structures)
         ↓ (translation)
Layer 2: Database (Tables/JSON/Graph)
         ↓ (translation)
Layer 3: Database Storage Engine (Bytes, B-trees, indexes)
         ↓ (translation)  
Layer 4: Hardware (Electrical signals, magnetic fields)
```

### Example: Sending an Email

**What you write:**
```python
send_email(to="user@example.com", subject="Welcome!")
```

**What happens underneath:**
- Layer 1: Email API formats message, handles auth
- Layer 2: SMTP protocol conversion
- Layer 3: TCP packet management
- Layer 4: Actual bits over network

**The point:** You don't think about SMTP, TCP, or packets. Each layer provides a clean abstraction.

---

## The Relational Model (SQL)

### Core Concepts

**What Edgar Codd proposed in 1970:**

**Relation (Table):** Unordered collection of tuples

**Tuple (Row):** A collection of values
- Example: `(1, "Alice", "alice@example.com", 25)`
- Note: NOT the same as Python tuples (which are immutable)
- In databases, tuples = rows, and they CAN be updated

**Unordered Collection:**
- Rows have no inherent order
- `SELECT * FROM users` might return different order each time
- Must explicitly use `ORDER BY` if order matters

### Why "Unordered" Matters

**Contrast with ordered structures:**
- Array: `[1, 2, 3]` - order matters
- Linked list - order matters
- SQL table without ORDER BY - order doesn't matter

**Practical implication:**
```sql
-- No guaranteed order
SELECT * FROM users;

-- Explicit order
SELECT * FROM users ORDER BY name;
```

---

## Polyglot Persistence

### Definition

**Polyglot Persistence:** Using multiple different types of databases in the same application, each for what it does best

### Real-World Example

**Building a social media app:**

```
PostgreSQL (Relational)
├─ User accounts, passwords, billing
└─ Good for: structured data, transactions, consistency

MongoDB (Document)
├─ User profiles, posts, settings
└─ Good for: flexible schemas, nested data

Redis (Key-Value)
├─ Session data, caching
└─ Good for: super fast reads/writes

Elasticsearch
├─ Search functionality
└─ Good for: full-text search

Neo4j (Graph)
├─ Friend connections, recommendations
└─ Good for: relationship queries ("friends of friends")
```

**The Philosophy:**
- Don't force everything into one database type
- Pick the right tool for each job
- SQL dominated for decades, but now we can mix and match

---

## The Object-Relational Mismatch

### The Problem: Impedance Mismatch

**In Your Code (Objects):**
```python
class User:
    def __init__(self):
        self.first_name = "Alice"
        self.last_name = "Smith"
        self.jobs = [
            {"title": "Engineer", "company": "Google"},
            {"title": "Intern", "company": "Microsoft"}
        ]
```

**In the Database (Tables):**
```sql
users table:
user_id | first_name | last_name
1       | Alice      | Smith

jobs table:
id | user_id | title    | company
1  | 1       | Engineer | Google
2  | 1       | Intern   | Microsoft
```

**The Mismatch:**
- Code: Nice nested structure (list inside object)
- Database: Separate tables with foreign keys
- Annoying translation needed!

### What ORMs Do

**ORM (Object-Relational Mapping):** Translates between objects and tables automatically

**Without ORM (Manual):**
```python
# Save user
cursor.execute("INSERT INTO users (first_name, last_name) VALUES (?, ?)", 
               (user.first_name, user.last_name))
user_id = cursor.lastrowid

# Save each job
for job in user.jobs:
    cursor.execute("INSERT INTO jobs (user_id, title, company) VALUES (?, ?, ?)",
                   (user_id, job['title'], job['company']))

# Load user - need to reconstruct object from multiple tables
cursor.execute("SELECT * FROM users WHERE id = ?", (1,))
user_row = cursor.fetchone()
cursor.execute("SELECT * FROM jobs WHERE user_id = ?", (1,))
job_rows = cursor.fetchall()
# Manually build User object...
```

**With ORM (e.g., SQLAlchemy):**
```python
# Save
session.add(user)
session.commit()

# Load
user = session.query(User).filter_by(id=1).first()
print(user.jobs)  # Jobs automatically loaded!
```

**But:** ORMs can't completely hide the mismatch. The fundamental difference between objects and tables still exists.

---

## Three Ways to Store One-to-Many Relationships

### Scenario: User with Multiple Jobs

**Option 1: Traditional SQL (Separate Tables)**

```sql
users table:
id | first_name | last_name
1  | Alice      | Smith

jobs table:
id | user_id | title    | company
1  | 1       | Engineer | Google
2  | 1       | Intern   | Microsoft
```

**To get data:**
```sql
SELECT * FROM users WHERE id = 1;
SELECT * FROM jobs WHERE user_id = 1;
```
Two queries, manual joining.

---

**Option 2: Modern SQL (JSON Column with Database Support)**

```sql
users table:
id | first_name | last_name | jobs (JSON column)
1  | Alice      | Smith     | [{"title":"Engineer","company":"Google"},
                             |  {"title":"Intern","company":"Microsoft"}]
```

**Can query inside JSON:**
```sql
SELECT * FROM users WHERE jobs->0->>'title' = 'Engineer';
```

Database understands JSON structure and can index it.

---

**Option 3: Dumb Text Storage**

```sql
users table:
id | first_name | last_name | jobs (TEXT column)
1  | Alice      | Smith     | '[{"title":"Engineer"...}]'
```

Database treats it as plain text string. Can't query inside it.

Must fetch entire row, parse JSON in application code.

---

## Self-Contained Documents

### Definition

**Self-contained document:** All information about one thing stored together in one place

### Example: Resume/LinkedIn Profile

**Self-contained (JSON):**
```json
{
  "user_id": 123,
  "first_name": "Alice",
  "last_name": "Smith",
  "jobs": [
    {"title": "Engineer", "company": "Google", "years": "2020-2023"},
    {"title": "Intern", "company": "Microsoft", "years": "2019-2020"}
  ],
  "education": [
    {"degree": "BS CS", "school": "MIT", "year": 2019}
  ],
  "contact": {
    "email": "alice@example.com",
    "phone": "555-1234"
  }
}
```

**One read = entire profile.** Everything together.

---

**NOT Self-contained (SQL - Spread Across Tables):**
```
users table: id, first_name, last_name
jobs table: id, user_id, title, company, years
education table: id, user_id, degree, school, year
contacts table: id, user_id, email, phone
```

Alice's info scattered across 4 tables. Need multiple queries and JOINs to reconstruct.

---

### Why It Matters

A resume is naturally a **single unit**. When you think "show me Alice's profile," you want ALL of it at once.

Document databases (MongoDB, CouchDB) excel at this - store and retrieve complete self-contained documents easily.

---

## XML vs JSON

### What XML Looks Like

```xml
<?xml version="1.0"?>
<user>
  <id>123</id>
  <first_name>Alice</first_name>
  <last_name>Smith</last_name>
  <jobs>
    <job>
      <title>Engineer</title>
      <company>Google</company>
    </job>
    <job>
      <title>Intern</title>
      <company>Microsoft</company>
    </job>
  </jobs>
</user>
```

### Same Data in JSON

```json
{
  "id": 123,
  "first_name": "Alice",
  "last_name": "Smith",
  "jobs": [
    {"title": "Engineer", "company": "Google"},
    {"title": "Intern", "company": "Microsoft"}
  ]
}
```

### Comparison

**XML:**
- Verbose (opening and closing tags)
- Looks like HTML
- Popular in 2000s for APIs, config files

**JSON:**
- Cleaner, more concise
- Uses `{}` and `[]`
- Easier to read
- Now dominates for web APIs

**Status:** XML still exists (RSS feeds, enterprise systems) but JSON has largely replaced it for most modern applications.

---

## History: Document Databases Are Repeating History

### The Problem They All Tried to Solve

How to represent relationships in a database?

---

### 1960s-70s: IMS (Hierarchical Model)

**What it was:**
- IBM's database for Apollo space program
- Data stored as **tree of records nested within records**
- Just like JSON!

**Good for:** One-to-many relationships (one user → many jobs)

**Bad for:** Many-to-many relationships

**Problem:** Didn't support joins. Developers had to:
- Duplicate (denormalize) data, OR
- Manually resolve references in application code

**Sound familiar?** This is exactly what modern document databases do!

---

### Network Model (CODASYL)

**Goal:** Fix IMS by allowing many-to-many relationships

**How it worked:**
- Records connected by **pointers** (like linked lists/graphs)
- NOT foreign keys, but actual memory pointers stored on disk

**Access Paths:**
- To access data, follow a **path** from root record along chains of links
- Example: Start at user → follow pointer to first job → follow pointer to next job → etc.

**The Problem:**
- Manually specifying access paths in application code
- Like navigating a maze - had to keep track in your head
- If relationships changed, rewrite all query code
- Committee members admitted it was "navigating an n-dimensional data space"

**Why it failed:** Too complicated and inflexible

---

### The Relational Model (Winner)

**What it did differently:**

1. **Simple structure:** Just tables and rows
   - No nested structures
   - No complicated pointer chains

2. **Query flexibility:** Can access data any way you want
   ```sql
   SELECT * FROM users WHERE name = 'Alice';
   -- OR
   SELECT * FROM users JOIN jobs ON users.id = jobs.user_id;
   -- Database figures out the path!
   ```

3. **Query Optimizer:** Database automatically decides:
   - Which indexes to use
   - What order to execute operations
   - Most efficient path through data

**The Key Innovation:**
- Developers write WHAT they want (declarative)
- Database figures out HOW to get it (access path)
- No manual navigation required

**Result:** SQL won and dominated for ~40 years

---

### Modern Document Databases

**What they brought back:**
- Hierarchical model (nested documents)
- One-to-many stored within parent

**What they avoided:**
- Complicated access paths (like CODASYL)
- Use simple references/IDs (like SQL foreign keys)

**The Author's Point:**
> "Document databases have not followed the path of CODASYL"

They learned from history - kept the good parts (nested documents), avoided the bad parts (manual access paths).

---

## Relational vs Document Databases: The Comparison

### Document Model Strengths

1. **Schema flexibility**
2. **Better performance due to locality**
3. **Closer to data structures used by application**

### Relational Model Strengths

1. **Better support for joins**
2. **Better support for many-to-one relationships**
3. **Better support for many-to-many relationships**

---

## Which Leads to Simpler Application Code?

### When Document Model is Better

**If your data has a document-like structure (tree of one-to-many relationships):**

Example: Resume, blog post, product catalog
- Self-contained
- Naturally hierarchical
- Retrieved as single unit

**Using relational (shredding) creates problems:**
- Cumbersome schemas
- Unnecessarily complicated application code
- Need to JOIN multiple tables to reconstruct the document

**Document model limitations:**
- Cannot directly reference nested items
  - Must say: "the second item in the list of positions for user 251"
  - Like access paths in hierarchical model
  - But not usually a problem if nesting isn't too deep

---

### When Relational Model is Better

**If your application uses many-to-many relationships:**

**Document model problems:**
- Poor join support (or none at all)
- Must emulate joins in application code with multiple queries
- Slower than database joins
- More complex application code

**Example needing many-to-many:**
- Social networks (users ←→ friends)
- E-commerce (orders ←→ products)
- Course registration (students ←→ classes)

**Options with document databases:**
1. **Denormalize:** Duplicate data (consistency problems)
2. **Application-side joins:** Multiple queries, manual merging (slow, complex)

---

### The Conclusion

**It depends on relationships between data:**

- **Document-like data:** Document model is natural
- **Highly interconnected data:** Document model is awkward, relational is acceptable
- **Graph-like data:** Graph models are most natural (Chapter 2 later)

---

## Many-to-One and Lookups

### The Scenario: Region and Industry

**Bill Gates' LinkedIn profile shows:**
- Region: "Greater Seattle Area"
- Industry: "Philanthropy"

**Question:** Store as text or as ID?

---

### Option 1: Store Text Directly

```json
{
  "user_id": 251,
  "name": "Bill",
  "region": "Greater Seattle Area",
  "industry": "Philanthropy"
}
```

Simple, but problems:
- Inconsistent spelling (Greater Seattle Area vs GREATER SEATTLE AREA vs Seattle Area)
- Ambiguity (Seattle, WA vs Seattle, OR)
- Duplicated data (1000 users = "Philanthropy" stored 1000 times)
- Hard to update (if region name changes, update everywhere)
- Can't translate to other languages

---

### Option 2: Store IDs with Lookup Tables

```json
{
  "user_id": 251,
  "name": "Bill",
  "region_id": "us:91",
  "industry_id": 131
}
```

```sql
regions table:
id    | region_name
us:91 | Greater Seattle Area

industries table:
id  | industry_name
131 | Philanthropy
```

**Advantages:**
- **Consistent spelling:** Everyone picks from dropdown
- **No ambiguity:** IDs are unique
- **Easy updates:** Change "Philanthropy" once, affects all users
- **Localization:** Can translate to other languages
- **Better search:** Can encode that Seattle is in Washington

**When to use IDs:**
✅ Regions, countries, industries (limited, standardized options)
✅ Product categories
✅ Any controlled vocabulary

**When to use text:**
✅ User bios, blog posts, comments (unique, freeform content)

---

### The Trade-off: Normalization

**Normalization:** Store data once, reference by ID
- "Philanthropy" stored once → referenced 1000 times

**Denormalization:** Duplicate data for performance
- "Philanthropy" text stored 1000 times

**The catch:** When using IDs, you need **joins** to get human-readable data back.

---

## Joins in Different Databases

### Relational Databases

**Joins are easy and core feature:**

```sql
SELECT u.first_name, r.region_name, i.industry_name
FROM users u
JOIN regions r ON u.region_id = r.id
JOIN industries i ON u.industry_id = i.id
WHERE u.user_id = 251;
```

Database handles it efficiently.

---

### Document Databases

**Joins are weak or nonexistent:**

**MongoDB:**
- Historically NO joins
- Added `$lookup` in v3.2, but slow and limited
- Not designed for joins

**CouchDB:**
- No joins at all

**The workaround - Application-side joins:**

```javascript
// Step 1: Get user
const user = db.users.findOne({user_id: 251});
// Result: {user_id: 251, name: "Bill", region_id: "us:91"}

// Step 2: Get region (separate query!)
const region = db.regions.findOne({id: user.region_id});
// Result: {id: "us:91", name: "Greater Seattle Area"}

// Step 3: Combine in application
const profile = {
  name: user.name,
  region: region.name
};
```

You're doing the "join" manually. Slower and more complex than database joins.

---

### Why Document Databases Avoid Joins

**Philosophy:** 
- Optimized for fetching complete documents in one read
- Store everything together (denormalized)
- Don't combine data from multiple places

**Document databases are best for:**
- Self-contained, hierarchical data
- Data fetched as complete unit
- Minimal cross-references

---

## Schema-on-Read vs Schema-on-Write

### The Analogy

**Schema-on-read** = Dynamic typing (Python, JavaScript)
- Structure checked at runtime
- Flexible

**Schema-on-write** = Static typing (Java, C++)
- Structure checked at compile time
- Enforced upfront

Like static vs dynamic typing debates: no universal right answer.

---

### Example: Changing Data Format

**Scenario:** Currently store full name in one field. Want to split into first_name and last_name.

---

### Document Database Approach (Schema-on-Read)

**What you do:**
Just start writing new documents with new structure. No migration.

**Result:**
Two different structures coexist:

```javascript
// Old documents (before change)
{name: "Bill Gates"}

// New documents (after change)
{first_name: "Bill", last_name: "Gates"}
```

**Application code handles both:**
```javascript
if (user && user.name && !user.first_name) {
  // Old document - convert on the fly
  user.first_name = user.name.split(" ")[0];
}
```

**Characteristics:**
- No migration needed
- Application handles inconsistency
- Flexible, fast to change
- But: implicit schema in application code

---

### Relational Database Approach (Schema-on-Write)

**What you do:**
Perform explicit migration:

```sql
-- Add new column
ALTER TABLE users ADD COLUMN first_name text;

-- Populate for all existing rows
UPDATE users SET first_name = split_part(name, ' ', 1);
```

**Result:**
All rows have same structure. Database enforces uniformity.

**Characteristics:**
- Explicit migration
- Database enforces consistency
- Schema visible and documented
- But: changes require planning

---

### Performance of Schema Changes

**Common belief:** Schema changes are slow and cause downtime

**Reality:**

**ALTER TABLE:**
- Most databases: milliseconds ✅
- **MySQL exception:** Copies entire table ❌
  - Can take minutes/hours on large tables
  - Tools exist to work around this

**UPDATE statement:**
```sql
UPDATE users SET first_name = split_part(name, ' ', 1);
```
- Slow on ANY database (rewrites every row) ❌

**Alternative:**
Leave `first_name` as NULL, fill at read time - just like document database approach!

---

### When Schema-on-Read is Better

**Data is heterogeneous (mixed structures):**

**Example 1: Event tracking system**
```javascript
// Different event types, completely different fields
{type: "button_click", button_id: "submit", timestamp: "..."}
{type: "page_view", url: "/products", referrer: "google.com", timestamp: "..."}
{type: "purchase", product_id: "123", amount: 99.99, timestamp: "..."}
```

Relational would need:
- Separate table per event type, OR
- One table with tons of nullable columns

Both messy!

---

**Example 2: External API data**
```javascript
// Storing webhook payloads from Stripe, Shopify, etc.
{source: "stripe", event: "payment.succeeded", data: {...}}
{source: "shopify", event: "order.created", data: {...}}
```

You don't control structure, and it could change anytime.

---

### When Schema-on-Write is Better

**All records expected to have same structure:**

Benefits:
- **Documents structure:** Schema makes it clear
- **Enforces correctness:** Catches mistakes at write time
- **Better tooling:** Database knows structure, can optimize

Example: All users should have email, first_name, last_name
→ Schema enforces this, prevents bugs

---

### The Balanced View

> "In situations where data is heterogeneous, a schema may hurt more than it helps, and schemaless documents can be a much more natural data model."

> "But where all records have the same structure, schemas are useful for documenting and enforcing that structure."

**Key word:** "expected"
- Data SHOULD be uniform → schema helps
- Data NATURALLY varies → schema hurts

---

## Key Terminology

| Term | Definition |
|------|------------|
| **Relation** | Table in SQL (unordered collection of tuples) |
| **Tuple** | Row in SQL (collection of values) |
| **Polyglot Persistence** | Using multiple database types in one application |
| **Impedance Mismatch** | Disconnect between object model (code) and relational model (database) |
| **ORM** | Object-Relational Mapping - translates objects to tables |
| **Self-Contained Document** | All data about one thing stored together |
| **Shredding** | Splitting document-like structure into multiple tables |
| **Hierarchical Model** | Tree structure (IMS, 1960s) |
| **Network Model** | Graph with pointers (CODASYL, 1970s) |
| **Access Path** | Manual navigation route through data |
| **Query Optimizer** | Database component that automatically finds efficient access paths |
| **Fan-out** | Number of downstream operations from one upstream operation |
| **Normalization** | Store data once, reference by ID (no duplication) |
| **Denormalization** | Intentionally duplicate data for performance |
| **Schema-on-Read** | Structure implicit, checked at read time (document databases) |
| **Schema-on-Write** | Structure explicit, enforced at write time (relational databases) |
| **Locality** | Storing related data together for efficient access |

---

## Key Takeaways

### On Data Models
1. **Data models shape thinking:** How you model data affects how you solve problems
2. **Layers hide complexity:** Each layer provides clean abstraction for layer above
3. **Choose based on data structure:** Tree-like → document, interconnected → relational, highly connected → graph

### On Relational vs Document
1. **Not either/or:** Models are converging (SQL adds JSON, MongoDB adds joins)
2. **Context matters:** Best choice depends on your data's natural relationships
3. **Joins are expensive in document DBs:** Many-to-many relationships suffer
4. **Documents excel at self-contained data:** Resumes, blog posts, product catalogs

### On Schema
1. **Schema always exists:** Either enforced by database or implicit in application
2. **Schema-on-write = safety:** Catches errors early, documents structure
3. **Schema-on-read = flexibility:** Easy to change, handles heterogeneous data
4. **No universal answer:** Depends on whether data should be uniform

### Historical Lessons
1. **History repeats:** Document databases brought back 1960s hierarchical model
2. **Learn from past:** Avoided CODASYL's mistakes (manual access paths)
3. **SQL won for good reasons:** Query optimizer, flexibility, declarative queries
4. **Different tools for different jobs:** Polyglot persistence is the future

---

## Design Questions to Ask

When choosing a data model:
1. Is my data naturally document-like (tree) or highly interconnected?
2. Do I need many-to-many relationships?
3. Is my data structure uniform or heterogeneous?
4. How important is schema enforcement vs flexibility?
5. Will I need complex joins?
6. Is data locality (reading complete documents) critical?
7. Do I need to query in many different ways?

---
