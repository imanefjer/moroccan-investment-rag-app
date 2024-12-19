class KnowledgeBase {
    constructor() {
        this.questionInput = document.getElementById('questionInput');
        this.submitButton = document.getElementById('submitButton');
        this.answerDiv = document.getElementById('answer');
        this.resultContainer = document.querySelector('.result-container');
        this.loadingDiv = document.querySelector('.loading');
        this.addUrlButton = document.getElementById('addUrlButton');
        this.urlInput = document.getElementById('urlInput');
        this.submitUrlButton = document.getElementById('submitUrlButton');
        this.cancelUrlButton = document.getElementById('cancelUrlButton');
        this.urlInputGroup = document.querySelector('.url-input-group');
        this.toggleSourcesButton = document.getElementById('toggleSourcesButton');
        this.sourcesList = document.getElementById('sourcesList');
        this.sourcesListContainer = document.querySelector('.sources-list');
        
        this.initializeEventListeners();
        this.loadSources();
    }

    initializeEventListeners() {
        this.submitButton.addEventListener('click', () => this.askQuestion());
        this.questionInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.askQuestion();
            }
        });
        this.addUrlButton.addEventListener('click', () => this.toggleUrlInput(true));
        this.cancelUrlButton.addEventListener('click', () => this.toggleUrlInput(false));
        this.submitUrlButton.addEventListener('click', () => this.submitUrl());
        this.urlInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.submitUrl();
            }
        });
        this.toggleSourcesButton.addEventListener('click', () => this.toggleSources());
    }

    async askQuestion() {
        const question = this.questionInput.value.trim();
        if (!question) return;

        this.setLoadingState(true);

        try {
            const response = await this.fetchAnswer(question);
            this.displayAnswer(response.answer);
        } catch (error) {
            console.error('Error:', error);
            this.displayError();
        } finally {
            this.setLoadingState(false);
        }
    }

    async fetchAnswer(question) {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    displayAnswer(answer) {
        this.loadingDiv.style.display = 'none';
        this.resultContainer.style.display = 'block';
        this.answerDiv.textContent = answer;
        
        // Animate result container
        setTimeout(() => {
            this.resultContainer.classList.add('visible');
        }, 10);
    }

    displayError() {
        this.answerDiv.textContent = 'Sorry, an error occurred while processing your question.';
    }

    setLoadingState(isLoading) {
        this.loadingDiv.style.display = isLoading ? 'block' : 'none';
        this.resultContainer.style.display = isLoading ? 'none' : 'block';
        this.submitButton.disabled = isLoading;
        if (!isLoading) {
            this.resultContainer.classList.remove('visible');
        }
    }

    toggleUrlInput(show) {
        this.urlInputGroup.style.display = show ? 'block' : 'none';
        if (show) {
            this.urlInput.value = '';
            this.urlInput.focus();
        }
    }

    async submitUrl() {
        const url = this.urlInput.value.trim();
        if (!url) return;

        try {
            const response = await fetch('/add_url', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url }),
            });

            const data = await response.json();

            if (response.ok) {
                this.showNotification('URL added successfully', 'success');
                this.toggleUrlInput(false);
                await this.loadSources();
            } else {
                this.showNotification(data.error || 'Failed to add URL', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showNotification('An error occurred while adding the URL', 'error');
        }
    }

    showNotification(message, type = 'success') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;

        // Add to document
        document.body.appendChild(notification);

        // Remove after delay
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    async loadSources() {
        try {
            const response = await fetch('/sources');
            const data = await response.json();
            
            if (data.sources && data.sources.length > 0) {
                this.updateSourcesList(data.sources);
            }
        } catch (error) {
            console.error('Error loading sources:', error);
        }
    }

    updateSourcesList(sources) {
        this.sourcesList.innerHTML = sources.map(source => `
            <li>
                <i class="fas fa-globe"></i>
                <a href="${source}" target="_blank" rel="noopener noreferrer">
                    ${this.formatUrl(source)}
                </a>
            </li>
        `).join('');
    }

    formatUrl(url) {
        try {
            const urlObj = new URL(url);
            return urlObj.hostname + urlObj.pathname;
        } catch {
            return url;
        }
    }

    toggleSources() {
        const isVisible = this.sourcesListContainer.style.display !== 'none';
        this.sourcesListContainer.style.display = isVisible ? 'none' : 'block';
        
        if (!isVisible) {
            // Update icon and text
            this.toggleSourcesButton.innerHTML = `
                <i class="fas fa-times"></i>
                <span>Hide Sources</span>
            `;
            // Add visible class after a small delay for animation
            setTimeout(() => {
                this.sourcesListContainer.classList.add('visible');
            }, 10);
        } else {
            // Update icon and text
            this.toggleSourcesButton.innerHTML = `
                <i class="fas fa-link"></i>
                <span>Show Sources</span>
            `;
            this.sourcesListContainer.classList.remove('visible');
        }
    }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new KnowledgeBase();
});
