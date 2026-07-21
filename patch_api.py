with open("ikp_platform/api.py", "r") as f:
    content = f.read()

target = """    # Search vector store (Gap 3.2: Passing filter_metadata to where clause)
    results = repo.vector_store.semantic_search(
        request.query, n_results=request.limit, filter_metadata=request.filter_metadata
    )

    formatted_results = []
    for res_id, score in results:
        node_data = {}
        if res_id in repo.graph.graph:
            node_data = repo.graph.graph.nodes[res_id]

        description = node_data.get("description") or node_data.get("title") or res_id
        formatted_results.append(
            {
                "id": res_id,
                "score": round(score, 4),
                "text": description,
                "title": node_data.get("title", res_id),
                "type": node_data.get("type", "unknown"),
                "vendor": node_data.get("vendor"),
                "category": node_data.get("component_category"),
                "subcategory": node_data.get("subcategory"),
                "price": node_data.get("price", "TBD"), # Gap 8.2: Hardcoded string instead of structured price data
                "metadata": node_data,
            }
        )
    return formatted_results"""

replacement = """    # Use Hybrid Search via RepoManager
    formatted_results = repo.search(
        query=request.query, limit=request.limit, filter_metadata=request.filter_metadata
    )

    return formatted_results"""

if target in content:
    content = content.replace(target, replacement)
    with open("ikp_platform/api.py", "w") as f:
        f.write(content)
    print("Patched api.py")
else:
    print("Target not found in api.py")
