# Almusaileem Prompt Agent V1
# Python 3.10+, standard library only.
# Run: python agents/prompt_agent.py --task video --subject "السحاب والبعير" --constraints "النص ثابت"
import argparse
import json
from datetime import datetime, timezone

PROMPTS = {
 "video": """Animate the supplied image for exactly 10 seconds. Animate ONLY: {subject}. Keep all other objects, logos, text, architecture, and background static. Locked camera, no zoom, pan, cuts, morphing, audio or additional objects. Preserve original aspect ratio. Additional restrictions: {constraints}.""",
 "design": """Act as a Kuwaiti interior design specialist. Design or edit ONLY: {subject}. Preserve dimensions, doors, windows, camera perspective, existing services and unrequested elements. Wood and stone alternatives must have smooth flat surfaces, never ribbed or fluted. Restrictions: {constraints}.""",
 "seo": """Write a useful, accurate Kuwaiti Arabic SEO article about: {subject}. Include direct answers, logical H1/H2, FAQs, meta description and image ALT. Do not invent reviews, prices or guarantees or stuff keywords. Restrictions: {constraints}.""",
 "marketing": """Create Kuwaiti Arabic marketing content about: {subject}. Include a clear hook, problem, solution, proof only if provided, CTA and five relevant hashtags. Never invent prices, results or guarantees. Include للاستفسار: 56510526. Restrictions: {constraints}."""
}
CHECKS = ["geometry", "text_and_logo", "allowed_changes", "realism", "format"]
def generate(task, subject, constraints):
    return PROMPTS[task].format(subject=subject, constraints=constraints)
def audit(scores, critical=False):
    if set(scores) != set(CHECKS) or any(not isinstance(v, int) or not 0 <= v <= 20 for v in scores.values()):
        raise ValueError("Supply five integer scores between 0 and 20")
    total = sum(scores.values())
    return {"total": total, "status": "PASS" if total >= 90 and not critical else "REVISE", "critical": critical}
def main():
    p = argparse.ArgumentParser(description="Almusaileem prompt composer and manual QA logger")
    p.add_argument("--task", choices=PROMPTS, required=True)
    p.add_argument("--subject", required=True)
    p.add_argument("--constraints", default="No changes beyond requested scope")
    p.add_argument("--scores", help="Optional five comma-separated scores (geometry,text/logo,allowed changes,realism,format)")
    p.add_argument("--critical", action="store_true")
    p.add_argument("--output", help="Optional JSON report path")
    a = p.parse_args()
    report = {"created_at": datetime.now(timezone.utc).isoformat(), "task": a.task, "subject": a.subject, "constraints": a.constraints, "prompt": generate(a.task,a.subject,a.constraints), "quality": "NOT_EVALUATED"}
    if a.scores:
        scores = dict(zip(CHECKS, [int(v) for v in a.scores.split(",")]))
        report["quality"] = audit(scores, a.critical)
        report["quality"]["scores"] = scores
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if a.output:
        with open(a.output,"w",encoding="utf-8") as f:
            json.dump(report,f,ensure_ascii=False,indent=2)
if __name__ == "__main__":
    main()
