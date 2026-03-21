import re

from scripts import markdown_helpers
import pytest


def test_render_note_includes_frontmatter_aliases_tags_and_links(tmp_path):
    from scripts import obsidian_note

    draft = {
        "title": "Test\nNote",
        "aliases": ["Alternate Title", "Alt 2"],
        "tags": ["ai", "reading-notes"],
        "source_type": "web",
        "source_url": "https://example.com/article",
        "published": "2024-01-02",
        "created": "2026-03-21",
        "updated": "2026-03-21",
        "importance": "core",
        "status": "processed",
        "summary": "One-line\nsummary.\n",
        "bullets": ["First point\nSecond line", "Second point"],
        "excerpts": [
            "Evidence excerpt line 1.\nEvidence excerpt line 2.",
        ],
        "related_notes": ["Alpha Note", "Beta Note"],
        "embeds": ["Beta Note"],
        "related_links": [
            {"note": "Gamma Note"},
            {"title": "External Ref ] (v1)", "url": "https://example.com/other(path)"},
        ],
    }

    rendered = obsidian_note.render_obsidian_note(draft, vault_root=tmp_path)
    assert rendered.destination_path == tmp_path / "Test Note.md"

    frontmatter = markdown_helpers.load_frontmatter(rendered.content)
    assert frontmatter["title"] == "Test Note"
    assert frontmatter["aliases"] == ["Alternate Title", "Alt 2"]
    assert frontmatter["tags"] == ["ai", "reading-notes"]
    assert frontmatter["source_type"] == "web"
    assert frontmatter["source_url"] == "https://example.com/article"
    assert frontmatter["published"] == "2024-01-02"
    assert frontmatter["created"] == "2026-03-21"
    assert frontmatter["updated"] == "2026-03-21"
    assert frontmatter["importance"] == "core"
    assert frontmatter["status"] == "processed"
    assert re.fullmatch(r"[a-f0-9]{64}", frontmatter["canonical_hash"])

    # Publishable note body structure.
    assert "One-line summary." in rendered.content
    assert "One-line\nsummary." not in rendered.content
    assert "## Key Points" in rendered.content
    assert "- First point" in rendered.content
    assert "- First point Second line" in rendered.content

    # Obsidian-native internal references: wikilinks and embeds.
    assert "[[Alpha Note]]" in rendered.content
    assert "![[Beta Note]]" in rendered.content
    assert "[[Gamma Note]]" in rendered.content
    assert "[External Ref \\] \\(v1\\)](<https://example.com/other(path)>)" in rendered.content
    assert "# Test Note" in rendered.content

    # Evidence block should include a block id for referencing.
    assert re.search(r"\^evidence-[a-f0-9]{8}(?:-\d+)?", rendered.content)
    assert re.search(r"^\^evidence-[a-f0-9]{8}(?:-\d+)?$", rendered.content, flags=re.MULTILINE) is None
    assert re.search(
        r"^> .* \^evidence-[a-f0-9]{8}(?:-\d+)?$",
        rendered.content,
        flags=re.MULTILINE,
    )


def test_render_note_rejects_empty_or_relative_vault_root():
    from scripts import obsidian_note

    with pytest.raises(ValueError):
        obsidian_note.render_obsidian_note({"title": "Test Note"}, vault_root="")

    with pytest.raises(ValueError):
        obsidian_note.render_obsidian_note({"title": "Test Note"}, vault_root="relative/path")


def test_destination_path_sanitizes_title(tmp_path):
    from scripts import obsidian_note

    rendered = obsidian_note.render_obsidian_note(
        {
            "title": 'Bad/Title: "Oops"?',
            "source_type": "web",
            "source_url": "https://example.com/article",
        },
        vault_root=tmp_path,
    )

    # Should remain within the provided vault root and end with .md.
    assert rendered.destination_path.parent == tmp_path
    assert rendered.destination_path.suffix == ".md"
    assert rendered.destination_path.name == "Bad-Title- -Oops-.md"
