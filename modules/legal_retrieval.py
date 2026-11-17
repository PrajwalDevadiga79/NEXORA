"""
NyayaSathi - Legal Knowledge Retrieval (RAG) Module
Loads verified Indian legal information from JSON and retrieves relevant provisions,
emergency protocols, and official statutory references for context grounding.

Updated: Supports 'general' category by searching across ALL categories.
"""

import json
import os
import re
from typing import Dict, List, Any, Optional

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "legal_information.json")


class LegalKnowledgeRetriever:
    """Manages verified legal knowledge retrieval for RAG pipeline."""

    def __init__(self, data_path: str = DATA_FILE):
        self.data_path = data_path
        self._data = self._load_data()

    def _load_data(self) -> Dict[str, Any]:
        """Loads the legal repository JSON safely."""
        if not os.path.exists(self.data_path):
            return {"categories": {}}
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading legal repository: {e}")
            return {"categories": {}}

    def get_category_data(self, category_id: str) -> Optional[Dict[str, Any]]:
        """Returns verified category information, helplines, and legal provisions."""
        categories = self._data.get("categories", {})
        return categories.get(category_id)

    def get_all_categories(self) -> Dict[str, Dict[str, Any]]:
        """Returns dictionary of all supported categories."""
        return self._data.get("categories", {})

    def retrieve_provisions(self, category_id: str, query: str = "") -> List[Dict[str, Any]]:
        """
        Retrieves verified legal provisions relevant to the category and query.
        For 'general' category, searches across ALL categories and returns best matches.
        """
        if category_id == "general":
            return self._retrieve_cross_category(query)

        cat_data = self.get_category_data(category_id)
        if not cat_data:
            return []

        provisions = cat_data.get("provisions", [])
        if not query:
            return provisions

        # Score provisions based on query keyword overlap
        query_words = set(re.findall(r"\w+", query.lower()))
        scored = []
        for prov in provisions:
            text_corpus = f"{prov.get('act', '')} {prov.get('section', '')} {prov.get('title', '')} {prov.get('description', '')} {prov.get('simple_explanation', '')}".lower()
            score = sum(1 for w in query_words if len(w) > 2 and w in text_corpus)
            scored.append((score, prov))

        # Sort highest relevance first, but preserve all verified provisions if query is broad
        scored.sort(key=lambda x: x[0], reverse=True)
        return [prov for _, prov in scored]

    def _retrieve_cross_category(self, query: str) -> List[Dict[str, Any]]:
        """
        For 'general' category: searches across ALL categories and returns
        the most relevant provisions based on query keyword matching.
        Only returns provisions that actually match the query.
        """
        if not query:
            return []

        query_words = set(re.findall(r"\w+", query.lower()))
        scored = []

        for cat_id, cat_data in self.get_all_categories().items():
            for prov in cat_data.get("provisions", []):
                text_corpus = f"{prov.get('act', '')} {prov.get('section', '')} {prov.get('title', '')} {prov.get('description', '')} {prov.get('simple_explanation', '')}".lower()
                score = sum(1 for w in query_words if len(w) > 2 and w in text_corpus)
                if score > 0:  # Only include provisions with at least one keyword match
                    scored.append((score, prov))

        scored.sort(key=lambda x: x[0], reverse=True)
        # Return top 5 most relevant provisions from any category
        return [prov for _, prov in scored[:5]]

    def format_rag_context(self, category_id: str, query: str = "") -> str:
        """
        Prepares a structured string context to pass directly to Gemini LLM prompt,
        ensuring zero hallucination of legal sections.
        """
        cat_data = self.get_category_data(category_id)
        if not cat_data:
            # For general category, try to build context from cross-category search
            if category_id == "general":
                provisions = self._retrieve_cross_category(query)
                if provisions:
                    context_lines = ["=== RELEVANT VERIFIED PROVISIONS FROM KNOWLEDGE BASE ==="]
                    for idx, prov in enumerate(provisions, 1):
                        context_lines.append(
                            f"\n[{idx}] {prov.get('act')} - {prov.get('section')} ({prov.get('title')})\n"
                            f"Statute Text: {prov.get('description')}\n"
                            f"Simple Meaning: {prov.get('simple_explanation')}\n"
                            f"Official Source: {prov.get('official_source')} (Verified: {prov.get('verified')})"
                        )
                    return "\n".join(context_lines)
            return "No verified legal provisions found for this category."

        context_lines = [
            f"=== VERIFIED INDIAN LEGAL REPOSITORY FOR: {cat_data.get('name')} ===",
            f"Legal Classification: {cat_data.get('classification')}",
            f"Statutory Urgency Level: {cat_data.get('urgency_level')}",
            "\nEMERGENCY HELPLINES & OFFICIAL DIRECTORIES:"
        ]

        for contact in cat_data.get("emergency_contacts", []):
            line = f"- {contact.get('name')}: {contact.get('number', contact.get('url', ''))} ({contact.get('details')})"
            context_lines.append(line)

        context_lines.append("\nVERIFIED STATUTORY PROVISIONS:")
        provisions = self.retrieve_provisions(category_id, query)
        for idx, prov in enumerate(provisions, 1):
            context_lines.append(
                f"\n[{idx}] {prov.get('act')} - {prov.get('section')} ({prov.get('title')})\n"
                f"Statute Text: {prov.get('description')}\n"
                f"Simple Meaning: {prov.get('simple_explanation')}\n"
                f"Official Source: {prov.get('official_source')} (Verified: {prov.get('verified')})"
            )

        context_lines.append(
            "\nSTRICT INSTRUCTION: Only reference the above verified provisions. "
            "Do NOT invent sections or fabricate penalties not provided in this text."
        )

        return "\n".join(context_lines)


# Singleton instance
legal_retriever = LegalKnowledgeRetriever()
