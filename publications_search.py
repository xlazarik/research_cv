import requests
from scholarly import scholarly
import os

def list_publications(researcher_name, output_folder):
    """
    Searches Google Scholar for the researcher's publications and retrieves basic information.

    Args:
        researcher_name (str): Name of the researcher to search for.
        output_folder (str): Path to the folder where publication information will be saved.
    """

    search_query = scholarly.search_author(researcher_name)
    author = next(search_query)  # Get the first author result
    author = scholarly.fill(author)
    scholarly.pprint(author)

    publications = author['publications']

    #publications = author.publications
    num_publications = len(publications)

    print(f"Found {num_publications} publications for {researcher_name}.")

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    files = []
    for i, publication in enumerate(publications):
        # Extract basic publication information
        publication = scholarly.fill(publication)
        title = None
        #title = publication["title"] if "title" in publication else None
        title = publication["bib"]['title'] if "title" in publication["bib"] and title is None else None

        year = None
        #year = publication["pub_year"] if "pub_year" in publication else None
        year = publication["bib"]['pub_year'] if "pub_year" in publication["bib"] and year is None else None

        url = None
        url = publication["pub_url"]
        #url = publication["bib"]['url'] if 'url' in publication["bib"] and url is None else None


        filename = f"{year} >> {title}: {url}"
        files.append(filename)
        print(f"\rProcessed {i}/{len(publications)}")


    for file in sorted(files):
        print(file)

    #journal = None
    #journal = publication

    filepath = os.path.join(output_folder, "output.txt")
    with open(filepath, 'w', encoding='utf-8') as file:
        for file_data in sorted(files):
            file.write(file_data + "\n")

    print(f"Saved publication information to: {filepath}")

if __name__ == "__main__":
    researcher_name = "Barbora Kozlikova"
    output_folder = "publications/"

    list_publications(researcher_name, output_folder)
