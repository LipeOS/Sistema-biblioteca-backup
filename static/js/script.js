document.getElementById('search-btn').addEventListener('click', function() {
    const query = document.getElementById('search-query').value;
    fetch(`/search_books?query=${query}`)
        .then(response => response.json())
        .then(data => {
            const resultsContainer = document.getElementById('search-results');
            resultsContainer.innerHTML = '';
            data.forEach(book => {
                const bookElement = document.createElement('div');
                bookElement.classList.add('book');
                bookElement.innerHTML = `
                    <h3>${book[1]}</h3>
                    <p>Autor: ${book[2]}</p>
                    <p>Gênero: ${book[3]}</p>
                    <p>Editora: ${book[4]}</p>
                    <p>Ano: ${book[5]}</p>
                    <p>Quantidade: ${book[6]}</p>
                    <form action="/edit_book/${book[0]}" method="POST">
                        <label for="quantidade">Quantidade</label>
                        <input type="number" name="quantidade" value="${book[6] || 0}" required>
                        <button type="submit" class="btn">Editar</button>
                    </form>
                    <form action="/delete_book/${book[0]}" method="POST">
                        <button type="submit" class="btn btn-danger">Excluir</button>
                    </form>
                `;
                resultsContainer.appendChild(bookElement);
            });
        });
});
