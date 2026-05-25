"""
One Long Impersonation -- Teacher-Student Network Analysis
Model 2: Influence graph analysis and gap computation.

Builds the directed influence graph from documented pairs.
Computes the Teacher-Student Gap: for each pair where the student
is inducted, measures induction_year(student) - induction_year(teacher).
If teacher was never inducted, gap = current_year - induction_year(student).

Decomposes gaps by racial composition of the pair.

Output: pairs dataset with gap metrics and racial breakdown statistics.
"""

import sys
import os
import json
import statistics

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from db import query
from config import CURRENT_YEAR, CHAPTERS_DIR

try:
    import networkx as nx
except ImportError:
    print("networkx not installed. Run: pip install networkx")
    sys.exit(1)


def build_influence_graph():
    """Build the directed influence graph from all documented pairs."""
    pairs = query("""
        SELECT
            ip.id,
            t.id as teacher_id, t.name as teacher_name,
            t.is_inducted as teacher_inducted, t.inducted_year as teacher_inducted_year,
            t.race as teacher_race, t.gender as teacher_gender,
            t.inducted_category as teacher_category,
            s.id as student_id, s.name as student_name,
            s.is_inducted as student_inducted, s.inducted_year as student_inducted_year,
            s.race as student_race, s.gender as student_gender,
            ip.source_type, ip.confidence
        FROM influence_pairs ip
        JOIN artists t ON ip.teacher_id = t.id
        JOIN artists s ON ip.student_id = s.id
    """)

    G = nx.DiGraph()

    for p in pairs:
        G.add_node(p["teacher_id"], name=p["teacher_name"],
                    inducted=bool(p["teacher_inducted"]),
                    inducted_year=p["teacher_inducted_year"],
                    race=p["teacher_race"],
                    gender=p["teacher_gender"],
                    category=p["teacher_category"])

        G.add_node(p["student_id"], name=p["student_name"],
                    inducted=bool(p["student_inducted"]),
                    inducted_year=p["student_inducted_year"],
                    race=p["student_race"],
                    gender=p["student_gender"])

        G.add_edge(p["teacher_id"], p["student_id"],
                    source_type=p["source_type"],
                    confidence=p["confidence"])

    return G, pairs


def compute_centrality(G):
    """Compute PageRank and betweenness centrality."""
    pagerank = nx.pagerank(G, alpha=0.85)
    betweenness = nx.betweenness_centrality(G)
    return pagerank, betweenness


def compute_gaps(pairs):
    """
    Compute the Teacher-Student Gap for each pair.

    Gap = student_inducted_year - teacher_inducted_year
    If teacher never inducted: gap uses current_year as teacher's "year"
    (representing ongoing injustice)

    Positive gap = teacher waited longer (or never inducted).
    """
    gap_records = []

    for p in pairs:
        if not p["student_inducted"]:
            continue  # Only measure gaps where student is inducted

        student_year = p["student_inducted_year"]
        teacher_year = p["teacher_inducted_year"]
        teacher_inducted = bool(p["teacher_inducted"])

        if teacher_inducted and teacher_year:
            gap = teacher_year - student_year  # Positive = teacher waited longer
            teacher_year_display = teacher_year
            status = "both_inducted"
        else:
            gap = CURRENT_YEAR - student_year  # Years since student inducted, teacher still waiting
            teacher_year_display = None
            status = "teacher_never_inducted"

        # Racial composition
        t_race = p["teacher_race"] or "unknown"
        s_race = p["student_race"] or "unknown"

        if t_race == "Black" and s_race == "white":
            composition = "BW"
        elif t_race == "Black" and s_race == "Black":
            composition = "BB"
        elif t_race == "white" and s_race == "white":
            composition = "WW"
        elif t_race == "white" and s_race == "Black":
            composition = "WB"
        else:
            composition = "other"

        gap_records.append({
            "teacher": p["teacher_name"],
            "student": p["student_name"],
            "teacher_inducted_year": teacher_year_display,
            "student_inducted_year": student_year,
            "gap_years": abs(gap),
            "gap_direction": "teacher_waited" if gap >= 0 else "teacher_first",
            "teacher_never_inducted": not teacher_inducted,
            "status": status,
            "teacher_race": t_race,
            "student_race": s_race,
            "composition": composition,
            "teacher_category": p["teacher_category"],
            "source_type": p["source_type"],
            "confidence": p["confidence"],
        })

    return gap_records


def analyze_gaps(gap_records):
    """Compute summary statistics on the gap distribution."""
    # Filter to pairs where teacher waited or was never inducted
    teacher_waited = [g for g in gap_records if g["gap_direction"] == "teacher_waited"
                      or g["teacher_never_inducted"]]

    # By racial composition
    bw_gaps = [g["gap_years"] for g in teacher_waited if g["composition"] == "BW"]
    bb_gaps = [g["gap_years"] for g in teacher_waited if g["composition"] == "BB"]
    ww_gaps = [g["gap_years"] for g in teacher_waited if g["composition"] == "WW"]
    same_race = bb_gaps + ww_gaps

    stats = {
        "total_pairs": len(gap_records),
        "teacher_waited_or_never": len(teacher_waited),
        "composition_counts": {
            "BW": len([g for g in gap_records if g["composition"] == "BW"]),
            "BB": len([g for g in gap_records if g["composition"] == "BB"]),
            "WW": len([g for g in gap_records if g["composition"] == "WW"]),
            "WB": len([g for g in gap_records if g["composition"] == "WB"]),
            "other": len([g for g in gap_records if g["composition"] == "other"]),
        },
    }

    if bw_gaps:
        stats["bw_median_gap"] = round(statistics.median(bw_gaps), 1)
        stats["bw_mean_gap"] = round(statistics.mean(bw_gaps), 1)
        stats["bw_gaps"] = sorted(bw_gaps)
    if same_race:
        stats["same_race_median_gap"] = round(statistics.median(same_race), 1)
        stats["same_race_mean_gap"] = round(statistics.mean(same_race), 1)
    if bb_gaps:
        stats["bb_median_gap"] = round(statistics.median(bb_gaps), 1)
    if ww_gaps:
        stats["ww_median_gap"] = round(statistics.median(ww_gaps), 1)

    # The unexplained difference
    if bw_gaps and same_race:
        stats["unexplained_difference"] = round(
            stats["bw_median_gap"] - stats["same_race_median_gap"], 1
        )

    return stats


def export_to_chapter_data(gap_records, stats, centrality_data):
    """Export to JavaScript data file for chapter visualization."""
    output_dir = os.path.join(CHAPTERS_DIR, "01-teachers")
    os.makedirs(output_dir, exist_ok=True)

    # Sort by gap size descending for visual impact
    sorted_gaps = sorted(gap_records, key=lambda g: g["gap_years"], reverse=True)

    data = {
        "pairs": sorted_gaps,
        "stats": stats,
        "centrality": centrality_data,
        "metadata": {
            "source": "Curated influence pairs + MusicBrainz relationships",
            "current_year": CURRENT_YEAR,
            "confidence_note": "All pairs documented from primary sources. See influence_pairs.yaml.",
            "methodology": "Gap = |teacher_inducted_year - student_inducted_year|. "
                           "If teacher never inducted, gap measured from student induction to current year.",
        }
    }

    js_path = os.path.join(output_dir, "teachers-data.js")
    with open(js_path, "w") as f:
        f.write("// One Long Impersonation -- Chapter 01: Teachers\n")
        f.write("// Teacher-Student Gap data -- generated by pipeline\n")
        f.write("// Source: Curated influence pairs with documented citations\n")
        f.write(f"// Generated: {CURRENT_YEAR}\n\n")
        f.write("window.TEACHERS_DATA = ")
        json.dump(data, f, indent=2)
        f.write(";\n")

    print(f"Exported to {js_path}")
    return js_path


def run():
    """Run the full teacher-student network analysis."""
    print("Building influence graph...")
    G, pairs = build_influence_graph()
    print(f"  Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    print("\nComputing centrality...")
    pagerank, betweenness = compute_centrality(G)

    # Top teachers by PageRank (most influential)
    top_teachers = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:10]
    print("\nTop 10 by PageRank (most cited as influence):")
    for node_id, score in top_teachers:
        node = G.nodes[node_id]
        inducted = "inducted" if node.get("inducted") else "NOT INDUCTED"
        print(f"  {node['name']}: {score:.4f} [{inducted}]")

    print("\nComputing teacher-student gaps...")
    gap_records = compute_gaps(pairs)
    stats = analyze_gaps(gap_records)

    print(f"\n{'='*60}")
    print("TEACHER-STUDENT GAP FINDINGS")
    print(f"{'='*60}")
    print(f"Total documented pairs: {stats['total_pairs']}")
    print(f"Pairs where teacher waited: {stats['teacher_waited_or_never']}")
    print(f"\nComposition breakdown:")
    for comp, count in stats["composition_counts"].items():
        print(f"  {comp}: {count}")

    if "bw_median_gap" in stats:
        print(f"\nBlack teacher / white student median gap: {stats['bw_median_gap']} years")
    if "same_race_median_gap" in stats:
        print(f"Same-race pairs median gap: {stats['same_race_median_gap']} years")
    if "unexplained_difference" in stats:
        print(f"Unexplained difference: {stats['unexplained_difference']} years")

    # Prepare centrality data for export
    centrality_data = []
    for node_id in G.nodes:
        node = G.nodes[node_id]
        centrality_data.append({
            "name": node["name"],
            "pagerank": round(pagerank.get(node_id, 0), 6),
            "betweenness": round(betweenness.get(node_id, 0), 6),
            "inducted": node.get("inducted", False),
            "inducted_year": node.get("inducted_year"),
            "race": node.get("race"),
        })

    print("\nExporting chapter data...")
    export_to_chapter_data(gap_records, stats, centrality_data)

    # Print the most egregious gaps
    print(f"\nMost egregious gaps (teacher waited or never inducted):")
    sorted_gaps = sorted(gap_records, key=lambda g: g["gap_years"], reverse=True)
    for g in sorted_gaps[:15]:
        teacher_yr = g["teacher_inducted_year"] or "NEVER"
        status = f"({g['composition']})"
        print(f"  {g['teacher']} [{teacher_yr}] -> {g['student']} [{g['student_inducted_year']}]: "
              f"{g['gap_years']}y {status}")

    return gap_records, stats


if __name__ == "__main__":
    run()
