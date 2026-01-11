# Chapter 1: Reliable, Scalable, and Maintainable Applications
## Study Notes - Pages 1-13

> From "Designing Data-Intensive Applications" by Martin Kleppmann

---

## Overview: Data-Intensive vs Compute-Intensive Applications

**Data-Intensive Applications:**
- Primary challenge: amount of data, complexity of data, speed of change
- CPU power rarely the limiting factor
- Most modern applications fall into this category

**Standard Building Blocks:**
- **Databases:** Store data for later retrieval
- **Caches:** Remember expensive operation results to speed up reads
- **Search Indexes:** Allow searching/filtering data by keywords
- **Stream Processing:** Send messages to other processes asynchronously
- **Batch Processing:** Periodically crunch large amounts of accumulated data

---

## Why "Data Systems" as an Umbrella Term?

**Blurring Boundaries:**
- Redis: Datastore used as message queue
- Apache Kafka: Message queue with database-like durability
- Traditional categories no longer fit neatly

**Modern Application Reality:**
- Single tools can't meet all data processing/storage needs
- Work broken down into tasks for different specialized tools
- Application code stitches tools together
- Example: Main database + Memcached cache + Elasticsearch search index
  - Application code keeps them in sync

**You become a data system designer** when you combine tools to create a composite system with specific guarantees (e.g., cache correctly invalidated on writes).

---

## Three Core Concerns of Software Systems

### 1. Reliability
**Definition:** System continues to work correctly even when things go wrong

**"Working Correctly" Means:**
- Performs expected function
- Tolerates user mistakes/unexpected usage
- Good enough performance for use case
- Prevents unauthorized access

**Key Terms:**
- **Fault:** One component deviating from its spec
- **Failure:** Entire system stops providing required service
- **Fault-Tolerant/Resilient:** System that anticipates and copes with faults

**Important Distinction:**
- Fault ≠ Failure
- Goal: Design fault-tolerance to prevent faults from causing failures
- Can't prevent all faults, so design to handle them

**Deliberate Fault Injection:**
- Increase fault rate intentionally (e.g., Netflix Chaos Monkey)
- Ensures fault-tolerance is exercised and tested
- Builds confidence in handling natural faults

---

### Types of Faults

#### Hardware Faults
**Examples:**
- Hard disk crashes
- RAM failures
- Power outages
- Network cable unplugged

**Statistics:**
- Hard disk MTTF (Mean Time To Failure): 10-50 years
- Storage cluster with 10,000 disks: expect ~1 disk failure per day

**Traditional Approach:**
- Add redundancy: RAID, dual power supplies, hot-swappable CPUs
- Batteries and diesel generators for backup power
- Keeps machines running for years

**Modern Evolution:**
- More machines = proportionally more hardware faults
- Cloud platforms (AWS) prioritize flexibility over single-machine reliability
- VMs can become unavailable without warning
- **Shift:** Software fault-tolerance techniques over/alongside hardware redundancy

**Benefits of Software Fault-Tolerance:**
- Can tolerate entire machine loss
- Rolling upgrades without downtime
- Patch one node at a time

#### Software Errors
**Characteristics:**
- Systematic errors within the system
- Correlated across nodes (not random/independent)
- Harder to anticipate
- Cause more failures than hardware faults

**Examples:**
- Bug causing all instances to crash on bad input (e.g., leap second bug 2012)
- Runaway process consuming shared resources (CPU, memory, disk, bandwidth)
- Service dependencies becoming slow/unresponsive/corrupted
- **Cascading failures:** Small fault triggers another fault, which triggers more

**Why They're Sneaky:**
- Often lie dormant for long time
- Triggered by unusual circumstances
- Reveal incorrect assumptions about environment

**Mitigation Strategies:**
- Careful thinking about assumptions and interactions
- Thorough testing
- Process isolation
- Allow processes to crash and restart
- Monitoring and analyzing system behavior
- Self-checking systems that verify guarantees

#### Human Errors
**Reality:**
- Configuration errors by operators = leading cause of outages
- Hardware faults only 10-25% of outages
- Humans are unreliable even with best intentions

**Making Systems Reliable Despite Humans:**

1. **Minimize Error Opportunities:**
   - Well-designed abstractions, APIs, admin interfaces
   - Make right thing easy, wrong thing hard
   - Balance: not too restrictive (people will work around)

2. **Decouple Mistakes from Failures:**
   - Sandbox environments for exploration
   - Use real data without affecting real users

3. **Thorough Testing:**
   - Unit tests to whole-system integration tests
   - Automated testing for corner cases
   - Manual tests

4. **Easy Recovery:**
   - Fast rollback of config changes
   - Gradual code rollout (limit blast radius)
   - Tools to recompute data

5. **Detailed Monitoring (Telemetry):**
   - Performance metrics and error rates
   - Early warning signals
   - Check assumptions/constraints
   - Invaluable for diagnosing issues

6. **Good Management & Training**

---

### 2. Scalability

**Definition:** System's ability to cope with increased load

**Important:** Not a binary label ("X is scalable" is meaningless)

**Right Questions:**
- "If system grows in particular way, what are options for coping?"
- "How can we add resources to handle additional load?"

---

## Describing Load: Load Parameters

**What are Load Parameters?**
- Numbers that describe current load on system
- Enable discussions about growth

**Examples:**
- Requests per second to web server
- Ratio of reads to writes in database
- Simultaneously active users in chat room
- Hit rate on cache
- **Key:** Average case vs. bottleneck from extreme cases

---

## Case Study: Twitter Scalability (Nov 2012)

### The Challenge: Fan-out

**Load Parameters:**
- **Post tweet:** 4.6k req/sec average, 12k req/sec peak
- **Home timeline:** 300k req/sec

**Core Problem:**
- Not raw tweet volume (12k writes/sec is manageable)
- **Fan-out:** Each user follows many people, each user followed by many people

**Fan-out Definition:**
> Borrowed from electronic engineering: number of logic gate inputs attached to another gate's output. In transaction processing: number of requests to other services needed to serve one incoming request.

---

### Approach 1: Query on Read (Original Twitter)

**How It Works:**
1. Store tweet in global tweets collection
2. When user requests timeline:
   - Look up who they follow
   - Find all tweets from those users
   - Merge and sort by time

**SQL Implementation:**
```sql
SELECT tweets.*, users.* 
FROM tweets
  JOIN users ON tweets.sender_id = users.id
  JOIN follows ON follows.followee_id = users.id
WHERE follows.follower_id = current_user
```

**SQL Evaluation Order:**
- NOT top-to-bottom!
- Database optimizer rewrites for efficiency (bottom-up)
- Typical execution:
  1. `WHERE` clause first (filter to your follows)
  2. JOIN with follows table (get your 1,000 followed users)
  3. JOIN with tweets table (find their tweets - expensive!)
  4. Sort and return

**The Problem:**
- 300k timeline reads/sec
- Each requires expensive multi-table JOINs
- Scan massive tweets table (billions of tweets globally)
- Find tweets from 1,000+ users you follow
- Every query is different (different follow lists)
- **Database couldn't handle this load**

**Architecture:**
```
Tables:
- tweets (all tweets from everyone)
- users (user information)
- follows (who follows whom)

Flow:
User refreshes → Query all tables → JOIN → Sort → Display
```

---

### Approach 2: Pre-compute on Write (Twitter's Solution)

**Core Concept:** Maintain cache for each user's home timeline (like a mailbox)

**How It Works:**

**Write Time:**
1. User posts tweet
2. Look up all their followers
3. Insert tweet into each follower's timeline cache

**Read Time:**
1. User refreshes timeline
2. Fetch their pre-computed list
3. Display immediately

**Why It's Better:**
- **Reads >> Writes:** 300k reads vs 4.6k writes per second
- Do work once at write time instead of 300k times at read time
- Reads become trivial lookups (no JOINs, no scanning)

**The Math:**
- 4.6k tweets/sec × 75 avg followers = 345k cache writes/sec
- But 300k reads become super cheap
- **Trade:** More work at write time, less at read time

**Architecture:**
```
Tables:
- tweets (source of truth)
- users (user information)  
- follows (who follows whom)
- timeline_cache (pre-computed timelines) ← KEY DIFFERENCE

Write Flow:
Alice posts "Hello world"
    ↓
Save to tweets table
    ↓
Look up Alice's 75 followers
    ↓
INSERT into each follower's timeline_cache:
  - INSERT (you, tweet_1, timestamp)
  - INSERT (dave, tweet_1, timestamp)
  - INSERT (sarah, tweet_1, timestamp)
  ... (75 inserts)

Read Flow:
You refresh
    ↓
SELECT * FROM timeline_cache
WHERE user_id = 'you'
ORDER BY timestamp DESC
LIMIT 100
    ↓
Display your pre-made list
```

---

### The Celebrity Problem (Downside of Approach 2)

**The Issue:**
- Average user: 75 followers → 75 writes ✅
- **Celebrity: 30+ million followers → 30+ million writes** ❌

**Problems:**
1. **Write Amplification:** One tweet = 30M writes
2. **Time Constraint:** Twitter wants < 5 second delivery
3. **System Overload:** Celebrity tweets overwhelm system
4. **Wasted Resources:** Many followers may never see tweet (inactive)

**Key Load Parameter:**
- **Distribution of followers per user** (weighted by tweet frequency)
- Follower count × tweet frequency = total fan-out load
- Captures both average and extreme cases

---

### The Hybrid Approach (Current Twitter)

**Strategy:** Different treatment based on follower count

**Regular Users (< threshold):**
- Use Approach 2 (fan-out on write)
- Pre-compute into followers' timeline caches

**Celebrities (30M+ followers):**
- Use Approach 1 (fan-out on read)
- DON'T pre-compute
- Fetch separately when users refresh

**Timeline Refresh Flow:**
```
You click refresh
    ↓
1. Fetch timeline_cache
   (pre-computed tweets from regular users)
    ↓
2. Check: Follow any celebrities?
   Yes → Taylor Swift, Elon Musk
    ↓
3. Query celebrity tweets separately:
   SELECT * FROM tweets
   WHERE user_id IN ('taylor_swift', 'elon_musk')
   ORDER BY timestamp DESC
   LIMIT 50
    ↓
4. MERGE both sets by timestamp
    ↓
5. Display combined timeline
```

**Why This Works:**

**Celebrity Posts (Write Time):**
- Pure Approach 2: 30M writes ❌
- Hybrid: 1 write to tweets table ✅

**You Refresh (Read Time):**
- 95% pre-computed (instant)
- 5% celebrity tweets (small query)
- Merge (milliseconds)
- **Total: ~5ms**

**The Key Insight:**
- **Reads are MUCH cheaper than writes** in databases
- Reads can be cached, parallelized, replicated
- Writes need disk updates, consistency maintenance
- Better: 1M distributed reads over time vs 30M writes at once
- Distributes load over time instead of sudden spike

---

## Describing Performance (Page 13)

**Two Key Questions:**
1. When load increases (resources unchanged): How is performance affected?
2. When load increases: How much more resources needed to maintain performance?

**Different Metrics for Different Systems:**

### Batch Processing (e.g., Hadoop)
- **Throughput:** Records processed per second
- **Job Duration:** Total time to run job on dataset
- Note: Ideal runtime = dataset size ÷ throughput
- Reality: Often longer due to skew and waiting for slowest task

### Online Systems
- **Response Time:** Time from client request to receiving response
- More important than raw throughput

**Response Time vs Latency:**
- **Response Time:** What client sees (includes service time + network delays + queueing)
- **Latency:** Duration request waits to be handled (latent, awaiting service)
- Often used synonymously but NOT the same!

**Response Time as Distribution:**
- Not a single number
- Varies even for identical requests
- Think of it as distribution of values
- Some requests fast, some slow (outliers exist)

---

## Key Terminology Summary

| Term | Definition |
|------|------------|
| **Data-Intensive** | Applications where data (amount, complexity, speed) is primary challenge |
| **Reliability** | Continuing to work correctly even when things go wrong |
| **Fault** | Component deviating from spec |
| **Failure** | System stops providing required service |
| **Fault-Tolerant** | System that anticipates and copes with faults |
| **MTTF** | Mean Time To Failure |
| **Cascading Failure** | Small fault triggers more faults in chain reaction |
| **Telemetry** | Detailed monitoring (borrowed from rocket science) |
| **Scalability** | Ability to cope with increased load |
| **Load Parameters** | Numbers describing current system load |
| **Fan-out** | Number of downstream operations from one upstream operation |
| **Throughput** | Records processed per second (batch systems) |
| **Response Time** | Client request to response duration |
| **Latency** | Duration request waits to be handled |
| **Write Amplification** | One logical write → multiple physical writes |
| **Pre-compute** | Computing results ahead of time and storing them |
| **Materialized View** | Pre-computed query result stored for fast access |

---

## Key Takeaways

### On System Design
1. **No Silver Bullets:** Every design choice involves trade-offs
2. **Context Matters:** Best choice depends on your specific load characteristics
3. **Measure What Matters:** Choose load parameters that capture your bottlenecks
4. **Plan for Extremes:** Average case ≠ worst case (celebrity problem)

### On Reliability
1. **Faults Will Happen:** Design for fault-tolerance, not fault prevention
2. **Layer Your Defenses:** Hardware redundancy + software fault-tolerance + human error mitigation
3. **Test Deliberately:** Chaos engineering builds confidence
4. **Monitor Everything:** You can't fix what you can't measure

### On Scalability
1. **One Size Doesn't Fit All:** Different users/use cases may need different strategies (hybrid approach)
2. **Optimize for Your Actual Load:** Twitter optimized for read-heavy workload
3. **Read vs Write Trade-offs:** Consider the ratio when designing
4. **Distribution Matters:** Don't just look at averages, examine the full distribution

### Twitter Case Study Lessons
1. **Fan-out is real:** Multiply effect of one action across many users
2. **Pre-computation wins** when reads >> writes
3. **Hybrid approaches** can get best of both worlds
4. **Load parameters must capture extremes** (celebrity followers)
5. **Database optimization matters:** JOINs vs simple lookups = huge difference

---

## Questions to Consider

When designing a data system:
1. What are my load parameters? (requests/sec, read/write ratio, etc.)
2. What's the distribution? (average vs extreme cases)
3. Where are my bottlenecks? (reads or writes?)
4. How can I pre-compute expensive operations?
5. Do I need different strategies for different user segments?
6. What faults am I designing for?
7. How will I monitor and debug in production?

---

## Further Reading Topics (Mentioned in Text)

- Chapter 4: Rolling upgrades and evolvability
- Chapter 12: Advanced Twitter architecture details
- Figure 1-1: Composite data system architecture
- Figure 1-2: Twitter relational schema
- Figure 1-3: Twitter data pipeline
- Netflix Chaos Monkey: Deliberate fault injection