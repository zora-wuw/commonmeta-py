"""Test base utils"""
import pytest
from commonmeta.base_utils import (
    parse_attributes,
    presence,
    compact,
    wrap,
    unwrap,
    sanitize,
    parse_xmldict,
)


def test_wrap():
    "wrap"
    # None
    assert [] == wrap(None)
    # dict
    assert [{"name": "test"}] == wrap({"name": "test"})
    # list
    assert [{"name": "test"}] == wrap([{"name": "test"}])


def test_unwrap():
    "unwrap"
    # None
    assert None is unwrap([])
    # dict
    assert {"name": "test"} == unwrap([{"name": "test"}])
    # list
    assert [{"name": "test"}, {"name": "test2"}] == unwrap(
        [{"name": "test"}, {"name": "test2"}]
    )


def test_presence():
    "presence"
    assert None is presence("")
    assert None is presence([])
    assert None is presence({})
    assert "test" == presence("test")
    assert [1] == presence([1])
    assert {"test": 1} == presence({"test": 1})


def test_compact():
    "compact"
    assert {"name": "test"} == compact({"name": "test", "other": None})
    assert None is compact(None)


def test_parse_attributes():
    "parse_attributes"
    # string
    assert "10.5061/DRYAD.8515" == parse_attributes("10.5061/DRYAD.8515")
    # dict
    assert "10.5061/DRYAD.8515" == parse_attributes({"#text": "10.5061/DRYAD.8515"})
    # dict with other keys
    assert "10.5061/DRYAD.8515" == parse_attributes(
        {"name": "10.5061/DRYAD.8515"}, content="name"
    )
    # list of dicts
    assert ["10.5061/DRYAD.8515", "10.5061/DRYAD.8516"] == parse_attributes(
        [{"#text": "10.5061/DRYAD.8515"}, {"#text": "10.5061/DRYAD.8516"}]
    )
    # first in list of dicts
    assert "10.5061/DRYAD.8515" == parse_attributes(
        [{"#text": "10.5061/DRYAD.8515"}, {"#text": "10.5061/DRYAD.8516"}], first=True
    )
    # list of strings
    assert ["10.5061/DRYAD.8515", "10.5061/DRYAD.8516"] == parse_attributes(
        ["10.5061/DRYAD.8515", "10.5061/DRYAD.8516"]
    )
    # None
    assert None is parse_attributes(None)


def test_parse_xmldict():
    """parse dict generated by xmltodict"""
    # ORCID
    orcid = {"@authenticated": "true", "#text": "https://orcid.org/0000-0003-4606-044X"}
    assert {"@id": "https://orcid.org/0000-0003-4606-044X"} == parse_xmldict(
        orcid, element_name="@id"
    )
    assert "https://orcid.org/0000-0003-4606-044X" == parse_xmldict(
        orcid, ignored_attributes="@authenticated"
    )
    assert {"@id": "https://orcid.org/0000-0003-4606-044X"} == parse_xmldict(
        orcid, element_name="@id", ignored_attributes="@authenticated"
    )
    assert "https://orcid.org/0000-0003-4606-044X" == parse_xmldict(orcid["#text"])
    # funding
    fundgroup = {
        "@name": "fundgroup",
        "assertion": {"@name": "funder_name", "#text": "SystemsX"},
    }
    assert {"fundgroup": {"funder_name": "SystemsX"}} == parse_xmldict(fundgroup)
    fundgroup = {
        "@name": "fundgroup",
        "assertion": {
            "@name": "funder_name",
            "assertion": {
                "@name": "funder_identifier",
                "@provider": "crossref",
                "#text": "501100006390",
            },
            "#text": "University of Lausanne",
        },
    }
    # assert {'fundgroup': {'funder_name': 'University of Lausanne', 'funder_identifier': '501100006390'}} == parse_xmldict(fundgroup, ignored_attributes='@provider')
    funder_identifier = {
        "@name": "funder_identifier",
        "#text": "https://doi.org/10.13039/100006959",
    }
    assert {"funder_identifier": "https://doi.org/10.13039/100006959"} == parse_xmldict(
        funder_identifier
    )
    funder_identifier = {
        "assertion": {
            "@name": "funder_identifier",
            "#text": "https://doi.org/10.13039/100006959",
        }
    }
    assert {"funder_identifier": "https://doi.org/10.13039/100006959"} == parse_xmldict(
        funder_identifier
    )
    funding = {
        "@name": "fundgroup",
        "@xmlns": {"": "http://www.crossref.org/fundref.xsd"},
        "assertion": {
            "@name": "funder_name",
            "assertion": {
                "@name": "funder_identifier",
                "#text": "https://doi.org/10.13039/100006959",
            },
            "#text": "U.S. Forest Service",
        },
    }
    formatted_funding = {
        "fundgroup": {
            "funder_name": "U.S. Forest Service",
            "funder_identifier": "https://doi.org/10.13039/100006959",
        }
    }
    assert formatted_funding == parse_xmldict(funding)
    funding = {
        "@name": "fundgroup",
        "assertion": [
            {
                "@name": "funder_name",
                "assertion": {
                    "@name": "funder_identifier",
                    "#text": "https://doi.org/10.13039/100000002",
                },
                "#text": "NIH",
            },
            {"@name": "award_number", "#text": "R01 NS089482"},
            {"@name": "award_number", "#text": "R01 NS077869"},
            {"@name": "award_number", "#text": "P01 MH070306"},
            {"@name": "award_number", "#text": "P40 OD013117"},
            {"@name": "award_number", "#text": "T32 OD011089"},
        ],
    }
    formatted_funding = {
        "fundgroup": [
            {
                "funder_name": "NIH",
                "funder_identifier": "https://doi.org/10.13039/100000002",
            },
            {"award_number": "R01 NS089482"},
            {"award_number": "R01 NS077869"},
            {"award_number": "P01 MH070306"},
            {"award_number": "P40 OD013117"},
            {"award_number": "T32 OD011089"},
        ]
    }
    assert formatted_funding == parse_xmldict(funding)


def test_sanitize():
    """Sanitize HTML"""
    text = 'In 1998 <strong>Tim Berners-Lee</strong> coined the term <a href="https://www.w3.org/Provider/Style/URI">cool URIs</a>'
    content = "In 1998 <strong>Tim Berners-Lee</strong> coined the term cool URIs"
    assert content == sanitize(text)

    text = 'In 1998 <strong>Tim Berners-Lee</strong> coined the term <a href="https://www.w3.org/Provider/Style/URI">cool URIs</a>'
    content = 'In 1998 Tim Berners-Lee coined the term <a href="https://www.w3.org/Provider/Style/URI">cool URIs</a>'
    assert content == sanitize(text, tags={"a"})
