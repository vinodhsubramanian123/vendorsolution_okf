# 03. Engineering Ontology & Information Model

---

# 1. Purpose

This blueprint defines **how IKP understands engineering knowledge**.

Every engineering source, regardless of vendor, format or technology, SHALL ultimately be converted into a common canonical engineering model.

This ontology becomes the common language used by every implementation component.

Without this ontology, engineering reasoning, validation and learning are impossible.

---

# 2. Engineering Philosophy

IKP does not organize documents.

IKP organizes engineering knowledge.

The implementation SHALL identify engineering concepts independent of how they are represented inside source documents.

The same engineering concept appearing in:

* PDF
* API
* Portal
* Spreadsheet
* Markdown
* Human Notes

SHALL become the same canonical engineering object.

---

# 3. Canonical Engineering Hierarchy

Every engineering object SHALL belong to a well-defined hierarchy.

```text
Engineering Domain

↓

Solution Domain

↓

Solution Category

↓

Vendor

↓

Product Family

↓

Generation

↓

Platform

↓

Variant

↓

Configuration

↓

Component

↓

SKU / Part Number
```

Example

```text
Infrastructure

↓

Storage

↓

Block Storage

↓

HPE

↓

Alletra

↓

6000

↓

Alletra 6050

↓

Base Configuration

↓

Controller

↓

Pxxxx-xxxxx
```

The implementation SHALL preserve hierarchy while allowing relationships across hierarchy levels.

---

# 4. Canonical Engineering Objects

The implementation SHALL recognize the following minimum engineering object types.

## Solution Domain

Examples

* Compute
* Storage
* Networking
* Virtualization
* Backup
* AI
* Security
* Cloud

---

## Product Family

Examples

* ProLiant
* Alletra
* Primera
* Synergy
* Aruba

---

## Generation

Examples

* Gen10
* Gen11
* 6000 Series
* 9000 Series

---

## Platform

Represents a commercially available product platform.

Example

DL380 Gen11

Alletra 6050

---

## Variant

Represents a specific implementation or model.

Examples

* SFF
* LFF
* GPU Variant
* NVMe Variant

---

## Configuration

Represents a buildable engineering configuration.

Configurations SHALL reference engineering objects.

Configurations SHALL NOT duplicate engineering knowledge.

---

## Component

Examples

* CPU
* Controller
* Drive
* DIMM
* GPU
* NIC
* Power Supply
* Fan
* Rail Kit
* Cable
* Riser
* Optics/Transceiver
* License

Components SHALL exist independently of products.

Components SHALL declare a **Category** and a **Subcategory** to support high-granularity validation (e.g. Category: `Infrastructure`, Subcategory: `Cable` or `Riser`). Vendor catalogues typically expose 25+ categories which must be accurately mapped.

---

## TopologyNode / SlotMapping

Represents spatial or topological connectivity within a product (e.g. Mezzanine to Bay mappings).
Topology mappings SHALL be treated as first-class engineering objects.

---

## SKU

Represents commercially orderable items.

A SKU SHALL reference engineering knowledge.

Engineering knowledge SHALL NOT depend upon a SKU.

---

# 5. Engineering Attributes

Every engineering object SHALL expose structured attributes.

Examples include:

Identity

Classification

Vendor

Generation

Lifecycle

Capabilities

Performance

Capacity

Latency

Read Profile

Write Profile

Expansion

Protocol

Interface

Power

Cooling

Dimensions

Firmware

Software

Licensing

Availability

Support Status

Lifecycle Status

Every attribute SHALL be typed.

Free-text SHALL be minimized.

---

# 6. Metadata Strategy

Metadata exists to reduce engineering search space before reasoning begins.

Metadata SHALL support rapid discovery of relevant engineering knowledge.

Examples include:

* Vendor
* Solution Domain
* Product Family
* Generation
* Platform
* Variant
* Component Types
* Protocols
* Workloads
* Performance Profile
* Capacity Profile
* AI Ready
* GPU Ready
* SAP Certified
* VMware Certified
* Kubernetes Ready
* Encryption Support
* Replication Support
* Lifecycle Status

Metadata SHALL guide reasoning.

Metadata SHALL NOT replace reasoning.

---

# 7. Engineering Relationships

Relationships SHALL be first-class engineering objects.

Minimum relationship types include:

* Contains
* Uses
* Requires
* Depends On
* Compatible With
* Incompatible With
* Replaces
* Supersedes
* Supports
* Managed By
* Connected To
* Validated By
* Evidenced By
* Recommended With

Relationships SHALL preserve direction.

Relationships SHALL preserve evidence.

Relationships SHALL remain independently versioned.

---

# 8. Engineering Rules

Rules SHALL exist independently from products.

Rule categories include:

* Static Rules
* Dynamic Rules
* Validation Rules
* Dependency Rules
* Compatibility Rules
* Configuration Rules
* Business Rules
* Human Approved Rules
* Derived Rules

Every rule SHALL expose:

* Identity
* Scope
* Severity
* Confidence
* Applicable Objects
* Trigger Conditions
* Expected Outcome
* Supporting Evidence
* Version

---

# 9. Engineering Constraints

Constraints SHALL represent engineering limitations.

Examples include:

* Maximum Controllers
* Maximum Drives
* Maximum Memory
* Maximum Power
* Firmware Requirements
* Software Requirements
* Licensing Requirements
* Slot Availability
* Chassis Restrictions

Constraints SHALL remain independent engineering objects.

---

# 10. Engineering Capabilities

Capabilities describe what an engineering object can provide.

Examples include:

* High Availability
* Replication
* Compression
* Deduplication
* NVMe Support
* Fibre Channel
* Ethernet
* GPU Acceleration
* AI Inference
* AI Training
* Database Optimization
* Backup
* Disaster Recovery
* Virtualization
* Kubernetes
* SAP HANA

Capabilities SHALL be reusable across vendors.

---

# 11. Engineering Workloads

Workloads represent customer intent rather than products.

Examples include:

* AI
* Machine Learning
* VMware
* VDI
* SAP
* Oracle
* SQL Server
* Backup
* Archive
* Object Storage
* File Services
* Video Surveillance
* HPC
* Analytics

Engineering reasoning SHALL begin from workloads whenever possible.

Products SHALL satisfy workloads.

Workloads SHALL never be derived from products.

---

# 12. Knowledge Integrity Principles

The implementation SHALL preserve engineering integrity.

Examples include:

* Never mix unrelated product families.
* Never inherit rules across incompatible generations.
* Never duplicate engineering rules.
* Never duplicate relationships.
* Never merge vendors without explicit mappings.
* Never lose engineering evidence.
* Never overwrite history.
* Never break canonical identities.

Knowledge integrity SHALL take precedence over convenience.

---

# 13. Ontology Evolution

The ontology SHALL remain extensible.

Adding:

* new vendors
* new technologies
* new workloads
* new engineering domains

SHALL require only ontology extensions.

Architectural redesign SHALL NOT be required.

---

# End of Blueprint 03