/* Connects the supplied template controls to Flask without changing its UI. */
(function () {
    const emailInput = document.getElementById('purchase-email');
    const keyInput = document.getElementById('activation-key');
    const licenseMessage = document.getElementById('license-message');
    const activationMessage = document.getElementById('activation-message');

    function showMessage(target, message) {
        target.textContent = message;
        target.classList.remove('hidden');
    }
    function clearMessage(target) { target.textContent = ''; target.classList.add('hidden'); }
    function showAuthStep(stepId) {
        document.querySelectorAll('.auth-step').forEach(step => step.classList.remove('active'));
        document.getElementById(stepId).classList.add('active');
    }
    function enterWorkspace() {
        document.getElementById('auth-view').classList.add('opacity-0', 'pointer-events-none');
        setTimeout(() => {
            document.getElementById('auth-view').style.display = 'none';
            document.getElementById('app-view').classList.remove('hidden');
            document.getElementById('app-view').classList.add('flex');
            switchTab('dashboard');
        }, 300);
    }
    async function postJson(path, body) {
        const response = await fetch(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
        const contentType = response.headers.get('content-type') || '';
        let data = {};
        if (contentType.includes('application/json')) {
            try { data = await response.json(); } catch (_) { data = {}; }
        }
        if (!response.ok) {
            if (response.status >= 500) throw new Error('The service is temporarily unavailable. Please try again later.');
            throw new Error(data.error || 'The request could not be completed. Please try again.');
        }
        return data;
    }
    async function findAndFillKey() {
        clearMessage(licenseMessage); clearMessage(activationMessage);
        const email = emailInput.value.trim();
        if (!email) { showMessage(licenseMessage, 'Enter the purchase email first.'); return; }
        try {
            const result = await postJson('/api/licenses/find-key', { email });
            keyInput.value = result.key;
            document.getElementById('auth-step-1').classList.remove('active');
            document.getElementById('auth-step-2').classList.add('active');
        } catch (error) { showMessage(licenseMessage, error.message); }
    }
    window.nextAuthStep = findAndFillKey;
    document.getElementById('find-key-button').addEventListener('click', findAndFillKey);
    document.getElementById('open-signup').addEventListener('click', () => showAuthStep('auth-step-signup'));
    document.getElementById('back-to-login').addEventListener('click', () => showAuthStep('auth-step-1'));
    document.getElementById('signup-button').addEventListener('click', async () => {
        const message = document.getElementById('signup-message');
        const button = document.getElementById('signup-button');
        clearMessage(message);
        const name = document.getElementById('signup-name').value.trim();
        const email = document.getElementById('signup-email').value.trim();
        const password = document.getElementById('signup-password').value;
        if (!name || !email || !password) { showMessage(message, 'Enter your name, email, and password.'); return; }
        button.disabled = true; button.textContent = 'Creating Account…';
        try {
            await postJson('/api/auth/register', { name, email, password });
            enterWorkspace();
        } catch (error) {
            showMessage(message, error.message === 'An account with that email already exists.' ? 'An account already exists with this email. Please sign in.' : error.message);
        } finally { button.disabled = false; button.textContent = 'Create Account'; }
    });
    window.mockActivate = async function () {
        clearMessage(activationMessage);
        const button = document.querySelector('#auth-step-2 .glass-button-primary');
        const original = button.textContent;
        button.disabled = true; button.textContent = 'Validating…';
        try {
            await postJson('/api/licenses/activate', { key: keyInput.value });
            enterWorkspace();
        } catch (error) { showMessage(activationMessage, error.message); }
        finally { button.disabled = false; button.textContent = original; }
    };
    const requestedTab = location.hash.slice(1);
    if (requestedTab && document.getElementById(`tab-${requestedTab}`) && typeof switchTab === 'function') {
        document.getElementById('auth-view').style.display = 'none';
        document.getElementById('app-view').classList.remove('hidden');
        document.getElementById('app-view').classList.add('flex');
        switchTab(requestedTab);
    }

    async function request(path, body) {
        const response = await fetch(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body || {}) });
        const contentType = response.headers.get('content-type') || '';
        let data = {};
        if (contentType.includes('application/json')) {
            try { data = await response.json(); } catch (_) { data = {}; }
        }
        if (!response.ok) {
            if (response.status >= 500) throw new Error('The service is temporarily unavailable. Please try again later.');
            throw new Error(data.error || 'The request could not be completed. Please try again.');
        }
        return data;
    }

    window.mockGenerate = async function () {
        const button = document.getElementById('generate-btn');
        const niche = document.getElementById('gen-niche').value.trim();
        const city = document.getElementById('gen-city').value.trim();
        const limit = Number(document.getElementById('gen-limit').value) || 20;
        const consoleBox = document.getElementById('gen-console');
        if (!niche || !city) { consoleBox.innerHTML = '<p class="text-red-400">[Error] Enter a niche and city first.</p>'; return; }
        button.disabled = true; button.textContent = 'Searching…';
        document.getElementById('gen-stage').textContent = 'Searching Google Maps…';
        document.getElementById('gen-total').textContent = limit;
        consoleBox.innerHTML = `<p>[Info] Searching ${niche} in ${city}…</p>`;
        try {
            const result = await request('/api/businesses/search', { keyword: niche, category: niche, location: city, limit });
            document.getElementById('gen-count').textContent = result.count;
            document.getElementById('gen-current').textContent = 'Saved unique leads';
            document.getElementById('gen-stage').textContent = 'Complete';
            document.getElementById('gen-progress').style.width = '100%';
            consoleBox.innerHTML += `<p class="text-green-400">[Success] Saved ${result.count} unique leads to database.</p>`;
            const table = document.getElementById('leads-table-body');
            if (table) table.innerHTML = result.leads.map(lead => `<tr class="border-b border-[var(--border-panel)] hover:bg-black/5 dark:hover:bg-white/5 transition-colors"><td class="px-4 py-3">${escape(lead.name)}</td><td class="px-4 py-3 text-center">${lead.rating || '—'}</td><td class="px-4 py-3 text-center">${lead.review_count || 0}</td><td class="px-4 py-3 text-center text-green-400">${lead.score}/100</td><td class="px-4 py-3 text-[var(--text-muted)]">${escape(lead.phone || '—')}</td><td class="px-4 py-3 text-[var(--text-muted)]">${escape(lead.email || '—')}</td><td class="px-4 py-3 text-[var(--text-muted)]">${escape(lead.website || '—')}</td><td class="px-4 py-3 text-[var(--text-muted)]">—</td><td class="px-4 py-3"><span class="bg-[var(--accent)]/20 text-[var(--accent)] px-2 py-1 rounded text-xs border border-[var(--accent)]/30">${escape(lead.status)}</span></td></tr>`).join('');
        } catch (error) {
            document.getElementById('gen-stage').textContent = 'Search failed';
            consoleBox.innerHTML += `<p class="text-red-400">[Error] ${error.message}</p>`;
        } finally { button.disabled = false; button.textContent = 'Start Scraping'; }
    };

    window.mockFindEmails = async function () {
        const button = document.getElementById('find-emails-btn');
        const consoleBox = document.getElementById('email-console');
        button.disabled = true; button.textContent = 'Scanning…';
        consoleBox.innerHTML = '<p>[Info] Checking public business websites…</p>';
        try {
            const result = await request('/api/businesses/enrich-emails');
            document.getElementById('email-queued').textContent = result.checked;
            document.getElementById('email-found').textContent = result.found;
            consoleBox.innerHTML += `<p class="text-green-400">[Success] Checked ${result.checked}; found ${result.found} public email address(es).</p>`;
        } catch (error) { consoleBox.innerHTML += `<p class="text-red-400">[Error] ${error.message}</p>`; }
        finally { button.disabled = false; button.textContent = 'Find Emails'; }
    };
    function escape(value) { const element = document.createElement('span'); element.textContent = value || ''; return element.innerHTML; }
})();
