with open("ikp_platform/core/reasoning/solution_generator.py", "r") as f:
    content = f.read()

target = """        candidate = SolutionCandidate(
            request_id=request.request_id,
            profile=profile,
            components=[platform_id] + components,
            reasoning_chain=reasoning_chain,
            requirements_satisfied=satisfied_reqs,
            confidence=confidence,
            validation_status="Valid" if is_valid else "Invalid: " + "; ".join(e.message for e in errors),
        )"""

replacement = """        # Phase 4c: Group solution output by category
        grouped_components = {}
        for cid in [platform_id] + components:
            if cid in self.graph.graph:
                cat = self.graph.graph.nodes[cid].get("attr_component_category", "Platform")
                if not cat:
                    cat = self.graph.graph.nodes[cid].get("type", "Unknown")
                if cat not in grouped_components:
                    grouped_components[cat] = []
                grouped_components[cat].append(cid)
                
        # Phase 4d: Add closeness scoring vs BOQ
        total_reqs = len(request.requirements) if request.requirements else 1
        closeness_score = len(satisfied_reqs) / total_reqs if total_reqs > 0 else 1.0

        candidate = SolutionCandidate(
            request_id=request.request_id,
            profile=profile,
            components=[platform_id] + components,
            grouped_components=grouped_components,
            closeness_score=closeness_score,
            reasoning_chain=reasoning_chain,
            requirements_satisfied=satisfied_reqs,
            confidence=confidence,
            validation_status="Valid" if is_valid else "Invalid: " + "; ".join(e.message for e in errors),
        )"""

if target in content:
    content = content.replace(target, replacement)
    
    # Phase 4a & 4b: Chassis variant selection logic.
    # I'll inject this inside the generic fallback loop or LLM selection to prefer chassis variants.
    # Actually, adding chassis variant constraint satisfaction can be done in rule engine,
    # but the implementation plan says "Add chassis variant selection logic: given storage requirements, pick the right chassis".
    
    with open("ikp_platform/core/reasoning/solution_generator.py", "w") as f:
        f.write(content)
    print("Patched solution_generator.py for groups and score")
else:
    print("Target not found in solution_generator.py")
