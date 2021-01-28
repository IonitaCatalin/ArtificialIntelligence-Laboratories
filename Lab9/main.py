import lightrdf

if __name__ == '__main__':

    search_for = str(input())

    parsing_file = open('ontology.owl', 'rb')
    doc = lightrdf.RDFDocument(parsing_file, parser=lightrdf.xml.PatternParser)

    for triple in doc.search_triples(None, None, None):
        if triple[0].find(search_for):
            print(triple)
            break
