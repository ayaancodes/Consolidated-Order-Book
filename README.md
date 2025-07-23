
# Consolidated Multi-Exchange Order Book Engine

## Overview

This project implements a **real-time, consolidated order book** aggregator for multiple trading exchanges, built in response to a proprietary specification. It consumes a sequence of market data feed updates from individual exchanges and maintains a unified, sorted order book that reflects the best bid/offer levels across the market.

Updates from individual exchanges are processed incrementally, with each action triggering a corresponding update to the consolidated book ("Exchange C").

---

## 📈 Key Features

- 📊 **Multi-exchange book synchronization**  
  Supports multiple independent order books (e.g., Exchange A, B) while maintaining a consolidated book (Exchange C) in real-time.

- ⚡ **Low-latency event processing model**  
  Efficiently handles `NEW`, `UPDATE`, and `DELETE` actions with index-aware shifting to reflect accurate price levels.

- 🧠 **Order book logic designed for consistency and determinism**  
  Ensures that quantities and price levels are updated atomically, and shifts in order depth are accurately propagated.

- 📤 **STDIN/STDOUT data pipeline**  
  Compatible with Unix-like streaming I/O:  
  `./market_feed < input.txt > output.txt`

---

## 🔧 Data Format

Each input line follows the schema:  
```
ExchangeID,BookIndex,UpdateAction,Side,Price,Quantity
```

- `ExchangeID`: A, B (input); C (output)  
- `BookIndex`: Index of book entry (0 = best price)  
- `UpdateAction`: NEW, UPDATE, DELETE  
- `Side`: BID or OFFER  
- `Price`: Integer > 0 (NEW only)  
- `Quantity`: Integer > 0 (NEW or UPDATE only)  

---

## 📚 Architecture

### Core Components

- **Exchange Book Handler:**  
  Maintains independent books per exchange, indexed by side and sorted by price.

- **Book Aggregator:**  
  Recalculates the consolidated book in response to each change in the input books, updating quantity at shared price levels.

- **Change Engine:**  
  Deduces the minimal set of actions (`NEW`, `UPDATE`, `DELETE`) needed to update the consolidated book from its current state.

- **Price-Level Normalizer:**  
  Ensures book indices remain gapless, while respecting price-time priority and preventing bid/offer crossover.

---

## 🧪 Sample I/O

**Input (STDIN):**
```
A,0,NEW,BID,100,75  
B,0,NEW,BID,99,100  
A,0,NEW,OFFER,102,88
```

**Output (STDOUT):**
```
C,0,NEW,BID,100,75  
C,1,NEW,BID,99,100  
C,0,NEW,OFFER,102,88
```

---

## 🚀 How to Run

1. Clone this repo and compile the program (if applicable):
```bash
g++ market_feed.cpp -o market_feed
```

2. Run on a sample input:
```bash
./market_feed < input.txt > output.txt
```

---

## 🛠️ Technologies Used

- **C++ STL** (or Python standard libs) for data structure efficiency  
- **Custom vector-based and map-based books** for sorted price/quantity storage  
- Designed to handle thousands of updates per second with minimal memory churn

---

## 🧠 Design Considerations

- Maintains **price-time priority**: inserts at BookIndex and shifts others as needed  
- Handles **multi-book updates** while ensuring atomicity in consolidation  
- Prevents bid-offer **crossing conditions** and maintains side isolation  
- Designed with extensibility in mind (e.g., support for partial fills, depth-of-book visualizations)

---

## 🧩 Possible Extensions

- Add support for **timestamped updates** and latency metrics  
- Integrate **order matching logic** to simulate trade execution  
- Visualize book evolution using **Plotly** or **matplotlib**  
- Export snapshots to **Parquet/CSV** for downstream analysis

---

## 🙌 Author

Built by Ayaan Munshi as part of a trading system design challenge.  
This project reflects a hands-on implementation of real-time market data processing and the foundations of order book engineering.
