// --- THEME & MODE MANAGEMENT ---
        const html = document.documentElement;
        const darkModeToggle = document.getElementById('dark-mode-toggle');

        // 1. Dark/Light Mode Toggle
        function toggleDarkMode() {
            if (html.classList.contains('dark')) {
                html.classList.remove('dark');
                localStorage.setItem('mode', 'light');
                darkModeToggle.checked = false;
            } else {
                html.classList.add('dark');
                localStorage.setItem('mode', 'dark');
                darkModeToggle.checked = true;
            }
        }

        // Initialize Mode (Default to Dark)
        const savedMode = localStorage.getItem('mode');
        if (savedMode === 'light') {
            html.classList.remove('dark');
            darkModeToggle.checked = false;
        } else {
            // Default to dark if no preference saved
            html.classList.add('dark');
            localStorage.setItem('mode', 'dark');
            darkModeToggle.checked = true;
        }

        // 2. Accent Color Theme
        function setTheme(color) {
            document.body.setAttribute('data-theme', color);
            localStorage.setItem('color-theme', color);
            
            // Update active state on buttons
            document.querySelectorAll('.theme-btn').forEach(btn => {
                btn.classList.remove('ring-2', 'ring-[var(--accent)]', 'border-[var(--accent)]');
                if(btn.dataset.color === color) {
                    btn.classList.add('ring-2', 'ring-[var(--accent)]', 'border-[var(--accent)]');
                }
            });
        }

        // Initialize Accent Theme
        const savedTheme = localStorage.getItem('color-theme') || 'blue';
        setTheme(savedTheme);

        // --- AUTH FLOW ---
        function nextAuthStep() {
            document.getElementById('auth-step-1').classList.remove('active');
            document.getElementById('auth-step-2').classList.add('active');
        }

        function prevAuthStep() {
            document.getElementById('auth-step-2').classList.remove('active');
            document.getElementById('auth-step-1').classList.add('active');
        }

        function mockActivate() {
            const btn = document.querySelector('#auth-step-2 .glass-button-primary');
            btn.textContent = 'Activating...';
            
            setTimeout(() => {
                document.getElementById('auth-view').classList.add('opacity-0', 'pointer-events-none');
                setTimeout(() => {
                    document.getElementById('auth-view').style.display = 'none';
                    document.getElementById('app-view').classList.remove('hidden');
                    document.getElementById('app-view').classList.add('flex');
                    switchTab('dashboard');
                }, 300);
            }, 1000);
        }

        // --- TAB SWITCHING ---
        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.getElementById('tab-' + tabId).classList.add('active');
            
            document.querySelectorAll('.sidebar-item').forEach(el => {
                el.classList.remove('active');
                if (el.dataset.tab === tabId) {
                    el.classList.add('active');
                }
            });
        }

        // --- MOCK GENERATE LEADS ---
        function mockGenerate() {
            const btn = document.getElementById('generate-btn');
            const stage = document.getElementById('gen-stage');
            const current = document.getElementById('gen-current');
            const count = document.getElementById('gen-count');
            const total = document.getElementById('gen-total');
            const progress = document.getElementById('gen-progress');
            const console = document.getElementById('gen-console');
            
            const niche = document.getElementById('gen-niche').value;
            const city = document.getElementById('gen-city').value;
            const limit = parseInt(document.getElementById('gen-limit').value) || 50;
            
            btn.disabled = true;
            btn.textContent = 'Scraping...';
            stage.textContent = 'Connecting to Google Maps API...';
            current.textContent = 'Initializing...';
            total.textContent = limit;
            console.innerHTML = `<p>[Info] Starting scrape for ${niche} in ${city}...</p>`;
            
            let currentCount = 0;
            const interval = setInterval(() => {
                currentCount++;
                count.textContent = currentCount;
                progress.style.width = `${(currentCount / limit) * 100}%`;
                current.textContent = `Mock Business ${currentCount}`;
                console.innerHTML += `<p>[Info] Found: Mock Business ${currentCount} (Rating: 4.${Math.floor(Math.random()*9)})</p>`;
                console.scrollTop = console.scrollHeight;
                
                if (currentCount >= limit) {
                    clearInterval(interval);
                    stage.textContent = 'Complete';
                    current.textContent = 'Done';
                    console.innerHTML += `<p class="text-green-400">[Success] Saved ${limit} leads to database.</p>`;
                    btn.disabled = false;
                    btn.textContent = 'Start Scraping';
                    
                    addMockLeads(limit, niche, city);
                    document.getElementById('kpi-total').textContent = limit;
                }
            }, 100);
        }

        function addMockLeads(count, niche, city) {
            const tbody = document.getElementById('leads-table-body');
            tbody.innerHTML = '';
            for (let i = 1; i <= count; i++) {
                const rating = (Math.random() * 2 + 3).toFixed(1);
                const reviews = Math.floor(Math.random() * 500);
                const fit = reviews > 100 ? 'High Fit' : 'Medium Fit';
                tbody.innerHTML += `
                    <tr class="border-b border-[var(--border-panel)] hover:bg-black/5 dark:hover:bg-white/5 transition-colors">
                        <td class="px-4 py-3">${niche} ${i} (${city})</td>
                        <td class="px-4 py-3 text-center">${rating}</td>
                        <td class="px-4 py-3 text-center">${reviews}</td>
                        <td class="px-4 py-3 text-center text-green-600 dark:text-green-400">${fit}</td>
                        <td class="px-4 py-3 text-[var(--text-muted)]">—</td>
                        <td class="px-4 py-3 text-[var(--text-muted)]">—</td>
                        <td class="px-4 py-3 text-[var(--text-muted)]">—</td>
                        <td class="px-4 py-3 text-[var(--text-muted)]">—</td>
                        <td class="px-4 py-3"><span class="bg-[var(--accent)]/20 text-[var(--accent)] px-2 py-1 rounded text-xs border border-[var(--accent)]/30">New</span></td>
                    </tr>
                `;
            }
        }

        // --- MOCK FIND EMAILS ---
        function mockFindEmails() {
            const btn = document.getElementById('find-emails-btn');
            const console = document.getElementById('email-console');
            const queued = document.getElementById('email-queued');
            const found = document.getElementById('email-found');
            
            btn.disabled = true;
            btn.textContent = 'Scanning...';
            console.innerHTML = '<p>[Info] Starting email finder...</p>';
            queued.textContent = '50';
            
            let f = 0;
            const interval = setInterval(() => {
                f++;
                found.textContent = f;
                console.innerHTML += `<p>[Info] Scanning website ${f}... Found: contact@business${f}.com</p>`;
                console.scrollTop = console.scrollHeight;
                if (f >= 15) {
                    clearInterval(interval);
                    console.innerHTML += '<p class="text-green-400">[Success] Email finder complete.</p>';
                    btn.disabled = false;
                    btn.textContent = 'Find Emails';
                }
            }, 200);
        }

        // --- MOCK AI COMPOSE ---
        function setPrompt(text) {
            document.getElementById('prompt-editor').value = text;
            document.getElementById('prompt-len').textContent = text.length;
            updatePreview();
        }

        function updatePreview() {
            const prompt = document.getElementById('prompt-editor').value;
            const preview = document.getElementById('ai-preview');
            preview.textContent = prompt.replace(/{business}/g, 'Turbo Cars');
        }

        document.getElementById('prompt-editor').addEventListener('input', (e) => {
            document.getElementById('prompt-len').textContent = e.target.value.length;
            updatePreview();
        });

        function mockAICompose() {
            const btn = document.getElementById('ai-compose-btn');
            const preview = document.getElementById('ai-preview');
            
            btn.disabled = true;
            btn.textContent = 'Generating...';
            preview.textContent = 'Connecting to OpenAI...';
            
            setTimeout(() => {
                preview.textContent = 'Hey Turbo Cars! 👋 I noticed your amazing work in the area. We help local businesses like yours get more customers through social media. Would you be open to a quick chat?';
                btn.disabled = false;
                btn.textContent = 'Generate Messages';
            }, 1500);
        }

        // Initialize preview on load
        updatePreview();
