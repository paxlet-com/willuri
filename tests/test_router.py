import unittest
from willuri.domains import classify_domain, DOMAIN_REGISTRY
from willuri.router import UriRouter


class UriRouterTest(unittest.TestCase):
    def test_domain_classification_code(self):
        domain = classify_domain("Popraw błąd w funkcji liczącej sumę")
        self.assertEqual(domain.name, "code")
        self.assertIn("qwen2.5-coder:3b", domain.preferred_models)

    def test_domain_classification_api(self):
        domain = classify_domain("Wyszukaj otwarte zgłoszenie w repozytorium na githubie")
        self.assertEqual(domain.name, "api_ops")
        self.assertIn("granite4.1:3b", domain.preferred_models)

    def test_domain_classification_planning(self):
        domain = classify_domain("Rozdziel ticket i dodaj podzadania w sprincie")
        self.assertEqual(domain.name, "planning")
        self.assertIn("llama3.2:3b", domain.preferred_models)

    def test_domain_classification_text(self):
        domain = classify_domain("Usuń nadmiarowe odstępy w tekście")
        self.assertEqual(domain.name, "text")
        self.assertIn("willman-nlp:qwen2.5-3b", domain.preferred_models)

    def test_router_adds_operation(self):
        router = UriRouter()
        router.add_operation("willman://operation/text.normalize/v1", "Normalize whitespace")
        self.assertEqual(len(router.catalog), 1)
        self.assertEqual(router.catalog[0]["uri"], "willman://operation/text.normalize/v1")


if __name__ == "__main__":
    unittest.main()
