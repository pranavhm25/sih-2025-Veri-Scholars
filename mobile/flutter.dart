import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:dotted_border/dotted_border.dart';
import 'package:file_picker/file_picker.dart';
import 'dart:math';

// --- Main Application Setup ---

void main() {
  runApp(const AuthenticityValidatorApp());
}

class AuthenticityValidatorApp extends StatelessWidget {
  const AuthenticityValidatorApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      navigatorKey: navigatorKey,
      title: 'Authenticity Validator',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
        scaffoldBackgroundColor: const Color(0xFFF4F7FC),
        textTheme: GoogleFonts.poppinsTextTheme(Theme.of(context).textTheme),
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF2A63E2),
          primary: const Color(0xFF2A63E2),
          background: const Color(0xFFF4F7FC),
        ),
        appBarTheme: const AppBarTheme(
          backgroundColor: Colors.white,
          elevation: 1,
          iconTheme: IconThemeData(color: Colors.black),
          titleTextStyle: TextStyle(color: Colors.black, fontSize: 18, fontWeight: FontWeight.w600),
        ),
        cardTheme: CardThemeData(
          elevation: 0.5,
          color: Colors.white,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
        ),
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => const LandingPage(),
        '/verify': (context) => const CertificateVerificationPage(),
        '/result': (context) => const VerificationResultPage(),
        '/login': (context) => const InstitutionLoginPage(),
        '/register': (context) => const RegistrationPage(),
        '/otp': (context) => const OtpVerificationPage(),
        '/dashboard': (context) => const InstitutionDashboardPage(),
        '/home_info': (context) => const InfoHomePage(),
        '/about': (context) => const AboutPage(),
        '/contact': (context) => const ContactPage(),
      },
    );
  }
}

// --- App Colors & Styles ---
const Color primaryColor = Color(0xFF2A63E2);
const Color lightBlueBg = Color(0xFFEAF0FE);
const Color textColor = Color(0xFF333333);
const Color subtleTextColor = Color(0xFF6B7280);
final GlobalKey<NavigatorState> navigatorKey = GlobalKey<NavigatorState>();

// --- Informational Pages (New Beautiful Designs) ---

class InfoHomePage extends StatelessWidget {
  const InfoHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Home'),
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            // Hero Section
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 60),
              decoration: const BoxDecoration(
                gradient: LinearGradient(
                  colors: [primaryColor, Color(0xFF4C86F9)],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
              ),
              child: Center(
                child: Column(
                  children: [
                    const Icon(Icons.verified_user_outlined, color: Colors.white, size: 80),
                    const SizedBox(height: 24),
                    Text(
                      'Ultimate Trust in Academic Credentials',
                      textAlign: TextAlign.center,
                      style: GoogleFonts.poppins(
                        fontSize: 32,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    const SizedBox(height: 16),
                    Text(
                      'Verify academic certificates instantly. A seamless, secure, and trusted platform for employers, institutions, and students.',
                      textAlign: TextAlign.center,
                      style: TextStyle(fontSize: 16, color: Colors.white.withOpacity(0.9)),
                    ),
                    const SizedBox(height: 32),
                    ElevatedButton(
                      onPressed: () => Navigator.pushNamed(context, '/verify'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.white,
                        foregroundColor: primaryColor,
                        padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 16),
                        textStyle: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                      ),
                      child: const Text('Verify a Certificate Now'),
                    ),
                  ],
                ),
              ),
            ),
            // Features Section
            Padding(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                children: [
                  const Text(
                    'Key Features',
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 24),
                  Wrap(
                    spacing: 20,
                    runSpacing: 20,
                    alignment: WrapAlignment.center,
                    children: [
                      _buildFeatureCard(
                        icon: Icons.flash_on,
                        title: 'Instant Verification',
                        description: 'Get verification results in seconds, not days.',
                      ),
                      _buildFeatureCard(
                        icon: Icons.lock_outline,
                        title: 'Bank-Grade Security',
                        description: 'All records are encrypted and securely stored.',
                      ),
                      _buildFeatureCard(
                        icon: Icons.business_center_outlined,
                        title: 'Employer Trusted',
                        description: 'The standard for pre-employment background checks.',
                      ),
                      _buildFeatureCard(
                        icon: Icons.school_outlined,
                        title: 'Institution Portal',
                        description: 'Manage and issue secure digital certificates with ease.',
                      ),
                    ],
                  )
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFeatureCard({required IconData icon, required String title, required String description}) {
    return SizedBox(
      width: 250,
      child: Card(
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            children: [
              Icon(icon, color: primaryColor, size: 40),
              const SizedBox(height: 16),
              Text(title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              Text(
                description,
                textAlign: TextAlign.center,
                style: const TextStyle(color: subtleTextColor),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class AboutPage extends StatelessWidget {
  const AboutPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('About Us'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 800),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Pioneering Trust in Education',
                  style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: primaryColor),
                ),
                const SizedBox(height: 16),
                const Text(
                  'The Authenticity Validator for Academia is a flagship initiative by the Department of Higher & Technical Education, Jharkhand, designed to combat academic fraud and streamline the verification process for the digital age.',
                  style: TextStyle(fontSize: 16, color: subtleTextColor, height: 1.5),
                ),
                const SizedBox(height: 40),
                _buildSectionTitle('Our Mission'),
                const Card(
                  child: Padding(
                    padding: EdgeInsets.all(20.0),
                    child: Text(
                      'To create a single, unified digital ecosystem where the authenticity of any academic award can be verified with complete confidence, fostering integrity and trust within the educational and professional communities.',
                      style: TextStyle(fontSize: 16, color: textColor, height: 1.5),
                    ),
                  ),
                ),
                const SizedBox(height: 40),
                _buildSectionTitle('How It Works: A Simple 3-Step Process'),
                _buildStep('1', 'Institutions Upload', 'Accredited institutions securely upload encrypted academic records to our national database.'),
                _buildStep('2', 'Users Request Verification', 'An employer, institution, or student submits certificate details for verification via our portal.'),
                _buildStep('3', 'Instant & Secure Results', 'Our system instantly matches the data against the secure records and provides a verifiable Certificate of Authenticity.'),
                const SizedBox(height: 40),
                _buildSectionTitle('Our Commitment'),
                const Wrap(
                  spacing: 20,
                  runSpacing: 20,
                  children: [
                    _CommitmentChip(icon: Icons.security, label: 'Data Security'),
                    _CommitmentChip(icon: Icons.check, label: 'Accuracy'),
                    _CommitmentChip(icon: Icons.accessibility_new, label: 'Accessibility'),
                    _CommitmentChip(icon: Icons.lightbulb_outline, label: 'Innovation'),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
  
  Widget _buildSectionTitle(String title) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16.0),
      child: Text(
        title,
        style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
      ),
    );
  }

  Widget _buildStep(String number, String title, String description) {
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 8),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            CircleAvatar(
              backgroundColor: primaryColor,
              child: Text(number, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
            ),
            const SizedBox(width: 20),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 4),
                  Text(description, style: const TextStyle(color: subtleTextColor, height: 1.5)),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _CommitmentChip extends StatelessWidget {
  final IconData icon;
  final String label;
  const _CommitmentChip({required this.icon, required this.label});

  @override
  Widget build(BuildContext context) {
    return Chip(
      avatar: Icon(icon, color: primaryColor, size: 20),
      label: Text(label, style: const TextStyle(fontWeight: FontWeight.w600)),
      backgroundColor: lightBlueBg,
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
    );
  }
}

class ContactPage extends StatelessWidget {
  const ContactPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Contact Us'),
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            Container(
              color: lightBlueBg,
              padding: const EdgeInsets.all(32.0),
              child: Center(
                child: Column(
                  children: [
                    const Text(
                      'We\'re Here to Help',
                      style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: primaryColor),
                    ),
                    const SizedBox(height: 16),
                    Text(
                      'Whether you\'re a student, an employer, or an institution, we\'re ready to assist you. Reach out through one of the methods below.',
                      textAlign: TextAlign.center,
                      style: TextStyle(fontSize: 16, color: subtleTextColor, height: 1.5),
                    ),
                  ],
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(24.0),
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 800),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('Contact Information', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 16),
                    Card(
                      child: Column(
                        children: [
                          _buildContactListTile(Icons.email_outlined, 'General Inquiries', 'support@authenticityvalidator.gov.jh', 'mailto:support@authenticityvalidator.gov.jh'),
                          const Divider(height: 1),
                          _buildContactListTile(Icons.business_outlined, 'Institutional Support', 'partners@authenticityvalidator.gov.jh', 'mailto:partners@authenticityvalidator.gov.jh'),
                          const Divider(height: 1),
                          _buildContactListTile(Icons.phone_outlined, 'Support Hotline', '1800-123-4567 (Toll-Free)', 'tel:18001234567'),
                        ],
                      ),
                    ),
                    const SizedBox(height: 40),
                    const Text('Frequently Asked Questions', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 16),
                    _buildFaq('How long does verification take?', 'Verifications are typically instant, returned within seconds of a successful query.'),
                    _buildFaq('Is my data secure?', 'Absolutely. All data is handled with bank-grade encryption both in transit and at rest. We are compliant with national data protection regulations.'),
                    _buildFaq('Which institutions are part of this program?', 'We are actively onboarding all government and major private institutions in Jharkhand. A full list is available on the Institution Portal.'),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildContactListTile(IconData icon, String title, String subtitle, String url) {
    return ListTile(
      leading: Icon(icon, color: primaryColor),
      title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
      subtitle: Text(subtitle, style: const TextStyle(color: subtleTextColor)),
      onTap: () {
        ScaffoldMessenger.of(navigatorKey.currentContext!).showSnackBar(
          SnackBar(content: Text('Simulating action for: $url')),
        );
      },
      trailing: const Icon(Icons.arrow_forward_ios, size: 16),
    );
  }

  Widget _buildFaq(String question, String answer) {
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 6),
      child: ExpansionTile(
        title: Text(question, style: const TextStyle(fontWeight: FontWeight.w600)),
        children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
            child: Text(answer, style: const TextStyle(color: subtleTextColor, height: 1.5)),
          ),
        ],
      ),
    );
  }
}


// --- Landing Page ---

class LandingPage extends StatelessWidget {
  const LandingPage({super.key});

  @override
  Widget build(BuildContext context) {
    // This simple check helps adapt the layout for smaller screens.
    bool isSmallScreen = MediaQuery.of(context).size.width < 850;
    
    return Scaffold(
      body: Container(
        width: double.infinity,
        color: lightBlueBg,
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 16.0),
              child: Row(
                children: [
                  const Icon(Icons.shield_outlined, color: primaryColor, size: 32),
                  const SizedBox(width: 8),
                  Text(
                    'Authenticity Validator',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: textColor),
                  ),
                   const Spacer(),
                  if (!isSmallScreen) ...[
                    TextButton(onPressed: () => Navigator.pushNamed(context, '/home_info'), child: const Text('Home')),
                    TextButton(onPressed: () => Navigator.pushNamed(context, '/about'), child: const Text('About')),
                    TextButton(onPressed: () => Navigator.pushNamed(context, '/contact'), child: const Text('Contact')),
                    const SizedBox(width: 20),
                  ],
                  ElevatedButton(onPressed: () => Navigator.pushNamed(context, '/login'), child: const Text('Sign In')),
                  if(isSmallScreen) 
                    IconButton(
                      onPressed: () {
                        // In a real app, this could open a drawer or a menu.
                        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Menu button tapped!')));
                      }, 
                      icon: const Icon(Icons.menu)
                    )
                ],
              ),
            ),
            Expanded(
              child: Center(
                child: SingleChildScrollView(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 20.0),
                        child: Text(
                          'Securely Verify Academic Credentials',
                          textAlign: TextAlign.center,
                          style: TextStyle(
                            fontSize: 32,
                            fontWeight: FontWeight.bold,
                            color: textColor,
                          ),
                        ),
                      ),
                      const SizedBox(height: 16),
                      Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 20.0),
                        child: Text(
                          'A trusted platform for students, employers, and academic institutions to validate\ncertificates and manage records efficiently.',
                          textAlign: TextAlign.center,
                          style: TextStyle(fontSize: 16, color: subtleTextColor),
                        ),
                      ),
                      const SizedBox(height: 48),
                      Wrap(
                        spacing: 24,
                        runSpacing: 24,
                        alignment: WrapAlignment.center,
                        children: [
                          _buildActionCard(
                            context,
                            icon: Icons.shield_outlined,
                            title: 'Verify a Certificate',
                            description: 'For employers and students. Instantly check the authenticity of an academic certificate.',
                            buttonText: 'Verify Now',
                            onPressed: () {
                              Navigator.pushNamed(context, '/verify');
                            },
                          ),
                          _buildActionCard(
                            context,
                            icon: Icons.school_outlined,
                            title: 'Institution Portal',
                            description: 'For universities and colleges. Login to manage records or upload new certificates.',
                            buttonText: 'Login / Upload',
                            onPressed: () {
                              Navigator.pushNamed(context, '/login');
                            },
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ),
             Padding(
              padding: const EdgeInsets.all(16.0),
              child: Text(
                'Powered by Department of Higher & Technical Education, Jharkhand',
                textAlign: TextAlign.center,
                style: TextStyle(color: subtleTextColor, fontSize: 12),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildActionCard(
    BuildContext context, {
    required IconData icon,
    required String title,
    required String description,
    required String buttonText,
    required VoidCallback onPressed,
  }) {
    return Container(
      width: 350,
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.grey.withOpacity(0.1),
            spreadRadius: 2,
            blurRadius: 10,
          )
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: primaryColor, size: 40),
          const SizedBox(height: 16),
          Text(title, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          Text(description, style: TextStyle(color: subtleTextColor, height: 1.5)),
          const SizedBox(height: 24),
          ElevatedButton(
            onPressed: onPressed,
            style: ElevatedButton.styleFrom(
              backgroundColor: primaryColor,
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(buttonText),
                const SizedBox(width: 8),
                const Icon(Icons.arrow_forward, size: 18),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

// --- (The rest of the file is identical to the previous version with the overflow fix) ---

// --- Registration Page ---

class RegistrationPage extends StatefulWidget {
  const RegistrationPage({super.key});
  @override
  _RegistrationPageState createState() => _RegistrationPageState();
}

class _RegistrationPageState extends State<RegistrationPage> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  void _register() async {
    if (_formKey.currentState!.validate()) {
      SharedPreferences prefs = await SharedPreferences.getInstance();
      await prefs.setString('user_name', _nameController.text);
      await prefs.setString('user_email', _emailController.text);
      await prefs.setString('user_password', _passwordController.text);
      
      String otp = (100000 + Random().nextInt(900000)).toString();
      await prefs.setString('otp', otp); 

      if (mounted) {
        showDialog(
          context: context,
          builder: (context) => AlertDialog(
                title: const Text("OTP Generated (Simulation)"),
                content: Text(
                    "This is a test. In a real application, an OTP would be sent to your email or phone.\n\nYour OTP is: $otp"),
                actions: [
                  TextButton(
                      onPressed: () {
                        Navigator.of(context).pop();
                        Navigator.pushReplacementNamed(context, '/otp');
                      },
                      child: const Text("OK"))
                ],
              ));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: lightBlueBg,
      body: ListView(
        padding: const EdgeInsets.symmetric(horizontal: 24.0),
        children: [
          SizedBox(height: MediaQuery.of(context).size.height * 0.15),
          ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 400),
            child: Card(
              elevation: 4,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              child: Padding(
                padding: const EdgeInsets.all(32.0),
                child: Form(
                  key: _formKey,
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Icon(Icons.shield_outlined, color: primaryColor, size: 40),
                      const SizedBox(height: 8),
                      const Text('Create Institution Account',
                          style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
                      const SizedBox(height: 8),
                      Text('Enter your details to get started', style: TextStyle(color: subtleTextColor)),
                      const SizedBox(height: 24),
                      TextFormField(
                        controller: _nameController,
                        decoration: const InputDecoration(labelText: 'Institution Name', prefixIcon: Icon(Icons.school)),
                        validator: (value) => value!.isEmpty ? 'Please enter a name' : null,
                      ),
                      const SizedBox(height: 16),
                      TextFormField(
                        controller: _emailController,
                        decoration: const InputDecoration(labelText: 'Email Address', prefixIcon: Icon(Icons.email)),
                        keyboardType: TextInputType.emailAddress,
                        validator: (value) => value!.isEmpty || !value.contains('@') ? 'Enter a valid email' : null,
                      ),
                      const SizedBox(height: 16),
                      TextFormField(
                        controller: _passwordController,
                        obscureText: true,
                        decoration: const InputDecoration(labelText: 'Password', prefixIcon: Icon(Icons.lock)),
                        validator: (value) => value!.length < 6 ? 'Password must be at least 6 characters' : null,
                      ),
                      const SizedBox(height: 24),
                      SizedBox(
                        width: double.infinity,
                        child: ElevatedButton(
                          onPressed: _register,
                          style: ElevatedButton.styleFrom(
                              backgroundColor: primaryColor,
                              foregroundColor: Colors.white,
                              padding: const EdgeInsets.symmetric(vertical: 16)),
                          child: const Text('Register'),
                        ),
                      ),
                      const SizedBox(height: 16),
                      TextButton(
                        onPressed: () => Navigator.pushReplacementNamed(context, '/login'),
                        child: const Text('Already have an account? Sign In'),
                      )
                    ],
                  ),
                ),
              ),
            ),
          ),
          SizedBox(height: 40),
        ],
      ),
    );
  }
}

// --- OTP Verification Page ---

class OtpVerificationPage extends StatefulWidget {
  const OtpVerificationPage({super.key});

  @override
  _OtpVerificationPageState createState() => _OtpVerificationPageState();
}

class _OtpVerificationPageState extends State<OtpVerificationPage> {
  final _otpController = TextEditingController();

  void _verifyOtp() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String? savedOtp = prefs.getString('otp');
    if (savedOtp == _otpController.text) {
      await prefs.setBool('is_logged_in', true);
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Registration Successful!'), backgroundColor: Colors.green));
      Navigator.pushNamedAndRemoveUntil(context, '/dashboard', (route) => false);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Invalid OTP. Please try again.'), backgroundColor: Colors.red));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: lightBlueBg,
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 400),
          child: Card(
            elevation: 4,
            child: Padding(
              padding: const EdgeInsets.all(32.0),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Text('Enter Verification Code', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 8),
                  Text('Check the pop-up from the previous screen for your simulated OTP.', textAlign: TextAlign.center, style: TextStyle(color: subtleTextColor)),
                  const SizedBox(height: 24),
                  TextField(
                    controller: _otpController,
                    keyboardType: TextInputType.number,
                    textAlign: TextAlign.center,
                    style: const TextStyle(fontSize: 24, letterSpacing: 10),
                    decoration: const InputDecoration(labelText: 'OTP'),
                  ),
                  const SizedBox(height: 24),
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: _verifyOtp,
                      style: ElevatedButton.styleFrom(
                          backgroundColor: primaryColor,
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(vertical: 16)),
                      child: const Text('Verify'),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}


// --- Institution Login Page ---

class InstitutionLoginPage extends StatefulWidget {
  const InstitutionLoginPage({super.key});

  @override
  _InstitutionLoginPageState createState() => _InstitutionLoginPageState();
}

class _InstitutionLoginPageState extends State<InstitutionLoginPage> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  
  void _login() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String? savedEmail = prefs.getString('user_email');
    String? savedPassword = prefs.getString('user_password');

    if (savedEmail != null && savedPassword != null && _emailController.text == savedEmail && _passwordController.text == savedPassword) {
      await prefs.setBool('is_logged_in', true);
      Navigator.pushReplacementNamed(context, '/dashboard');
    } else {
       ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Invalid credentials. Please register if you are a new institution.'),
          backgroundColor: Colors.red,
        ),
      );
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: lightBlueBg,
      body: ListView(
        padding: const EdgeInsets.symmetric(horizontal: 24.0),
        children: [
          SizedBox(height: MediaQuery.of(context).size.height * 0.15),
          ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 400),
            child: Card(
              elevation: 4,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              child: Padding(
                padding: const EdgeInsets.all(32.0),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Icon(Icons.shield_outlined, color: primaryColor, size: 40),
                    const SizedBox(height: 8),
                    const Text('Institution Login', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 8),
                    Text('Welcome back, please enter your details.', style: TextStyle(color: subtleTextColor)),
                    const SizedBox(height: 24),
                    TextField(
                      controller: _emailController,
                      decoration: const InputDecoration(
                        labelText: 'Email address',
                        prefixIcon: Icon(Icons.email_outlined),
                        border: OutlineInputBorder(),
                      ),
                    ),
                    const SizedBox(height: 16),
                    TextField(
                      controller: _passwordController,
                      obscureText: true,
                      decoration: const InputDecoration(
                        labelText: 'Password',
                        prefixIcon: Icon(Icons.lock_outline),
                        border: OutlineInputBorder(),
                      ),
                    ),
                    const SizedBox(height: 16),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Row(
                          children: [
                            Checkbox(value: false, onChanged: (val) {}),
                            const Text('Remember me'),
                          ],
                        ),
                        TextButton(onPressed: () {}, child: const Text('Forgot your password?')),
                      ],
                    ),
                    const SizedBox(height: 24),
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton(
                        onPressed: _login,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: primaryColor,
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(vertical: 16),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                        ),
                        child: const Text('Sign in'),
                      ),
                    ),
                     const SizedBox(height: 16),
                      TextButton(
                        onPressed: () => Navigator.pushReplacementNamed(context, '/register'),
                        child: const Text('New Institution? Register here'),
                      )
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

// --- Certificate Verification Page ---

class CertificateVerificationPage extends StatelessWidget {
  const CertificateVerificationPage({super.key});

  void _pickFile(BuildContext context) async {
    try {
      FilePickerResult? result = await FilePicker.platform.pickFiles();
      if (result != null) {
        String fileName = result.files.single.name;
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('File picked: $fileName'),
            backgroundColor: Colors.green,
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('No file selected.')),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error picking file: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Authenticity Validator'),
        actions: [
          TextButton(onPressed: () => Navigator.pushNamed(context, '/home_info'), child: const Text('Home')),
          TextButton(onPressed: () => Navigator.pushNamed(context, '/about'), child: const Text('About')),
          TextButton(onPressed: () => Navigator.pushNamed(context, '/contact'), child: const Text('Contact')),
          const SizedBox(width: 20),
          ElevatedButton(onPressed: () => Navigator.pushNamed(context, '/login'), child: const Text('Sign In')),
          const SizedBox(width: 20),
        ],
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(32.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text('Certificate Verification',
                  style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold)),
              const SizedBox(height: 16),
              Text('Verify the authenticity of academic certificates with ease.', style: TextStyle(fontSize: 16, color: subtleTextColor)),
              const SizedBox(height: 48),
              Wrap(
                spacing: 40,
                runSpacing: 40,
                alignment: WrapAlignment.center,
                crossAxisAlignment: WrapCrossAlignment.center,
                children: [
                  _buildFileUploadCard(context),
                  _buildManualEntryCard(context),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildFileUploadCard(BuildContext context) {
    return Card(
      child: Container(
        width: 400,
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            GestureDetector(
              onTap: () => _pickFile(context),
              child: DottedBorder(
                color: primaryColor,
                strokeWidth: 1,
                dashPattern: const [6, 6],
                borderType: BorderType.RRect,
                radius: const Radius.circular(12),
                child: Container(
                  padding: const EdgeInsets.symmetric(vertical: 40),
                  color: lightBlueBg,
                  child: const Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.cloud_upload_outlined, color: primaryColor, size: 50),
                        SizedBox(height: 16),
                        Text('Drag & Drop Certificate', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                        SizedBox(height: 8),
                        Text('or click to browse files'),
                      ],
                    ),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 8),
            Text('PDF, JPG, PNG up to 10MB', style: TextStyle(fontSize: 12, color: subtleTextColor)),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: () => _pickFile(context),
                style: ElevatedButton.styleFrom(
                    backgroundColor: primaryColor,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 16)),
                child: const Text('Upload File'),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildManualEntryCard(BuildContext context) {
    return Card(
      child: Container(
        width: 400,
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Or Enter Details Manually',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 24),
            const TextField(
                decoration: InputDecoration(
                    labelText: 'Certificate ID', hintText: 'e.g., 123-ABC-456', border: OutlineInputBorder())),
            const SizedBox(height: 16),
            const TextField(
                decoration: InputDecoration(
                    labelText: 'Roll Number', hintText: 'e.g., CS-2024-001', border: OutlineInputBorder())),
            const SizedBox(height: 16),
            const TextField(
                decoration:
                    InputDecoration(labelText: 'Full Name', hintText: 'e.g., John Doe', border: OutlineInputBorder())),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: () {
                  Navigator.pushNamed(context, '/result');
                },
                style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF111827),
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 16)),
                child: const Text('Check Authenticity'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// --- Verification Result Page ---

class VerificationResultPage extends StatelessWidget {
  const VerificationResultPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Authenticity Validator'),
        actions: [
          const CircleAvatar(
            child: Icon(Icons.person),
          ),
          const SizedBox(width: 20),
        ],
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(32.0),
          child: Column(
            children: [
              const Text('Verification Result', style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              Text('The certificate details are displayed below.', style: TextStyle(fontSize: 16, color: subtleTextColor)),
              const SizedBox(height: 32),
              ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 800),
                child: Container(
                  padding: const EdgeInsets.all(32),
                  decoration: BoxDecoration(
                    color: primaryColor,
                    borderRadius: BorderRadius.circular(16),
                    boxShadow: [
                      BoxShadow(color: primaryColor.withOpacity(0.3), blurRadius: 20, offset: const Offset(0, 10))
                    ],
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text('Certificate of Authenticity',
                                  style: GoogleFonts.poppins(
                                      fontSize: 24, fontWeight: FontWeight.bold, color: Colors.white)),
                              const SizedBox(height: 4),
                              Text('This certificate has been successfully verified.',
                                  style: TextStyle(color: Colors.white.withOpacity(0.8))),
                            ],
                          ),
                          Container(
                            padding: const EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color: Colors.white.withOpacity(0.1),
                              shape: BoxShape.circle,
                            ),
                            child: const Icon(Icons.verified_user_outlined, color: Colors.white, size: 28),
                          )
                        ],
                      ),
                      const SizedBox(height: 32),
                      const Divider(color: Colors.white24),
                      const SizedBox(height: 24),
                      _buildResultGrid(),
                      const SizedBox(height: 24),
                       _buildResultRow('Status',
                         Container(
                           padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                           decoration: BoxDecoration(
                             color: Colors.green.shade50,
                             borderRadius: BorderRadius.circular(20),
                           ),
                           child: const Row(
                             mainAxisSize: MainAxisSize.min,
                             children: [
                               Icon(Icons.check_circle, color: Colors.green, size: 16),
                               SizedBox(width: 6),
                               Text('Verified', style: TextStyle(color: Colors.green, fontWeight: FontWeight.bold)),
                             ],
                           ),
                         ),
                       ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 32),
              ElevatedButton.icon(
                onPressed: () {},
                icon: const Icon(Icons.download_rounded),
                label: const Text('Download Report'),
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
                  textStyle: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildResultGrid() {
    return IntrinsicHeight(
      child: Row(
        children: [
          Expanded(flex: 2, child: _buildDetailItem('Name', 'Sophia Clark')),
          const VerticalDivider(color: Colors.white24, width: 32),
          Expanded(flex: 1, child: _buildDetailItem('Roll No', '123456')),
          const VerticalDivider(color: Colors.white24, width: 32),
          Expanded(flex: 1, child: _buildDetailItem('Year', '2023')),
          const VerticalDivider(color: Colors.white24, width: 32),
          Expanded(flex: 3, child: _buildDetailItem('Course', 'Bachelor of Science in Computer Science')),
        ],
      ),
    );
  }
  
  Widget _buildResultRow(String label, Widget valueWidget) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 120,
            child: Text(
              label,
              style: TextStyle(fontSize: 14, color: Colors.white.withOpacity(0.7)),
            ),
          ),
          Expanded(child: valueWidget),
        ],
      ),
    );
  }

  Widget _buildDetailItem(String label, String value) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: TextStyle(fontSize: 14, color: Colors.white.withOpacity(0.7))),
        const SizedBox(height: 4),
        Text(value, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white)),
      ],
    );
  }
}

// --- Institution Admin Dashboard ---

class InstitutionDashboardPage extends StatefulWidget {
  const InstitutionDashboardPage({super.key});

  @override
  _InstitutionDashboardPageState createState() => _InstitutionDashboardPageState();
}

class _InstitutionDashboardPageState extends State<InstitutionDashboardPage> {
  void _logout() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.setBool('is_logged_in', false);
    Navigator.pushNamedAndRemoveUntil(context, '/login', (route) => false);
  }

  @override
  Widget build(BuildContext context) {
    bool isLargeScreen = MediaQuery.of(context).size.width > 800;

    return Scaffold(
      body: Row(
        children: [
          if (isLargeScreen)
          Container(
            width: 250,
            color: Colors.white,
            child: Column(
              children: [
                Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Row(
                    children: [
                      const Icon(Icons.shield_outlined, color: primaryColor, size: 32),
                      const SizedBox(width: 8),
                      const Text('Authenticity\nValidator', style: TextStyle(fontWeight: FontWeight.bold)),
                    ],
                  ),
                ),
                _buildSideBarItem(Icons.upload_file, 'Upload Records', true),
                _buildSideBarItem(Icons.verified_user_outlined, 'Verification Requests', false),
                _buildSideBarItem(Icons.bar_chart, 'Reports', false),
                _buildSideBarItem(Icons.settings_outlined, 'Settings', false),
                const Spacer(),
                 _buildSideBarItem(Icons.help_outline, 'Help & Support', false),
                 const Divider(height: 1),
                Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Row(
                    children: [
                       const CircleAvatar(child: Icon(Icons.school)),
                       const SizedBox(width: 12),
                       const Expanded(child: Column(
                         crossAxisAlignment: CrossAxisAlignment.start,
                         children: [
                           Text('Oxford University', style: TextStyle(fontWeight: FontWeight.bold)),
                           Text('Log Out', style: TextStyle(fontSize: 12, color: Colors.grey)),
                         ],
                       )),
                       IconButton(onPressed: _logout, icon: const Icon(Icons.logout, color: Colors.red)),
                    ],
                  ),
                )
              ],
            ),
          ),

          // Main Content
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Institution Admin Dashboard', style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 8),
                  Text('Welcome back, manage your records and verifications.', style: TextStyle(color: subtleTextColor)),
                  const SizedBox(height: 32),
                  Wrap(
                    spacing: 24,
                    runSpacing: 24,
                    children: [
                      const _MassUploadCard(),
                      _StatsAndMonitoringCard(),
                    ],
                  ),
                  const SizedBox(height: 32),
                  const _RecentActivityTable(),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSideBarItem(IconData icon, String title, bool isActive) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      decoration: BoxDecoration(
        color: isActive ? lightBlueBg : Colors.transparent,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Row(
        children: [
          Icon(icon, color: isActive ? primaryColor : subtleTextColor),
          const SizedBox(width: 16),
          Text(title, style: TextStyle(fontWeight: isActive ? FontWeight.bold : FontWeight.normal, color: isActive ? primaryColor : textColor)),
        ],
      ),
    );
  }
}

class _MassUploadCard extends StatelessWidget {
  const _MassUploadCard();
  @override
  Widget build(BuildContext context) {
    return Card(
      child: Container(
        width: 500,
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Mass Upload Records', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Text('Easily upload multiple academic records at once using a CSV or Excel file.', style: TextStyle(color: subtleTextColor)),
            const SizedBox(height: 24),
             DottedBorder(
              color: Colors.grey.shade400,
              strokeWidth: 1,
              dashPattern: const [6, 6],
              borderType: BorderType.RRect,
              radius: const Radius.circular(12),
              child: Container(
                padding: const EdgeInsets.symmetric(vertical: 40),
                child: const Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.cloud_upload_outlined, color: primaryColor, size: 50),
                      SizedBox(height: 16),
                      Text('Drag & Drop Files Here', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                      SizedBox(height: 8),
                      Text('or'),
                      SizedBox(height: 8),
                      OutlinedButton(onPressed: null, child: Text('Browse Files'))
                    ],
                  ),
                ),
              ),
            ),
             const SizedBox(height: 16),
             Row(
               mainAxisAlignment: MainAxisAlignment.spaceBetween,
               children: [
                 Text('Supported formats: .csv, .xlsx', style: TextStyle(fontSize: 12, color: subtleTextColor)),
                 TextButton.icon(onPressed: (){}, icon: const Icon(Icons.download, size: 16), label: const Text('Download sample template'))
               ],
             )
          ],
        ),
      ),
    );
  }
}

class _StatsAndMonitoringCard extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Card(
      child: Container(
        width: 300,
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Stats & Monitoring', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 24),
            _buildStatItem(Icons.inventory_2_outlined, 'Total Records Uploaded', '12,453', Colors.blue),
            const SizedBox(height: 20),
            _buildStatItem(Icons.timelapse_outlined, 'Recent Verifications', '340', Colors.green),
            const SizedBox(height: 20),
            _buildStatItem(Icons.warning_amber_rounded, 'Failed / Forged Attempts', '3', Colors.orange),
            const SizedBox(height: 20),
            _buildStatItem(Icons.gpp_bad_outlined, 'Critical Security Alerts', '1', Colors.red),
          ],
        ),
      ),
    );
  }

  Widget _buildStatItem(IconData icon, String title, String value, Color color) {
    return Row(
      children: [
        Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: color.withOpacity(0.1),
            borderRadius: BorderRadius.circular(8),
          ),
          child: Icon(icon, color: color),
        ),
        const SizedBox(width: 16),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
             Text(title, style: TextStyle(fontSize: 14, color: subtleTextColor)),
             Text(value, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          ],
        )
      ],
    );
  }
}


class _RecentActivityTable extends StatelessWidget {
  const _RecentActivityTable();
  
  final List<Map<String, String>> activities = const [
    {'name': 'Graduates_Spring2023.csv', 'date': '2023-10-26', 'records': '450', 'status': 'Completed'},
    {'name': 'Transcripts_Fall2023.xlsx', 'date': '2023-10-24', 'records': '1200', 'status': 'Completed'},
    {'name': 'Verification_Request_Batch_12.csv', 'date': '2023-10-22', 'records': '58', 'status': 'In Progress'},
    {'name': 'Alumni_Data_Update.csv', 'date': '2023-10-21', 'records': '832', 'status': 'Failed'},
  ];

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text('Recent Activity', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                TextButton(onPressed: (){}, child: const Text('View All'))
              ],
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: DataTable(
                headingTextStyle: const TextStyle(fontWeight: FontWeight.bold, color: textColor),
                columns: const [
                  DataColumn(label: Text('File Name')),
                  DataColumn(label: Text('Date Uploaded')),
                  DataColumn(label: Text('Records')),
                  DataColumn(label: Text('Status')),
                ], 
                rows: activities.map((activity) => DataRow(
                  cells: [
                    DataCell(Text(activity['name']!)),
                    DataCell(Text(activity['date']!)),
                    DataCell(Text(activity['records']!)),
                    DataCell(_buildStatusChip(activity['status']!)),
                  ]
                )).toList(),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatusChip(String status) {
    Color color;
    switch (status) {
      case 'Completed':
        color = Colors.green;
        break;
      case 'In Progress':
        color = Colors.orange;
        break;
      case 'Failed':
        color = Colors.red;
        break;
      default:
        color = Colors.grey;
    }
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Text(
        status,
        style: TextStyle(color: color, fontWeight: FontWeight.w600, fontSize: 12),
      ),
    );
  }
}
