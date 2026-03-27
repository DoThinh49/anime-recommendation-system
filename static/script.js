const animeInput = document.getElementById("animeInput");
const countInput = document.getElementById("countInput");
const recommendBtn = document.getElementById("recommendBtn");
const autocompleteList = document.getElementById("autocompleteList");
const resultsGrid = document.getElementById("resultsGrid");
const statusText = document.getElementById("statusText");

const animeDataElement = document.getElementById("animeData");
let allTitles = [];

if (animeDataElement) {
  try {
    const parsed = JSON.parse(animeDataElement.textContent || "[]");
    allTitles = Array.isArray(parsed) ? parsed : [];
  } catch (error) {
    allTitles = [];
  }
}

function clearAutocomplete() {
  autocompleteList.innerHTML = "";
  autocompleteList.classList.add("hidden");
}

function renderAutocomplete(matches) {
  autocompleteList.innerHTML = "";

  if (!matches.length) {
    clearAutocomplete();
    return;
  }

  matches.forEach((title) => {
    const item = document.createElement("div");
    item.className = "autocomplete-item";
    item.textContent = title;
    item.addEventListener("click", () => {
      animeInput.value = title;
      clearAutocomplete();
    });
    autocompleteList.appendChild(item);
  });

  autocompleteList.classList.remove("hidden");
}

function findMatches(keyword) {
  const text = keyword.trim().toLowerCase();
  if (!text) {
    return [];
  }

  return allTitles
    .filter((title) => title.toLowerCase().includes(text))
    .slice(0, 30);
}

function setStatus(message, isError = false) {
  statusText.textContent = message || "";
  statusText.classList.toggle("error", isError);
}

function renderResults(items) {
  resultsGrid.innerHTML = "";

  if (!items.length) {
    setStatus("Khong co ket qua goi y.", true);
    return;
  }

  const fragment = document.createDocumentFragment();

  items.forEach((anime, idx) => {
    const card = document.createElement("article");
    card.className = "anime-card";
    card.style.animationDelay = `${idx * 40}ms`;

    const image =
      anime.image_url || "https://via.placeholder.com/300x450?text=No+Image";

    card.innerHTML = `
            <img src="${image}" alt="${anime.title}" loading="lazy" referrerpolicy="no-referrer" onerror="this.src='https://via.placeholder.com/300x450?text=No+Image'">
            <div class="card-body">
                <h3>${anime.title}</h3>
                <p>${anime.genres || "Chua co thong tin the loai"}</p>
            </div>
        `;

    fragment.appendChild(card);
  });

  resultsGrid.appendChild(fragment);
  setStatus(`Da tim thay ${items.length} anime tuong tu.`);
}

async function fetchRecommendations() {
  const title = animeInput.value.trim();
  const topN = parseInt(countInput.value, 10) || 10;

  if (!title) {
    setStatus("Vui long nhap ten anime.", true);
    return;
  }

  setStatus("Dang tim goi y...");
  resultsGrid.innerHTML = "";

  try {
    const response = await fetch("/recommend", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ title, top_n: topN }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Khong the lay du lieu goi y.");
    }

    renderResults(data.recommendations || []);
  } catch (error) {
    setStatus(error.message, true);
  }
}

animeInput.addEventListener("input", (event) => {
  const matches = findMatches(event.target.value);
  renderAutocomplete(matches);
});

animeInput.addEventListener("focus", () => {
  const matches = findMatches(animeInput.value);
  renderAutocomplete(matches);
});

document.addEventListener("click", (event) => {
  if (!event.target.closest(".autocomplete-wrap")) {
    clearAutocomplete();
  }
});

recommendBtn.addEventListener("click", fetchRecommendations);

animeInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    fetchRecommendations();
  }
});
