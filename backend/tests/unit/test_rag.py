from app.services.rag import citations
from app.services.rag.abstention import should_abstain
from app.services.rag.embeddings import HashEmbeddingProvider
from app.services.rag.generation import GroqClient, parse_json_object
from app.services.rag.pipeline import NO_ANSWER, RagPipeline
from app.services.rag.retrieval import InMemoryRetriever, load_chunks


def make(settings):
    chunks = load_chunks(settings.data_dir)
    assert chunks, "run scripts/build_corpus.py first"
    return RagPipeline(InMemoryRetriever(chunks, HashEmbeddingProvider(384)), GroqClient(settings), 6, 0.12)


def test_retrieves_snakebite(settings):
    rag = make(settings)
    res = rag.retrieve("should I tie a tourniquet on a snake bite")
    assert any("snake" in c.topic.lower() for c in res[:4])


def test_handbook_boost_and_citations(settings):
    rag = make(settings)
    ans = rag.answer("how do I give chest compressions to an adult")
    assert not ans.abstained and ans.citations
    assert all(c["label"] for c in ans.citations)


def test_abstains_on_nonsense(settings):
    rag = make(settings)
    assert rag.answer("quantum chromodynamics lagrangian renormalization").text == NO_ANSWER


def test_restricted_topics_not_retrievable(settings):
    chunks = load_chunks(settings.data_dir)
    assert not any("suicidal" in c.topic.lower() for c in chunks)


def test_citation_labels():
    assert "IFRC" in citations.label("ifrc", "340")
    assert "Handbook" in citations.label("handbook", "12")
    assert "not yet medically reviewed" in citations.label("authored")


def test_should_abstain_empty():
    assert should_abstain([], 0.1)


def test_parse_json_object():
    assert parse_json_object('```json\n{"a": 1}\n```') == {"a": 1}
    assert parse_json_object("no json here") == {}
