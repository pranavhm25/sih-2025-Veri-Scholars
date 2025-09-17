$(document).ready(function() {
    const $allSections = $('main > section');
    const $themeToggle = $('#theme-toggle');
    const $body = $('body');
    const sunIcon = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>`;
    const moonIcon = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>`;

    // --- Core Logic (Navigation, Init) ---
    function initialize() {
        $allSections.hide();
        $('#home').show();
        checkLoginState();
        const savedTheme = localStorage.getItem('theme') || 'light';
        applyTheme(savedTheme);
        setupScrollAnimations();
    }

    function showSection(id) {
        if ($(id).is(':visible') && id !== '#home') return;
        $allSections.fadeOut(200);
        setTimeout(() => {
            $(id).fadeIn(300);
            window.scrollTo({ top: 0, behavior: 'smooth' });
            updateActiveNav(id);
            $(id).find('.anim-fade-in, .anim-fade-in-up').addClass('is-visible');
        }, 200);
    }

    function updateActiveNav(targetId) {
        $('.nav-link').removeClass('active');
        let navLinkSelector = targetId.startsWith('#') ? targetId : '#' + targetId;
        $(`.nav-link[href="${navLinkSelector}"]`).addClass('active');
    }

    // --- Theme Toggle Logic ---
    function applyTheme(theme) {
        if (theme === 'dark') {
            $body.addClass('dark-mode');
            $themeToggle.html(sunIcon);
        } else {
            $body.removeClass('dark-mode');
            $themeToggle.html(moonIcon);
        }
    }

    // --- Scroll Animations ---
    function setupScrollAnimations() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('.anim-fade-in, .anim-fade-in-up').forEach(el => {
            observer.observe(el);
        });
    }

    // --- Auth Logic (Login, Register, Logout, Password Toggle) ---
    function checkLoginState() {
        if (localStorage.getItem('loggedInUser')) {
            $('#auth-controls').html('<button class="btn btn-secondary" id="viewDashboard">My Dashboard</button>');
        } else {
            $('#auth-controls').html('<button class="btn btn-primary" data-target="#loginPage">Sign In</button>');
        }
    }

    function loginUser() {
        const email = $('#email').val().trim();
        const pass = $('#password').val().trim();
        const storedUser = JSON.parse(localStorage.getItem('registeredUser'));

        if (!email || !pass) {
            return showToast("Please enter your login credentials.", "error");
        }
        
        if (storedUser && storedUser.email === email && storedUser.pass === pass) {
            const $btn = $('#signinBtn');
            $btn.text('Signing in...').prop('disabled', true);
            setTimeout(() => {
                $btn.text('Sign In').prop('disabled', false);
                localStorage.setItem('loggedInUser', JSON.stringify({ name: storedUser.name, email: storedUser.email }));
                checkLoginState();
                populateDashboard();
                showSection('#dashboard');
                showToast(`Login successful! Welcome back, ${storedUser.name}.`, "success");
            }, 900);
        } else {
            showToast("Invalid email or password.", "error");
        }
    }
    
    function registerUser() {
        const instName = $('#instName').val().trim();
        const instEmail = $('#instEmail').val().trim();
        const instPass = $('#instPass').val().trim();
        const instPassConfirm = $('#instPassConfirm').val().trim();

        if (!instName || !instEmail || !instPass || !instPassConfirm) {
            return showToast('Please fill in all fields.', 'error');
        }
        if (!instEmail.endsWith('@gmail.com')) {
            return showToast('Email must be a @gmail.com address.', 'error');
        }
        if (instPass.length < 6) {
            return showToast('Password must be at least 6 characters.', 'error');
        }
        if (instPass !== instPassConfirm) {
            return showToast('Passwords do not match.', 'error');
        }

        const $btn = $('#registerBtn');
        $btn.text('Creating Account...').prop('disabled', true);
        setTimeout(() => {
            $btn.text('Create Account').prop('disabled', false);
            const newUser = { name: instName, email: instEmail, pass: instPass };
            localStorage.setItem('registeredUser', JSON.stringify(newUser));
            showToast('Account created successfully! Please sign in.', 'success');
            showSection('#loginPage');
        }, 1200);
    }
    
    function logoutUser() {
        localStorage.removeItem('loggedInUser');
        checkLoginState();
        showSection('#home');
        showToast("You have been logged out.", "info");
    }

    // --- UI Logic (Toasts, File Upload, Dashboard, etc.) ---
    function showToast(message, type = 'info', duration = 3000) {
        const toast = $(`<div class="toast ${type}">${message}</div>`);
        $('#toast-container').append(toast);
        setTimeout(() => toast.addClass('show'), 100);
        setTimeout(() => {
            toast.removeClass('show');
            toast.on('transitionend', () => toast.remove());
        }, duration);
    }
    
    function handleFileUpload(files, allowedTypes = ['application/pdf', 'image/jpeg', 'image/png'], isDashboard = false) {
        if (!files || files.length === 0) return;

        const file = files[0];
        const MAX_SIZE = 10 * 1024 * 1024; // 10 MB

        const fileExtension = file.name.split('.').pop().toLowerCase();
        const isTypeAllowed = isDashboard ? allowedTypes.includes(fileExtension) : allowedTypes.includes(file.type);
        
        if (!isTypeAllowed) {
            showToast(`Invalid file type. Please upload ${allowedTypes.join(', ')}.`, 'error');
            return;
        }

        if (file.size > MAX_SIZE) {
            const fileSizeMB = (file.size / 1024 / 1024).toFixed(1);
            showToast(`File is too large (${fileSizeMB} MB). Maximum size is 10 MB.`, 'error');
            return;
        }

        if (isDashboard) {
             showToast(`File "${file.name}" selected for mass upload.`, 'info');
        } else {
            $('#fileNameDisplay').text(`Selected: ${file.name}`);
            showToast(`File "${file.name}" selected. Simulating verification...`, 'info');
            setTimeout(() => {
                showResult({ name: 'John Doe', roll: '21CS123', institution: 'MSRIT' });
                $('#fileNameDisplay').text('');
                $('#fileInput').val('');
            }, 1500);
        }
    }
    
    function manualCheck() {
        const certId = $('#cid').val().trim();
        const rollNum = $('#rid').val().trim();
        const fullName = $('#rname').val().trim();

        if (!certId || !rollNum || !fullName) {
            return showToast("Please fill in all fields for manual verification.", "error");
        }

        const $btn = $('#checkBtn');
        $btn.text('Checking...').prop('disabled', true);

        // Valid certificate data for ALAN DOE
        const mockData = {
            certId: "1X2501176",
            rollNum: "21CS123",
            fullName: "ALAN DOE"
        };

        setTimeout(() => {
            // Comparison is case-insensitive for better UX
            if (certId.toLowerCase() === mockData.certId.toLowerCase() && 
                rollNum.toLowerCase() === mockData.rollNum.toLowerCase() && 
                fullName.toLowerCase() === mockData.fullName.toLowerCase()) {
                
                showResult({ name: mockData.fullName, roll: mockData.rollNum, institution: 'National Institute of Technology' });
                showToast("Certificate successfully verified!", "success");
            } else {
                // On failure, show the 'not-verified' result page (fake certificate)
                showSection('#result-not-verified');
            }

            // Reset form and button after the check is complete
            $('#cid').val('');
            $('#rid').val('');
            $('#rname').val('');
            $btn.text('Check Authenticity').prop('disabled', false);
        }, 1500); // Simulate network delay
    }

    function populateDashboard() {
        const loggedInUser = JSON.parse(localStorage.getItem('loggedInUser'));
        if (loggedInUser) {
            $('#instNameDisplay').text(loggedInUser.name);
        }
        $('#totalRecords').text('12,453');
        $('#recentVerifications').text('128');
        $('#forgedAttempts').text('3');
        const recentUploads = [
            { name: 'Graduates_Spring2025.csv', date: '2025-09-15', records: 450, status: 'Completed', type: 'success' },
            { name: 'Transcripts_Fall2024.xlsx', date: '2025-09-14', records: 1200, status: 'Completed', type: 'success' },
            { name: 'Verification_Batch_12.csv', date: '2025-09-12', records: 58, status: 'In Progress', type: 'in-progress' },
            { name: 'Alumni_Data_Update.csv', date: '2025-09-10', records: 832, status: 'Failed', type: 'failed' }
        ];
        let tableHtml = recentUploads.map(upload => `
            <tr>
                <td><strong>${upload.name}</strong></td>
                <td>${upload.date}</td>
                <td>${upload.records}</td>
                <td><span class="status-pill ${upload.type}">${upload.status}</span></td>
            </tr>`).join('');
        $('#recentTbl').html(tableHtml);
    }

    function showResult(data) {
        $('#vName').text(data.name);
        $('#vRoll').text(data.roll);
        $('#vInstitution').text(data.institution);
        showSection('#result');
    }
    
    // --- Event Handlers ---
    $themeToggle.on('click', function() {
        const newTheme = $body.hasClass('dark-mode') ? 'light' : 'dark';
        localStorage.setItem('theme', newTheme);
        applyTheme(newTheme);
    });

    $(document).on('click', '.password-toggle', function() {
        const $input = $(this).prev('input');
        const type = $input.attr('type');
        if (type === 'password') {
            $input.attr('type', 'text');
            $(this).text('🙈');
        } else {
            $input.attr('type', 'password');
            $(this).text('👁️');
        }
    });

    $('.nav-link').on('click', function(e) {
        e.preventDefault();
        const target = $(this).attr('href');
        if (target && $(target).length) {
            showSection(target);
        }
    });
    
    $(document).on('click', '[data-target]', function() {
        const target = $(this).data('target');
        showSection(target);
    });
    
    $(document).on('click', '#viewDashboard', () => showSection('#dashboard'));
    $(document).on('click', '#logoutBtn', logoutUser);
    
    $('#signinBtn').on('click', loginUser);
    $('#registerBtn').on('click', registerUser);
    
    $('#checkBtn').on('click', manualCheck);

    $('#contactForm').on('submit', function(e){
        e.preventDefault();
        showToast('Thank you for your message! We will get back to you shortly.', 'success');
        $(this).trigger('reset');
    });

    $('#uploadBtn').on('click', () => $('#fileInput').click());
    $('#fileInput').on('change', function() {
        handleFileUpload(this.files);
    });

    // Dashboard navigation and file upload
    $('.dash-nav-link').on('click', function(e) {
        e.preventDefault();
        $('.dash-nav-link').removeClass('active');
        $(this).addClass('active');
        const targetView = $(this).data('target');
        $('.dash-view').hide();
        $('#' + targetView).show();
    });

    $('#dashboardUploadBtn, #dashboardDropZone').on('click', () => $('#dashboardFileInput').click());
    $('#dashboardFileInput').on('change', function() {
        handleFileUpload(this.files, ['csv', 'xlsx'], true);
    });

    // Initialize the App
    initialize();
});
