import datetime as dt
import shutil
import subprocess
from importlib import resources
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner
from pydantic import ValidationError

from resumate.check import check_cover_letter, check_resume, pdf_text
from resumate.cli import main
from resumate.loader import ResumateError, load_cover_letter, load_resume
from resumate.markup import blocks, inline
from resumate.models import Certificate, Entry, Resume, Style
from resumate.render import render_cover_letter, render_resume
from resumate.workspace import (
    init_workspace,
    list_applications,
    new_application,
    resolve_application,
    set_status,
)

TODAY = dt.date(2026, 10, 22)


@pytest.fixture
def workspace(tmp_path: Path) -> Path:
    init_workspace(tmp_path, name="Ada Lovelace")
    return tmp_path


# --- markup ----------------------------------------------------------------------------


def test_inline_escapes_and_formats():
    assert inline("a < b & **c**") == "a &lt; b &amp; <b>c</b>"
    assert inline("*em* and _em_") == "<i>em</i> and <i>em</i>"
    assert inline("[site](https://x.io)") == '<a href="https://x.io">site</a>'
    assert inline("2 * 3 * 4") == "2 * 3 * 4"
    assert inline("snake_case_name") == "snake_case_name"


def test_blocks_paragraphs_and_bullets():
    parsed = blocks("Hello\nthere\n\n- one\n- two\n  continued\n\nSincerely,\nAda")
    assert [b.kind for b in parsed] == ["paragraph", "bullets", "paragraph"]
    assert parsed[1].lines == ["one", "two continued"]
    assert parsed[2].lines == ["Sincerely,", "Ada"]


# --- models and loading ----------------------------------------------------------------


def test_certificate_round_trip(tmp_path: Path):
    path = tmp_path / "r.yaml"
    path.write_text(
        "name: A\nsections:\n  - title: Certifications\n    certificates:\n"
        "      - name: AWS Certified Solutions Architect\n        issued: 2024\n"
        "        expires: 2027-06-01\n"
        "  - title: Hidden\n    certificates:\n      # - name: Commented out\n"
    )
    resume = load_resume(path)
    cert = resume.sections[0].certificates[0]
    assert cert.issued == "2024" and cert.expires == "2027-06-01"
    assert resume.sections[1].is_empty
    with pytest.raises(ResumateError, match="organisation"):
        path.write_text(
            "name: A\nsections:\n  - title: Certifications\n    certificates:\n"
            "      - name: AWS\n        organisation: Amazon\n"
        )
        load_resume(path)
    with pytest.raises(ValidationError, match="only one of"):
        Resume.model_validate(
            {
                "name": "A",
                "sections": [
                    {
                        "title": "X",
                        "entries": [{"title": "Job"}],
                        "certificates": [{"name": "Cert"}],
                    }
                ],
            }
        )


def test_yaml_scalars_coerced_to_text(tmp_path: Path):
    path = tmp_path / "r.yaml"
    path.write_text(
        "name: A\nsections:\n  - title: Education\n    entries:\n"
        "      - title: BS\n        dates: 2018\n        start: 2020-01-01\n"
    )
    entry = load_resume(path).sections[0].entries[0]
    assert entry.dates == "2018" and entry.start == "2020-01-01"


def test_commenting_out_everything_is_allowed(tmp_path: Path):
    path = tmp_path / "r.yaml"
    path.write_text(
        "name: A\nsections:\n  - title: Jobs\n    entries:\n      - title: Eng\n"
        "        bullets:\n          # - hidden\n  - title: Awards\n    bullets:\n      # - x\n"
    )
    resume = load_resume(path)
    assert resume.sections[0].entries[0].bullets == []
    assert resume.sections[1].is_empty


def test_unknown_keys_and_mixed_sections_rejected(tmp_path: Path):
    path = tmp_path / "r.yaml"
    path.write_text("name: A\nsections:\n  - title: X\n    bulets: [a]\n")
    with pytest.raises(ResumateError, match="bulets"):
        load_resume(path)
    with pytest.raises(ValidationError, match="only one of"):
        Resume.model_validate(
            {"name": "A", "sections": [{"title": "X", "bullets": ["a"], "text": "b"}]}
        )


def test_cover_letter_front_matter_and_comments(tmp_path: Path):
    path = tmp_path / "c.md"
    path.write_text("---\ncompany: Acme\ndate: 2026-01-02\n---\nHi <!-- note -->there\n")
    letter = load_cover_letter(path)
    assert letter.company == "Acme"
    assert letter.date == dt.date(2026, 1, 2)
    assert letter.body == "Hi there"


# --- rendering -------------------------------------------------------------------------


def test_resume_pdf_is_extractable_and_excludes_comments(workspace: Path, tmp_path: Path):
    resume = load_resume(workspace / "master" / "resume.yaml")
    out = tmp_path / "out" / "resume.pdf"
    pages = render_resume(resume, out, Style(layout="classic"))
    text = " ".join(pdf_text(out).split())
    assert pages == 1
    assert "ADA LOVELACE" in text  # classic layout capitalizes the name
    assert "• Led redesign" in text  # bullets extract as real bullet characters
    assert "Experience" in text
    assert "15 min to 4 s" in text
    assert "hackathon" not in text  # commented out in the example master
    assert "AWS Certified Solutions Architect - Associate" in text
    assert "Amazon Web Services" in text
    assert "Credential ID SAA-EXAMPLE" in text
    assert "example.com/certs/saa" in text
    assert "Jun 2024 (expires Jun 2027)" in text


@pytest.mark.skipif(not shutil.which("pdftotext"), reason="needs poppler's pdftotext")
@pytest.mark.parametrize("layout", ["classic", "modern"])
def test_dates_stay_with_their_entries(workspace: Path, tmp_path: Path, layout: str):
    # Poppler's default reading order moves flush-right dates to the end of the page.
    resume = load_resume(workspace / "master" / "resume.yaml")
    out = tmp_path / "resume.pdf"
    render_resume(resume, out, Style(layout=layout))
    text = subprocess.run(
        ["pdftotext", str(out), "-"], capture_output=True, text=True, check=True
    ).stdout
    lines = [line for line in text.splitlines() if line.strip()]
    for section in resume.sections:
        if not section.entries:
            continue
        start = next(n for n, line in enumerate(lines) if line.lower() == section.title.lower())
        for entry in section.entries:
            line = next(line for line in lines[start:] if line.startswith(entry.title))
            assert f"| {entry.date_range}" in line


def test_date_ranges_use_plain_hyphens():
    assert Entry(title="A", start="Mar 2022", end="Present").date_range == "Mar 2022 - Present"
    assert Entry(title="A", dates="2018–2022").date_range == "2018-2022"


def test_certificate_dates_use_plain_hyphens():
    assert Certificate(name="A", issued="Jun 2024", expires="Jun 2027").date_text == (
        "Jun 2024 (expires Jun 2027)"
    )
    assert Certificate(name="A", issued="2018–2020").date_text == "2018-2020"
    assert Certificate(name="A", expires="Jun 2027").date_text == "expires Jun 2027"
    assert Certificate(name="A").date_text == ""


@pytest.mark.skipif(not shutil.which("pdftotext"), reason="needs poppler's pdftotext")
@pytest.mark.parametrize("layout", ["classic", "modern"])
def test_certificate_dates_stay_with_the_name(tmp_path: Path, layout: str):
    path = tmp_path / "r.yaml"
    path.write_text(
        "name: Ada Lovelace\nsections:\n  - title: Certifications\n    certificates:\n"
        "      - name: Google Cybersecurity Certificate\n        issuer: Google\n"
        "        issued: Nov 2026\n        credential_id: DEMO-123\n"
        "        url: https://example.com/certs/google\n"
    )
    out = tmp_path / "resume.pdf"
    render_resume(load_resume(path), out, Style(layout=layout))
    text = subprocess.run(
        ["pdftotext", str(out), "-"], capture_output=True, text=True, check=True
    ).stdout
    line = next(line for line in text.splitlines() if "Google Cybersecurity Certificate" in line)
    assert "| Nov 2026" in line
    assert "Google" in text and "DEMO-123" in text and "example.com/certs/google" in text


def test_right_aligned_dates_still_render(workspace: Path, tmp_path: Path):
    resume = load_resume(workspace / "master" / "resume.yaml")
    out = tmp_path / "resume.pdf"
    render_resume(resume, out, Style(date_align="right"))
    text = pdf_text(out)
    assert "Mar 2022 - Present" in text and "| Mar 2022" not in text


def test_page_count_reported(workspace: Path, tmp_path: Path):
    resume = load_resume(workspace / "master" / "resume.yaml")
    entry = resume.sections[0].entries[0]
    entry.bullets = entry.bullets * 15
    assert render_resume(resume, tmp_path / "long.pdf", Style()) > 1


def test_cover_letter_pdf(workspace: Path, tmp_path: Path):
    letter_path = tmp_path / "c.md"
    letter_path.write_text(
        "---\ncompany: Acme\nrecipient: Grace Hopper\n---\n"
        "Dear Grace,\n\nI **love** compilers.\n\n- Built one\n\nSincerely,\nAda Lovelace\n"
    )
    sender = load_resume(workspace / "master" / "resume.yaml")
    out = tmp_path / "letter.pdf"
    render_cover_letter(load_cover_letter(letter_path), sender, out, Style())
    text = pdf_text(out)
    for expected in ("Grace Hopper", "Acme", "I love compilers.", "Built one", "Sincerely,"):
        assert expected in text
    assert sender.headline and sender.headline not in text  # plain letterhead
    assert sender.contact.email in text
    assert sender.contact.location and sender.contact.location not in text


def test_cover_letter_without_recipient_has_no_inside_address(workspace: Path, tmp_path: Path):
    letter_path = tmp_path / "c.md"
    letter_path.write_text("---\ncompany: Acme\n---\nDear Hiring Team,\n\nHello.\n")
    sender = load_resume(workspace / "master" / "resume.yaml")
    out = tmp_path / "letter.pdf"
    render_cover_letter(load_cover_letter(letter_path), sender, out, Style())
    assert "Acme" not in pdf_text(out)


# --- workspace -------------------------------------------------------------------------


SKILLS = {
    "resumate",
    "resumate-apply",
    "resumate-capture",
    "resumate-cover-letter",
    "resumate-interview-prep",
    "resumate-questions",
    "resumate-research",
    "resumate-review",
    "resumate-setup",
    "resumate-tailor",
    "resumate-voice",
}


def test_init_installs_skills_and_examples(workspace: Path):
    assert (workspace / "resumate.yaml").exists()
    for skill_dir in (".agents/skills", ".claude/skills"):
        installed = {p.parent.name for p in (workspace / skill_dir).glob("*/SKILL.md")}
        assert installed == SKILLS
    for pointer in ("CLAUDE.md", "GEMINI.md"):
        assert (workspace / pointer).read_text().strip() == "@AGENTS.md"
    assert "Ada Lovelace" in (workspace / "master/resume.yaml").read_text()
    with pytest.raises(ResumateError, match="already"):
        init_workspace(workspace)


def test_bundled_skills_are_well_formed():
    skills = resources.files("resumate") / "skills"
    found = set()
    for folder in skills.iterdir():
        text = (folder / "SKILL.md").read_text(encoding="utf-8")
        meta = yaml.safe_load(text.split("---")[1])
        assert meta["name"] == folder.name
        assert 50 < len(meta["description"]) <= 1024
        assert "\u2013" not in text and "\u2014" not in text, folder.name  # house style
        found.add(folder.name)
    assert found == SKILLS
    reference = (skills / "resumate" / "SKILL.md").read_text(encoding="utf-8")
    for name in SKILLS - {"resumate"}:
        assert f"`{name}`" in reference  # the reference lists every skill


def test_install_skills_refreshes_without_removing(workspace: Path, monkeypatch):
    monkeypatch.chdir(workspace)
    extra = workspace / ".agents/skills/my-own-skill/SKILL.md"
    extra.parent.mkdir(parents=True)
    extra.write_text("mine")
    (workspace / ".claude/skills/resumate-apply/SKILL.md").write_text("stale")
    result = CliRunner().invoke(main, ["install-skills"])
    assert result.exit_code == 0, result.output
    assert extra.read_text() == "mine"
    assert "stale" not in (workspace / ".claude/skills/resumate-apply/SKILL.md").read_text()


def test_application_lifecycle(workspace: Path):
    app = new_application(workspace, "Acme, Inc.", "Staff Engineer", url="u", today=TODAY)
    assert app.name == "2026-10-22-acme-inc-staff-engineer"
    assert "company: Acme, Inc." in (app / "job.md").read_text()
    assert (app / "resume.yaml").read_text().startswith("# Tailored resume for Staff Engineer")
    assert load_resume(app / "resume.yaml").name == "Ada Lovelace"

    [listed] = list_applications(workspace)
    assert (listed.company, listed.status) == ("Acme, Inc.", "drafting")
    assert resolve_application(workspace, "acme") == app

    set_status(app, "applied")
    assert list_applications(workspace)[0].status == "applied"
    with pytest.raises(ResumateError):
        set_status(app, "ghosted")


# --- CLI -------------------------------------------------------------------------------


def test_cli_end_to_end(workspace: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(workspace)
    runner = CliRunner()

    result = runner.invoke(main, ["new", "Acme", "Platform Engineer"])
    assert result.exit_code == 0, result.output
    app = next((workspace / "applications").glob("*acme*"))

    resume = app / "resume.yaml"
    resume.write_text(
        resume.read_text().replace(
            "          - Mentored 5 engineers",
            "          # TODO(review): confirm count\n          - Mentored 5 engineers",
        )
    )

    result = runner.invoke(main, ["check", "acme"])
    assert result.exit_code == 0, result.output
    assert "TODO(review): confirm count" in result.output

    assert "TODO" not in result.output.replace("TODO(review): confirm count", "")
    answers = app / "answers.md"
    answers.write_text(answers.read_text() + "<!-- TODO(review): sponsorship? -->\n")
    result = runner.invoke(main, ["check", "acme"])
    assert "answers.md" in result.output and "sponsorship?" in result.output

    result = runner.invoke(main, ["build", "acme"])
    assert result.exit_code == 0, result.output
    assert (app / "out" / "Ada_Lovelace_Resume.pdf").exists()
    assert (app / "out" / "Ada_Lovelace_Cover_Letter.pdf").exists()

    result = runner.invoke(main, ["diff", "acme"])
    assert "+          # TODO(review): confirm count" in result.output

    result = runner.invoke(main, ["build", "master"])
    assert result.exit_code == 0, result.output


def test_cli_reports_errors_cleanly(workspace: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(workspace)
    (workspace / "master" / "resume.yaml").write_text("name: A\nsections: [{title: X, oops: 1}]\n")
    result = CliRunner().invoke(main, ["check", "master"])
    assert result.exit_code == 1
    assert "sections.0.oops" in result.output
    assert "Traceback" not in result.output


def test_master_resume_skips_the_page_limit(workspace: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(workspace)
    bullets = "\n".join(
        f"          - Delivered lab result {i} with a measured outcome" for i in range(50)
    )
    (workspace / "master" / "resume.yaml").write_text(
        "name: Ada Lovelace\ncontact:\n  email: ada@example.com\nsections:\n"
        "  - title: Experience\n    entries:\n      - title: Engineer\n        org: Lab\n"
        f"        bullets:\n{bullets}\n"
    )
    runner = CliRunner()
    master = runner.invoke(main, ["check", "master"])
    assert master.exit_code == 0, master.output
    assert "page" not in master.output.lower()

    app = new_application(workspace, "Acme", "Engineer", today=TODAY)
    # Drop the sample marker warning's noise: the copy has no marker. Page limit still applies.
    application = runner.invoke(main, ["check", app.name])
    assert application.exit_code == 1
    assert "pages" in application.output


def test_sample_master_is_flagged_until_replaced(workspace: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(workspace)
    runner = CliRunner()
    result = runner.invoke(main, ["check", "master"])
    assert "still the sample resume" in result.output
    assert "still the sample resume" in runner.invoke(main, ["new", "Acme", "Eng"]).output

    master = workspace / "master" / "resume.yaml"
    master.write_text(master.read_text().replace("# resumate:example\n", ""))
    assert "sample" not in runner.invoke(main, ["check", "master"]).output


def test_init_from_existing_resume(workspace: Path, tmp_path: Path):
    pdf = tmp_path / "old.pdf"
    render_resume(load_resume(workspace / "master" / "resume.yaml"), pdf, Style(layout="classic"))
    target = tmp_path / "career"
    result = CliRunner().invoke(main, ["init", str(target), "--from", str(pdf)])
    assert result.exit_code == 0, result.output
    assert (target / "master" / "source" / "old.pdf").exists()
    assert "ADA LOVELACE" in (target / "master" / "source" / "old.pdf.txt").read_text()


# --- ATS / Workday parse safety ---------------------------------------------------------

WORKDAY_YAML = """\
name: Ada Lovelace
contact:
  email: ada@example.com
  phone: (555) 123-4567
  location: Ann Arbor, MI
summary: Engineer who likes compilers.
sections:
  - title: Experience
    entries:
      - title: Associate Mechanic
        org: Round1 Bowling and Arcade
        location: Auburn Hills, MI
        start: May 2025
        end: August 2025
        bullets: [Fixed machines]
  - title: Education
    entries:
      - title: University of Michigan
        degree: Bachelor of Science in Engineering
        major: Computer Science
        location: Ann Arbor, MI
        dates: May 2026
"""


def _pdftotext(path: Path) -> list[str]:
    text = subprocess.run(
        ["pdftotext", str(path), "-"], capture_output=True, text=True, check=True
    ).stdout
    return [line.strip() for line in text.splitlines() if line.strip()]


def test_defaults_are_the_workday_tested_shape():
    style = Style()
    assert (style.layout, style.entry_heading, style.date_align) == ("modern", "stacked", "inline")


@pytest.mark.skipif(not shutil.which("pdftotext"), reason="needs poppler's pdftotext")
@pytest.mark.parametrize("layout", ["classic", "modern"])
def test_stacked_heading_and_labeled_degree(tmp_path: Path, layout: str):
    path = tmp_path / "r.yaml"
    path.write_text(WORKDAY_YAML)
    out = tmp_path / "r.pdf"
    render_resume(load_resume(path), out, Style(layout=layout))
    lines = _pdftotext(out)
    assert "Associate Mechanic | May 2025 - August 2025" in lines
    assert "Round1 Bowling and Arcade | Auburn Hills, MI" in lines
    assert "University of Michigan | May 2026" in lines
    assert "Bachelor of Science in Engineering | Ann Arbor, MI" in lines
    assert "Major: Computer Science" in lines
    # The summary sits under its own heading, before the first section.
    summary = next(n for n, line in enumerate(lines) if line.lower() == "summary")
    assert lines[summary + 1] == "Engineer who likes compilers."


@pytest.mark.skipif(not shutil.which("pdftotext"), reason="needs poppler's pdftotext")
def test_one_line_heading_uses_pipes(tmp_path: Path):
    path = tmp_path / "r.yaml"
    path.write_text(WORKDAY_YAML)
    out = tmp_path / "r.pdf"
    render_resume(load_resume(path), out, Style(layout="classic", entry_heading="one_line"))
    lines = _pdftotext(out)
    assert (
        "Associate Mechanic | Round1 Bowling and Arcade | Auburn Hills, MI | May 2025 - August 2025"
        in lines
    )
    assert "Major: Computer Science" in lines


def test_summary_heading_can_be_turned_off(tmp_path: Path):
    path = tmp_path / "r.yaml"
    path.write_text(WORKDAY_YAML + 'summary_title: ""\n')
    out = tmp_path / "r.pdf"
    render_resume(load_resume(path), out, Style())
    assert "SUMMARY" not in pdf_text(out)
    path.write_text(WORKDAY_YAML + "summary_title: Profile\n")
    render_resume(load_resume(path), out, Style())
    assert "PROFILE" in pdf_text(out)


def test_degree_and_org_are_exclusive():
    with pytest.raises(ValidationError, match="both org and degree"):
        Entry(title="U", org="X", degree="BS")


@pytest.mark.parametrize("layout", ["classic", "modern"])
def test_no_en_or_em_dashes_in_rendered_output(workspace: Path, tmp_path: Path, layout: str):
    from pypdf import PdfReader

    resume = load_resume(workspace / "master" / "resume.yaml")
    for heading in ("stacked", "one_line"):
        out = tmp_path / f"{heading}.pdf"
        render_resume(resume, out, Style(layout=layout, entry_heading=heading))
        meta = PdfReader(out).metadata
        everything = pdf_text(out) + str(meta.title) + str(meta.subject)
        assert "\u2013" not in everything and "\u2014" not in everything
        assert meta.title == "Ada Lovelace Resume"
    letter = tmp_path / "c.md"
    letter.write_text("---\ncompany: Acme\nrole: Engineer\n---\nHello.\n")
    out = tmp_path / "letter.pdf"
    render_cover_letter(load_cover_letter(letter), resume, out, Style(layout=layout))
    assert PdfReader(out).metadata.title == "Ada Lovelace Cover Letter | Engineer | Acme"


def test_check_passes_clean_workday_resume(tmp_path: Path):
    path = tmp_path / "resume.yaml"
    path.write_text(WORKDAY_YAML)
    findings, _ = check_resume(path, None)
    assert findings == []


def test_check_warns_about_workday_parse_risks(tmp_path: Path):
    path = tmp_path / "resume.yaml"
    path.write_text(
        "name: Ada Lovelace\n"
        "contact:\n  phone: +1 (555) 123-4567\n"
        "summary: May 2026 graduate \u2013 likes compilers.\n"
        "sections:\n  - title: Experience\n    entries:\n"
        "      - title: Technician\n        org: Sky Systems (contractor, on-call)\n"
        "        location: Detroit, MI\n        dates: 2026\n"
        "      - title: Trainer\n        org: Handshake\n        dates: 2026\n"
        "      - title: Analyst\n        org: Acme\n        location: Remote\n"
        "  - title: Education\n    entries:\n"
        "      - title: B.S.E. Computer Science\n        org: University of Michigan\n"
        "        location: Ann Arbor, MI\n"
        "      - title: State University\n        degree: Bachelor of Arts\n"
        "        location: Lansing, MI\n"
    )
    findings, _ = check_resume(path, None)
    messages = "\n".join(f.message for f in findings)
    assert all(f.level == "warning" for f in findings), messages
    assert "comma or parentheses" in messages
    assert "'Trainer' (Experience) has no location" in messages
    assert "'Remote' has no City, ST" in messages
    assert "looks like a degree" in messages
    assert "has a degree but no `major:`" in messages
    assert "summary contains a date ('May 2026')" in messages
    assert "starts with +1" in messages
    assert "en or em dashes" in messages


def test_remote_with_city_and_dash_in_comment_are_fine(tmp_path: Path):
    path = tmp_path / "resume.yaml"
    path.write_text(
        WORKDAY_YAML.replace("Auburn Hills, MI", "Remote, Detroit, MI")
        + "# a comment \u2014 with an em dash is never rendered\n"
    )
    findings, _ = check_resume(path, None)
    assert findings == []


def test_check_warns_about_dashes_in_cover_letter(tmp_path: Path):
    path = tmp_path / "cover_letter.md"
    path.write_text("---\ncompany: Acme\n---\nI build things \u2014 fast.\n")
    assert any("en or em dashes" in f.message for f in check_cover_letter(path, None, None))
    path.write_text("---\ncompany: Acme\n---\nI build things fast.\n<!-- note \u2014 -->\n")
    assert not any("dashes" in f.message for f in check_cover_letter(path, None, None))


def test_sample_master_has_no_parse_warnings(workspace: Path):
    findings, _ = check_resume(workspace / "master" / "resume.yaml", workspace)
    assert [f.message for f in findings if "sample resume" not in f.message] == []
