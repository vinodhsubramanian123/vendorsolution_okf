"""
IKP Canonical Engineering Ontology — Complete Model Definitions

Governs: Blueprint 03 (Engineering Ontology & Information Model)
         Blueprint 04 §5 (Source Registration)
         Blueprint 02 §7 (Knowledge Delta)
         Blueprint 05 §4 (Customer Requirements)
         Blueprint 05 §13 (Recommendation Output)

Every engineering concept in IKP is represented by one of these Pydantic models.
These models are the single source of truth for the in-memory graph, the OKF
Markdown persistence layer, and the LLM extraction pipeline.
"""

from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, timezone
import uuid


def _utcnow() -> datetime:
    """Return current UTC time (timezone-aware). Replaces deprecated datetime.utcnow()."""
    return datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------


class EngineeringObjectType(str, Enum):
    """Canonical hierarchy levels from Blueprint 03 §3."""

    SOLUTION_DOMAIN = "Solution Domain"
    SOLUTION_CATEGORY = "Solution Category"
    PRODUCT_FAMILY = "Product Family"
    GENERATION = "Generation"
    PLATFORM = "Platform"
    VARIANT = "Variant"
    CONFIGURATION = "Configuration"
    COMPONENT = "Component"
    SKU = "SKU"
    WORKLOAD = "Workload"
    CAPABILITY = "Capability"
    RULE = "Rule"
    CONSTRAINT = "Constraint"
    SLOT_MAPPING = "Slot Mapping"
    CATEGORY_LIMIT = "Category Limit"


class RelationshipType(str, Enum):
    """Minimum relationship types from Blueprint 03 §7."""

    CONTAINS = "Contains"
    USES = "Uses"
    REQUIRES = "Requires"
    DEPENDS_ON = "Depends On"
    COMPATIBLE_WITH = "Compatible With"
    INCOMPATIBLE_WITH = "Incompatible With"
    REPLACES = "Replaces"
    SUPERSEDES = "Supersedes"
    SUPPORTS = "Supports"
    MANAGED_BY = "Managed By"
    CONNECTED_TO = "Connected To"
    VALIDATED_BY = "Validated By"
    EVIDENCED_BY = "Evidenced By"
    RECOMMENDED_WITH = "Recommended With"
    MEMBER_OF = "Member Of"  # Sub-platform is member of parent (blade in enclosure)
    HOSTED_BY = "Hosted By"  # VM hosted by physical server
    HAS_SKU = "Has SKU"  # Component has a commercial SKU
    BELONGS_TO = "Belongs To"  # Component belongs to a solution category


class SourceType(str, Enum):
    """Source classification from Blueprint 04 §3."""

    PDF = "PDF"
    EXCEL = "Excel"
    CSV = "CSV"
    JSON = "JSON"
    XML = "XML"
    API = "API"
    VENDOR_PORTAL = "Vendor Portal"
    BOQ = "BOQ"
    HUMAN_FEEDBACK = "Human Feedback"
    FIRMWARE_CATALOG = "Firmware Catalog"
    CONFIGURATION_PORTAL = "Configuration Portal"
    VALIDATION_PORTAL = "Validation Portal"


class ProcessingStatus(str, Enum):
    """Source processing lifecycle status."""

    PENDING = "Pending"
    REGISTERED = "Registered"
    CLASSIFYING = "Classifying"
    EXTRACTING = "Extracting"
    NORMALIZING = "Normalizing"
    VALIDATING = "Validating"
    COMPLETED = "Completed"
    FAILED = "Failed"


class LifecycleStatus(str, Enum):
    """Product lifecycle status for engineering objects."""

    ACTIVE = "Active"
    END_OF_SALE = "End of Sale"
    END_OF_LIFE = "End of Life"
    DEPRECATED = "Deprecated"
    ANNOUNCED = "Announced"
    UNKNOWN = "Unknown"


class DeltaStatus(str, Enum):
    """Knowledge Delta lifecycle status."""

    PENDING = "Pending"
    VALIDATED = "Validated"
    MERGED = "Merged"
    REJECTED = "Rejected"
    NEEDS_REVIEW = "Needs Review"


class DeltaChangeType(str, Enum):
    """Types of changes a Knowledge Delta can contain."""

    NEW_OBJECT = "New Object"
    UPDATED_ATTRIBUTE = "Updated Attribute"
    NEW_RELATIONSHIP = "New Relationship"
    UPDATED_RULE = "Updated Rule"
    NEW_RULE = "New Rule"
    DEPRECATED = "Deprecated"
    RETIRED = "Retired"
    NEW_CAPABILITY = "New Capability"
    FIRMWARE_UPDATE = "Firmware Update"
    COMPATIBILITY_CHANGE = "Compatibility Change"
    NEW_COMPONENT = "New Component"
    NEW_SKU = "New SKU"
    UPDATE_COMPONENT = "Update Component"


class RuleSeverity(str, Enum):
    """Rule severity levels."""

    INFO = "Info"
    WARNING = "Warning"
    ERROR = "Error"
    CRITICAL = "Critical"


class ValidationFailureType(str, Enum):
    RULE_VIOLATION = "rule_violation"
    CATEGORY_LIMIT_EXCEEDED = "category_limit_exceeded"
    INCOMPATIBLE = "incompatible"
    MISSING_REQUIRED_CATEGORY = "missing_required_category"
    INVALID_SKU = "invalid_sku"


class ConfidenceLevel(str, Enum):
    """Confidence levels for extracted knowledge."""

    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    UNVERIFIED = "Unverified"


class PackagingType(str, Enum):
    """Packaging classification for components and SKUs."""

    BUNDLE = "Bundle"
    STANDALONE = "Standalone"
    SPARE = "Spare"


# ---------------------------------------------------------------------------
# Evidence & History — Blueprint 06 §7
# ---------------------------------------------------------------------------


class EvidenceRecord(BaseModel):
    """
    Tracks provenance of an engineering fact.
    Blueprint 06 §7: "Never overwrite evidence."
    """

    source_id: str
    source_version: Optional[str] = None
    acquisition_date: datetime = Field(default_factory=_utcnow)
    confidence: ConfidenceLevel = ConfidenceLevel.UNVERIFIED
    original_text_snippet: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None


class HistoryEntry(BaseModel):
    """
    Immutable change record for an engineering object.
    Blueprint 06 §7: "Never overwrite history."
    """

    timestamp: datetime = Field(default_factory=_utcnow)
    change_type: DeltaChangeType
    field_name: Optional[str] = None
    previous_value: Optional[Any] = None
    new_value: Optional[Any] = None
    delta_id: Optional[str] = None
    author: str = "system"
    reason: Optional[str] = None


# ---------------------------------------------------------------------------
# Engineering Relationships — Blueprint 03 §7
# ---------------------------------------------------------------------------


class EngineeringRelationship(BaseModel):
    """
    A directed, typed, evidence-backed relationship between two engineering objects.
    Blueprint 03 §7: "Relationships SHALL be first-class engineering objects."
    """

    target_id: str
    relationship_type: RelationshipType
    evidence: List[EvidenceRecord] = Field(default_factory=list)
    version: int = 1


# ---------------------------------------------------------------------------
# Engineering Attributes — Blueprint 03 §5
# ---------------------------------------------------------------------------


class EngineeringAttribute(BaseModel):
    """A typed, structured engineering attribute."""

    name: str
    value: Any
    unit: Optional[str] = None
    evidence: Optional[EvidenceRecord] = None


# ---------------------------------------------------------------------------
# Base Engineering Object — Blueprint 03 §4
# ---------------------------------------------------------------------------


class BaseEngineeringObject(BaseModel):
    """
    The canonical base for all engineering knowledge.
    Blueprint 03 §4: Every engineering object SHALL expose structured attributes.
    """

    id: str
    type: EngineeringObjectType
    title: str
    description: Optional[str] = None
    vendor: Optional[str] = None
    solution_domain: Optional[str] = None
    product_family: Optional[str] = None
    generation: Optional[str] = None
    platform_id: Optional[str] = None
    lifecycle_status: LifecycleStatus = LifecycleStatus.UNKNOWN

    attributes: List[EngineeringAttribute] = Field(default_factory=list)
    capabilities: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    aliases: List[str] = Field(default_factory=list)
    provided_resources: Dict[str, float] = Field(default_factory=dict)
    consumed_resources: Dict[str, float] = Field(default_factory=dict)

    relationships: List[EngineeringRelationship] = Field(default_factory=list)
    evidence: List[EvidenceRecord] = Field(default_factory=list)
    history: List[HistoryEntry] = Field(default_factory=list)
    confidence: ConfidenceLevel = ConfidenceLevel.UNVERIFIED
    timestamp: datetime = Field(default_factory=_utcnow)
    version: int = 1
    
    # Internal metadata for avoiding path duplication on updates
    source_filepath: Optional[str] = Field(default=None, exclude=True)


class SlotMapping(BaseEngineeringObject):
    """Spatial topology mapping for physical components."""

    type: EngineeringObjectType = EngineeringObjectType.SLOT_MAPPING
    source_slot: str = ""
    target_bays: List[str] = Field(default_factory=list)
    redundancy_link: Optional[str] = None
    constraints: List[str] = Field(default_factory=list)

    # Provenance
    evidence: List[EvidenceRecord] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Specialized Engineering Objects
# ---------------------------------------------------------------------------


class Platform(BaseEngineeringObject):
    """A commercially available product platform (e.g., DL380 Gen11, Alletra 6050)."""

    type: EngineeringObjectType = EngineeringObjectType.PLATFORM
    parent_platform_id: Optional[str] = None  # For sub-platforms (blades in enclosures)
    variants: List[str] = Field(default_factory=list)  # IDs of Variant objects
    slot_mapping_ids: List[str] = Field(default_factory=list)  # IDs of SlotMapping objects
    platform_sku: Optional[str] = None  # Master SKU for the platform itself
    mandatory_categories: List[str] = Field(default_factory=list)


class Component(BaseEngineeringObject):
    """A reusable component (CPU, Controller, Drive, DIMM, GPU, NIC, PSU, etc.).
    Blueprint 03 §4: Components SHALL exist independently of products."""

    type: EngineeringObjectType = EngineeringObjectType.COMPONENT
    component_category: Optional[str] = None  # e.g., "CPU", "Drive", "NIC"
    component_subcategory: Optional[str] = None  # e.g., "Riser", "Cable"
    packaging_type: PackagingType = PackagingType.STANDALONE
    inclusive_qty: Optional[int] = None
    is_required: bool = True  # False = safe to drop entirely if causing a validation failure


class SKU(BaseEngineeringObject):
    """A commercially orderable item.
    Blueprint 03 §4: Engineering knowledge SHALL NOT depend upon a SKU."""

    type: EngineeringObjectType = EngineeringObjectType.SKU
    part_number: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    packaging_type: PackagingType = PackagingType.STANDALONE
    inclusive_qty: Optional[int] = None
    component_id: Optional[str] = (
        None  # Link to the engineering Component this SKU represents
    )


class Workload(BaseEngineeringObject):
    """Customer intent rather than products.
    Blueprint 03 §11: Workloads SHALL never be derived from products."""

    type: EngineeringObjectType = EngineeringObjectType.WORKLOAD
    performance_requirements: Dict[str, Any] = Field(default_factory=dict)
    capacity_requirements: Dict[str, Any] = Field(default_factory=dict)


class Rule(BaseEngineeringObject):
    """
    An engineering rule with full metadata.
    Blueprint 03 §8: Every rule SHALL expose Identity, Scope, Severity,
    Confidence, Applicable Objects, Trigger Conditions, Expected Outcome,
    Supporting Evidence, Version.
    """

    type: EngineeringObjectType = EngineeringObjectType.RULE
    scope: Optional[str] = None
    severity: RuleSeverity = RuleSeverity.INFO
    applicable_objects: List[str] = Field(default_factory=list)  # IDs of objects this rule applies to
    trigger_conditions: List[str] = Field(default_factory=list)
    expected_outcome: str = ""
    version: int = 1
    negated: bool = False
    scaling_factor: Optional[str] = None
    dependency_targets: List[str] = Field(default_factory=list)


class Constraint(BaseEngineeringObject):
    """
    An engineering limitation (max controllers, max drives, max memory, etc.).
    Blueprint 03 §9.
    """

    type: EngineeringObjectType = EngineeringObjectType.CONSTRAINT
    limit_name: str = ""
    limit_value: Any = None
    limit_unit: Optional[str] = None


class CategoryLimit(Constraint):
    """
    A constraint specifically targeting a maximum or minimum quantity for a category or subcategory.
    """

    type: EngineeringObjectType = EngineeringObjectType.CATEGORY_LIMIT
    target_category: Optional[str] = None
    target_subcategory: Optional[str] = None
    min_qty: Optional[int] = None  # if set, dropping below this count is itself a violation


class SolutionCategory(BaseEngineeringObject):
    """Groups product families (e.g., 'Composable Infrastructure', 'Rack Servers', 'Tower Servers')."""

    type: EngineeringObjectType = EngineeringObjectType.SOLUTION_CATEGORY


class Variant(BaseEngineeringObject):
    """A configuration variant of a platform (e.g., 'SFF CTO', '8LFF CTO', '3-Frame')."""

    type: EngineeringObjectType = EngineeringObjectType.VARIANT
    base_platform_id: str = ""
    differentiators: List[str] = Field(default_factory=list)  # What makes this variant different


class Configuration(BaseEngineeringObject):
    """A pre-validated, named configuration (e.g., 'SAP HANA Optimized', 'VMware vSAN Ready Node')."""

    type: EngineeringObjectType = EngineeringObjectType.CONFIGURATION
    base_platform_id: str = ""
    included_components: List[str] = Field(default_factory=list)  # Component IDs in this config
    validated: bool = False
    validation_source: Optional[str] = None  # Where this config was validated


# ---------------------------------------------------------------------------
# Source Registration — Blueprint 04 §5
# ---------------------------------------------------------------------------


class Source(BaseModel):
    """
    Every engineering source SHALL receive a permanent identity.
    Blueprint 04 §5: Minimum metadata includes Source ID, Source Type, Vendor,
    Product Family, Generation, Version, Publication Date, Language,
    Acquisition Date, Confidence, Original File, Processing Status.
    """

    source_id: str = Field(default_factory=lambda: f"SRC-{str(uuid.uuid4())[:8]}")
    source_type: SourceType
    vendor: Optional[str] = None
    product_family: Optional[str] = None
    product_generation: Optional[str] = None
    version: Optional[str] = Field(
        default=None,
        description="Computed deterministically via SHA-256 or modDate during ingestion.",
    )
    publication_date: Optional[datetime] = None
    language: str = "en"
    acquisition_date: datetime = Field(default_factory=_utcnow)
    confidence: ConfidenceLevel = ConfidenceLevel.UNVERIFIED
    original_file_path: str = ""
    processing_status: ProcessingStatus = ProcessingStatus.PENDING
    title: Optional[str] = None
    description: Optional[str] = None
    file_hash: Optional[str] = None  # For duplicate detection


# ---------------------------------------------------------------------------
# Knowledge Delta — Blueprint 02 §7
# ---------------------------------------------------------------------------


class DeltaChange(BaseModel):
    """A single change within a Knowledge Delta."""

    change_type: DeltaChangeType
    object_id: str
    field_name: Optional[str] = None
    old_value: Optional[Any] = None
    new_value: Optional[Any] = None
    evidence: Optional[EvidenceRecord] = None


class KnowledgeDelta(BaseModel):
    """
    Every newly acquired engineering source produces a Knowledge Delta.
    Blueprint 02 §7: A Knowledge Delta represents engineering changes
    introduced by new information.
    """

    delta_id: str = Field(default_factory=lambda: f"DELTA-{str(uuid.uuid4())[:8]}")
    source_id: str
    timestamp: datetime = Field(default_factory=_utcnow)
    changes: List[DeltaChange] = Field(default_factory=list)
    status: DeltaStatus = DeltaStatus.PENDING
    review_notes: Optional[str] = None
    reviewed_by: Optional[str] = None


# ---------------------------------------------------------------------------
# Customer Request & Solution — Blueprint 05 §4, §13
# ---------------------------------------------------------------------------


class CustomerRequirement(BaseModel):
    """A single structured requirement extracted from a customer request."""

    category: str  # "business", "technical", "operational", "commercial"
    name: str
    value: Any
    priority: Optional[str] = None  # "required", "preferred", "nice_to_have"


class ValidationFailure(BaseModel):
    model_config = ConfigDict(extra="forbid")

    failure_type: ValidationFailureType
    object_id: Optional[str] = None       # the specific component/SKU at fault, if any
    rule_id: Optional[str] = None         # which Rule/CategoryLimit fired, if any
    category: Optional[str] = None        # e.g. "GPU", for category-level failures
    message: str                          # human-readable, for logs/UI -- not for parsing
    payload: Dict[str, Any] = Field(default_factory=dict) # structured data for programmatic recovery
    remediations: List[str] = Field(default_factory=list) # Recommended solutions (e.g. "Add Controller", "Use Direct NVMe")


class CustomerRequest(BaseModel):
    """
    Structured customer engineering request.
    Blueprint 05 §4: Customer requests SHALL be converted into
    structured engineering requirements.
    """

    request_id: str = Field(default_factory=lambda: f"REQ-{str(uuid.uuid4())[:8]}")
    raw_text: str = ""
    requirements: List[CustomerRequirement] = Field(default_factory=list)
    workloads: List[str] = Field(default_factory=list)
    vendor_preference: Optional[str] = None
    target_platform: Optional[str] = None
    budget: Optional[float] = None
    previous_errors: List[Any] = Field(default_factory=list)
    excluded_component_ids: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=_utcnow)


class SolutionCandidate(BaseModel):
    """
    A generated solution with full explainability.
    Blueprint 05 §13: Every recommendation SHALL include reasoning,
    alternatives, evidence, trade-offs, confidence, validation status.
    """

    solution_id: str = Field(default_factory=lambda: f"SOL-{str(uuid.uuid4())[:8]}")
    request_id: str
    profile: str  # "Lowest Cost", "Balanced", "Performance Optimized", etc.
    components: List[str] = Field(default_factory=list)  # IDs of engineering objects in the solution
    reasoning_chain: List[str] = Field(default_factory=list)  # Step-by-step reasoning
    requirements_satisfied: List[str] = Field(default_factory=list)
    rules_applied: List[str] = Field(default_factory=list)
    constraints_evaluated: List[str] = Field(default_factory=list)
    dependencies_resolved: List[str] = Field(default_factory=list)
    trade_offs: List[str] = Field(default_factory=list)
    confidence: ConfidenceLevel = ConfidenceLevel.UNVERIFIED
    evidence: List[EvidenceRecord] = Field(default_factory=list)
    validation_status: Optional[str] = None
    estimated_risks: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=_utcnow)
