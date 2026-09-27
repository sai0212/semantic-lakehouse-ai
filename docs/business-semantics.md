---

document: "Business Semantics"
version: "0.1.0"
status: "Draft"
last_updated: "2026-09-27"
author: "Your Name"
description: "Business definitions, metrics, terminology, and analytical rules for the Semantic Lakehouse AI project."
----------------------------------------------------------------------------------------------------------------------

# Business Semantics

## 1. Purpose

This document defines the business meaning of the data model used by the
Semantic Lakehouse AI project.

The purpose is to explicitly capture business terminology, metric definitions,
calculation rules, synonyms, and analytical conventions that cannot be reliably
inferred from the physical data model alone.

This document serves as the human-readable semantic specification for the
project and will later inform the machine-readable Apache Ossie semantic model.

---

# 2. Business Domain

## 2.1 Domain

Fictional e-commerce / retail business.

The business sells products to customers through physical stores.

## 2.2 Core Business Processes

The model represents the following business processes:

1. Customer acquisition
2. Product sales
3. Order processing
4. Refunds
5. Revenue analysis

---

# 3. Business Vocabulary

| Business Term | Definition                                        | Related Data  |
| ------------- | ------------------------------------------------- | ------------- |
| Customer      | A person or organization that purchases products. | `customers`   |
| Product       | An item available for purchase.                   | `products`    |
| Store         | A physical location associated with an order.     | `stores`      |
| Order         | A customer purchase transaction.                  | `orders`      |
| Order Item    | An individual product included in an order.       | `order_items` |
| Refund        | Money returned to a customer against an order.    | `refunds`     |

---

# 4. Order Semantics

## 4.1 Order

An order represents a customer purchase transaction.

The lifecycle of an order is represented by `orders.status`.

Valid order statuses are:

* `completed`
* `cancelled`
* `pending`

Refund information is **not represented by order status**.

Refund information must be derived exclusively from the `refunds` table.

---

## 4.2 Completed Order

An order is considered a completed order when:

```text
orders.status = 'completed'
```

Only completed orders contribute to completed-order metrics and sales-related
metrics unless explicitly stated otherwise.

---

## 4.3 Cancelled Order

An order with:

```text
orders.status = 'cancelled'
```

is not considered a completed order and does not contribute to revenue.

---

## 4.4 Pending Order

An order with:

```text
orders.status = 'pending'
```

has not been completed and does not contribute to revenue.

---

# 5. Refund Semantics

## 5.1 Refund

A refund represents a monetary return against an order.

Refund information is stored exclusively in the `refunds` table.

An order can have:

* zero refunds
* one refund
* multiple refund events

The existence of one or more refund records indicates that the order has been
refunded to some extent.

---

## 5.2 Refund Amount

Total refund amount for an order is:

```text
SUM(refunds.refund_amount)
```

grouped by `refunds.order_id`.

---

## 5.3 Partially Refunded Order

An order is considered partially refunded when:

```text
total_refunded > 0
```

and:

```text
total_refunded < eligible_order_value
```

The exact definition of `eligible_order_value` must follow the revenue
calculation rules defined in this document.

---

## 5.4 Fully Refunded Order

An order is considered fully refunded when:

```text
total_refunded >= eligible_order_value
```

The order's original `orders.status` remains unchanged.

For example, a completed order that is fully refunded remains:

```text
orders.status = 'completed'
```

The refund state is derived independently from the `refunds` table.

---

# 6. Revenue Semantics

## 6.1 Revenue

Revenue represents the net value of completed sales after discounts and
applicable refunds.

Only completed orders contribute to revenue.

### Order Item Value

For each order item:

```text
gross_value =
    quantity × unit_price
```

### Discounted Value

```text
discounted_value =
    quantity × unit_price × (1 - discount_pct)
```

### Net Revenue

Conceptually:

```text
revenue =
    SUM(discounted_value for completed orders)
    - applicable refunds
```

The refund amount is sourced from the `refunds` table.

---

## 6.2 Gross Sales

Gross sales represent the value of products before discounts and refunds.

```text
gross_sales =
    SUM(quantity × unit_price)
```

Only completed orders are included.

---

## 6.3 Discounted Sales

Discounted sales represent product value after discounts but before refunds.

```text
discounted_sales =
    SUM(
        quantity × unit_price × (1 - discount_pct)
    )
```

Only completed orders are included.

---

# 7. Core Metrics

## 7.1 Revenue

**Definition**

Net value of completed sales after discounts and refunds.

**Primary Data**

* `orders`
* `order_items`
* `refunds`

**Default Filter**

```text
orders.status = 'completed'
```

**Synonyms**

* Revenue
* Net revenue
* Sales revenue

---

## 7.2 Gross Sales

**Definition**

Value of completed order items before discounts and refunds.

**Formula**

```text
SUM(quantity × unit_price)
```

**Synonyms**

* Gross sales
* Gross sales value

---

## 7.3 Units Sold

**Definition**

Total quantity of products sold through completed orders.

**Formula**

```text
SUM(order_items.quantity)
```

**Default Filter**

```text
orders.status = 'completed'
```

**Synonyms**

* Units sold
* Units
* Quantity sold

---

## 7.4 Completed Orders

**Definition**

Number of completed customer orders.

**Formula**

```text
COUNT(DISTINCT orders.order_id)
```

**Filter**

```text
orders.status = 'completed'
```

---

## 7.5 Average Order Value

**Definition**

Average net revenue generated per completed order.

**Formula**

```text
revenue / completed_orders
```

**Synonyms**

* AOV
* Average order value

---

## 7.6 Refund Amount

**Definition**

Total amount returned to customers through refund events.

**Formula**

```text
SUM(refunds.refund_amount)
```

**Primary Data**

`refunds`

---

## 7.7 Customer Lifetime Value

**Definition**

Total net revenue attributed to a customer across their completed orders.

**Formula**

```text
SUM(net revenue)
GROUP BY customer
```

**Synonyms**

* Customer lifetime value
* CLV
* LTV
* Lifetime value

---

# 8. Business Dimensions

## 8.1 Customer Segment

Valid customer segments:

* `Consumer`
* `SMB`
* `Enterprise`

### Definitions

| Segment    | Meaning                        |
| ---------- | ------------------------------ |
| Consumer   | Individual customer            |
| SMB        | Small or medium-sized business |
| Enterprise | Large business customer        |

---

## 8.2 Region

Valid regions:

* `North`
* `South`
* `East`
* `West`
* `Central`

There are two distinct regional concepts:

* Customer region: `customers.region`
* Store region: `stores.region`

These must not be treated as interchangeable.

If a question asks for "revenue by region" without additional context,
the semantic layer must eventually define which regional concept is intended.

This is intentionally retained as an open semantic decision.

---

## 8.3 Product Category

Valid product categories:

* `Electronics`
* `Furniture`
* `Office Supplies`
* `Software`
* `Accessories`

---

# 9. Time Semantics

## 9.1 Order Date

`orders.order_date` represents the date on which the order was placed.

This is the default date for sales and revenue analysis.

---

## 9.2 Refund Date

`refunds.refund_date` represents the date on which a refund was issued.

Refund analysis should use the refund date unless the question explicitly asks
for refunds associated with orders placed during a particular period.

---

## 9.3 Default Time Interpretation

| Question            | Default Date          |
| ------------------- | --------------------- |
| Revenue by month    | `orders.order_date`   |
| Sales by month      | `orders.order_date`   |
| Orders by month     | `orders.order_date`   |
| Units sold by month | `orders.order_date`   |
| Refunds by month    | `refunds.refund_date` |

---

# 10. Default Analytical Rules

| Scenario         | Default Interpretation                      |
| ---------------- | ------------------------------------------- |
| Revenue          | Completed sales after discounts and refunds |
| Orders           | Completed orders                            |
| Units sold       | Quantity from completed order items         |
| Refunds          | Refund events from `refunds`                |
| Refund amount    | Sum of `refunds.refund_amount`              |
| Customer value   | Net revenue from completed orders           |
| Revenue by month | Group using `orders.order_date`             |
| Refunds by month | Group using `refunds.refund_date`           |

---

# 11. Synonyms & Natural Language

The semantic layer should recognize common business terminology.

| User Term           | Intended Concept        |
| ------------------- | ----------------------- |
| revenue             | Revenue                 |
| net revenue         | Revenue                 |
| sales revenue       | Revenue                 |
| orders              | Completed orders        |
| completed orders    | Completed orders        |
| units               | Units sold              |
| units sold          | Units sold              |
| quantity sold       | Units sold              |
| AOV                 | Average Order Value     |
| average order value | Average Order Value     |
| LTV                 | Customer Lifetime Value |
| CLV                 | Customer Lifetime Value |
| lifetime value      | Customer Lifetime Value |
| refunds             | Refund events           |
| refund amount       | Total refund amount     |

---

# 12. Ambiguous Business Terms

Some natural-language terms intentionally have multiple possible
interpretations.

| Term      | Possible Interpretation                          |
| --------- | ------------------------------------------------ |
| Sales     | Revenue, gross sales, or discounted sales        |
| Customers | All customers or customers with completed orders |
| Orders    | All orders or completed orders                   |
| Region    | Customer region or store region                  |
| Value     | Revenue, gross sales, or customer lifetime value |

The semantic layer should avoid silently resolving these ambiguities when
the user's question does not provide sufficient context.

---

# 13. Metric Aggregation Rules

## Orders

Orders must be counted at the order grain.

```text
COUNT(DISTINCT order_id)
```

Do not count `order_items` rows as orders.

---

## Units Sold

Units sold must be calculated from:

```text
SUM(order_items.quantity)
```

for completed orders.

---

## Revenue

Revenue is calculated from completed order items and applicable refunds.

---

## Refunds

Refunds must be aggregated from the `refunds` table.

```text
SUM(refunds.refund_amount)
```

---

# 14. Business Rules

### Rule 1 — Order Status

Valid order statuses are:

```text
completed
cancelled
pending
```

There is no `refunded` order status.

---

### Rule 2 — Refund Source of Truth

All refund information must be derived from the `refunds` table.

Do not infer refund state from `orders.status`.

---

### Rule 3 — Completed Orders

Only orders with:

```text
orders.status = 'completed'
```

contribute to completed-order metrics and revenue.

---

### Rule 4 — Cancelled Orders

Cancelled orders contribute no revenue.

---

### Rule 5 — Pending Orders

Pending orders contribute no revenue.

---

### Rule 6 — Historical Price

`order_items.unit_price` represents the transaction price at the time of
purchase.

`products.current_unit_price` represents the current product price.

Historical revenue calculations must use:

```text
order_items.unit_price
```

and not:

```text
products.current_unit_price
```

---

### Rule 7 — Refunds Reduce Net Revenue

Refund amounts reduce net revenue associated with completed sales.

---

# 15. Analytical Examples

## Example 1 — Revenue by Product Category

**Question**

> Which product categories generated the most revenue?

**Interpretation**

* Metric: Revenue
* Dimension: Product category
* Filter: Completed orders
* Join path:

```text
orders
  ↓
order_items
  ↓
products
```

---

## Example 2 — Completed Orders

**Question**

> How many orders did we have last month?

**Interpretation**

* Metric: Completed Orders
* Date: `orders.order_date`
* Filter: `orders.status = 'completed'`
* Aggregation:

```text
COUNT(DISTINCT order_id)
```

---

## Example 3 — Refunds

**Question**

> How much money was refunded last month?

**Interpretation**

* Metric: Refund Amount
* Date: `refunds.refund_date`
* Source: `refunds`
* Aggregation:

```text
SUM(refund_amount)
```

---

## Example 4 — Customer Lifetime Value

**Question**

> Who are our top 10 customers by lifetime value?

**Interpretation**

* Metric: Customer Lifetime Value
* Dimension: Customer
* Filter: Completed orders
* Aggregate net revenue by customer
* Sort by lifetime value descending
* Return top 10

---

# 16. Open Semantic Decisions

The following decisions remain intentionally unresolved and should be finalized
before the semantic model is implemented.

| Topic    | Question                                                       | Status |
| -------- | -------------------------------------------------------------- | ------ |
| Revenue  | How should refunds spanning multiple order items be allocated? | Open   |
| Region   | Should "region" default to customer or store region?           | Open   |
| Sales    | Should "sales" default to revenue or remain ambiguous?         | Open   |
| Customer | Does "customer" include customers with no completed orders?    | Open   |
| AOV      | Should refunds affect the numerator of AOV?                    | Open   |
| Quarter  | How should "last quarter" be defined?                          | Open   |

---

# 17. Semantic Design Principles

The semantic layer should:

1. Prefer explicit business definitions over inferred meanings.
2. Preserve the grain of the underlying data.
3. Distinguish metrics from dimensions.
4. Distinguish order dates from refund dates.
5. Treat `refunds` as the source of truth for refund information.
6. Avoid silently resolving ambiguous terminology.
7. Make metric calculations reproducible.
8. Provide useful business synonyms.
9. Keep unresolved semantic decisions explicit.
10. Separate physical data structure from business meaning.

---

# 18. Relationship to the Machine-Readable Semantic Model

This document is the human-readable business semantic specification.

The future Apache Ossie semantic model will translate these concepts into a
machine-readable representation containing concepts such as:

* Metrics
* Dimensions
* Relationships
* Business definitions
* Synonyms
* Filters
* AI context
* Examples

The semantic runtime will consume that representation and provide appropriate
context to the LLM during analytical query planning.

---

# 19. Change Log

| Version | Date       | Author    | Description                             |
| ------- | ---------- | --------- | --------------------------------------- |
| `0.1.0` | 2026-09-27 | Your Name | Initial business semantic specification |
