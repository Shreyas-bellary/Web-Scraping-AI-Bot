

window.addEventListener("DOMContentLoaded", function () {
  const heroSection = document.getElementById("hero");
  const heroGif = document.querySelector(".hero-gif");
});


// Sample data for comments
const comments = [
  { author: "John", message: "Great article!", timestamp: "2023-06-27 10:30:00" },
  { author: "Jane", message: "Well written!", timestamp: "2023-06-27 11:15:00" },
];


// Execute the functions when the DOM content is loaded
document.addEventListener("DOMContentLoaded", function () {
  generateNewsArticles();
});


// Function to generate comment section
function generateCommentSection() {
  const commentSection = document.getElementById("comment-section");
  commentSection.innerHTML = "";

  comments.forEach((comment) => {
    const commentElement = document.createElement("div");
    commentElement.classList.add("comment");

    const authorElement = document.createElement("span");
    authorElement.classList.add("author");
    authorElement.textContent = comment.author;

    const messageElement = document.createElement("p");
    messageElement.textContent = comment.message;

    const timestampElement = document.createElement("span");
    timestampElement.classList.add("timestamp");
    timestampElement.textContent = comment.timestamp;

    commentElement.appendChild(authorElement);
    commentElement.appendChild(messageElement);
    commentElement.appendChild(timestampElement);

    commentSection.appendChild(commentElement);
  });
}

// Event listener for comment form submission
const commentForm = document.getElementById("comment-form");
commentForm.addEventListener("submit", function (e) {
  e.preventDefault();

  const authorInput = document.getElementById("author-input");
  const messageInput = document.getElementById("message-input");

  const author = authorInput.value;
  const message = messageInput.value;

  if (author && message) {
    const timestamp = new Date().toLocaleString();
    const newComment = { author, message, timestamp };

    comments.push(newComment);

    // Clear input fields
    authorInput.value = "";
    messageInput.value = "";

    // Regenerate comment section
    generateCommentSection();
  }
});

function removeUnsupportedCharacters(text) {
  // Remove unsupported characters using the 'replace' method
  const cleanedText = text.replace(/�/g, '');

  // Or remove unsupported characters using regular expressions
  // const cleanedText = text.replace(/[^\x00-\x7F]+/g, '');

  return cleanedText;
}
function generateNewsArticles() {
  const newsSection = document.getElementById("news");
  
  Papa.parse("output.csv", {
    download: true,
    header: true,
    encoding: "utf8", // Specify the correct character encoding
    complete: function(results) {
     
      // Access the parsed CSV data
      const data = results.data;

      // Generate news articles
      data.forEach((row, i) => {
        const articleBox = document.createElement("div");
        articleBox.classList.add("box");

        const articleTitle = document.createElement("h2");
        articleTitle.classList.add("article-title","hover-3");

        // Create a link for the heading
        const headingLink = document.createElement("a");
        headingLink.href = row.Link; // Assuming the link is in a column named "link"
        headingLink.textContent = row.Text; // Assuming the heading is in a column named "heading"
        articleTitle.appendChild(headingLink);

        const articleContent = document.createElement("p");
        articleContent.classList.add("article-content");
        articleContent.textContent = removeUnsupportedCharacters(row.Summarized_Data); // Assuming the summary is in a column named "summary"

        const sentiment = document.createElement("p");
        sentiment.classList.add("sentiment");
        sentiment.textContent = row.Sentiment; // Assuming the sentiment is in a column named "sentiment"

        articleBox.appendChild(articleTitle);
        articleBox.appendChild(articleContent);
        articleBox.appendChild(sentiment);
        newsSection.appendChild(articleBox);
      });
    }
  });
}






