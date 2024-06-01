from flask import Flask, render_template, request
import spacy
import networkx as nx
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
nlp = spacy.load('en_core_web_sm')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['text']
    doc = nlp(text)
    edges = []
    for token in doc:
        for child in token.children:
            edges.append((token.lower_, child.lower_))

    graph = nx.DiGraph(edges)
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=1500, edge_color='gray')
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return render_template('result.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
