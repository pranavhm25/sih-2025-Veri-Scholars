(function () {

  function showSection(id) {
    $('section').hide();
    $(id).fadeIn();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  $('[data-target]').on('click', function () {
    const t = $(this).data('target');
    showSection(t);
  });

  $('.nav-link').on('click', function (e) {
    e.preventDefault();
    const href = $(this).attr('href');

    if (href === '#home') showSection('#home');
    if (href === '#verify') showSection('#verify');
    if (href === '#dashboard') showSection('#loginSection');

    $('.nav-link').removeClass('active');
    $(this).addClass('active');
  });

  $("nav.links a, .large-btn").on("click", function (e) {
    const target = $(this).attr("data-target") || $(this).attr("href");
    if (target && target.startsWith("#")) {
      e.preventDefault();
      $("html, body").animate({
        scrollTop: $(target).offset().top - 60
      }, 600);
      $("nav.links a").removeClass("active");
      $("nav.links a[href='" + target + "']").addClass("active");
    }
  });

  $('.openInstitution').on('click', function () {
    $('section').hide();
    if (!sessionStorage.getItem('loggedIn')) {
      $('#loginSection').show();
    } else {
      $('#dashboard').show();
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  $('#logoutBtn').on('click', function () {
    sessionStorage.removeItem('loggedIn');
    showSection('#home');
  });

  $('#openSign').on('click', function () {
    showSection('#loginSection');
    $('html,body').scrollTop(0);
  });

  $('#darkToggle').on('click', function () {
    $('body').toggleClass('dark-mode');
    $(this).text($('body').hasClass('dark-mode') ? '☀️' : '🌙');
  });

  const uploader = $('#uploader');
  uploader.on('dragenter dragover', function (e) {
    e.preventDefault();
    e.stopPropagation();
    $(this).addClass('dragover');
  });
  uploader.on('dragleave drop', function (e) {
    e.preventDefault();
    e.stopPropagation();
    $(this).removeClass('dragover');
  });
  uploader.on('drop', function (e) {
    const files = (e.originalEvent.dataTransfer || {}).files || [];
    handleFiles(files);
  });

  $('#uploadBtn').on('click', function () {
    $('#fileInput').click();
  });
  $('#fileInput').on('change', function () {
    handleFiles(this.files);
  });

  const allowedTypes = [
    "application/pdf",
    "image/jpeg",
    "image/png",
    "text/csv",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
  ];

  function handleFiles(files) {
    if (!files || files.length === 0) return;
    const f = files[0];
    $('#filePreview').text(f.name + ' • ' + Math.round(f.size / 1024) + 'KB');
    $('.uploader .upload-btn').text('Processing...').prop('disabled', true);

    if (!allowedTypes.includes(f.type)) {
      alert("Unsupported file type! Please upload PDF, JPG, PNG, or CSV/XLSX.");
      resetUploader();
      return;
    }
    if (f.size > 10 * 1024 * 1024) {
      alert("File too large! Max 10MB allowed.");
      resetUploader();
      return;
    }

    if (f.type.startsWith("image/")) {
      const reader = new FileReader();
      reader.onload = e => {
        $('#filePreview').html(
          '<img src="' + e.target.result +
          '" style="max-width:200px;border-radius:8px;margin-top:8px" />'
        );
      };
      reader.readAsDataURL(f);
      resetUploader();
      showResult({ name: 'Sophia Clark', roll: '123456' });

    } else if (f.type === "application/pdf") {
      f.text().then(text => {
        resetUploader();
        if (!text.includes("EXPECTED_KEYWORD")) {
          alert("Verification failed: Invalid PDF document.");
          return;
        }
        showResult({ name: 'Sophia Clark', roll: '123456' });
      }).catch(err => {
        console.error(err);
        resetUploader();
      });

    } else if (f.type === "text/csv" || f.type.includes("spreadsheet")) {
      const reader = new FileReader();
      reader.onload = e => {
        console.log("CSV content:", e.target.result);
        resetUploader();
        showResult({ name: 'CSV Upload User', roll: 'N/A' });
      };
      reader.readAsText(f);
    }
  }

  function resetUploader() {
    $('.uploader .upload-btn').text('Upload File').prop('disabled', false);
  }
  $('#checkBtn').on('click', function () {
    const cid = $('#cid').val().trim();
    const rid = $('#rid').val().trim();
    const rname = $('#rname').val().trim();
    if (!cid && !rid && !rname) {
      alert('Enter at least one detail to check');
      return;
    }
    $(this).text('Checking...').prop('disabled', true);
    setTimeout(() => {
      $(this).text('Check Authenticity').prop('disabled', false);
      showResult({ name: rname || 'Sophia Clark', roll: rid || '123456' });
    }, 1200);
  });

  $('#signinBtn').on('click', function () {
    const email = $('#email').val().trim();
    const pass = $('#password').val().trim();
    if (!email || !pass) {
      alert("Please enter your login credentials");
      return;
    }
    $(this).text('Signing in...').prop('disabled', true);
    setTimeout(() => {
      $(this).text('Sign in').prop('disabled', false);
      sessionStorage.setItem('loggedIn', true);
      showSection('#dashboard');
      $('html,body').scrollTop(0);
    }, 900);
  });

  $('#openCreate').on('click', function () {
    $('#loginCard').hide();
    $('#createAccountCard').show();
  });

  $('#backToLogin').on('click', function () {
    $('#createAccountCard').hide();
    $('#loginCard').show();
  });

  $('#createAccountBtn').on('click', function () {
    const instName = $('#instName').val().trim();
    const instEmail = $('#instEmail').val().trim();
    const instPass = $('#instPass').val().trim();

    if (!instName || !instEmail || !instPass) {
      alert('Please fill in all fields');
      return;
    }

    $(this).text('Creating Account...').prop('disabled', true);
    setTimeout(() => {
      alert('Account created successfully!');
      $(this).text('Create Account').prop('disabled', false);

      $('#instName,#instEmail,#instPass').val('');

      $('#backToLogin').click();
    }, 1200);
  });

  $('#browseMass').on('click', function () {
    alert('This is a frontend template — wire up real upload logic on the backend.');
  });

  $('#downloadReport').on('click', function () {
    const csv = 'Name,Roll,Year,Course,Status\n' + $('#vName').text() + ',123456,2023,BSc Computer Science,Verified';
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'verification_report.csv';
    a.click();
    URL.revokeObjectURL(url);
  });

  function showResult(data) {
    $('#vName').text(data.name || 'Sophia Clark');
    $('#vRoll').text(data.roll || '123456');
    showSection('#result');
  }

  $(document).on('keydown', function (e) {
    if (e.key === 'Escape') {
      showSection('#home');
    }
  });

  $('section').hide();
  $('#home').show();

  const els = document.querySelectorAll('.card');
  const obs = new IntersectionObserver(entries => {
    entries.forEach(ent => {
      if (ent.isIntersecting) ent.target.classList.add('fade-in');
    });
  }, { threshold: 0.12 });
  els.forEach(e => obs.observe(e));

})();
