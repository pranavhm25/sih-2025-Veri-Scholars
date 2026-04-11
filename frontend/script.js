document.addEventListener('DOMContentLoaded', () => {
    // --- State Elements ---
    const pages = document.querySelectorAll('.page-section');
    const navLinks = document.querySelectorAll('.nav-link, [data-target]');
    const themeToggle = document.getElementById('theme-toggle');
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mainNav = document.querySelector('.main-nav');
    
    // --- Initialize ---
    const init = () => {
        // Hide all pages except home
        pages.forEach(p => p.style.display = 'none');
        document.getElementById('home').style.display = 'block';

        // Load Theme
        const savedTheme = localStorage.getItem('theme') || 'light';
        applyTheme(savedTheme);

        // Setup Observers for Animations
        setupIntersectionObserver();

        // Check Auth
        checkAuth();

        // Animate Counters
        animateCounters();
    };

    // --- Navigation Logic ---
    const showPage = (targetId) => {
        const target = targetId.startsWith('#') ? targetId.substring(1) : targetId;
        
        pages.forEach(p => p.style.display = 'none');
        const targetEl = document.getElementById(target);
        if(targetEl) {
            targetEl.style.display = 'block';
            window.scrollTo({ top: 0, behavior: 'smooth' });
            
            // Re-trigger animations
            const anims = targetEl.querySelectorAll('.anim-fade-in, .anim-fade-in-up');
            anims.forEach(el => {
                el.classList.remove('is-visible');
                // trigger reflow
                void el.offsetWidth;
                el.classList.add('is-visible');
            });

            // Initialize charts if dashboard
            if (target === 'dashboard') {
                initCharts();
            }
        }

        // Update active nav
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        const activeLink = document.querySelector(`.nav-link[data-target="#${target}"]`);
        if (activeLink) activeLink.classList.add('active');
        
        // Close mobile menu if open
        mainNav.classList.remove('active');
    };

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = link.getAttribute('data-target');
            if (target) showPage(target);
        });
    });

    // --- Theme Logic ---
    const applyTheme = (theme) => {
        if (theme === 'dark') {
            document.body.classList.add('dark-mode');
            themeToggle.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>`;
        } else {
            document.body.classList.remove('dark-mode');
            themeToggle.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>`;
        }
    };

    themeToggle.addEventListener('click', () => {
        const newTheme = document.body.classList.contains('dark-mode') ? 'light' : 'dark';
        localStorage.setItem('theme', newTheme);
        applyTheme(newTheme);
    });

    mobileMenuBtn.addEventListener('click', () => {
        mainNav.style.display = mainNav.style.display === 'flex' ? 'none' : 'flex';
        mainNav.style.flexDirection = 'column';
        mainNav.style.position = 'absolute';
        mainNav.style.top = '70px';
        mainNav.style.left = '0';
        mainNav.style.right = '0';
        mainNav.style.background = 'var(--background)';
        mainNav.style.padding = '24px';
        mainNav.style.boxShadow = 'var(--shadow-lg)';
    });

    // --- Animations ---
    const setupIntersectionObserver = () => {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('.anim-fade-in, .anim-fade-in-up').forEach(el => observer.observe(el));
    };

    const animateValue = (id, start, end, duration, formatter = (v) => v) => {
        const obj = document.getElementById(id);
        if(!obj) return;
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            const current = Math.floor(progress * (end - start) + start);
            obj.innerHTML = formatter(current);
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    };

    const animateCounters = () => {
        animateValue("count-verified", 0, 12453, 2000, (v) => v.toLocaleString());
        animateValue("count-institutions", 0, 42, 1500, (v) => v);
        animateValue("count-accuracy", 0, 99, 2000, (v) => v + "%");
    };

    // --- Toast Notifications ---
    const showToast = (title, message, type = 'info') => {
        const container = document.getElementById('toast-container');
        const icon = type === 'success' ? '✓' : type === 'error' ? '⚠' : 'ℹ';
        
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <div class="toast-icon">${icon}</div>
            <div class="toast-content">
                <h4>${title}</h4>
                <p>${message}</p>
            </div>
        `;
        
        container.appendChild(toast);
        
        // trigger reflow
        void toast.offsetWidth;
        toast.classList.add('show');
        
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 400);
        }, 4000);
    };

    // --- Verify Section Tabs ---
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            // tab buttons
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            
            // tab panels
            document.querySelectorAll('.verify-panel').forEach(p => p.classList.remove('active'));
            document.getElementById(e.target.dataset.tab).classList.add('active');
        });
    });

    // --- Demo Verification Logic ---
    // The problem statement asks for Jharkhand. We use JHK-2025-CS-042 as the "Gold" success case.
    const SUCCESS_MOCK_DATA = {
        id: "JHK-2025-CS-042",
        name: "Aditi Sharma",
        inst: "Birla Institute of Technology, Mesra",
        course: "B.Tech Computer Science",
        year: "2025"
    };

    const executeVerification = (certId, name) => {
        const normalizedId = certId.trim().toUpperCase();
        const now = new Date();
        const timeStr = now.toLocaleDateString() + ' ' + now.toLocaleTimeString();

        // Simulation delay
        setTimeout(() => {
            if (normalizedId === SUCCESS_MOCK_DATA.id || normalizedId === 'SUCCESS') {
                // Success Flow
                document.getElementById('timestamp-success').textContent = `Verified on: ${timeStr}`;
                document.getElementById('res-id').textContent = SUCCESS_MOCK_DATA.id;
                document.getElementById('res-name').textContent = SUCCESS_MOCK_DATA.name;
                document.getElementById('res-inst').textContent = SUCCESS_MOCK_DATA.inst;
                document.getElementById('res-course').textContent = SUCCESS_MOCK_DATA.course;
                document.getElementById('res-year').textContent = SUCCESS_MOCK_DATA.year;
                
                showPage('result-success');
                showToast("Verification Complete", "Authentic certificate detected.", "success");
            } else {
                // Failure Flow
                document.getElementById('timestamp-failed').textContent = `Attempted on: ${timeStr}`;
                document.getElementById('fail-id').textContent = certId;
                document.getElementById('fail-name').textContent = name || "Extracted from document";
                
                showPage('result-failed');
                showToast("Verification Failed", "Document anomalies detected.", "error");
            }
        }, 2000);
    };

    // Manual Form Submit
    document.getElementById('manualVerifyForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const btn = document.getElementById('manualCheckBtn');
        btn.textContent = "Checking Blockchain Ledger...";
        btn.disabled = true;

        const cid = document.getElementById('cid').value;
        const name = document.getElementById('rname').value;

        executeVerification(cid, name);

        // Reset button after delay
        setTimeout(() => {
            btn.textContent = "Verify Authenticity";
            btn.disabled = false;
        }, 2000);
    });

    // File Upload Handlers
    const uploadBtn = document.getElementById('uploadBtn');
    const fileInput = document.getElementById('fileInput');
    const dropZone = document.getElementById('drop-zone');
    const overlay = document.getElementById('scanningOverlay');

    uploadBtn.addEventListener('click', () => fileInput.click());

    const handleFile = (file) => {
        if(!file) return;
        const validTypes = ['application/pdf', 'image/jpeg', 'image/png'];
        if (!validTypes.includes(file.type)) {
            return showToast("Invalid File", "Please upload PDF, JPG, or PNG only.", "error");
        }
        
        overlay.classList.add('active');
        // Fake OCR extraction -> Verification
        setTimeout(() => {
            overlay.classList.remove('active');
            // Randomly pass or fail for demo if they upload a file, 
            // but let's make it succeed to show the cool success page
            executeVerification('SUCCESS', 'Extracted User');
        }, 2500);
    };

    fileInput.addEventListener('change', (e) => handleFile(e.target.files[0]));

    // Drag and Drop styling
    dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('dragover'); });
    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        handleFile(e.dataTransfer.files[0]);
    });

    // QR Mock
    document.getElementById('mockQrBtn').addEventListener('click', () => {
        showToast("Scanning...", "Analyzing QR Code structural data", "info");
        setTimeout(() => {
            executeVerification('SUCCESS', '');
        }, 1500);
    });

    // --- Dashboard & Auth Logic ---
    let authState = false;

    const checkAuth = () => {
        const authControls = document.getElementById('auth-controls');
        if (authState) {
            authControls.innerHTML = `<button class="btn btn-primary" data-target="#dashboard">Dashboard Form</button>`;
            // rebind
            authControls.querySelector('.btn').addEventListener('click', () => showPage('dashboard'));
        }
    };

    document.getElementById('loginForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const btn = document.getElementById('signinBtn');
        btn.textContent = "Authenticating...";
        
        setTimeout(() => {
            authState = true;
            btn.textContent = "Sign In";
            checkAuth();
            showPage('dashboard');
            showToast("Welcome Back", "Signed in as Institute Admin", "success");
        }, 1000);
    });

    document.getElementById('demoLoginBtn').addEventListener('click', () => {
        document.getElementById('email').value = "admin@jtu.ac.in";
        document.getElementById('password').value = "password123";
        showToast("Demo Mode", "Credentials filled. Proceed to Login.", "info");
    });

    document.getElementById('logoutBtn').addEventListener('click', () => {
        authState = false;
        document.getElementById('auth-controls').innerHTML = `<button class="btn btn-secondary" data-target="#loginPage">Institution Login</button>`;
        document.getElementById('auth-controls').querySelector('.btn').addEventListener('click', () => showPage('loginPage'));
        showPage('home');
        showToast("Logged Out", "Session ended securely.", "info");
    });

    // Dashboard View Toggles
    document.querySelectorAll('.dash-nav a').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            document.querySelectorAll('.dash-nav a').forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            
            document.querySelectorAll('.dash-view').forEach(v => v.style.display = 'none');
            document.getElementById(link.dataset.view).style.display = 'block';
        });
    });

    // --- Charts ---
    let chartsInitialized = false;
    const initCharts = () => {
        if (chartsInitialized) return;
        
        // Define theme-aware colors
        const textColor = getComputedStyle(document.body).getPropertyValue('--text-dark').trim() || '#0F172A';
        const gridColor = getComputedStyle(document.body).getPropertyValue('--medium-grey').trim() || '#E2E8F0';
        
        const volCtx = document.getElementById('volumeChart');
        if(volCtx) {
            new Chart(volCtx, {
                type: 'line',
                data: {
                    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                    datasets: [{
                        label: 'Successful Verifications',
                        data: [1200, 1900, 2400, 2704],
                        borderColor: '#4F46E5',
                        backgroundColor: 'rgba(79, 70, 229, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'Failed Verifications',
                        data: [3, 5, 2, 8],
                        borderColor: '#EF4444',
                        backgroundColor: 'rgba(239, 68, 68, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { labels: { color: textColor } } },
                    scales: {
                        y: { 
                            grid: { color: gridColor },
                            ticks: { color: textColor }
                        },
                        x: {
                            grid: { color: gridColor },
                            ticks: { color: textColor }
                        }
                    }
                }
            });
        }

        const anomalyCtx = document.getElementById('anomalyChart');
        if(anomalyCtx) {
            new Chart(anomalyCtx, {
                type: 'doughnut',
                data: {
                    labels: ['ID Mismatch', 'Hash Tampering', 'Date Alteration', 'Invalid Format'],
                    datasets: [{
                        data: [18, 12, 5, 7],
                        backgroundColor: ['#EF4444', '#F59E0B', '#8B5CF6', '#64748B'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { position: 'bottom', labels: { color: textColor } } },
                    cutout: '75%'
                }
            });
        }
        
        chartsInitialized = true;
    };

    // Dash Upload
    document.getElementById('dashUploadBtn').addEventListener('click', () => document.getElementById('dashFileInput').click());
    document.getElementById('dashFileInput').addEventListener('change', (e) => {
        if(e.target.files.length > 0) {
            showToast("Upload Started", `Processing ${e.target.files[0].name}...`, "info");
            setTimeout(() => {
                showToast("Upload Complete", "124 records added to the blockchain ledger.", "success");
            }, 2000);
        }
    });

    // Init
    init();
});
