"""Test utils"""
from os import path
import pytest

from commonmeta.utils import (
    dict_to_spdx,
    normalize_orcid,
    validate_orcid,
    normalize_id,
    normalize_ids,
    normalize_cc_url,
    normalize_issn,
    from_citeproc,
    find_from_format_by_id,
    find_from_format_by_string,
    find_from_format_by_filename,
    find_from_format_by_ext,
    from_schema_org,
    from_schema_org_creators,
    pages_as_string,
    subjects_as_string,
    to_citeproc,
    to_ris,
    to_schema_org,
    to_schema_org_container,
    to_schema_org_creators,
    to_schema_org_identifiers,
    github_from_url,
    github_as_codemeta_url,
    github_as_cff_url,
    github_as_repo_url,
)
from commonmeta.base_utils import wrap


def test_dict_to_spdx_id():
    "dict_to_spdx id"
    assert {
        "rights": "Creative Commons Attribution 4.0 International",
        "rightsUri": "https://creativecommons.org/licenses/by/4.0/legalcode",
        "rightsIdentifier": "cc-by-4.0",
        "rightsIdentifierScheme": "SPDX",
        "schemeUri": "https://spdx.org/licenses/",
    } == dict_to_spdx({"rightsIdentifier": "CC-BY-4.0"})
    assert {
        "rights": "Apache License 2.0",
        "rightsUri": "http://www.apache.org/licenses/LICENSE-2.0",
        "rightsIdentifier": "apache-2.0",
        "rightsIdentifierScheme": "SPDX",
        "schemeUri": "https://spdx.org/licenses/",
    } == dict_to_spdx({"rightsIdentifier": "Apache-2.0"})


def test_dict_to_spdx_url():
    "dict_to_spdx url"
    assert {
        "rights": "Creative Commons Attribution 4.0 International",
        "rightsUri": "https://creativecommons.org/licenses/by/4.0/legalcode",
        "rightsIdentifier": "cc-by-4.0",
        "rightsIdentifierScheme": "SPDX",
        "schemeUri": "https://spdx.org/licenses/",
    } == dict_to_spdx(
        {"rightsUri": "https://creativecommons.org/licenses/by/4.0/legalcode"}
    )


def test_dict_to_spdx_not_found():
    "dict_to_spdx not found"
    assert {"rightsUri": "info:eu-repo/semantics/openAccess"} == dict_to_spdx(
        {"rightsUri": "info:eu-repo/semantics/openAccess"}
    )


def test_validate_orcid():
    "validate_orcid"
    assert "0000-0002-2590-225X" == validate_orcid(
        "http://orcid.org/0000-0002-2590-225X"
    )
    # orcid https
    assert "0000-0002-2590-225X" == validate_orcid(
        "https://orcid.org/0000-0002-2590-225X"
    )
    # orcid id
    assert "0000-0002-2590-225X" == validate_orcid("0000-0002-2590-225X")
    # orcid www
    assert "0000-0002-2590-225X" == validate_orcid(
        "https://www.orcid.org/0000-0002-2590-225X"
    )
    # orcid with spaces
    assert "0000-0002-1394-3097" == validate_orcid("0000 0002 1394 3097")
    # orcid sandbox
    assert "0000-0002-2590-225X" == validate_orcid(
        "http://sandbox.orcid.org/0000-0002-2590-225X"
    )
    # orcid sandbox https
    assert "0000-0002-2590-225X" == validate_orcid(
        "https://sandbox.orcid.org/0000-0002-2590-225X"
    )
    # orcid wrong id format
    assert None is validate_orcid("0000-0002-1394-309")
    # None
    assert None is validate_orcid(None)


def test_normalize_orcid():
    "normalize_orcid"
    assert "https://orcid.org/0000-0002-2590-225X" == normalize_orcid(
        "http://orcid.org/0000-0002-2590-225X"
    )
    # orcid https
    assert "https://orcid.org/0000-0002-2590-225X" == normalize_orcid(
        "https://orcid.org/0000-0002-2590-225X"
    )
    # orcid id
    assert "https://orcid.org/0000-0002-2590-225X" == normalize_orcid(
        "0000-0002-2590-225X"
    )
    # invalid orcid id
    assert None == normalize_orcid("0002-2590-225X")
    # None
    assert None is normalize_orcid(None)


def test_normalize_id():
    "normalize_id"
    assert "https://doi.org/10.5061/dryad.8515" == normalize_id("10.5061/DRYAD.8515")
    # doi as url
    assert "https://doi.org/10.5061/dryad.8515" == normalize_id(
        "http://dx.doi.org/10.5061/DRYAD.8515"
    )
    # url
    assert "https://blog.datacite.org/eating-your-own-dog-food" == normalize_id(
        "https://blog.datacite.org/eating-your-own-dog-food/"
    )
    # cff url
    assert (
        "https://github.com/citation-file-format/ruby-cff/blob/main/CITATION.cff"
        == normalize_id(
            "https://github.com/citation-file-format/ruby-cff/blob/main/CITATION.cff"
        )
    )
    # codemeta url
    assert (
        "https://github.com/datacite/metadata-reports/blob/master/software/codemeta.json"
        == normalize_id(
            "https://github.com/datacite/metadata-reports/blob/master/software/codemeta.json"
        )
    )
    # http url
    assert "https://blog.datacite.org/eating-your-own-dog-food" == normalize_id(
        "http://blog.datacite.org/eating-your-own-dog-food/"
    )
    # url with utf-8
    # assert 'http://www.xn--8ws00zhy3a.com/eating-your-own-dog-food' == normalize_id('http://www.詹姆斯.com/eating-your-own-dog-food/')
    # ftp
    assert None is normalize_id("ftp://blog.datacite.org/eating-your-own-dog-food/")
    # invalid url
    assert None is normalize_id("http://")
    # bytes object
    assert "https://blog.datacite.org/eating-your-own-dog-food" == normalize_id(
        b"https://blog.datacite.org/eating-your-own-dog-food/"
    )
    # string
    assert None is normalize_id("eating-your-own-dog-food")
    # filename
    assert None is normalize_id("crossref.xml")
    # sandbox via url
    assert (
        "https://handle.stage.datacite.org/10.20375/0000-0001-ddb8-7"
        == normalize_id("https://handle.stage.datacite.org/10.20375/0000-0001-ddb8-7")
    )
    # sandbox via options
    assert (
        "https://handle.stage.datacite.org/10.20375/0000-0001-ddb8-7"
        == normalize_id("10.20375/0000-0001-ddb8-7", sandbox=True)
    )
    # None
    assert None is normalize_id(None)


def test_normalize_ids():
    "normalize_ids"
    # doi
    ids = [
        {"@type": "CreativeWork", "@id": "https://doi.org/10.5438/0012"},
        {"@type": "CreativeWork", "@id": "https://doi.org/10.5438/55E5-T5C0"},
    ]
    response = [
        {
            "relatedIdentifier": "10.5438/0012",
            "relatedIdentifierType": "DOI",
            "resourceTypeGeneral": "Text",
        },
        {
            "relatedIdentifier": "10.5438/55e5-t5c0",
            "relatedIdentifierType": "DOI",
            "resourceTypeGeneral": "Text",
        },
    ]
    assert response == normalize_ids(ids=ids)
    # url
    ids = [
        {
            "@type": "CreativeWork",
            "@id": "https://blog.datacite.org/eating-your-own-dog-food/",
        }
    ]
    response = [
        {
            "relatedIdentifier": "https://blog.datacite.org/eating-your-own-dog-food",
            "relatedIdentifierType": "URL",
            "resourceTypeGeneral": "Text",
        }
    ]
    assert response == normalize_ids(ids=ids)


def test_normalize_cc_url():
    """normalize_cc_url"""
    assert "https://creativecommons.org/licenses/by/4.0/legalcode" == normalize_cc_url(
        "https://creativecommons.org/licenses/by/4.0/"
    )
    assert (
        "https://creativecommons.org/publicdomain/zero/1.0/legalcode"
        == normalize_cc_url("https://creativecommons.org/publicdomain/zero/1.0")
    )
    # http scheme
    assert (
        "https://creativecommons.org/publicdomain/zero/1.0/legalcode"
        == normalize_cc_url("http://creativecommons.org/publicdomain/zero/1.0")
    )
    assert None is normalize_cc_url(None)
    assert None is normalize_cc_url(
        {"url": "https://creativecommons.org/licenses/by/4.0/legalcode"}
    )


def test_normalize_issn():
    """normalize_issn"""
    # from list
    string = [
        {"media_type": "print", "#text": "13040855"},
        {"media_type": "electronic", "#text": "21468427"},
    ]
    assert "2146-8427" == normalize_issn(string)
    # from empty list
    string = []
    assert None is normalize_issn(string)
    # from dict
    string = {"media_type": "electronic", "#text": "21468427"}
    assert "2146-8427" == normalize_issn(string)
    # from string
    string = "2146-8427"
    assert "2146-8427" == normalize_issn(string)


def test_from_citeproc():
    "from_citeproc"
    assert [
        {
            "@type": "Person",
            "affiliation": [
                {
                    "name": "Department of Plant Molecular Biology, University of Lausanne, Lausanne, Switzerland"
                }
            ],
            "familyName": "Sankar",
            "givenName": "Martial",
            "name": "Martial Sankar",
        }
    ] == from_citeproc(
        [
            {
                "given": "Martial",
                "family": "Sankar",
                "sequence": "first",
                "affiliation": [
                    {
                        "name": "Department of Plant Molecular Biology, University of Lausanne, Lausanne, Switzerland"
                    }
                ],
            }
        ]
    )
    assert [
        {
            "@type": "Organization",
            "name": "University of Lausanne",
        }
    ] == from_citeproc(
        [
            {
                "literal": "University of Lausanne",
                "sequence": "first",
            }
        ]
    )
    assert [
        {
            "@type": "Organization",
            "name": "University of Lausanne",
        }
    ] == from_citeproc(
        [
            {
                "name": "University of Lausanne",
                "sequence": "first",
            }
        ]
    )


def find_from_format():
    """find_from_format"""


def test_find_from_format_by_id():
    "find_from_format_by_id"
    assert "crossref" == find_from_format_by_id("10.1371/journal.pone.0042793")
    assert "datacite" == find_from_format_by_id("https://doi.org/10.5061/dryad.8515")
    assert "medra" == find_from_format_by_id("10.1392/roma081203")
    assert "kisti" == find_from_format_by_id(
        "https://doi.org/10.5012/bkcs.2013.34.10.2889"
    )
    assert "jalc" == find_from_format_by_id("https://doi.org/10.11367/grsj1979.12.283")
    assert "op" == find_from_format_by_id("https://doi.org/10.2903/j.efsa.2018.5239")
    # cff
    assert "cff" == find_from_format_by_id(
        "https://github.com/citation-file-format/ruby-cff/blob/main/CITATION.cff"
    )
    # codemeta
    assert "codemeta" == find_from_format_by_id(
        "https://github.com/datacite/maremma/blob/master/codemeta.json"
    )
    # schema_org
    assert "schema_org" == find_from_format_by_id(
        "https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/GAOC03"
    )


def test_find_from_format_by_filename():
    """find_from_format_by_filename"""
    assert "cff" == find_from_format_by_filename("CITATION.cff")
    assert None is find_from_format_by_filename("text.docx")


def test_find_from_format_by_ext():
    """find_from_format_by_ext"""
    assert "bibtex" == find_from_format_by_ext(".bib")
    assert "ris" == find_from_format_by_ext(".ris")
    assert None is find_from_format_by_ext(".docx")


def test_find_from_format_by_string():
    """find_from_format_by_string"""
    # datacite
    filepath = path.join(path.dirname(__file__), "fixtures", "datacite.json")
    with open(filepath, encoding="utf-8") as file:
        string = file.read()
    assert "datacite" == find_from_format_by_string(string)
    # crossref
    filepath = path.join(path.dirname(__file__), "fixtures", "crossref.json")
    with open(filepath, encoding="utf-8") as file:
        string = file.read()
    assert "crossref" == find_from_format_by_string(string)
    # schema_org
    filepath = path.join(path.dirname(__file__), "fixtures", "schema_org_topmed.json")
    with open(filepath, encoding="utf-8") as file:
        string = file.read()
    assert "schema_org" == find_from_format_by_string(string)
    # datacite_xml
    filepath = path.join(path.dirname(__file__), "fixtures", "datacite_dataset.xml")
    with open(filepath, encoding="utf-8") as file:
        string = file.read()
    assert "datacite_xml" == find_from_format_by_string(string)
    # crossref_xml
    filepath = path.join(path.dirname(__file__), "fixtures", "crossref.xml")
    with open(filepath, encoding="utf-8") as file:
        string = file.read()
    assert "crossref_xml" == find_from_format_by_string(string)
    # ris
    filepath = path.join(path.dirname(__file__), "fixtures", "crossref.ris")
    with open(filepath, encoding="utf-8") as file:
        string = file.read()
    assert "ris" == find_from_format_by_string(string)
    # bibtex
    filepath = path.join(path.dirname(__file__), "fixtures", "pure.bib")
    with open(filepath, encoding="utf-8") as file:
        string = file.read()
    assert "bibtex" == find_from_format_by_string(string)
    # cff
    filepath = path.join(path.dirname(__file__), "fixtures", "CITATION.cff")
    with open(filepath, encoding="utf-8") as file:
        string = file.read()
    assert "cff" == find_from_format_by_string(string)
    # codemeta
    filepath = path.join(path.dirname(__file__), "fixtures", "codemeta_v2.json")
    with open(filepath, encoding="utf-8") as file:
        string = file.read()
    assert "codemeta" == find_from_format_by_string(string)
    # citeproc
    filepath = path.join(path.dirname(__file__), "fixtures", "citeproc.json")
    with open(filepath, encoding="utf-8") as file:
        string = file.read()
    assert "citeproc" == find_from_format_by_string(string)
    assert None is find_from_format_by_string('{"foo": "bar"}')
    assert None is find_from_format_by_string(None)


def test_from_schema_org():
    "from_schema_org"
    author = {
        "@type": "Person",
        "@id": "http://orcid.org/0000-0003-1419-2405",
        "givenName": "Martin",
        "familyName": "Fenner",
        "name": "Martin Fenner",
    }
    assert {
        "givenName": "Martin",
        "familyName": "Fenner",
        "name": "Martin Fenner",
        "type": "Person",
        "id": "http://orcid.org/0000-0003-1419-2405",
    } == from_schema_org(author)


def test_from_schema_org_creators():
    "from_schema_org creators"
    authors = [
        {
            "@type": "Person",
            "@id": "http://orcid.org/0000-0003-1419-2405",
            "givenName": "Martin",
            "familyName": "Fenner",
            "name": "Martin Fenner",
            "affiliation": {
                "@id": "https://ror.org/04wxnsj81",
                "name": "DataCite",
                "@type": "Organization",
            },
        }
    ]
    response = from_schema_org_creators(authors)
    assert response == [
        {
            "givenName": "Martin",
            "familyName": "Fenner",
            "affiliation": {
                "#text": "DataCite",
                "affiliationIdentifier": "https://ror.org/04wxnsj81",
                "affiliationIdentifierScheme": "ROR",
                "schemeUri": "https://ror.org/",
            },
            "nameIdentifier": [
                {
                    "#text": "http://orcid.org/0000-0003-1419-2405",
                    "nameIdentifierScheme": "ORCID",
                    "schemeUri": "https://orcid.org",
                }
            ],
            "creatorName": {"nameType": "Personal", "#text": "Martin Fenner"},
        }
    ]
    # without affiliation
    authors = [
        {
            "@type": "Person",
            "@id": "http://orcid.org/0000-0003-1419-2405",
            "givenName": "Martin",
            "familyName": "Fenner",
            "name": "Martin Fenner",
        }
    ]
    response = from_schema_org_creators(authors)
    assert response == [
        {
            "givenName": "Martin",
            "familyName": "Fenner",
            "nameIdentifier": [
                {
                    "#text": "http://orcid.org/0000-0003-1419-2405",
                    "nameIdentifierScheme": "ORCID",
                    "schemeUri": "https://orcid.org",
                }
            ],
            "creatorName": {"nameType": "Personal", "#text": "Martin Fenner"},
        }
    ]


def test_pages_as_string():
    """pages as string"""
    container = {
        "firstPage": "2832",
        "identifier": "0012-9658",
        "identifierType": "ISSN",
        "issue": "11",
        "lastPage": "2841",
        "title": "Ecology",
        "type": "Journal",
        "volume": "87",
    }
    assert "2832-2841" == pages_as_string(container)
    container = {
        "type": "Journal",
        "title": "Publications",
        "firstPage": "15",
        "issue": "2",
        "volume": "6",
        "identifier": "2304-6775",
        "identifierType": "ISSN",
    }
    assert "15" == pages_as_string(container)
    assert None is pages_as_string(None)


def test_subjects_as_string():
    """subjects as string"""
    subjects = [
        {"subject": "Ecology", "scheme": "http://id.loc.gov/authorities/subjects"},
        {"subject": "Biodiversity", "scheme": "http://id.loc.gov/authorities/subjects"},
    ]
    assert "Ecology, Biodiversity" == subjects_as_string(subjects)
    assert None is subjects_as_string(None)


def test_to_citeproc():
    """to citeproc"""
    authors = [
        {
            "ORCID": "http://orcid.org/0000-0003-0077-4738",
            "givenName": "Matt",
            "familyName": "Jones",
        }
    ]
    organization_authors = [{"name": "University of California, Berkeley"}]
    assert [{"family": "Jones", "given": "Matt"}] == to_citeproc(authors)
    assert [{"literal": "University of California, Berkeley"}] == to_citeproc(
        organization_authors
    )


def test_to_ris():
    """to ris"""
    authors = [
        {
            "ORCID": "http://orcid.org/0000-0003-0077-4738",
            "givenName": "Matt",
            "familyName": "Jones",
        }
    ]
    organization_authors = [{"name": "University of California, Berkeley"}]
    assert ["Jones, Matt"] == to_ris(authors)
    assert ["University of California, Berkeley"] == to_ris(organization_authors)


def test_to_schema_org():
    """to schema.org"""
    author = {
        "id": "http://orcid.org/0000-0003-0077-4738",
        "type": "Person",
        "givenName": "Matt",
        "familyName": "Jones",
    }
    organization_author = {
        "id": "https://ror.org/01an7q238",
        "type": "Organization",
        "name": "University of California, Berkeley",
    }

    assert {
        "givenName": "Matt",
        "familyName": "Jones",
        "@type": "Person",
        "@id": "http://orcid.org/0000-0003-0077-4738",
    } == to_schema_org(author)
    assert {
        "name": "University of California, Berkeley",
        "@type": "Organization",
        "@id": "https://ror.org/01an7q238",
    } == to_schema_org(organization_author)
    assert None is to_schema_org(None)


def test_to_schema_org_container():
    """to schema.org container"""
    pangaea = {
        "identifier": "https://www.pangaea.de/",
        "identifierType": "URL",
        "title": "PANGAEA",
        "type": "DataRepository",
    }
    assert {
        "@id": "https://www.pangaea.de/",
        "@type": "Periodical",
        "name": "PANGAEA",
    } == to_schema_org_container(pangaea)
    assert None is to_schema_org_container("Pangaea")
    assert None is to_schema_org_container(None)


def test_to_schema_org_creators():
    """to schema.org creators"""
    authors = [{"givenName": "Matt", "familyName": "Jones", "nameType": "Personal"}]
    organization_authors = [{"name": "University of California, Berkeley"}]
    assert [
        {
            "givenName": "Matt",
            "familyName": "Jones",
            "name": "Matt Jones",
            "@type": "Person",
        }
    ] == to_schema_org_creators(authors)
    assert [
        {"name": "University of California, Berkeley", "@type": "Organization"}
    ] == to_schema_org_creators(organization_authors)


def test_to_schema_org_identifiers():
    """to schema.org identifiers"""
    identifiers = [
        {
            "identifier": "10.5061/dryad.8515",
            "identifierType": "DOI",
        }
    ]
    assert [
        {"@type": "PropertyValue", "propertyID": "DOI", "value": "10.5061/dryad.8515"}
    ] == to_schema_org_identifiers(identifiers)
    assert [] == to_schema_org_identifiers(wrap(None))


def test_github_from_url():
    """github from url"""
    url = "https://github.com/datacite/bolognese"
    response = github_from_url(url)
    assert response == {"owner": "datacite", "repo": "bolognese"}
    # organization
    url = "https://github.com/datacite"
    response = github_from_url(url)
    assert response == {"owner": "datacite"}
    # not a repo
    url = "https://docs.github.com/en/get-started"
    assert {} == github_from_url(url)
    # codemeta file
    url = "https://github.com/datacite/metadata-reports/blob/master/software/codemeta.json"
    response = github_from_url(url)
    assert response == {
        "owner": "datacite",
        "repo": "metadata-reports",
        "release": "master",
        "path": "software/codemeta.json",
    }
    # cff file
    url = "https://github.com/citation-file-format/ruby-cff/blob/main/CITATION.cff"
    response = github_from_url(url)
    assert response == {
        "owner": "citation-file-format",
        "repo": "ruby-cff",
        "release": "main",
        "path": "CITATION.cff",
    }
    # branch
    url = "https://github.com/front-matter/Headline/tree/schlagzeile"
    response = github_from_url(url)
    assert response == {
        "owner": "front-matter",
        "repo": "Headline",
        "release": "schlagzeile",
    }


def test_github_as_codemeta_url():
    """github as codemeta url"""
    url = "https://github.com/datacite/bolognese"
    response = github_as_codemeta_url(url)
    assert (
        response
        == "https://raw.githubusercontent.com/datacite/bolognese/master/codemeta.json"
    )


def test_github_as_cff_url():
    """github as cff url"""
    url = "https://github.com/citation-file-format/ruby-cff"
    response = github_as_cff_url(url)
    assert (
        response
        == "https://raw.githubusercontent.com/citation-file-format/ruby-cff/main/CITATION.cff"
    )


def test_github_as_codemeta_url_file():
    """github as codemeta url file"""
    url = "https://github.com/datacite/metadata-reports/blob/master/software/codemeta.json"
    response = github_as_codemeta_url(url)
    assert (
        response
        == "https://raw.githubusercontent.com/datacite/metadata-reports/master/software/codemeta.json"
    )


def test_github_as_repo_url():
    """github as repo url"""
    # codemeta.json
    url = "https://github.com/datacite/metadata-reports/blob/master/software/codemeta.json"
    response = github_as_repo_url(url)
    assert response == "https://github.com/datacite/metadata-reports"
    # CITATION.cff
    url = "https://raw.githubusercontent.com/citation-file-format/ruby-cff/main/CITATION.cff"
    response = github_as_repo_url(url)
    assert response == "https://github.com/citation-file-format/ruby-cff"
    # any other file
    url = "https://github.com/mkdocs/mkdocs/blob/master/mkdocs/localization.py"
    response = github_as_repo_url(url)
    assert response == "https://github.com/mkdocs/mkdocs"
    # github repo url
    url = "https://github.com/datacite/metadata-reports"
    response = github_as_repo_url(url)
    assert response == "https://github.com/datacite/metadata-reports"
