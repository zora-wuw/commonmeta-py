# pylint: disable=invalid-name
"""Citeproc writer tests"""
import json
import pytest

from commonmeta import Metadata


@pytest.mark.vcr
# def test_dataset():
#     "Dataset"
#     input = "https://doi.org/10.5061/DRYAD.8515"
#     subject = Metadata(input, via='datacite')
#     assert subject.id == "https://doi.org/10.5061/dryad.8515"
#     assert subject.types.get('bibtex') == 'dataset'
# it 'Dataset' do
#       input = 'https://doi.org/10.5061/DRYAD.8515'
#       subject = described_class.new(input: input, from: 'datacite')
#       expect(subject.valid?).to be true
#       json = JSON.parse(subject.citeproc)
#       expect(json['type']).to eq('dataset')
#       expect(json['id']).to eq('https://doi.org/10.5061/dryad.8515')
#       expect(json['DOI']).to eq('10.5061/dryad.8515')
#       expect(json['title']).to eq('Data from: A new malaria agent in African hominids.')
#       expect(json['author']).to eq([{ 'family' => 'Ollomo', 'given' => 'Benjamin' },
#                                     { 'family' => 'Durand', 'given' => 'Patrick' },
#                                     { 'family' => 'Prugnolle', 'given' => 'Franck' },
#                                     { "literal"=>"Douzery, Emmanuel J. P."},
#                                     { 'family' => 'Arnathau', 'given' => 'Céline' },
#                                     { 'family' => 'Nkoghe', 'given' => 'Dieudonné' },
#                                     { 'family' => 'Leroy', 'given' => 'Eric' },
#                                     { 'family' => 'Renaud', 'given' => 'François' }])
#       expect(json['publisher']).to eq('Dryad')
#       expect(json['issued']).to eq('date-parts' => [[2011]])
#       expect(json['submitted'].nil?).to be(true)
#       expect(json['copyright']).to eq('Creative Commons Zero v1.0 Universal')
#     end
#     it 'BlogPosting' do
#       input = 'https://doi.org/10.5438/4K3M-NYVG'
#       subject = described_class.new(input: input, from: 'datacite')
#       expect(subject.valid?).to be true
#       json = JSON.parse(subject.citeproc)
#       expect(json['type']).to eq('article-journal')
#       expect(json['id']).to eq('https://doi.org/10.5438/4k3m-nyvg')
#       expect(json['DOI']).to eq('10.5438/4k3m-nyvg')
#       expect(json['title']).to eq('Eating your own Dog Food')
#       expect(json['author']).to eq([{ 'family' => 'Fenner', 'given' => 'Martin' }])
#       expect(json['publisher']).to eq('DataCite')
#       expect(json['issued']).to eq('date-parts' => [[2016, 12, 20]])
#     end
#     it 'BlogPosting DataCite JSON' do
#       input = "#{fixture_path}datacite.json"
#       subject = described_class.new(input: input, from: 'datacite_json')
#       json = JSON.parse(subject.citeproc)
#       expect(json['type']).to eq('article-journal')
#       expect(json['id']).to eq('https://doi.org/10.5438/4k3m-nyvg')
#       expect(json['DOI']).to eq('10.5438/4k3m-nyvg')
#       expect(json['title']).to eq('Eating your own Dog Food')
#       expect(json['author']).to eq([{ 'family' => 'Fenner', 'given' => 'Martin' }])
#       expect(json['publisher']).to eq('DataCite')
#       expect(json['issued']).to eq('date-parts' => [[2016, 12, 20]])
#     end
#     it 'BlogPosting schema.org' do
#       input = 'https://blog.front-matter.io/posts/eating-your-own-dog-food/'
#       subject = described_class.new(input: input, from: 'schema_org')
#       json = JSON.parse(subject.citeproc)
#       expect(json['type']).to eq('article-newspaper')
#       expect(json['id']).to eq('https://doi.org/10.53731/r79vxn1-97aq74v-ag58n')
#       expect(json['DOI']).to eq('10.53731/r79vxn1-97aq74v-ag58n')
#       expect(json['title']).to eq('Eating your own Dog Food')
#       expect(json['author']).to eq([{ 'family' => 'Fenner', 'given' => 'Martin' }])
#       expect(json['publisher']).to eq('Front Matter')
#       expect(json['issued']).to eq('date-parts' => [[2016, 12, 20]])
#     end
#     it 'Another dataset' do
#       input = '10.26301/qdpd-2250'
#       subject = described_class.new(input: input, from: 'datacite')
#       json = JSON.parse(subject.citeproc)
#       expect(json['type']).to eq('dataset')
#       expect(json['id']).to eq('https://doi.org/10.26301/qdpd-2250')
#       expect(json['DOI']).to eq('10.26301/qdpd-2250')
#       expect(json['title']).to eq('USS Pampanito Submarine')
#       expect(json['author']).to eq([{ 'literal' => 'USS Pampanito' },
#                                     { 'literal' => 'Autodesk' },
#                                     { 'literal' => 'Topcon' },
#                                     { 'literal' => '3D Robotics' },
#                                     { 'literal' => 'CyArk' },
#                                     { 'literal' => 'San Francisco Maritime National Park Association' }])
#       expect(json['publisher']).to eq('OpenHeritage3D')
#       expect(json['issued']).to eq('date-parts' => [[2020]])
#     end
def test_doi_with_data_citation():
    "doi with data citation"
    subject = Metadata("10.7554/elife.01567")
    assert subject.id == "https://doi.org/10.7554/elife.01567"
    assert subject.type == "JournalArticle"

    citeproc = json.loads(subject.citeproc())
    assert citeproc.get("type") == "article-journal"
    assert citeproc.get("DOI") == "10.7554/elife.01567"
    assert (
        citeproc.get("title")
        == "Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth"
    )
    assert citeproc.get("author") == [
        {"family": "Sankar", "given": "Martial"},
        {"family": "Nieminen", "given": "Kaisa"},
        {"family": "Ragni", "given": "Laura"},
        {"family": "Xenarios", "given": "Ioannis"},
        {"family": "Hardtke", "given": "Christian S"},
    ]
    assert citeproc.get("publisher") == "eLife Sciences Publications, Ltd"

    assert citeproc.get("issued") == {"date-parts": [[2014, 2, 11]]}
    assert citeproc.get("URL") == "https://elifesciences.org/articles/01567"
    assert citeproc.get("container-title") == "eLife"
    assert citeproc.get("volume") == "3"
    assert citeproc.get("page") is None
    assert citeproc.get("language") == "en"
    assert citeproc.get(
        "copyright") == "Creative Commons Attribution 3.0 Unported"


#     it 'software' do
#       input = 'https://doi.org/10.6084/m9.figshare.4906367.v1'
#       subject = described_class.new(input: input, from: 'datacite')
#       json = JSON.parse(subject.citeproc)
#       expect(json['type']).to eq('article')
#       expect(json['DOI']).to eq('10.6084/m9.figshare.4906367.v1')
#       expect(json['title']).to eq('Scimag catalogue of LibGen as of January 1st, 2014')
#       expect(json['copyright']).to eq('Creative Commons Zero v1.0 Universal')
#     end

#     it 'software w/version' do
#       input = 'https://doi.org/10.5281/zenodo.2598836'
#       subject = described_class.new(input: input, from: 'datacite')
#       json = JSON.parse(subject.citeproc)
#       expect(json['type']).to eq('book')
#       expect(json['DOI']).to eq('10.5281/zenodo.2598836')
#       expect(json['version']).to eq('1.0.0')
#       expect(json['copyright']).to eq('Open Access')
#     end

#     it 'software w/version from datacite_json' do
#       input = "#{fixture_path}datacite_software_version.json"
#       subject = described_class.new(input: input, from: 'datacite_json')
#       json = JSON.parse(subject.citeproc)
#       expect(json['type']).to eq('book')
#       expect(json['DOI']).to eq('10.5281/ZENODO.2598836')
#       expect(json['version']).to eq('1.0.0')
#       expect(json['copyright']).to eq('Open Access')
#     end

#     it 'multiple abstracts' do
#       input = 'https://doi.org/10.12763/ona1045'
#       subject = described_class.new(input: input, from: 'datacite')
#       json = JSON.parse(subject.citeproc)
#       expect(json['type']).to eq('article-journal')
#       expect(json['DOI']).to eq('10.12763/ona1045')
#       expect(json['abstract']).to eq("Le code est accompagné de commentaires de F. A. Vogel, qui signe l'épitre dédicatoire")
#     end


def test_with_pages():
    "with pages"
    subject = Metadata("10.1155/2012/291294")
    assert subject.id == "https://doi.org/10.1155/2012/291294"
    assert subject.type == "JournalArticle"

    citeproc = json.loads(subject.citeproc())
    assert citeproc.get("type") == "article-journal"
    assert citeproc.get("DOI") == "10.1155/2012/291294"
    assert citeproc.get(
        "URL") == "http://www.hindawi.com/journals/pm/2012/291294"
    assert (
        citeproc.get("title")
        == "Delineating a Retesting Zone Using Receiver Operating Characteristic Analysis on Serial QuantiFERON Tuberculosis Test Results in US Healthcare Workers"
    )
    assert citeproc.get("author") == [
        {"family": "Thanassi", "given": "Wendy"},
        {"family": "Noda", "given": "Art"},
        {"family": "Hernandez", "given": "Beatriz"},
        {"family": "Newell", "given": "Jeffery"},
        {"family": "Terpeluk", "given": "Paul"},
        {"family": "Marder", "given": "David"},
        {"family": "Yesavage", "given": "Jerome A."},
    ]
    assert citeproc.get("publisher") == "Hindawi Limited"
    assert citeproc.get("issued") == {"date-parts": [[2012]]}
    assert citeproc.get("container-title") == "Pulmonary Medicine"
    assert citeproc.get("volume") == "2012"
    assert citeproc.get("page") == "1-7"
    assert citeproc.get("language") == "en"
    assert citeproc.get(
        "copyright") == "Creative Commons Attribution 3.0 Unported"


def test_only_first_page():
    "only first page"
    subject = Metadata("10.1371/journal.pone.0214986")
    assert subject.id == "https://doi.org/10.1371/journal.pone.0214986"
    assert subject.type == "JournalArticle"

    citeproc = json.loads(subject.citeproc())
    assert citeproc.get("type") == "article-journal"
    assert citeproc.get("DOI") == "10.1371/journal.pone.0214986"
    assert citeproc.get(
        "URL") == "https://dx.plos.org/10.1371/journal.pone.0214986"
    assert citeproc.get(
        "title") == "River metrics by the public, for the public"
    assert citeproc.get("author") == [
        {"family": "Weber", "given": "Matthew A."},
        {"family": "Ringold", "given": "Paul L."},
    ]
    assert citeproc.get("publisher") == "Public Library of Science (PLoS)"
    assert citeproc.get("issued") == {"date-parts": [[2019, 5, 8]]}
    assert citeproc.get("container-title") == "PLOS ONE"
    assert citeproc.get("volume") == "14"
    assert citeproc.get("page") == "e0214986"
    assert citeproc.get("language") == "en"
    assert citeproc.get("copyright") == "Creative Commons Zero v1.0 Universal"


def test_missing_creator():
    "missing creator"
    subject = Metadata("10.3390/publications6020015")
    assert subject.id == "https://doi.org/10.3390/publications6020015"
    assert subject.type == "JournalArticle"

    citeproc = json.loads(subject.citeproc())
    assert citeproc.get("type") == "article-journal"
    assert citeproc.get("DOI") == "10.3390/publications6020015"
    assert citeproc.get("URL") == "https://www.mdpi.com/2304-6775/6/2/15"
    assert (
        citeproc.get("title")
        == "Converting the Literature of a Scientific Field to Open Access through Global Collaboration: The Experience of SCOAP3 in Particle Physics"
    )
    assert citeproc.get("author") == [
        {"family": "Kohls", "given": "Alexander"},
        {"family": "Mele", "given": "Salvatore"},
    ]
    assert citeproc.get("publisher") == "MDPI AG"
    assert citeproc.get("issued") == {"date-parts": [[2018, 4, 9]]}
    assert citeproc.get("container-title") == "Publications"
    assert citeproc.get("volume") == "6"
    assert citeproc.get("page") == "15"
    assert citeproc.get("language") == "en"
    assert citeproc.get(
        "copyright") == "Creative Commons Attribution 4.0 International"


#     it 'container title' do
#       input = 'https://doi.org/10.6102/ZIS146'
#       subject = described_class.new(input: input, from: 'datacite')
#       json = JSON.parse(subject.citeproc)
#       expect(json['type']).to eq('article-journal')
#       expect(json['id']).to eq('https://doi.org/10.6102/zis146')
#       expect(json['DOI']).to eq('10.6102/zis146')
#       expect(json['title']).to eq('Deutsche Version der Positive and Negative Affect Schedule (PANAS)')
#       expect(json['author']).to eq([{ 'family' => 'Janke', 'given' => 'S.' },
#                                     { 'family' => 'Glöckner-Rist', 'given' => 'A.' }])
#       expect(json['container-title']).to eq('Zusammenstellung sozialwissenschaftlicher Items und Skalen (ZIS)')
#       expect(json['issued']).to eq('date-parts' => [[2012]])
#     end

#     it 'Crossref DOI' do
#       input = "#{fixture_path}crossref.bib"
#       subject = described_class.new(input: input, from: 'bibtex')
#       json = JSON.parse(subject.citeproc)
#       expect(json['type']).to eq('article-journal')
#       expect(json['id']).to eq('https://doi.org/10.7554/elife.01567')
#       expect(json['DOI']).to eq('10.7554/elife.01567')
#       expect(json['URL']).to eq('http://elifesciences.org/lookup/doi/10.7554/eLife.01567')
#       expect(json['title']).to eq('Automated quantitative histology reveals vascular morphodynamics during Arabidopsis hypocotyl secondary growth')
#       expect(json['author']).to eq([{ 'family' => 'Sankar', 'given' => 'Martial' },
#                                     { 'family' => 'Nieminen', 'given' => 'Kaisa' },
#                                     { 'family' => 'Ragni', 'given' => 'Laura' },
#                                     { 'family' => 'Xenarios', 'given' => 'Ioannis' },
#                                     { 'family' => 'Hardtke', 'given' => 'Christian S' }])
#       expect(json['container-title']).to eq('eLife')
#       expect(json['issued']).to eq('date-parts' => [[2014]])
#     end

#     it 'author is organization' do
#       input = "#{fixture_path}gtex.xml"
#       subject = described_class.new(input: input, from: 'datacite')
#       json = JSON.parse(subject.citeproc)
#       expect(json['id']).to eq('https://doi.org/10.25491/9hx8-ke93')
#       expect(json['author']).to eq([{ 'literal' => 'The GTEx Consortium' }])
#     end

#     it 'maremma' do
#       input = 'https://github.com/datacite/maremma'
#       subject = described_class.new(input: input, from: 'codemeta')
#       json = JSON.parse(subject.citeproc)
#       expect(json['type']).to eq('article-journal')
#       expect(json['id']).to eq('https://doi.org/10.5438/qeg0-3gm3')
#       expect(json['DOI']).to eq('10.5438/qeg0-3gm3')
#       expect(json['title']).to eq('Maremma: a Ruby library for simplified network calls')
#       expect(json['author']).to eq([{ 'family' => 'Fenner', 'given' => 'Martin' }])
#       expect(json['publisher']).to eq('DataCite')
#       expect(json['issued']).to eq('date-parts' => [[2017, 2, 24]])
#       expect(json['copyright']).to eq('MIT License')
#     end

#     it 'keywords subject scheme' do
#       input = 'https://doi.org/10.1594/pangaea.721193'
#       subject = described_class.new(input: input, from: 'datacite')
#       json = JSON.parse(subject.citeproc)
#       expect(json['type']).to eq('dataset')
#       expect(json['id']).to eq('https://doi.org/10.1594/pangaea.721193')
#       expect(json['DOI']).to eq('10.1594/pangaea.721193')
#       expect(json['categories']).to include('animalia',
#                                             'bottles or small containers/aquaria (&lt;20 l)')
#       expect(json['copyright']).to eq('Creative Commons Attribution 3.0 Unported')
#     end


def test_organization_author():
    "organization author"
    subject = Metadata("10.1186/s13742-015-0103-4")
    assert subject.id == "https://doi.org/10.1186/s13742-015-0103-4"
    assert subject.type == "JournalArticle"

    citeproc = json.loads(subject.citeproc())
    assert citeproc.get("type") == "article-journal"
    assert citeproc.get("DOI") == "10.1186/s13742-015-0103-4"
    assert (
        citeproc.get("URL")
        == "https://academic.oup.com/gigascience/article-lookup/doi/10.1186/s13742-015-0103-4"
    )
    assert (
        citeproc.get("title")
        == "Discovery, genotyping and characterization of structural variation and novel sequence at single nucleotide resolution from de novo genome assemblies on a population scale"
    )
    assert citeproc.get("author") == [
        {"family": "Liu", "given": "Siyang"},
        {"literal": "The Genome Denmark Consortium"},
        {"family": "Huang", "given": "Shujia"},
        {"family": "Rao", "given": "Junhua"},
        {"family": "Ye", "given": "Weijian"},
        {"family": "Krogh", "given": "Anders"},
        {"family": "Wang", "given": "Jun"},
    ]
    assert citeproc.get("publisher") == "Oxford University Press (OUP)"
    assert citeproc.get("issued") == {"date-parts": [[2015, 12]]}
    assert citeproc.get("container-title") == "GigaScience"
    assert citeproc.get("volume") == "4"
    assert citeproc.get("page") is None
    assert citeproc.get("language") == "en"
    assert citeproc.get("copyright") is None


#     it 'interactive resource without dates' do
#       input = 'https://doi.org/10.34747/g6yb-3412'
#       subject = described_class.new(input: input, from: 'datacite')
#       json = JSON.parse(subject.citeproc)
#       expect(json['type']).to eq('article')
#       expect(json['DOI']).to eq('10.34747/g6yb-3412')
#       expect(json['issued']).to eq('date-parts' => [[2019]])
