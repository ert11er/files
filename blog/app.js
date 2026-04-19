const state = {
    posts: [],
    currentTag: null,
    searchQuery: '',
};

const dom = {
    postList: document.getElementById('post-list'),
    postContent: document.getElementById('post-content'),
    mdRender: document.getElementById('md-render'),
    searchInput: document.getElementById('search-input'),
    tagCloud: document.getElementById('tag-cloud'),
    loading: document.getElementById('loading'),
    backButton: document.getElementById('back-button'),
    themeToggle: document.getElementById('theme-toggle'),
};

// --- Initialization ---
async function init() {
    setupTheme();
    setupEventListeners();
    await loadPosts();
    handleRouting();
}

// --- Theme Logic ---
function setupTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.body.setAttribute('data-theme', savedTheme);
}

dom.themeToggle.addEventListener('click', () => {
    const currentTheme = document.body.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    document.body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
});

// --- Data Fetching ---
async function loadPosts() {
    dom.loading.classList.remove('hidden');
    try {
        const response = await fetch('/files/blog/posts.json');
        state.posts = await response.json();
        renderTagCloud();
        renderPostList();
    } catch (error) {
        console.error('Error loading posts:', error);
        dom.postList.innerHTML = '<p>Yazılar yüklenirken bir hata oluştu.</p>';
    } finally {
        dom.loading.classList.add('hidden');
    }
}

async function loadMarkdown(slug) {
    dom.loading.classList.remove('hidden');
    try {
        const response = await fetch(`/files/blog/posts/${slug}.md`);
        const text = await response.text();

        // Remove yaml frontmatter if present
        const cleanText = text.replace(/^---[\s\S]*?---/, '');

        dom.mdRender.innerHTML = marked.parse(cleanText);
        showView('post');
        window.scrollTo(0, 0);
    } catch (error) {
        console.error('Error loading markdown:', error);
        dom.mdRender.innerHTML = '<p>İçerik yüklenirken bir hata oluştu.</p>';
    } finally {
        dom.loading.classList.add('hidden');
    }
}

// --- Rendering ---
function renderPostList() {
    const filtered = state.posts.filter(post => {
        const matchesSearch = post.title.toLowerCase().includes(state.searchQuery.toLowerCase()) ||
            post.description.toLowerCase().includes(state.searchQuery.toLowerCase());
        const matchesTag = !state.currentTag || post.tags.includes(state.currentTag);
        return matchesSearch && matchesTag;
    });

    if (filtered.length === 0) {
        dom.postList.innerHTML = '<p class="no-posts">Eşleşen not bulunamadı.</p>';
        return;
    }

    dom.postList.innerHTML = filtered.map(post => `
        <div class="post-entry" onclick="location.hash = '#/post/${post.slug}'">
            <h2>${post.title}</h2>
            <div class="post-meta">
                <span>📅 ${post.date}</span>
                <span class="post-tags">${post.tags.map(t => `<span class="tag-inline">#${t}</span>`).join(' ')}</span>
            </div>
            <p class="post-description">${post.description}</p>
        </div>
    `).join('');
}

function renderTagCloud() {
    const allTags = new Set();
    state.posts.forEach(p => p.tags.forEach(t => allTags.add(t)));

    dom.tagCloud.innerHTML = `
        <span class="tag ${!state.currentTag ? 'active' : ''}" onclick="filterByTag(null)">Tümü</span>
        ${Array.from(allTags).map(tag => `
            <span class="tag ${state.currentTag === tag ? 'active' : ''}" onclick="filterByTag('${tag}')">${tag}</span>
        `).join('')}
    `;
}

// --- Actions ---
window.filterByTag = (tag) => {
    state.currentTag = tag;
    renderTagCloud();
    renderPostList();
    if (location.hash !== '') location.hash = '';
};

function setupEventListeners() {
    dom.searchInput.addEventListener('input', (e) => {
        state.searchQuery = e.target.value;
        renderPostList();
    });

    dom.backButton.addEventListener('click', () => {
        location.hash = '';
    });

    window.addEventListener('hashchange', handleRouting);
}

function handleRouting() {
    const hash = location.hash;
    if (hash.startsWith('#/post/')) {
        const slug = hash.replace('#/post/', '');
        loadMarkdown(slug);
    } else {
        showView('list');
        renderPostList();
    }
}

function showView(view) {
    if (view === 'list') {
        dom.postList.classList.remove('hidden');
        dom.postContent.classList.add('hidden');
        dom.tagCloud.classList.remove('hidden');
        dom.searchInput.parentElement.classList.remove('hidden');
    } else {
        dom.postList.classList.add('hidden');
        dom.postContent.classList.remove('hidden');
        dom.tagCloud.classList.add('hidden');
        dom.searchInput.parentElement.classList.add('hidden');
    }
}

init();
