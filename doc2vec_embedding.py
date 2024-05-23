import numpy as np
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import os
from PyPDF2 import PdfReader


def create_doc2vec_embeddings(folder_path, vector_size=100, window=5, min_count=2, epochs=20):
    """
    This function trains a Doc2Vec model on a folder of PDF articles.

    Args:
        folder_path (str): Path to the folder containing the PDF articles.
        vector_size (int, optional): Dimensionality of the document vectors.
        window (int, optional): Context window size for local context.
        min_count (int, optional): Minimum word count for vocabulary inclusion.
        epochs (int, optional): Number of training epochs.

    Returns:
        gensim.models.doc2vec.Doc2Vec: The trained Doc2Vec model.
    """
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'rb') as f:
                pdf_reader = PdfReader(f)
                full_text = ""
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    full_text += text  # Concatenate text from all pages

                documents.append(full_text)

    # Preprocess documents
    processed_docs = [word_tokenize(doc.lower()) for doc in documents]

    # Add document tags
    tagged_docs = [TaggedDocument(doc, [i]) for i, doc in enumerate(processed_docs)]

    # Define Doc2Vec model
    model = Doc2Vec(vector_size=vector_size, window=window, min_count=min_count, epochs=epochs)

    # Build vocabulary
    model.build_vocab(tagged_docs)

    # Train the Doc2Vec model
    model.train(tagged_docs, total_examples=model.corpus_count, epochs=model.epochs)

    return model, tagged_docs


if __name__ == "__main__":
    output_folder = "publications"

    model, tagged_docs = create_doc2vec_embeddings(output_folder, vector_size=300, epochs=40)

    # sanity check
    ranks = []
    second_ranks = []
    for doc_id in range(len(tagged_docs)):
        inferred_vector = model.infer_vector(tagged_docs[doc_id].words)
        sims = model.dv.most_similar([inferred_vector], topn=len(model.dv))
        rank = [docid for docid, sim in sims].index(doc_id)
        ranks.append(rank)

        second_ranks.append(sims[1])

    import collections
    counter = collections.Counter(ranks)
    print(counter)

    # visualization

    from sklearn.manifold import TSNE
    import matplotlib.pyplot as plt


    doc_labels = range(0, len(tagged_docs))

    # Get document vectors
    doc_vectors = [model.docvecs[label] for label in doc_labels]

    for i in range(1, 10):
        # Reduce dimensions using t-SNE
        tsne_model = TSNE(n_components=2, perplexity=i)  # Adjust perplexity as needed
        tsne_data = tsne_model.fit_transform(np.array(doc_vectors))

        # Create a scatter plot
        plt.figure(figsize=(8, 6))
        for label, vec in zip(doc_labels, tsne_data):
            plt.scatter(vec[0], vec[1], label=label)
        plt.title("t-SNE Visualization of Doc2Vec Embeddings")
        plt.legend()
        plt.show()
