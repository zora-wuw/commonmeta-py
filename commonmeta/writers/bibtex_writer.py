"""Bibtex writer for commonmeta-py"""
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.customization import author

from ..utils import pages_as_string
from ..base_utils import compact
from ..author_utils import authors_as_string
from ..date_utils import get_month_from_date, get_iso8601_date, MONTH_SHORT_NAMES
from ..doi_utils import doi_from_url
from ..constants import CM_TO_BIB_TRANSLATIONS, Commonmeta


def write_bibtex(metadata: Commonmeta) -> str:
    """Write bibtex"""
    container = metadata.container if metadata.container else {}
    date_published = get_iso8601_date(metadata.date.get("published", None))

    id_ = metadata.id
    type_ = CM_TO_BIB_TRANSLATIONS.get(metadata.type, "misc")
    abstract = metadata.descriptions[0].get("description", None) if metadata.descriptions else None
    author = authors_as_string(metadata.creators)
    license_ = str(metadata.license.get("url")) if metadata.license else None
    doi = doi_from_url(metadata.id)
    issn = container.get("identifier", None) if container.get("identifierType", None) == "ISSN" else None
    issue = container.get("issue", None)
    journal = container.get("title", None) if type_ not in ["inbook", "inproceedings"] else None
    booktitle = container.get("title", None) if type_ in ["inbook", "inproceedings"] else None
    language = metadata.language
    month = get_month_from_date(date_published)
    pages = pages_as_string(container)
    publisher = metadata.publisher.get("name", None) if type_ not in ["article", "phdthesis"] else None
    institution = metadata.publisher.get("name", None) if type_ == "phdthesis" else None
    title = metadata.titles[0].get("title", None)
    url = metadata.url
    year = date_published[:4] if date_published else None

    bib_database = BibDatabase()
    bib_database.entries = [
        compact(
            {
                "ID": id_,
                "ENTRYTYPE": type_,
                "abstract": abstract,
                "author": author,
                "copyright": license_,
                "doi": doi,
                "issn": issn,
                "issue": issue,
                "journal": journal,
                "booktitle": booktitle,
                "language": language,
                "month": month,
                "pages": pages,
                "publisher": publisher,
                "institution": institution,
                "title": title,
                "url": url,
                "urldate": date_published,
                "year": year,
            }
        )
    ]
    writer = BibTexWriter()
    writer.common_strings = True
    writer.indent = "    "
    bibtex_str = writer.write(bib_database)

    # Hack to remove curly braces around month names
    for month_name in MONTH_SHORT_NAMES:
        bibtex_str = bibtex_str.replace(f"{{{month_name}}}", month_name)
    return bibtex_str
