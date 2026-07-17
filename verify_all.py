import json
from ikp_platform.core.repository.repo_manager import RepoManager

def run_verification():
    repo = RepoManager('repository', '.')
    repo.bootstrap()
    
    cats = {}
    subcats = {}
    skus = 0
    components = 0
    limits = 0
    
    for nid, data in repo.graph.graph.nodes(data=True):
        t = data.get('type')
        if t == 'Component':
            components += 1
            cat = data.get('attr_component_category') or data.get('component_category', 'NONE')
            sub = data.get('attr_component_subcategory') or data.get('component_subcategory', 'NONE')
            cats[cat] = cats.get(cat, 0) + 1
            subcats[f'{cat}/{sub}'] = subcats.get(f'{cat}/{sub}', 0) + 1
        elif t == 'SKU':
            skus += 1
        elif t == 'Category Limit':
            limits += 1
            
    print("=== CATEGORY TAXONOMY ===")
    for k, v in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {k:20s}: {v:3d}")
        
    print("\n=== SUBCATEGORY TAXONOMY ===")
    for k, v in sorted(subcats.items(), key=lambda x: -x[1]):
        print(f"  {k:30s}: {v:3d}")
        
    print(f"\n=== OVERALL COUNTS ===")
    print(f"  Total Components : {components}")
    print(f"  Total SKUs       : {skus}")
    print(f"  Total Limits     : {limits}")
    
    # Check relationships
    has_sku = 0
    for u, v, data in repo.graph.graph.edges(data=True):
        if data.get('relationship_type') == 'Has SKU':
            has_sku += 1
            
    print(f"  'Has SKU' Edges  : {has_sku}")
    
    print("\n=== SAMPLE SKUs ===")
    sample_skus = [n for n, d in repo.graph.graph.nodes(data=True) if d.get('type') == 'SKU'][:5]
    for nid in sample_skus:
        print(f"  {nid}")
        
if __name__ == "__main__":
    run_verification()
