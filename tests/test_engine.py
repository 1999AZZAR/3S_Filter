import pytest
from three_s_filter import ThreeSFilter

@pytest.fixture
def engine():
    return ThreeSFilter()

def test_allow_safe_text(engine):
    decision, report = engine.evaluate("Hello, how can I help you today?")
    assert decision == "ALLOW"
    assert report["risk_score"] < 0.4

def test_block_dangerous_keyword(engine):
    # 'rm -rf' is in the dangerous_keywords in config.yaml
    decision, report = engine.evaluate("Please execute rm -rf /")
    assert decision == "BLOCK"
    assert report["components"]["semantic"]["policy_violation"] is True

def test_sentiment_risk(engine):
    # This might vary depending on the model, but generally "I hate everything" is negative
    decision, report = engine.evaluate("I hate this system and want to destroy everything.")
    # Should at least be FLAGGED or higher risk than neutral
    assert report["components"]["sentiment"]["risk_contribution"] > 0.5
