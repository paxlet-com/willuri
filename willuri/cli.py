"""CLI for willuri router."""
import argparse
import json
import sys
from .router import UriRouter
from .domains import classify_domain


def main():
    parser = argparse.ArgumentParser(prog="willuri", description="Willuri: NL to URI Process Router")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("domains", help="List all registered domains and specialized models")

    classify_cmd = sub.add_parser("classify", help="Classify instruction domain")
    classify_cmd.add_argument("instruction", help="Natural language instruction")

    route_cmd = sub.add_parser("route", help="Route instruction to URI via specialized LLM")
    route_cmd.add_argument("instruction", help="Natural language instruction")
    route_cmd.add_argument("--model", help="Override LLM model")
    route_cmd.add_argument("--input", default="{}", help="Input JSON data")

    args = parser.parse_args()

    if args.command == "domains":
        from .domains import DOMAIN_REGISTRY
        res = {
            name: {
                "description": prof.description,
                "preferred_models": prof.preferred_models,
                "uri_prefixes": prof.uri_prefixes,
                "keywords": prof.keywords,
            }
            for name, prof in DOMAIN_REGISTRY.items()
        }
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return 0

    if args.command == "classify":
        domain = classify_domain(args.instruction)
        print(json.dumps({
            "domain": domain.name,
            "description": domain.description,
            "preferred_models": domain.preferred_models,
            "uri_prefixes": domain.uri_prefixes,
        }, indent=2, ensure_ascii=False))
        return 0

    if args.command == "route":
        input_data = json.loads(args.input)
        router = UriRouter()
        result = router.route(args.instruction, input_data=input_data, model_override=args.model)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result.get("status") == "routed" else 1


if __name__ == "__main__":
    sys.exit(main())
