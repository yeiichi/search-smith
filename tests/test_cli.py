from search_smith import SearchResult
from search_smith.cli import main
from search_smith.exceptions import ConfigurationError


def test_cli_text_output(monkeypatch, capsys) -> None:
    monkeypatch.setattr(
        "search_smith.cli.search",
        lambda query, count, offset: [
            SearchResult(
                title="Example",
                url="https://example.com",
                snippet="A result.",
                source="brave",
                rank=1,
            )
        ],
    )

    exit_code = main(["Python semantic release", "--count", "5"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "1. Example" in captured.out
    assert "https://example.com" in captured.out
    assert "A result." in captured.out
    assert captured.err == ""


def test_cli_json_output(monkeypatch, capsys) -> None:
    monkeypatch.setattr(
        "search_smith.cli.search",
        lambda query, count, offset: [
            SearchResult(
                title="Example",
                url="https://example.com",
                snippet="A result.",
                source="brave",
                rank=1,
                metadata={"age": "1 day"},
            )
        ],
    )

    exit_code = main(["Brave Search API", "--format", "json"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert '"title": "Example"' in captured.out
    assert '"metadata": {' in captured.out


def test_cli_failure_exit_status(monkeypatch, capsys) -> None:
    def fail(query, count, offset):
        raise ConfigurationError("Set BRAVE_SEARCH_API_KEY.")

    monkeypatch.setattr("search_smith.cli.search", fail)

    exit_code = main(["missing key"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "BRAVE_SEARCH_API_KEY" in captured.err
    assert "Traceback" not in captured.err
