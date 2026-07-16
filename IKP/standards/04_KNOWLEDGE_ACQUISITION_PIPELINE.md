# 04. Knowledge Acquisition Pipeline

---

# 1. Purpose

This blueprint defines how engineering knowledge enters IKP.

The objective is **not to ingest documents**.

The objective is to understand engineering information from heterogeneous sources and convert it into canonical engineering knowledge.

Every future source SHALL follow this pipeline.

---

# 2. Engineering Philosophy

Every source is evidence.

Every source contains engineering knowledge.

Every source contributes a Knowledge Delta.

No source owns the canonical knowledge.

Canonical knowledge is synthesized from all available evidence.

---

# 3. Supported Engineering Sources

The implementation SHALL support any source capable of contributing engineering knowledge.

### Phase 2: Metadata & Workload Indexing

The pipeline SHALL extract high-level customer requirements (Workloads) from the document introduction (e.g. AI, Virtualization, Database).
These workloads SHALL be vendor-agnostic and linked to the Platform via `SUPPORTS` relationships. This guarantees that customer requirements can be directly matched to hardware solutions regardless of the vendor catalogue.

### Phase 3: Logical Block Segmentation

* QuickSpecs
* Technical Guides
* User Guides
* Installation Guides
* Maintenance Guides
* Release Notes
* Compatibility Guides
* Best Practices
* Whitepapers

---

### Structured Data

* Excel
* CSV
* JSON
* XML
* APIs
* Databases

---

### Vendor Systems

* Configuration Portals
* Validation Portals
* Support Portals
* Firmware Catalogs
* Partner Portals

---

### Customer Sources

* BOQs
* Existing Configurations
* Requirement Documents
* Architecture Diagrams
* Discovery Data

---

### Operational Sources

* Firmware Inventories
* Health Reports
* Telemetry
* Monitoring
* Support Cases

---

### Human Sources

* Engineering Notes
* Manual Corrections
* Architecture Reviews
* Approved Decisions

---

# 4. Universal Acquisition Pipeline

Every source SHALL follow the same lifecycle.

```text
Acquire

↓

Identify Source

↓

Register

↓

Extract Metadata

↓

Determine Extraction Strategy

↓

Extract Engineering Objects

↓

Normalize

↓

Ontology Mapping

↓

Relationship Discovery

↓

Rule Discovery

↓

Knowledge Candidate

↓

Validation

↓

Knowledge Delta

↓

Canonical Repository

↓

Indexes

↓

Ready for Engineering Reasoning
```

Only the extraction strategy differs between source types.

---

# 5. Source Registration

Every source SHALL receive a permanent identity.

Minimum metadata includes:

* Source ID
* Source Type
* Vendor
* Product Family (if known)
* Product Generation (if known)
* Version
* Publication Date
* Language
* Acquisition Date
* Confidence
* Original File
* Processing Status

### 5.1 Deterministic External Versioning
The implementation SHALL NOT rely on hardcoded incremental version strings (e.g. `1.0`, `1.1`) for external vendor documents, as vendors do not expose version APIs consistently.

The implementation SHALL enforce a **3-Pillar Deterministic Versioning Strategy**:
1. **Cryptographic Hashing (Primary Fallback)**: The pipeline SHALL compute a SHA-256 hash of the binary file content. If any character changes, the hash guarantees a new version string.
2. **Embedded Metadata (Primary Identifier)**: The pipeline SHALL extract embedded compilation metadata from the source (e.g., PDF `modDate`).
3. **HTTP ETag / Last-Modified (Network Tier)**: The pipeline SHALL use standard HTTP cache headers to skip downloading unmodified external files.

The resulting deterministic string (e.g., `modDate_...` or `sha256_...`) SHALL become the `version`. The pipeline leverages this to skip heavy extraction entirely if the incoming version string exactly matches the active graph representation.

The implementation SHALL preserve the original source unchanged.

---

# 6. Engineering Metadata Extraction

Before parsing content, the implementation SHALL identify high-level engineering metadata.

Examples include:

* Vendor
* Solution Domain
* Product Category
* Product Family
* Generation
* Platform
* Variant
* Technologies
* Workloads
* Firmware
* Software
* Supported Protocols
* Lifecycle Status

This metadata is used to reduce the search space for downstream reasoning.

---

# 7. Engineering Object Extraction

The implementation SHALL extract engineering objects rather than paragraphs.

Minimum object categories include:

### Identity

* Product Names
* Component Names
* SKUs
* Part Numbers
* Models
* Versions

---

### Capabilities

Examples:

* Replication
* Encryption
* AI
* GPU
* Backup
* High Availability

---

### Components

Examples:

* Controller
* CPU
* GPU
* Memory
* Drive
* NIC
* PSU
* Fan
* Cable
* Chassis
* Rail Kit

---

### Attributes

Examples:

* Capacity
* Performance
* Ports
* Interfaces
* Read Speed
* Write Speed
* Bandwidth
* Latency
* Power
* Dimensions

---

### Rules

Examples:

* Maximum supported memory
* Minimum firmware
* Required controller
* Slot restrictions
* Licensing requirements

---

### Relationships

Examples:

* Requires
* Supports
* Replaces
* Compatible With
* Depends On

---

### Constraints

Examples:

* Maximum drives
* Maximum controllers
* Chassis limitations
* Firmware limitations
* Generation limitations

---

### Workloads

Examples:

* AI
* VMware
* SAP
* Backup
* HPC
* Database
* Archive
* File Services

---

# 8. Source-Specific Engineering Expectations

## PDF

Extract engineering meaning from:

* headings
* tables
* comparison tables
* specifications
* notes
* warnings
* footnotes
* diagrams
* images
* captions
* appendices

Ignore decorative content.

---

## BOQ

Extract:

* Customer intent
* Requested products
* Quantities
* SKUs
* Unknown products
* Missing information
* Constraints
* Budget indicators

The BOQ describes **what the customer wants**, not necessarily the correct solution.

---

## Vendor Configuration Portal

Extract:

* Selected products
* Configuration
* Dependencies
* Auto-selected components
* Unsupported combinations
* Missing components
* Recommendations

The portal exposes engineering relationships.

---

## Vendor Validation Portal

Extract:

* Errors
* Warnings
* Informational messages
* Recommended actions
* Validation logic
* Dependency failures
* Compatibility failures

Every validation result SHALL become a candidate for engineering learning.

---

## APIs

Extract structured engineering information directly.

Avoid unnecessary transformation.

---

## Excel / CSV

Infer engineering structure.

Examples:

* BOMs
* Compatibility matrices
* Performance tables
* Pricing
* Firmware matrices

---

## Human Feedback

Capture:

* Engineering decisions
* Corrections
* Exceptions
* Approved overrides
* Lessons learned

Human feedback SHALL always preserve author and rationale.

---

# 9. Knowledge Normalization

Engineering information from different vendors SHALL be normalized into canonical concepts.

Example:

Different vendor terms describing the same engineering capability SHALL map to a common canonical capability while preserving original terminology as evidence.

Normalization SHALL never discard vendor-specific information.

---

# 10. Knowledge Candidate Generation

The implementation SHALL combine extracted objects into knowledge candidates.

Knowledge candidates SHALL include:

* identity
* metadata
* attributes
* capabilities
* relationships
* rules
* constraints
* workloads
* evidence

Knowledge candidates SHALL NOT become canonical until validated.

---

# 11. Knowledge Delta Generation

Every processed source SHALL generate a Knowledge Delta.

A Knowledge Delta may contain:

* New products
* New SKUs
* Updated attributes
* Changed firmware
* New rules
* Updated rules
* New relationships
* New workloads
* Deprecated information
* Retired products

Only validated deltas SHALL update the canonical repository.

---

# 12. Acceptance Criteria

A compliant implementation SHALL:

* Ingest any supported engineering source.
* Automatically classify the source.
* Extract engineering objects instead of document text.
* Preserve source evidence.
* Normalize engineering terminology.
* Generate knowledge candidates.
* Produce Knowledge Deltas.
* Update canonical knowledge only after validation.
* Preserve history and traceability.

The output of this blueprint SHALL be validated engineering knowledge ready for reasoning, recommendation, and continuous learning.

---

# End of Blueprint 04