# List of CP Algorithms
## FENWICK TREE (Binary Indexed Tree)
### Introduction

To compute the sum of a subarray (range sum), we often use **Prefix Sum**. This approach precomputes the cumulative sum of the array in `O(n)` time, allowing for each range sum query to be answered in `O(1)`.

However, the prefix sum becomes inefficient when the array is dynamically updated. An update at index `j` requires recalculating all subsequent prefix sums, costing `O(n - j)` time. For `k` such updates, the total time becomes `O(k * (n - j))`, which, in the worst case (when `k = n` and `j = 0`), becomes `O(n²)` — highly inefficient.

This inefficiency arises because each index's prefix sum is dependent on previous elements, meaning any update can cascade through the entire array.

**Fenwick Tree** (or **Binary Indexed Tree**) overcomes this issue using a clever structure that minimizes dependencies and allows for efficient updates and queries.

### Fenwick Tree Construction

Despite its name, a Fenwick Tree is not a traditional tree with nodes and pointers. It is implemented using a **1-indexed array**, but for computation, we use a **0-indexed array of length `n+1`**, where the 0th index is a dummy (unused), enabling easier 1-based indexing.

### Intuition

Every integer can be uniquely expressed as a sum of powers of 2. This binary representation is the key idea behind Fenwick Trees.

| Decimal | Binary | Power of 2 Representation     |
|---------|--------|-------------------------------|
| 1       | 0001   | 2⁰                             |
| 2       | 0010   | 2¹                             |
| 3       | 0011   | 2¹ + 2⁰ = 2 + 1                |
| 4       | 0100   | 2²                             |
| 5       | 0101   | 2² + 2⁰ = 4 + 1                |
| 6       | 0110   | 2² + 2¹ = 4 + 2                |
| 7       | 0111   | 2² + 2¹ + 2⁰ = 4 + 2 + 1       |
| 8       | 1000   | 2³                             |

This breakdown helps identify the **range** each index in a Fenwick Tree is responsible for.

| Decimal | Power of 2        | Range             |
|---------|-------------------|-------------------|
| 0       | 0                 | dummy             |
| 1       | 2⁰                | [0, 0+2⁰) = [0, 1) = [0, 0]    |
| 2       | 2¹                | [0, 0+2¹) = [0, 2) = [0, 1]    |
| 3       | 2¹ + 2⁰           | [2¹, 2¹+2⁰) = [2, 3) = [2, 2]    |
| 4       | 2²                | [0, 0+2²) = [0, 4) = [0, 3]    |
| 5       | 2² + 2⁰           | [2², 2²+2⁰) = [4, 5) = [4, 4]    |
| 6       | 2² + 2¹           | [2², 2²+2¹) = [4, 6) = [4, 5]    |
| 7       | 2² + 2¹ + 2⁰      | [2²+2¹, 2²+2¹+2⁰) = [6, 7) = [6, 6]    |
| 8       | 2³                | [0, 0+2³) = [0, 8) = [0, 7]    |

### Fenwick Tree Range Representation

From any index, we can construct its range by **flipping bits from the least significant bit (LSB) upward** until the first set bit is flipped. Every new number formed this way represents a range:

Example (starting from index 0):

```
0000 → 0001 → [0, 1) → [0, 0]
     → 0010 → [0, 2) → [0, 1]
     → 0100 → [0, 4) → [0, 3]
     → 1000 → [0, 8) → [0, 7]
```

Similarly:

```
0010 → 0011 → [2, 3) → [2, 2]
0100 → 0101 → [4, 5) → [4, 4]
     → 0110 → [4, 6) → [4, 5]
0110 → 0111 → [6, 7) → [6, 6]
1000 → 1001 → [8, 9) → [8, 8]
     → 1010 → [8,10) → [8, 9]
     → 1100 → [8,12) → [8,11]
```

**Key Insight:** When an index `i` is updated in the original array, the update affects index `i+1` in the Fenwick Tree and all of its subsequent **Next Nodes**.

#### Next Nodes Table

| Node | Next Node |
|------|-----------|
| 1    | 2         |
| 2    | 4         |
| 3    | 4         |
| 4    | 8         |
| 5    | 6         |
| 6    | 8         |
| 7    | 8         |
| 8    | Out of bound |

### Querying with Fenwick Tree

To compute the **prefix sum** from index 0 to `i` in the original array, traverse **backwards** from index `i+1` in the Fenwick Tree to the root by repeatedly going to the **Parent Node**.

Example: `range_sum(0, 5)`:

```
Fenwick[6] + parent(6)
= Fenwick[6] + Fenwick[4] + parent(4)
= Fenwick[6] + Fenwick[4] + Fenwick[0]
= [4, 5] + [0, 3] + dummy
= [0, 5]
```

### Core Operations

#### 1. Get Next Node (for Update)

```text
Next_node(i) = i + (i & -i)
```

**Explanation:**
- `-i` is the two's complement of `i`
- `i & -i` isolates the lowest set bit
- Adding this gives the next affected index

**Example:**
```
i = 2 → Binary: 010
-i = 110 (2's complement)
i & -i = 010
Next node = 010 + 010 = 100 → 4
```

#### 2. Get Parent Node (for Query)

```text
Parent(i) = i - (i & -i)
```

### Visual Observation

| Node | Binary | Level |
|------|--------|-------|
| 0001 | 1      | L1    |
| 0010 | 2      | L1    |
| 0100 | 4      | L1    |
| 1000 | 8      | L1    |
| 0011 | 3      | L2    |
| 0101 | 5      | L2    |
| 0110 | 6      | L2    |
| 0111 | 7      | L3    |

**Observation:**
- A node at level `L` depends on prior nodes of the same level.
- The last node of level `L` depends on the adjacent node of level `L-1`.

### Building the Fenwick Tree

#### `update(index, delta)`

Updates the tree when the original array is modified.

Steps:
1. Compute `delta = new_value - old_value`
2. Go to index `i + 1` in the Fenwick Tree
3. Update current node: `fenwick[i] += delta`
4. Move to `i = i + (i & -i)` (next node)
5. Repeat until `i` exceeds array length

**Time Complexity:** `O(log n)`

#### Constructing the Tree

1. Initialize a Fenwick Tree array of length `n + 1` with zeros.
2. For each index in the original array, call the `update()` function.

#### Point Query: `sum(i)`

Computes sum of range `[0, i]`.

Steps:
1. Initialize `sum = 0`
2. Start at `i + 1`
3. Add `fenwick[i]` to sum
4. Move to `i = i - (i & -i)` (parent)
5. Repeat until `i` becomes 0

#### Range Query: `range_sum(i, j)`

To compute the sum of range `[i, j]`:

```python
range_sum(i, j) = point_query(j) - point_query(i - 1)
```
## Sieve of Eratosthenes
## Topological Sorting
## Union Find Disjoint Set
## Bipartite Graph Check
