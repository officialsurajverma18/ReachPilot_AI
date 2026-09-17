/* Opens the existing template sidebar from a three-line mobile menu. */
(function () {
    const toggle = document.getElementById('mobile-menu-toggle');
    const sidebar = document.querySelector('#app-view > aside');
    const backdrop = document.getElementById('mobile-menu-backdrop');
    if (!toggle || !sidebar || !backdrop) return;
    const close = () => {
        document.body.classList.remove('mobile-menu-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.setAttribute('aria-label', 'Open navigation menu');
    };
    const open = () => {
        document.body.classList.add('mobile-menu-open');
        toggle.setAttribute('aria-expanded', 'true');
        toggle.setAttribute('aria-label', 'Close navigation menu');
    };
    toggle.addEventListener('click', () => document.body.classList.contains('mobile-menu-open') ? close() : open());
    backdrop.addEventListener('click', close);
    sidebar.querySelectorAll('.sidebar-item').forEach(item => item.addEventListener('click', close));
    window.addEventListener('resize', () => { if (window.innerWidth > 900) close(); });
})();
