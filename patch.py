with open("ikp_platform/scripts/ingest_catalog.py", "r") as f:
    content = f.read()

target = "repo._record_delta(delta)"
replacement = """
            from ikp_platform.core.ontology.models import KnowledgeDelta, DeltaStatus
            import uuid, datetime
            delta_obj = KnowledgeDelta(
                delta_id=str(uuid.uuid4()),
                source_id=source.source_id,
                changes=delta,
                timestamp=datetime.datetime.utcnow(),
                status=DeltaStatus.DRAFT
            )
            repo._record_delta(delta_obj)
"""
content = content.replace(target, replacement)
content = content.replace("if manifest.get(pdf_file.name) == checksum:", "if False:")
with open("ikp_platform/scripts/ingest_catalog.py", "w") as f:
    f.write(content)
