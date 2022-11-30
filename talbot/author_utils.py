from .utils import parse_attributes, wrap, unwrap, compact, normalize_orcid, normalize_id
import re

def get_one_author(author):
    """parse one author string into CSL format"""
    # if author is a string
    if type(author) == str:
        author = { 'creatorName': author } 

    # malformed XML
    if type(author.get('creatorName', None)) == list:
        return None 

    name = (parse_attributes(author.get('creatorName', None)) or
        parse_attributes(author.get('contributorName', None)) or
        parse_attributes(author.get('name', None)))
    given_name = (parse_attributes(author.get('givenName', None)) or
        parse_attributes(author.get('given', None)))
    family_name = (parse_attributes(author.get('familyName', None)) or
        parse_attributes(author.get('family', None)))
    name = cleanup_author(name)
    if family_name and given_name:
        name = f"{family_name}, {given_name}"
    contributor_type = parse_attributes(author.get('contributorType', None))

    # name_type = (parse_attributes(author.get('creatorName', None), content: 'nameType, first: true) or 
    #    parse_attributes(author.get('contributorName', None), content: 'nameType')                                                                             first: true)
    # name_identifiers = Array.wrap(author.get('nameIdentifier', None)).map do |ni|
      #   if ni['nameIdentifierScheme'] == 'ORCID'
      #     {
      #       'nameIdentifier' => normalize_orcid(ni['__content__']),
      #       'schemeUri' => 'https://orcid.org',
      #       'nameIdentifierScheme' => 'ORCID'
      #     }.compact
      #   elsif ni['schemeURI'].present?
      #     {
      #       'nameIdentifier' => ni['schemeURI'].to_s + ni['__content__'].to_s,
      #       'schemeUri' => ni['schemeURI'].to_s,
      #       'nameIdentifierScheme' => ni['nameIdentifierScheme']
      #     }.compact
      #   else
      #     {
      #       'nameIdentifier' => ni['__content__'],
      #       'schemeUri' => None,
      #       'nameIdentifierScheme' => ni['nameIdentifierScheme']
      #     }.compact
      #   end
      # end.presence

      # Crossref metadata
    if name_identifiers is None and author.get('ORCID', None):
          name_identifiers = [{
              'nameIdentifier': normalize_orcid(author.get('ORCID', None)),
              'schemeUri': 'https://orcid.org',
              'nameIdentifierScheme': 'ORCID' }]


    # if name_type is None and Array.wrap(name_identifiers).find { |ni| ni['nameIdentifierScheme'] == 'ORCID' }:
    #     name_type = 'Personal'
    # elif name_type is None and Array.wrap(name_identifiers).find { |ni| %w(ISNI ROR).include? ni['nameIdentifierScheme'] }:
    #     name_type = 'Organizational'
    # elif name_type is None and is_personal_name?(given_name: given_name, name: name) && name.to_s.exclude?(';'):
    #     name_type = 'Personal'

    # author = { 
    #     'nameType': name_type,
    #     'name': name,
    #     'givenName': given_name,
    #     'familyName': family_name,
    #     'nameIdentifiers': name_identifiers,
    #     'affiliation': get_affiliations(author.get('affiliation', None)),
    #     'contributorType': contributor_type }

    if family_name:
        return author

    # if name_type == 'Personal':
    #     names = HumanName(name)
    #     parsed_name = names.first
        
    #     if parsed_name:
    #         given_name = parsed_name.first
    #         family_name = parsed_name.last
    #         name = [family_name, given_name].join(', ')
    #     else
    #         given_name = None
    #         family_name = None

    #     return { 
    #         'nameType': 'Personal',
    #         'name': name,
    #         'givenName': given_name,
    #         'familyName': family_name,
    #         'nameIdentifiers': name_identifiers,
    #         'affiliation': get_affiliations(author.get('affiliation', None)),
    #         'contributorType': contributor_type }
    # else
    #     return { 
    #         'nameType': name_type,
    #         'name': name,
    #         'nameIdentifiers': name_identifiers,
    #         'affiliation': get_affiliations(author.get('affiliation', None)),
    #         'contributorType': contributor_type }
  
def cleanup_author(author):
    if author is None:
        return None

    # detect pattern "Smith J.", but not "Smith, John K."
    if not ',' in author:
        author = re.sub(r'/([A-Z]\.)?(-?[A-Z]\.)$/', ', \1\2', author)

    # remove spaces around hyphens
    author = author.replace(' - ', '-')

    # remove non-standard space characters
    author = re.sub('/[ \t\r\n\v\f]/', ' ', author)
    return author

def get_authors(authors):
    """parse array of author strings into CSL format"""
    return list(map(lambda author: get_one_author(author), authors))

def authors_as_string(authors):
    """convert CSL authors list to string, e.g. for bibtex"""
    if authors is None:
        return None
    formatted_authors = []
    for author in wrap(authors):
        if author.get('familyName', None):
            a = f"{author['familyName']}, {author['givenName']}"
            formatted_authors.append(a)
        elif author.get('type', None) == 'Person':
            a = author['name']
            formatted_authors.append(a)
        elif author.get('name', None):
            a = f"{{{author['name']}}}"
            formatted_authors.append(a)   
    return ' and '.join(formatted_authors)

def get_affiliations(affiliations):
    """parse array of affiliation strings into CSL format"""
    if affiliations is None:
        return None

    formatted_affiliations = []
    for affiliation in wrap(affiliations):
        affiliation_identifier = None
        if type(affiliation) is str:
            name = affiliation
            affiliation_identifier_scheme = None
            scheme_uri = None
        else:
            if affiliation.get('affiliationIdentifier', None) is not None:
                affiliation_identifier = affiliation['affiliationIdentifier']
                if affiliation.get('schemeURI', None) is not None:
                    schemeURI = affiliation['schemeURI'] if affiliation['schemeURI'].endswith('/') else "{affiliation['schemeURI']}/"
                affiliation_identifier = normalize_id(schemeURI + affiliation_identifier) if (not affiliation_identifier.startswith('https://') and schemeURI is not None) else normalize_id(affiliation_identifier)
            name = affiliation['name'] or affiliation['__content__']
            affiliation_identifier_scheme = affiliation.get('affiliationIdentifierScheme', None)
            scheme_uri = affiliation.get('SchemeURI', None)

        if name is None:
            continue

        formatted_affiliations.append({
             'name': name,
             'affiliationIdentifier': affiliation_identifier,
             'affiliationIdentifierScheme': affiliation_identifier_scheme,
             'schemeUri': scheme_uri })

    return compact(formatted_affiliations)
 
