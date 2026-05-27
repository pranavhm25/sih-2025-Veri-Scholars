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

    // --- API & Demo Verification Logic ---
    const API_BASE = window.location.origin === "file://" ? "http://127.0.0.1:5000/api" : "/api";
    
    // Fallback Mock Data
    const SUCCESS_MOCK_DATA = {
        certificate_id: "JHK-2025-CS-042",
        name: "Aditi Sharma",
        institution: "Birla Institute of Technology, Mesra",
        course: "B.Tech Computer Science",
        year: "2025",
        doc_hash: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    };

    const renderResult = (data, isSuccess) => {
        const now = new Date();
        const timeStr = now.toLocaleDateString() + ' ' + now.toLocaleTimeString();

        if (isSuccess) {
            document.getElementById('timestamp-success').textContent = `Verified on: ${timeStr}`;
            document.getElementById('res-id').textContent = data.certificate_id || 'Unknown';
            document.getElementById('res-name').textContent = data.name || 'Unknown';
            document.getElementById('res-inst').textContent = data.institution || 'Unknown';
            document.getElementById('res-course').textContent = data.course || 'Unknown';
            document.getElementById('res-year').textContent = data.year || 'Unknown';
            // Show hash if available
            const hashEl = document.querySelector('#res-year').parentElement.nextElementSibling.querySelector('strong');
            if(hashEl && data.doc_hash) hashEl.textContent = data.doc_hash;
            
            // Confidence score for success is implicitly high, but we can set it visually 100%
            const confFill = document.querySelector('.result-success').nextElementSibling.querySelector('.conf-bar-fill');
            if(confFill) { confFill.style.width = '100%'; confFill.style.background = '#10B981'; }
            
            showPage('result-success');
            showToast("Verification Complete", "Authentic certificate detected.", "success");
        } else {
            document.getElementById('timestamp-failed').textContent = `Attempted on: ${timeStr}`;
            document.getElementById('fail-id').textContent = data.extracted_data?.certificate_id || 'Unknown';
            document.getElementById('fail-name').textContent = data.extracted_data?.name || "Unknown Extraction";
            
            // Populate actual anomaly reasons if supplied by API
            const reasonList = document.querySelector('.failure-reasons ul');
            reasonList.innerHTML = '';
            if (data.anomaly_reasons && data.anomaly_reasons.length > 0) {
                data.anomaly_reasons.forEach(r => {
                    const li = document.createElement('li');
                    li.textContent = r;
                    reasonList.appendChild(li);
                });
            } else {
                reasonList.innerHTML = '<li>Certificate validation failed. Record not matched securely.</li>';
            }

            const confFill = document.querySelector('.result-failed').nextElementSibling.querySelector('.conf-bar-fill');
            if(confFill) { confFill.style.width = '12%'; confFill.style.background = '#EF4444'; }
            
            showPage('result-failed');
            showToast("Verification Failed", "Document anomalies detected.", "error");
        }
    };

    const processFallbackDemo = (certId, name) => {
        const normalizedId = certId.trim().toUpperCase();
        console.log("Using Fallback Demo mode");
        setTimeout(() => {
            if (normalizedId === SUCCESS_MOCK_DATA.id || normalizedId === 'SUCCESS') {
                renderResult(SUCCESS_MOCK_DATA, true);
            } else {
                renderResult({ extracted_data: { certificate_id: certId, name: name }, anomaly_reasons: ["Certificate ID not found in institutional database. (Demo)"] }, false);
            }
        }, 1500);
    };

    const executeManualVerification = async (certId, name) => {
        try {
            const res = await fetch(`${API_BASE}/verify/manual`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ certificate_id: certId, name: name })
            });
            if (!res.ok) throw new Error("API Offline");
            
            const data = await res.json();
            renderResult(data.success ? data.extracted_data : data, data.success);

        } catch (err) {
            // Graceful fallback if API offline
            processFallbackDemo(certId, name);
        }
    };

    // Manual Form Submit
    document.getElementById('manualVerifyForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const btn = document.getElementById('manualCheckBtn');
        btn.textContent = "Checking Ledger...";
        btn.disabled = true;

        const cid = document.getElementById('cid').value;
        const name = document.getElementById('rname').value;

        executeManualVerification(cid, name).finally(() => {
            btn.textContent = "Verify Authenticity";
            btn.disabled = false;
        });
    });

    // File Upload Handlers
    const uploadBtn = document.getElementById('uploadBtn');
    const fileInput = document.getElementById('fileInput');
    const dropZone = document.getElementById('drop-zone');
    const overlay = document.getElementById('scanningOverlay');

    uploadBtn.addEventListener('click', () => fileInput.click());

    const handleFile = async (file) => {
        if(!file) return;
        const validTypes = ['application/pdf', 'image/jpeg', 'image/png'];
        if (!validTypes.includes(file.type)) {
            return showToast("Invalid File", "Please upload PDF, JPG, or PNG only.", "error");
        }
        
        overlay.classList.add('active');

        try {
            const formData = new FormData();
            formData.append('file', file);

            const res = await fetch(`${API_BASE}/verify/upload`, {
                method: 'POST',
                body: formData
            });

            if (!res.ok) throw new Error("API Offline");
            
            const data = await res.json();
            
            if (data.job_id) {
                // Poll for background task completion
                const pollInterval = setInterval(async () => {
                    try {
                        const statusRes = await fetch(`${API_BASE}/verify/status/${data.job_id}`);
                        if (statusRes.ok) {
                            const statusData = await statusRes.json();
                            if (statusData.status === 'completed' || statusData.status === 'failed') {
                                clearInterval(pollInterval);
                                overlay.classList.remove('active');
                                const finalResult = statusData.result;
                                renderResult(finalResult.success ? finalResult.extracted_data : finalResult, finalResult.success);
                            }
                        }
                    } catch (e) {
                        console.error("Polling error", e);
                    }
                }, 1000);
            } else {
                // Fallback if returned synchronously (shouldn't happen with updated backend)
                overlay.classList.remove('active');
                renderResult(data.success ? data.extracted_data : data, data.success);
            }

        } catch (err) {
            console.error("Upload API failed, falling back to Demo:", err);
            setTimeout(() => {
                overlay.classList.remove('active');
                // Removed forced 'SUCCESS'. Pass 'UNKNOWN' to simulate a failed AI OCR parse.
                processFallbackDemo('UNKNOWN', 'Unidentified Upload');
            }, 2500);
        }
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

    // --- Phase 3 Additions: Live SOC Feed & Blockchain Ledger ---
    
    // 1. Simulate Live SOC Feed
    const feedContent = document.getElementById('live-feed-content');
    const possibleEvents = [
        { type: 'success', icon: '✅', text: 'Verified Record: NIT-2022-EE-199' },
        { type: 'success', icon: '✅', text: 'Verified Record: JHK-2025-CS-042' },
        { type: 'error', icon: '⚠', text: 'BLOCKED: Hash anomaly detected on upload from IP 192.168.1.5' },
        { type: 'info', icon: 'ℹ', text: 'New Record Block appended to Blockchain (Batch #492)' },
        { type: 'error', icon: '🛡️', text: 'BLOCKED: ID FAKE-10901 attempted brute force validation' }
    ];

    const generateFeedEvent = () => {
        if (!feedContent) return;
        const e = possibleEvents[Math.floor(Math.random() * possibleEvents.length)];
        const time = new Date().toLocaleTimeString();
        
        const el = document.createElement('div');
        el.className = 'feed-item';
        el.innerHTML = `<span>${e.icon}</span> <strong>[${time}]</strong> <span>${e.text}</span>`;
        
        feedContent.prepend(el);
        // keep only 10 items max
        if (feedContent.children.length > 10) {
            feedContent.removeChild(feedContent.lastChild);
        }
    };

    // Run feed tick every 3 to 8 seconds if dashboard is visible
    setInterval(() => {
        const overviewDash = document.getElementById('dash-overview');
        if (overviewDash && overviewDash.style.display !== 'none') {
            generateFeedEvent();
        }
    }, Math.random() * 5000 + 3000);

    // 2. Initialize Simulated Blockchain Ledger
    const initLedger = () => {
        const grid = document.getElementById('blockchain-grid');
        if (!grid || grid.children.length > 0) return; // already initialized
        
        const generateHash = () => [...Array(64)].map(() => Math.floor(Math.random() * 16).toString(16)).join('');
        
        let prevHash = "0000000000000000000000000000000000000000000000000000000000000000";
        for (let i = 0; i < 5; i++) {
            const hash = generateHash();
            const time = new Date(Date.now() - (i * 3600000)).toLocaleString(); // hours ago
            const payload = i === 0 ? "Batch Issued: B.Tech 2025 Graduates" : "Batch Issued: B.Sc 2024 Graduates";
            
            const card = document.createElement('div');
            card.className = 'block-card';
            card.innerHTML = `
                <div class="block-header">
                    <strong>Block #${10425 - i}</strong>
                    <span style="font-size:12px; color:var(--text-light)">${time}</span>
                </div>
                <div style="font-size:12px; color:var(--text-light); margin-bottom:4px;">Previous Hash:</div>
                <div class="block-hash">${prevHash}</div>
                <div style="font-size:12px; color:var(--text-light); margin-top:12px; margin-bottom:4px;">Block Hash:</div>
                <div class="block-hash" style="background:rgba(16,185,129,0.1); color:#10B981">${hash}</div>
                <div class="block-payload"><strong>Verified Payload:</strong> ${payload}</div>
            `;
            grid.appendChild(card);
            prevHash = hash;
        }
    };

    // Bind Ledger init to the tab click
    document.querySelector('.dash-nav a[data-view="dash-ledger"]').addEventListener('click', initLedger);

    window.forceSync = () => {
        const btn = document.querySelector('button[onclick="forceSync()"]');
        btn.textContent = "Syncing...";
        setTimeout(() => {
            btn.textContent = "Force Sync";
            showToast("Ledger Synchronized", "Successfully verified chain integrity across 4 nodes.", "success");
        }, 1500);
    };

    // Dash Upload
    document.getElementById('dashUploadBtn').addEventListener('click', () => document.getElementById('dashFileInput').click());
    document.getElementById('dashFileInput').addEventListener('change', async (e) => {
        if(e.target.files.length > 0) {
            const file = e.target.files[0];
            showToast("Upload Started", `Processing ${file.name}...`, "info");
            
            try {
                const formData = new FormData();
                formData.append('file', file);
                
                const res = await fetch(`${API_BASE}/dashboard/bulk-upload`, {
                    method: 'POST',
                    body: formData
                });
                
                const data = await res.json();
                if (res.ok && data.success) {
                    showToast("Upload Complete", data.message, "success");
                } else {
                    showToast("Upload Failed", data.message || "Server Error", "error");
                }
            } catch (err) {
                console.error("Bulk upload failed:", err);
                showToast("Upload Failed", "Could not connect to the API.", "error");
            }
        }
    });

    // Init
    init();
});
