<input type="text" id="search" placeholder="Search Textbooks">
<button onclick="searchBooks()">Search</button>

<div id="results"></div>

<script>
  function searchBooks() {
    const query = document.getElementById('search').value;
    fetch(`https://www.googleapis.com/books/v1/volumes?q=${query}&key=AIzaSyC4aFyijjXKG9MsGeaxhf7KF9TOyTobQoc`)
      .then(response => response.json())
      .then(data => {
        const results = data.items.map(item => `
          <div>
            <h3>${item.volumeInfo.title}</h3>
            <p>${item.volumeInfo.authors}</p>
            <a href="${item.volumeInfo.previewLink}" target="_blank">Read more</a>
          </div>
        `).join('');
        document.getElementById('results').innerHTML = results;
      })
      .catch(error => console.error('Error:', error));
  }
</script>